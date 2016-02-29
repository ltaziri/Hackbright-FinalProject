

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from model import User, Group, UserGroup, Comment, Invite, Pattern, Vote, connect_to_db, db
from datetime import datetime, timedelta
import sendgrid
from email_test import send_email
import sendgrid
import os
import sys
from chart import chart_data
from delorean import Delorean
import twitter
import requests


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN'],
    access_token_secret=os.environ['TWITTER_TOKEN_SECRET'])

photos = UploadSet('photos', IMAGES)
manuals = UploadSet('manuals')

app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
app.config['UPLOADED_PHOTOS_ALLOW'] = set(['jpg', 'JPG'])
app.config['UPLOADED_MANUALS_ALLOW']= set(['pdf', 'PDF'])
app.config['UPLOADED_MANUALS_DEST'] = 'static/pdfs'


configure_uploads(app, (photos, manuals))


patch_request_class(app)

@app.route('/')
def index():
    """Homepage"""

    if session.get("user_id"):
        return redirect("/user")

    else:
        return render_template("homepage.html")


@app.route('/sign_in', methods=['POST'])
def handle_sign_in_form():
    """Handle submission of the sign in form."""

    email = request.form.get("email")
    password = request.form.get("password")

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        if password == existing_user.password:
            session["user_id"] = existing_user.user_id
            return redirect("/user")
        else:
            flash("Invalid password.")
            return redirect("/")
    else:
        flash("You are not signed up yet, please sign up.")
        return redirect('/sign_up_form')


@app.route('/log_out')
def log_out():
    """Log user out"""

    del session['user_id']

    return redirect("/")


@app.route('/sign_up_form')
def show_sign_up_form():    
    """Show sign up form"""

    return render_template("sign_up_form.html")


@app.route('/sign_up', methods=['POST'])
def new_user_sign_up():    
    """Handle sign up form submission"""

    email = request.form.get("email")
    existing_user = User.query.filter_by(email=email).first()


    if existing_user:
        flash("email already exists, please sign in")
        return redirect("/")
    else:    
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        if request.form.get("user_photo") == " ":
            filename = photos.save(request.files['photo'])
            user_photo = str(photos.path(filename))
        else:
            user_photo = request.form.get("user_photo")
                
        user = User(
                    email=email, 
                    password=password, 
                    first_name=first_name, 
                    last_name=last_name, 
                    user_photo=user_photo
                    )
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.user_id

        flash("You are successfully signed up!")

        return redirect('/user')


@app.route('/user')
def show_user_home(): 
    """Show user's homepage""" 

    user = User.query.get(session["user_id"])

    open_invites = Invite.query.filter(Invite.invite_email == user.email, 
                                       Invite.invite_confirm == False).all()
    groups = user.groups

    group_vote_messages = {}
    for group in groups:
        message_dict ={}
        users_in_group = UserGroup.query.filter_by(group_id=group.group_id).all()
        votes_for_group = Vote.query.filter_by(group_id=group.group_id).all()
        patterns_for_group = Pattern.query.filter_by(group_id =group.group_id).all()

        if group.vote_timestamp:
            clock_start = Delorean(datetime=group.vote_timestamp, timezone='UTC')
            time_in_hours  = group.vote_days * 24
            clock_end = clock_start + timedelta(hours = time_in_hours)
            current_day_time = Delorean()
            days_remaining =  clock_end - current_day_time
            seconds_remaining = int(days_remaining.total_seconds())
            message_dict['remaining_time'] = seconds_remaining
        else:
            message_dict['remaining_time'] = False 
        
        for pattern in patterns_for_group:
            if pattern.chosen == True:
                message_dict['pattern_chosen'] = True;
        if message_dict.get('pattern_chosen', False) == False:
            message_dict['pattern_chosen'] = False;

        message_dict['group_id'] = group.group_id
        message_dict['admin'] = group.admin_id
        message_dict['user_count'] = len(users_in_group)
        message_dict['vote_count'] = len(votes_for_group)
        # message_dict['vote_timestamp'] = group.vote_timestamp
        group_vote_messages[group.group_name] = message_dict

    # print "Message dict!!!!!!!!!!!!!!!", group_vote_messages 
    return render_template("user_home.html", 
                            user=user, 
                            groups=groups, 
                            open_invites = open_invites, 
                            group_vote_messages=group_vote_messages)


