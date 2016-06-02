

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from model import User, Group, UserGroup, Comment, Invite, Pattern, Vote, connect_to_db, db
from datetime import datetime, timedelta
import sendgrid
from sg_email import send_email
import os
import sys
from chart import chart_data
from delorean import Delorean
import twitter
import requests
import helper
import re



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

# Twitter enviornment variables, stored in secrets script file
api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN'],
    access_token_secret=os.environ['TWITTER_TOKEN_SECRET'])

# Flask Uploads image and pdf location and configuration
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
    """Show homepage template"""

    # If user is already logged in, redirect them to user homepage
    # If not render the homepage template

    if session.get("user_id"):
        return redirect("/user")

    else:
        return render_template("homepage.html")


@app.route('/sign_in', methods=['POST'])
def handle_sign_in_form():
    """Handle submission of the sign in form."""

    # Get form values from sign in form and check if email exists in database

    email = request.form.get("email")
    password = request.form.get("password")

    existing_user = User.query.filter_by(email=email).first()

    # If email is database, check if the password entered matches.
    # If email is not in database, redirect to the sign up page.

    
    if existing_user:
        if password == existing_user.password:
            session["user_id"] = existing_user.user_id

            # vote time reset added for demo, pull from session
            session["group_timestamps"] = [(2,datetime.now()), (5, datetime.now())]
               
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

    # Delete user_id in the session, redirect to homepage

    del session['user_id']

    # demo reset
    del session["group_timestamps"]

    if session.get('chosen_pattern'):
        del session['chosen_pattern']

    return redirect("/")


@app.route('/sign_up_form')
def show_sign_up_form():    
    """Show sign up form"""

    return render_template("sign_up_form.html")


@app.route('/sign_up', methods=['POST'])
def new_user_sign_up():    
    """Handle sign up form submission"""

    # Get email from form first, check if it already exists in the database

    email = request.form.get("email")
    existing_user = User.query.filter_by(email=email).first()

    # If email is in database redirect to homepage, if not handle remaining form
    # submissions

    if existing_user:
        flash("email already exists, please sign in")
        return redirect("/")
    else:    
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        # Check if a user uploaded a photo. If so save it to the photos folder, 
        # if not save the photo path for the default photo selected.

        if request.form.get("user_photo") == " ":
            filename = photos.save(request.files['photo'])
            user_photo = str(photos.path(filename))
        else:
            user_photo = request.form.get("user_photo")

        # Instantiate a new User in the database 

        user = User(email=email, 
                    password=password, 
                    first_name=first_name, 
                    last_name=last_name, 
                    user_photo=user_photo)
        # db.session.add(user)
        # db.session.commit()

        # Store new user_id in session, let them know sign up was successfull
        # and send user to their user homepage

        session["user_id"] = user.user_id
        flash("You are successfully signed up!")

        return redirect('/user')


@app.route('/user')
def show_user_home(): 
    """Show user's homepage""" 

    # Get user from user id in session

    user = User.query.get(session["user_id"])

    # Use foreign key, groups, in users table to get the groups that the user is
    # in. Sort the list of Group objects that is returned so the groups will 
    # appear in group_id order on user homepage.

    groups = user.groups
    groups.sort(key=lambda x: x.group_id)

    # Check if the user has any invites in the Invite table that haven't been 
    # confirmed. If so a message is triggered on the user homepage.

    open_invites = Invite.query.filter(Invite.invite_email == user.email, 
                                       Invite.invite_confirm == False).all()

    # Call helper function to create a dictionary for message area of homepage.

    group_vote_messages = {}
    for group in groups:
        group_vote_messages[group.group_name] = helper.create_group_messages(group)

    # Render user homepage template with group, invite and message info.

    return render_template("user_home.html", 
                            user=user, 
                            groups=groups, 
                            open_invites = open_invites, 
                            group_vote_messages=group_vote_messages)


