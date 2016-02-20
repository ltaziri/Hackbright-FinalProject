

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from model import User, Group, UserGroup, Comment, Invite, Pattern, connect_to_db, db
from datetime import datetime
import sendgrid
from email_test import send_email
import sendgrid
import os
import sys
from chart import chart_data

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

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


@app.route('/invite/<invite_id>')
def invite_index(invite_id):
    """Redirect to landing page when accepting an invite"""

    session["invite_id"] = invite_id

    return redirect("/")


@app.route('/sign_in', methods=['POST'])
def handle_sign_in_form():
    """Handle submission of the sign in form."""

    email = request.form.get("email")
    password = request.form.get("password")

    existing_user = User.query.filter_by(email=email).one()

    if existing_user:
        if password == existing_user.password:
            session["user_id"] = existing_user.user_id
            if session.get("invite_id"):
                invite = Invite.query.get(session["invite_id"])
                if invite.invite_confirm == False and email == invite.invite_email: 
                    invite.invite_confirm = True
                    user_group = UserGroup(
                                           group_id=invite.group_id,
                                           user_id=existing_user.user_id
                                           )
                    db.session.add(user_group)
                    db.session.commit()
                del session['invite_id']
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
    password = request.form.get("password")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    
    # use Flask-Uploads to add file path for uploaded photo or add path
    # to default image that was selected on radio button.  
    if request.form.get("user_photo") == " ":
        filename = photos.save(request.files['photo'])
        user_photo = str(photos.path(filename))
    else:
        user_photo = request.form.get("user_photo")
    
    # check if someone is already signed up for an account with that email
    # if not create a new user in users table. Check if that person came to 
    # the website via and invite link, if so add an entry to the association
    # usergroup table so the user joins the group.

    existing_user = User.query.filter_by(email=email).first()
    
    if existing_user:
        flash("email already exists, please sign in")
        return redirect("/")
    else:
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

        if session.get("invite_id"):
            print session
            invite = Invite.query.get(session["invite_id"])
            if email == invite.invite_email:  
                invite.invite_confirm = True
                user_group = UserGroup(
                                       group_id=invite.group_id,
                                       user_id=user.user_id
                                       )
                db.session.add(user_group)
                db.session.commit()
            del session['invite_id']

        flash("You are successfully signed up!")

    return redirect('/user')


@app.route('/user')
def show_user_home(): 
    """Show user's homepage""" 

    user = User.query.get(session["user_id"])

    groups = user.groups

    return render_template("user_home.html", user=user, groups=groups)


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
    
    if request.form.get("group_image") == " ":
        filename = photos.save(request.files['photo'])
        group_image = str(photos.path(filename))

    else:
        group_image = request.form.get("group_image")

    group = Group(group_name=group_name,
                  group_descrip=group_descrip, 
                  group_image=group_image,  
                  admin_id=user.user_id)

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
        or  "pattern_pdf_a" in request.files):

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
        or  "pattern_pdf_b" in request.files):

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
        or  "pattern_pdf_c" in request.files):

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

    groups_ids = []
    for group_user in group_users:
        groups_ids.append(group_user.user_id)

    if session["user_id"] in groups_ids:

        user = session["user_id"]

        comments =  Comment.query.filter_by(group_id=group_id)

        patterns = Pattern.query.filter_by(group_id=group_id).all()

        chosen_pattern = Pattern.query.filter(Pattern.group_id == group_id, Pattern.chosen == True).all()
        

        if chosen_pattern:
            return render_template("group_page.html", 
                        group=group, 
                        group_users=group_users, 
                        user=user,
                        comments=comments,
                        patterns = chosen_pattern)
        else:
            return render_template("group_page.html", 
                        group=group, 
                        group_users=group_users, 
                        user=user,
                        comments=comments,
                        patterns = patterns)

    else:
        return redirect("/user")


@app.route('/group_profile_form/<int:group_id>')
def show_group_profile_form(group_id): 
    """Show group's profile form so they can update information"""

    group = Group.query.get(group_id)

    group_users = group.users

    groups_ids = []
    for group_user in group_users:
        groups_ids.append(group_user.user_id)

    if session["user_id"] in groups_ids:
        return render_template("group_update_form.html", group=group)
    else:
        return redirect("/user")


@app.route('/group_profile_update/<int:group_id>', methods=['POST'])
def update_group_profile(group_id):
    """Update group profile using inputs from group update form"""

    group = Group.query.get(group_id)

    new_group_name = request.form.get("group_name")
    new_group_descrip = request.form.get("group_descrip")
    new_group_pattern_name = request.form.get("pattern_name")
    new_group_pattern_link = request.form.get("pattern_link")
    

    if new_group_name != "":
        group.group_name = new_group_name
        db.session.commit()
    if new_group_descrip != "":
        group.group_descrip = new_group_descrip
        db.session.commit()
    if "group_img" in request.files:
        group_photo_filename = photos.save(request.files["group_img"])
        new_group_image = str(photos.path(group_photo_filename))
        group.group_image = new_group_image
        db.session.commit()
    if new_group_pattern_name != "":
        group.pattern_name = new_group_pattern_name
        db.session.commit()
    if "pattern_pdf" in request.files:
        pattern_pdf_filename = manuals.save(request.files['pattern_pdf'])
        new_group_pattern_pdf = str(manuals.path(pattern_pdf_filename))
        group.pattern_pdf = new_group_pattern_pdf
        db.session.commit()
    if new_group_pattern_link != "":
        group.pattern_link = new_group_pattern_link
        db.session.commit()
        
    return redirect("/group_home/%d" % (group.group_id))

@app.route('/poll_chart')
def show_pattern_poll():

    return render_template('chart_test.html')


@app.route('/poll.json')
def send_pattern_poll_data():
    """ send voting data to pattern poll"""

    poll_data = chart_data('pattern1', 'pattern2', 'pattern3', 1, 5, 6)

    return jsonify(poll_data) 


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

    group_users = group.users

    groups_ids = []
    for group_user in group_users:
        groups_ids.append(group_user.user_id)

    if session["user_id"] in groups_ids:
        return render_template("invite_form.html", group=group)
    else:
        return redirect("/user")


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

    send_email(invite_email, invite_name, user.first_name, group.group_name, invite_text, invite.invite_id)

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