@app.route('/invite_confirm.json', methods=['POST'])
def add_group_to_user():
    """User confirm invite, join group, and return group info for AJAX temp div"""

    invite_id = request.form.get('invite_id')

    user = session["user_id"]

    invite = Invite.query.get(invite_id)
    invite.invite_confirm = True

    user_group = UserGroup(
                           group_id=invite.group_id,
                           user_id=user
                           )
    db.session.add(user_group)
    db.session.commit()

    group_dict = {}

    group_dict['group_id'] = invite.group_id
    group_dict['group_name'] = invite.group.group_name
    group_dict['group_image'] = invite.group.group_image

    return jsonify(group_dict)


@app.route('/user_profile')
def show_user_profile(): 
    """Show users profile page"""

    user = User.query.get(session["user_id"])

    return render_template("user_profile.html", user=user)


@app.route('/user_profile_form')
def show_user_profile_form(): 
    """Show users profile form so they can update information"""

    user = User.query.get(session["user_id"])

    return render_template("user_profile_form.html", user=user)


@app.route('/user_profile_update',methods=['POST'])
def user_profile_update(): 
    """Handle user profile form to update user's profile"""

    user = User.query.get(session["user_id"])

    new_user_descrip = request.form.get("user_descrip")


    if 'user_photo' in request.files:
        user_photo_filename = photos.save(request.files['user_photo'])
        new_user_photo = str(photos.path(user_photo_filename))
        user.user_photo = new_user_photo
        db.session.commit()
    if new_user_descrip != "":
        user.user_descrip = new_user_descrip
        db.session.commit()

    return redirect("/user_profile")


@app.route('/group_form')
def show_group_form():
    """Create a new group form"""

    user = User.query.get(session["user_id"])

    return render_template("group_form.html", user=user)