@app.route('/invite_confirm.json', methods=['POST'])
def add_group_to_user():
    """AJAX call from user homepage to confirm an unconfirmed invite"""

    # Get the invited id from the form and the user from the session.

    invite_id = request.form.get('invite_id')
    user = session["user_id"]

    # Get the invite object from the database, mark the confirm field to true.

    invite = Invite.query.get(invite_id)
    # disabled for demo
    # invite.invite_confirm = True

    # Instantiate a new UserGroup object and save it to usergroups which is an 
    # association table for groups and users.
    # disabled for demo
    # user_group = UserGroup(group_id=invite.group_id,
    #                        user_id=user)
    # db.session.add(user_group)
    # db.session.commit()

    # Create dictionary to send back to AJAX call as a JSON.

    group_dict = {}
    group_dict['group_id'] = invite.group_id
    group_dict['group_name'] = invite.group.group_name
    group_dict['group_image'] = invite.group.group_image

    return jsonify(group_dict)



@app.route('/user_profile_update',methods=['POST'])
def user_profile_update(): 
    """Handle user profile form to update user's profile"""

    # Get user using user_id in session.

    user = User.query.get(session["user_id"])

    # Check if request files contains a user photo key by checking for the 
    # filename property. If a photo was uploaded, add it to the photo folder 
    # and save the photo file path to the database.

    if 'user_photo' in request.files and request.files['user_photo'].filename:
        user_photo_filename = photos.save(request.files['user_photo'])
        new_user_photo = str(photos.path(user_photo_filename))
        user.user_photo = new_user_photo
        db.session.commit()

    # Get form input for user description, if it is not blank add the new
    # description to the database. 

    new_user_descrip = request.form.get("user_descrip")

    if new_user_descrip != "":
        user.user_descrip = new_user_descrip
        
        # disabled for demo
        # db.session.commit()

    # Flash profile update success and redirect to user homepage.

    flash("Your profile has been updated!")

    return redirect("/user")


@app.route('/group_form')
def show_group_form():
    """Show new group form"""

    user = User.query.get(session["user_id"])
    return render_template("group_form.html", user=user)


@app.route('/create_group', methods=['POST'])
def create_group():
    """Handle submission of new group form"""

    # form inputs
    group_name = request.form.get("group_name")
    group_descrip = request.form.get("group_descrip")
    hashtag = request.form.get("hashtag")

    # If a hashtag was entered append makealong tag to beginning of value
    if hashtag != "":
        hashtag = '#makealong' + hashtag
    else:
        hashtag = None

    # If upload your own photo radio button was selected save the photo from 
    # request files to the photo folder and save the photo path in database. 
    # If one of the default photos was selected, set group_image to the photo 
    # path for the default photo selected.

    if request.form.get("group_image") == " ":
        filename = photos.save(request.files['photo'])
        group_image = str(photos.path(filename))

    else:
        group_image = request.form.get("group_image")

    # New group object if pattern poll was created, use vote days field as poll 
    # indicator. Using pattern helper function that instantiates poll patterns in 
    # the database.

    if request.form.get("vote_days"):
        vote_days = request.form.get("vote_days")
        vote_timestamp = datetime.now()

        group = Group(group_name=group_name,
                      group_descrip=group_descrip, 
                      group_image=group_image,  
                      admin_id=session["user_id"],
                      vote_days=vote_days,
                      vote_timestamp=vote_timestamp,
                      hashtag=hashtag)
        # disabled for demo
        # db.session.add(group)
        # db.session.commit()

        helper.create_patterns_for_poll(group.group_id)
    
    # New group without pattern poll.      
    else:
        group = Group(group_name=group_name,
                      group_descrip=group_descrip, 
                      group_image=group_image,  
                      admin_id=session["user_id"],
                      hashtag=hashtag)
        # disabled for demo
        # db.session.add(group)
        # db.session.commit()

        # If pattern name was entered in form, call helper function to instantiate
        # pattern in database.

        if request.form.get("pattern_name"):             
            helper.add_chosen_pattern("pattern_name", "pattern_link","pattern_pdf", group.group_id)
    
    # Instantiate a new UserGroup object and save it to usergroups which is an 
    # association table for groups and users.

    user_group= UserGroup(group_id=group.group_id,
                          user_id=session["user_id"])
    # disabled for demo
    # db.session.add(user_group)
    # db.session.commit()
    
    return redirect("/group_home/%d" % (group.group_id))