@app.route('/create_group', methods=['POST'])
def create_group():
    """Handle submission of new group form"""

    user = User.query.get(session["user_id"])

    group_name = request.form.get("group_name")

    group_descrip = request.form.get("group_descrip")

    hashtag = request.form.get("hashtag")
    hashtag = '#makealong' + hashtag

    if request.form.get("group_image") == " ":
        filename = photos.save(request.files['photo'])
        group_image = str(photos.path(filename))

    else:
        group_image = request.form.get("group_image")

    if request.form.get("vote_days"):
        vote_days = request.form.get("vote_days")
        vote_timestamp = datetime.now()

        group = Group(group_name=group_name,
                  group_descrip=group_descrip, 
                  group_image=group_image,  
                  admin_id=user.user_id,
                  vote_days=vote_days,
                  vote_timestamp=vote_timestamp,
                  hashtag=hashtag)

        db.session.add(group)
        db.session.commit()
    else:
        group = Group(group_name=group_name,
                  group_descrip=group_descrip, 
                  group_image=group_image,  
                  admin_id=user.user_id,
                  hashtag=hashtag)

        db.session.add(group)
        db.session.commit()

    user_group= UserGroup(group_id=group.group_id,
                          user_id=user.user_id)

    db.session.add(user_group)
    db.session.commit()

    if (request.form.get("pattern_name") 
        or request.form.get("pattern_link") 
        or  "pattern_pdf" in request.files):

        base_pattern_name = request.form.get("pattern_name")
        base_pattern_link = request.form.get("pattern_link")

        if "pattern_pdf" in request.files and request.files['pattern_pdf'].filename:
            pdf_filename = manuals.save(request.files['pattern_pdf'])
            base_pattern_pdf = str(manuals.path(pdf_filename))
        else:
            base_pattern_pdf = None

        pattern = Pattern(pattern_name = base_pattern_name,
                          pattern_link = base_pattern_link,
                          pattern_pdf = base_pattern_pdf,
                          chosen = True,
                          group_id = group.group_id)
        db.session.add(pattern)
        db.session.commit()

    if (request.form.get("pattern_name_a") 
        or request.form.get("pattern_link_a") 
        or ("pattern_pdf_a" in request.files and request.files['pattern_pdf_a'].filename)):

        pattern_name = request.form.get("pattern_name_a")
        pattern_link = request.form.get("pattern_link_a")
        

        if "pattern_pdf_a" in request.files and request.files['pattern_pdf_a'].filename:
            pdf_filename = manuals.save(request.files['pattern_pdf_a'])
            pattern_pdf = str(manuals.path(pdf_filename))
        else:
            pattern_pdf = None

        pattern_one = Pattern(pattern_name = pattern_name,
                          pattern_link = pattern_link,
                          pattern_pdf = pattern_pdf,
                          chosen = False,
                          group_id = group.group_id)
        db.session.add(pattern_one)
        db.session.commit()

    if (request.form.get("pattern_name_b") 
        or request.form.get("pattern_link_b") 
        or ("pattern_pdf_b" in request.files and request.files['pattern_pdf_b'].filename)):

        pattern_name = request.form.get("pattern_name_b")
        pattern_link = request.form.get("pattern_link_b")

        if "pattern_pdf_b" in request.files and request.files['pattern_pdf_b'].filename:
            pdf_filename = manuals.save(request.files['pattern_pdf_b'])
            pattern_pdf = str(manuals.path(pdf_filename))
        else:
            pattern_pdf = None

        pattern_two = Pattern(pattern_name = pattern_name,
                          pattern_link = pattern_link,
                          pattern_pdf = pattern_pdf,
                          chosen = False,
                          group_id = group.group_id) 
        db.session.add(pattern_two)
        db.session.commit()

    if (request.form.get("pattern_name_c") 
        or request.form.get("pattern_link_c") 
        or ("pattern_pdf_c" in request.files and request.files['pattern_pdf_c'].filename)):

        pattern_name = request.form.get("pattern_name_c")
        pattern_link = request.form.get("pattern_link_c")

        if "pattern_pdf_c" in request.files and request.files['pattern_pdf_c'].filename:
            pdf_filename = manuals.save(request.files['pattern_pdf_c'])
            pattern_pdf = str(manuals.path(pdf_filename))
        else:
            pattern_pdf = None

        pattern_three = Pattern(pattern_name = pattern_name,
                          pattern_link = pattern_link,
                          pattern_pdf = pattern_pdf,
                          chosen = False,
                          group_id = group.group_id) 
        db.session.add(pattern_three)
        db.session.commit()
    
    return redirect("/group_home/%d" % (group.group_id))


@app.route('/group_home/<int:group_id>')
def show_group_page(group_id):
    """Show group's homepage"""

    group = Group.query.get(group_id)

    group_users = group.users

    if group.is_user_in_group(session["user_id"])==False:
        return redirect("/user")     
    else: 
        user = session["user_id"]
        
        votes = Vote.query.filter_by(group_id = group_id).all()

        voter_ids =[]
        for voter in votes:
            voter_ids.append(voter.user_id)

        num_group_users = len(group_users)
        comments =  Comment.query.filter_by(group_id=group_id)
        patterns = Pattern.query.filter_by(group_id=group_id).all()
        chosen_pattern = Pattern.query.filter(Pattern.group_id == group_id, Pattern.chosen == True).all()

        if chosen_pattern:
            return render_template("group_page.html", 
                        group=group, 
                        group_users=group_users, 
                        user=user,
                        comments=comments,
                        patterns = chosen_pattern,
                        votes=voter_ids,
                        num_group_users=num_group_users)
        else:
            return render_template("group_page.html", 
                        group=group, 
                        group_users=group_users, 
                        user=user,
                        comments=comments,
                        patterns = patterns,
                        votes=voter_ids,
                        num_group_users=num_group_users)


@app.route('/group_twitter.json/<int:group_id>')
def get_twitter_feed(group_id):
    """Make twitter request to api and return data"""
       
    group = Group.query.get(group_id)
    
    tagged_tweets = api.GetSearch(term=group.hashtag, 
                                  geocode=None, 
                                  since_id=None, 
                                  max_id=None, 
                                  until=None, 
                                  count=15, 
                                  lang=None, 
                                  locale=None, 
                                  result_type='mixed', 
                                  include_entities=None)
    
    twitter_feed = {}
    tweet_id = 1
    for tweet in tagged_tweets:
        if tweet.media:
            tweet_photo = tweet.media
            twitter_feed[tweet_id] = { 'screen_name': tweet.user.screen_name,
                                    'text':tweet.text, 
                                    'user_profile_pic': tweet.user.profile_image_url,
                                    'image_url' : tweet_photo[0]['media_url_https']
                                    }
            tweet_id = tweet_id + 1
        else:
            twitter_feed[tweet_id] = { 'screen_name': tweet.user.screen_name,
                                    'text':tweet.text, 
                                    'user_profile_pic': tweet.user.profile_image_url
                                    }
            tweet_id = tweet_id + 1  
 
    return jsonify(twitter_feed)


@app.route('/group_profile_form/<int:group_id>')
def show_group_profile_form(group_id): 
    """Show group's profile form so they can update information"""

    group = Group.query.get(group_id)

    if group.is_user_in_group(session["user_id"])==False:
        return redirect("/user") 

    else: 
        user = session["user_id"]
        patterns = Pattern.query.filter_by(group_id=group_id).all()
        chosen_pattern = Pattern.query.filter(Pattern.group_id == group_id, Pattern.chosen == True).all()
        if chosen_pattern:
            return render_template("group_update_form.html", group=group, patterns=chosen_pattern)
        else:
            return render_template("group_update_form.html", group=group, patterns=patterns)
    