@app.route('/group_home/<int:group_id>')
def show_group_page(group_id):
    """Show group's homepage"""

    # Get group from database and the users in the group
    group = Group.query.get(group_id)
    group_users = group.users

    # Use instance method on the Group class to check if the user id in the session
    # is in the group. If not, redirect to the user homepage. If so render
    # group page template.

    if group.is_user_in_group(session["user_id"])==False:
        return redirect("/user")     
    else: 
        user = session["user_id"]
        
        # Vote objects for the group, list of the user_ids who have voted and
        # number of group users to determine if everyone has voted. 

        votes = Vote.query.filter_by(group_id = group_id).all()

        voter_ids = []
        for voter in votes:
            voter_ids.append(voter.user_id)

        num_group_users = len(group_users)

        # Get group comments from database, create list of comment_image paths
        # for photo album.

        comments =  Comment.query.filter_by(group_id=group_id).all()
        comment_pics = []
        for comment in comments:
            if comment.comment_image:
                comment_pics.append(comment.comment_image)

        # Get patterns for the group and determine if one is marked chosen. If
        # if a pattern is marked chosen, render group page template with that 
        # pattern, if not render page with all pattern objects for poll

        patterns = Pattern.query.filter_by(group_id=group_id).order_by(Pattern.pattern_name).all()
        chosen_pattern = Pattern.query.filter(Pattern.group_id == group_id, Pattern.chosen == True).all()

        # also check session for chosen pattern. This is for the demo only
        if not chosen_pattern:
            if session.get('chosen_pattern') and session['chosen_pattern'][0] == group_id:
                pattern_id = session['chosen_pattern'][1]
                chosen_pattern = Pattern.query.filter(Pattern.pattern_id == pattern_id).all()
       

        if chosen_pattern:
            return render_template("group_page.html", 
                        group=group, 
                        group_users=group_users, 
                        user=user,
                        comments=comments,
                        comment_pics=comment_pics,
                        patterns = chosen_pattern,
                        votes=voter_ids,
                        num_group_users=num_group_users)
        else:
            return render_template("group_page.html", 
                        group=group, 
                        group_users=group_users, 
                        user=user,
                        comments=comments,
                        comment_pics=comment_pics,
                        patterns = patterns,
                        votes=voter_ids,
                        num_group_users=num_group_users)