@app.route('/group_profile_update/<int:group_id>', methods=['POST'])
def update_group_profile(group_id):
    """Update group profile using inputs from group update form"""

    group = Group.query.get(group_id)

    if group.is_user_in_group(session["user_id"])==False:
        return redirect("/user") 

    else: 
        chosen_pattern = Pattern.query.filter(Pattern.group_id == group_id, Pattern.chosen == True)

        update_group_name = request.form.get("group_name")
        update_group_descrip = request.form.get("group_descrip")
        update_group_hashtag = request.form.get("hashtag")
        
        update_group_pattern_name = request.form.get("update_pattern_name")
        update_group_pattern_link = request.form.get("update_pattern_link")
        
    #basic user description update
        if update_group_name != "":
            group.group_name = update_group_name
            db.session.commit()

        if update_group_descrip != "":
            group.group_descrip = update_group_descrip
            db.session.commit()

        if update_group_hashtag != "":
            group.hashtag = update_group_hashtag
            db.session.commit()

        if "group_img" in request.files and request.files['group_img'].filename:
            group_photo_filename = photos.save(request.files["group_img"])
            update_group_image = str(photos.path(group_photo_filename))
            group.group_image = update_group_image
            db.session.commit()

    #update if group had a pattern, and is just changing info about it.
        if update_group_pattern_name != "":
            chosen_pattern.pattern_name = update_group_pattern_name
            db.session.commit()

        if update_group_pattern_link != "":
            chosen_pattern.pattern_link = update_group_pattern_link
            db.session.commit()

        if "update_pattern_pdf" in request.files and request.files['update_pattern_pdf'].filename:
            pattern_pdf_filename = manuals.save(request.files['update_pattern_pdf'])
            new_group_pattern_pdf = str(manuals.path(pattern_pdf_filename))
            chosen_pattern.pattern_pdf = new_group_pattern_pdf
            db.session.commit()

    # add pattern if one is selected and a poll is not created.

        if (request.form.get("new_pattern_name") 
            or request.form.get("new_pattern_link") 
            or ("new_pattern_pdf" in request.files and request.files['new_pattern_pdf'].filename)):

            new_group_pattern_name = request.form.get("new_pattern_name")
            new_group_pattern_link = request.form.get("new_pattern_link")

            if "new_pattern_pdf" in request.files and request.files['new_pattern_pdf'].filename:
                pdf_filename = manuals.save(request.files['new_pattern_pdf'])
                new_pattern_pdf = str(manuals.path(pdf_filename))
            else:
                new_pattern_pdf = None

            pattern = Pattern(pattern_name = new_group_pattern_name,
                              pattern_link = new_group_pattern_link,
                              pattern_pdf = new_pattern_pdf,
                              chosen = True,
                              group_id = group.group_id)
            db.session.add(pattern)
            db.session.commit()

    ##info if pattern poll was created##
        
        if request.form.get("vote_days"):
            vote_days = request.form.get("vote_days")
            vote_timestamp = datetime.now()
            group.vote_days = vote_days
            group.vote_timestamp = vote_timestamp
            db.session.commit()

        if (request.form.get("pattern_name_a") 
            or request.form.get("pattern_link_a") 
            or  ("pattern_pdf_a" in request.files and request.files['pattern_pdf_a'].filename)):

            pattern_name = request.form.get("pattern_name_a")
            pattern_link = request.form.get("pattern_link_a")

            if "pattern_pdf_a" in request.files and request.files['pattern_pdf_a'].filename:
                pdf_filename = manuals.save(request.files['pattern_pdf_a'])
                pattern_pdf = str(manuals.path(pdf_filename))
            else:
                pattern_pdf = None

            pattern_one = Pattern(pattern_name = pattern_name,
                              pattern_link = pattern_link,
                              pattern_pdf = pattern_pdf,
                              chosen = False,
                              group_id = group.group_id)
            db.session.add(pattern_one)
            db.session.commit()

        if (request.form.get("pattern_name_b") 
            or request.form.get("pattern_link_b") 
            or ("pattern_pdf_b" in request.files and request.files['pattern_pdf_b'].filename)):

            pattern_name = request.form.get("pattern_name_b")
            pattern_link = request.form.get("pattern_link_b")

            if "pattern_pdf_b" in request.files and request.files['pattern_pdf_b'].filename:
                pdf_filename = manuals.save(request.files['pattern_pdf_b'])
                pattern_pdf = str(manuals.path(pdf_filename))
            else:
                pattern_pdf = None

            pattern_two = Pattern(pattern_name = pattern_name,
                              pattern_link = pattern_link,
                              pattern_pdf = pattern_pdf,
                              chosen = False,
                              group_id = group.group_id) 
            db.session.add(pattern_two)
            db.session.commit()

        if (request.form.get("pattern_name_c") 
            or request.form.get("pattern_link_c") 
            or  ("pattern_pdf_c" in request.files and request.files['pattern_pdf_c'].filename)):

            pattern_name = request.form.get("pattern_name_c")
            pattern_link = request.form.get("pattern_link_c")

            if "pattern_pdf_c" in request.files and request.files['pattern_pdf_c'].filename:
                pdf_filename = manuals.save(request.files['pattern_pdf_c'])
                pattern_pdf = str(manuals.path(pdf_filename))
            else:
                pattern_pdf = None

            pattern_three = Pattern(pattern_name = pattern_name,
                                  pattern_link = pattern_link,
                                  pattern_pdf = pattern_pdf,
                                  chosen = False,
                                  group_id = group.group_id) 
            db.session.add(pattern_three)
            db.session.commit()
        db.session.commit()
    return redirect("/group_home/%d" % (group.group_id))


@app.route('/flip_clock.json/<int:group_id>')
def update_clock(group_id):
    """Update clock based on time remaining"""

    group = Group.query.get(group_id)

    clock_start = group.vote_timestamp
    clock_start = Delorean(datetime=clock_start, timezone='UTC')
    
    time_in_hours  = group.vote_days * 24
    clock_end = clock_start + timedelta(hours = time_in_hours)
    current_day_time = Delorean()
    days_remaining =  clock_end - current_day_time

    seconds_remaining = int(days_remaining.total_seconds())

    clock_time = {}

    clock_time['seconds'] = seconds_remaining

    return jsonify(clock_time)


@app.route('/update_poll.json', methods=['POST'])
def update_vote():
    """Update voting table based on form input"""

    group_id = request.form.get("group_id")
    pattern_id = request.form.get("pattern_id")

    vote = Vote(group_id = group_id,
                user_id = session["user_id"],
                pattern_id = pattern_id)

    db.session.add(vote)
    db.session.commit()

    vote_update = {}
    vote_update['label'] = vote.pattern.pattern_name
    vote_update['data'] = 0

    current_votes = Vote.query.filter(Vote.group_id == group_id).all()

    for current_vote in current_votes:
        if current_vote.pattern_id == vote.pattern_id:
            vote_update['data'] +=1

    return jsonify(vote_update)


@app.route('/poll.json/<int:group_id>')
def get_pattern_poll_data(group_id):
    """ get voting data and send back json """

    group_patterns = Pattern.query.filter_by(group_id=group_id).all()

    votes = Vote.query.filter(Vote.group_id == group_id).all()
    vote_data = {} 

    for vote in votes:
        if vote_data.get(vote.pattern.pattern_name, False) == False:
            vote_data[vote.pattern.pattern_name] = 1
        else:
            vote_data[vote.pattern.pattern_name] +=1

    for pattern in group_patterns:
        if vote_data.get(pattern.pattern_name, False) == False:
            vote_data[pattern.pattern_name] = 0

   
    labels = []
    data = []

    for tup in vote_data.items():
        labels.append(tup[0])
        data.append(tup[1])

    data_set = {'label': "Votes",
                'fillColor': "rgba(220,220,220,0.5)",
                'strokeColor': "rgba(220,220,220,0.8)",
                'highlightFill': "rgba(220,220,220,0.75)",
                'highlightStroke': "rgba(220,220,220,1)"}

    data_set['data'] = data            

    poll_data = {}
    poll_data['labels'] = labels
    poll_data['datasets'] = [data_set]
    print poll_data
    return jsonify(poll_data)


@app.route('/final_vote/<int:group_id>', methods=['POST'] )
def handle_final_vote_submit(group_id):
    """process final pattern vote and mark it confirmed in the pattern table"""

    vote = request.form.get('final_vote_submit')
    vote = int(vote)
    print vote
    pattern = Pattern.query.filter_by(pattern_id = vote).one()
    print pattern
    pattern.chosen = True
    db.session.commit()


    return redirect('/group_home/%d' % group_id)


@app.route('/comment_add.json', methods=['POST'])
def add_comment():
    """Handle comment form submissions"""

    group_id = request.form.get("group_id")
    comment_text = request.form.get("comment_text")
    
    if 'comment_image' in request.files and request.files['comment_image'].filename:
        comment_img_filename = photos.save(request.files['comment_image'])
        comment_image = str(photos.path(comment_img_filename))
    else:
        comment_image = None
    print comment_image
        
    comment = Comment(comment_text=comment_text, 
                      comment_image=comment_image, 
                      comment_timestamp=datetime.now(),
                      user_id=session["user_id"],
                      group_id=group_id)

    db.session.add(comment)
    db.session.commit()    

    format_timestamp = comment.comment_timestamp.strftime('%m/%d/%y %X')

    comment_dict = {'comment_user_photo': comment.user.user_photo,
                    'comment_user_name': comment.user.first_name,
                    'comment_timestamp':format_timestamp,
                    'comment_text': comment.comment_text,
                    'comment_image': comment.comment_image }

    return jsonify(comment_dict)


@app.route('/invite_form/<int:group_id>')
def show_invite_form(group_id):
    """Show group invite form"""

    group = Group.query.get(group_id)

    if group.is_user_in_group(session["user_id"])==False:
        return redirect("/user") 
    else:
        return render_template("invite_form.html", group=group)
    

@app.route('/send_invite/<int:group_id>', methods=['POST'])
def send_invitation(group_id):
    """Send email invitation, store invite in databse"""

    group = Group.query.get(group_id)
    user=User.query.get(session["user_id"])

    invite_name = request.form.get("name")

    invite_email = request.form.get("email")
    invite_text= request.form.get("text")


    invite = Invite(invite_email=invite_email, 
                    invite_text=invite_text, 
                    invite_timestamp=datetime.now(),
                    group_id=group_id,
                    user_id=session["user_id"],
                    )

    db.session.add(invite)
    db.session.commit()

    send_email(invite_email, invite_name, user.first_name, group.group_name, invite_text)

    flash("Invitation sent!")

    return redirect("/group_home/%d" % (group_id))


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