@app.route('/group_twitter.json/<int:group_id>')
def get_twitter_feed(group_id):
    """Make twitter request to api and return data"""
    
    # Get group from database in order to get the group hashtag

    group = Group.query.get(group_id)
    
    # Hit the twitter api to get JSON of tweets matching group hashtag

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
    
    # Create dictionary with only the relevent data from the twitter JSON. 
    # Twitter photo data stored in media key, if that key exsists in twitter 
    # JSON, include the twitter photo file path in the dictionary.

    twitter_feed = {}
    tweet_id = 1
    for tweet in tagged_tweets:
        if tweet.media:
            tweet_photo = tweet.media
            twitter_feed[tweet_id] = {'screen_name': tweet.user.screen_name,
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
    
    # Return JSON of dictionary to twitter feed AJAX call on group page.

    return jsonify(twitter_feed)


@app.route('/group_profile_form/<int:group_id>')
def show_group_profile_form(group_id): 
    """Show group's profile form so they can update information"""

    # Get group from database.

    group = Group.query.get(group_id)

    # Use instance method on the class to check if the user id in the session
    # is in the group. 
    if group.is_user_in_group(session["user_id"])==False:
        return redirect("/user") 

    # If user is the group admin, get the group's patterns, check if one is marked 
    # chosen. Render form template with pattern or poll patterns. If user is not 
    # admin, just redirect to grouppage

    else:
        if group.admin_id == session["user_id"]: 
            user = session["user_id"]
            patterns = Pattern.query.filter_by(group_id=group_id).all()
            chosen_pattern = Pattern.query.filter(Pattern.group_id == group_id, Pattern.chosen == True).all()

            if chosen_pattern:
                return render_template("group_update_form.html", group=group, patterns=chosen_pattern)
            else:
                return render_template("group_update_form.html", group=group, patterns=patterns)
        else:
            return redirect("/group_home/%d" % (group.group_id))


@app.route('/group_profile_update/<int:group_id>', methods=['POST'])
def update_group_profile(group_id):
    """Update group profile using inputs from group update form"""

    # Get group from database, use instance method on Group class to check if
    # user in the session is in the group, if not redirect to user homepage.

    group = Group.query.get(group_id)

    if group.is_user_in_group(session["user_id"])==False:
        return redirect("/user") 

    # Get form inputs
    else:
        if group.admin_id == session["user_id"]: 
            chosen_pattern = Pattern.query.filter(Pattern.group_id == group_id, Pattern.chosen == True)

            update_group_name = request.form.get("group_name")
            
            update_group_descrip = request.form.get("group_descrip")
            update_group_hashtag = request.form.get("hashtag")
            
            update_group_pattern_name = request.form.get("update_pattern_name")
            update_group_pattern_link = request.form.get("update_pattern_link")
            
        #Handle basic user name, description, hashtag and image updates from inputs
            if update_group_name != "":
                group.group_name = update_group_name
                # db.session.commit()

            if update_group_descrip != "":
                group.group_descrip = update_group_descrip
                # db.session.commit()

            if update_group_hashtag != "":
                group.hashtag = '#makealong' + update_group_hashtag
                # db.session.commit()

            if "group_img" in request.files and request.files['group_img'].filename:
                group_photo_filename = photos.save(request.files["group_img"])
                update_group_image = str(photos.path(group_photo_filename))
                group.group_image = update_group_image
                # db.session.commit()

        #Update if group had a pattern, and is just changing info about it.
            if update_group_pattern_name != "":
                chosen_pattern.pattern_name = update_group_pattern_name
                # db.session.commit()

            if update_group_pattern_link != "":
                chosen_pattern.pattern_link = update_group_pattern_link
                # db.session.commit()

            if "update_pattern_pdf" in request.files and request.files['update_pattern_pdf'].filename:
                pattern_pdf_filename = manuals.save(request.files['update_pattern_pdf'])
                new_group_pattern_pdf = str(manuals.path(pattern_pdf_filename))
                chosen_pattern.pattern_pdf = new_group_pattern_pdf
                # db.session.commit()

        # Add a pattern to database using helper function if a pattern was inputed
        # on the form and a poll was not created.

            if (request.form.get("new_pattern_name") 
                or request.form.get("new_pattern_link") 
                or ("new_pattern_pdf" in request.files and request.files['new_pattern_pdf'].filename)):

                helper.add_chosen_pattern("new_pattern_name", "new_pattern_link","new_pattern_pdf", group.group_id)

        # If vote days was entered in table, a pattern poll was created. Update fields
        # in group table for poll and use pattern poll helper function to instantiate
        # pattern objects in database.
            
            if request.form.get("vote_days"):
                vote_days = request.form.get("vote_days")
                vote_timestamp = datetime.now()
                group.vote_days = vote_days
                group.vote_timestamp = vote_timestamp
                db.session.commit()

                helper.create_patterns_for_poll(group.group_id)
                

    return redirect("/group_home/%d" % (group.group_id))


@app.route('/flip_clock.json/<int:group_id>')
def update_clock(group_id):
    """Update clock based on time remaining"""

    # Get group from server, call helper function to calculate time left to vote.

    group = Group.query.get(group_id)
    for entry in session["group_timestamps"]:
        if entry[0] == group_id:
            timestamp = entry[1]
    clock_time = {}
    # for demo, use session instead of db
    clock_time['seconds'] = helper.calculate_vote_time_left(
                                                            timestamp,
                                                            group.vote_days)

    # clock_time['seconds'] = helper.calculate_vote_time_left(
    #                                                         group.vote_timestamp,
    #                                                         group.vote_days)
    
    # Send seconds left JSON to clock AJAX call on group page
    return jsonify(clock_time)


@app.route('/poll.json/<int:group_id>')
def get_pattern_poll_data(group_id):
    """ Get and send voting data for vote graph on page load """

    # Get group patterns and votes from database.

    group_patterns = Pattern.query.filter_by(group_id=group_id).all()
    votes = Vote.query.filter(Vote.group_id == group_id).all()

    # Create vote_data dictionary with tallied votes for each pattern.

    vote_data = {} 

    for vote in votes:
        if vote_data.get(vote.pattern.pattern_name, False) == False:
            vote_data[vote.pattern.pattern_name] = 1
        else:
            vote_data[vote.pattern.pattern_name] +=1
        
    for pattern in group_patterns:
        if not vote_data.get(pattern.pattern_name, False):
            vote_data[pattern.pattern_name] = 0

    # Create required poll labels list and data list for chart.js dictionary using
    # vote_data dictionary.

    labels = []
    data = []

    for key in sorted(vote_data):
        labels.append(key)
        data.append(vote_data[key])

    # Create data_set dictionary which is a required value for the datasets key
    # in the chart.js library.

    data_set = {'label': "Votes",
                'fillColor': "rgba(127,89,89,0.5)",
                'highlightFill': "rgba(127,89,89,0.75)",
                'highlightStroke': "rgba(140,98,98,1)"}

    data_set['data'] = data            

    # Create final poll_data dictionary in format required by chart.js, return as 
    # a JSON.

    poll_data = {}
    poll_data['labels'] = labels
    poll_data['datasets'] = [data_set]
    
    return jsonify(poll_data)


@app.route('/update_poll.json', methods=['POST'])
def update_vote():
    """Update voting table based on form input"""

    # Get form inputs from vote form. Instantiate new Vote object in database.

    group_id = request.form.get("group_id")
    pattern_id = request.form.get("pattern_id")

    # disabled for demo
    # vote = Vote(group_id = group_id,
    #             user_id = session["user_id"],
    #             pattern_id = pattern_id)

    # db.session.add(vote)
    # db.session.commit()


    # Create dictionary with new vote info and existing votes in database.

    # vote_update = {}
    # vote_update['label'] = vote.pattern.pattern_name
    # vote_update['data'] = 0

    # current_votes = Vote.query.filter(Vote.group_id == group_id).all()

    # for current_vote in current_votes:
    #     if current_vote.pattern_id == vote.pattern_id:
    #         vote_update['data'] +=1

    # for demo purposes only
    pattern = Pattern.query.filter(Pattern.pattern_id == pattern_id).one()
    vote_update = {}
    vote_update['label'] = pattern.pattern_name
    vote_update['data'] = 1

    current_votes = Vote.query.filter(Vote.group_id == group_id).all()

    for current_vote in current_votes:
        if current_vote.pattern_id == pattern.pattern_id:
            vote_update['data'] +=1
    # Send dictionary JSON to AJAX call that updates poll graph
    return jsonify(vote_update)


@app.route('/final_vote/<int:group_id>', methods=['POST'] )
def handle_final_vote_submit(group_id):
    """Process final pattern vote and mark it confirmed in the pattern table"""

    # Get form value from group admin final vote submission, input value is the
    # pattern id.

    vote = request.form.get('final_vote_submit')
    vote = int(vote)

    # Get pattern by id, mark it confirmed and redirect to the group page.
    # disabled for demo
    pattern = Pattern.query.filter_by(pattern_id = vote).one()
    # pattern.chosen = True
    # db.session.commit()

    # for demo, adding chosen pattern info to session instead of db
    session['chosen_pattern'] = (pattern.group_id, pattern.pattern_id)

    return redirect('/group_home/%d' % group_id)


@app.route('/comment_add.json', methods=['POST'])
def add_comment():
    """Handle comment form submissions"""

    # Get comment form submissions from AJAX form object.

    group_id = request.form.get("group_id")
    comment_text = request.form.get("comment_text")

    # Use helper function to parse text and find YouTube links.

    linked_comment = helper.find_comment_url(comment_text)
    comment_text = linked_comment[0]
    youtube_id = linked_comment[1]
    
    # Check if comment photo exists in form object.

    # if 'comment_image' in request.files and request.files['comment_image'].filename:
    #     comment_img_filename = photos.save(request.files['comment_image'])
    #     comment_image = str(photos.path(comment_img_filename))
    # else:
    #     comment_image = None

    # Disable photo upload for demo
    comment_image = None
    
    # Instantiate Comment object in database.

    # comment = Comment(comment_text=comment_text, 
    #                   comment_image=comment_image, 
    #                   comment_timestamp=datetime.now(),
    #                   youtube_id=youtube_id,
    #                   user_id=session["user_id"],
    #                   group_id=group_id)

    # db.session.add(comment)
    # db.session.commit()    

    # Create dictionary to send as JSON back to comment AJAX call.

    # format_timestamp = comment.comment_timestamp.strftime('%m/%d/%y %X')

    # comment_dict = {'comment_user_photo': comment.user.user_photo,
    #                 'comment_user_name': comment.user.first_name,
    #                 'comment_timestamp':format_timestamp,
    #                 'comment_text': comment.comment_text,
    #                 'comment_image': comment.comment_image,
    #                 'youtube_id': youtube_id }


    # temp comment dictionary created for demo only. Comments will not be
    # added to the database but will still appear on group page
    user = User.query.get(session["user_id"])
    comment_timestamp = datetime.now()
    format_timestamp = comment_timestamp.strftime('%m/%d/%y %X')

    comment_dict = {'comment_user_photo': user.user_photo,
                    'comment_user_name': user.first_name,
                    'comment_timestamp':format_timestamp,
                    'comment_text': comment_text,
                    'comment_image': comment_image,
                    'youtube_id': youtube_id }

    return jsonify(comment_dict)
    

@app.route('/send_invite/<int:group_id>', methods=['POST'])
def send_invitation(group_id):
    """Send email invitation, store invite in database"""

    # Get group and user information from database for the invite

    group = Group.query.get(group_id)
    user=User.query.get(session["user_id"])

    # Get form data and instantiate new Invite object in database.

    invite_name = request.form.get("name")
    invite_email = request.form.get("email")
    invite_text= request.form.get("text")

    invite = Invite(invite_email=invite_email, 
                    invite_text=invite_text, 
                    invite_timestamp=datetime.now(),
                    group_id=group_id,
                    user_id=session["user_id"])
    # disabled for demo
    # db.session.add(invite)
    # db.session.commit()

    # Send email invite using SendGrid API and email.py file, show confirmation
    # flash message and redirect to homepage.

     # disabled for demo
    # send_email(invite_email, invite_name, user.first_name, group.group_name, invite_text)

    flash("Invitation sent!")

    return redirect("/group_home/%d" % (group_id))


if __name__ == "__main__":
    # debug=True here, since it has to be True at the point
    # that the DebugToolbarExtension is invoked
    # app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()
