

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Group, UserGroup, Comment, Invite, connect_to_db, db
from datetime import datetime
import sendgrid
from email_test import send_email
import sendgrid

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""

    if session.get("user_id"):
        return redirect("/users/"+str(session["user_id"]))

    else:
        return render_template("homepage.html")

@app.route('/<int:group_id>')
def index(group_id):
    """Homepage"""

    group = Group.query.get(group_id)

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
            return redirect("/users/%s" % str(existing_user.user_id)) # log in
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
    flash("You have been logged out.")

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

    
    new_user = User.query.filter_by(email=email).first()

    if new_user:
        flash("email already exists, please sign in")
        return redirect("/")
    else:
        user = User(email=email, password=password, first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()
        flash("You are successfully signed up! Please sign in.")

    return redirect('/')

   
@app.route('/users/<int:user_id>')
def show_user_home(user_id):    
    """User's homepage after loging in"""

    user = User.query.get(user_id)

    groups = user.groups


    return render_template("user_home.html", user=user, groups=groups)

@app.route('/user_profile/<int:user_id>')
def show_user_profile(user_id): 
    """Show users profile page"""

    user = User.query.get(user_id)

    return render_template("user_profile.html", user=user)


@app.route('/user_profile_form/<int:user_id>')
def show_user_profile_form(user_id): 
    """Show users profile form so they can update information"""

    user = User.query.get(user_id)

    return render_template("user_profile_form.html", user=user)


@app.route('/user_profile_update/<int:user_id>',methods=['POST'])
def user_profile_update(user_id): 
    """Handle user profile form to update users profile"""

    user = User.query.get(user_id)
    user_photo = request.form.get("user_photo")
    user_descrip = request.form.get("user_descrip")

    if user_photo:
        user.user_photo = user_photo
        db.session.commit()

    if user_descrip:
        user.user_descrip = user_descrip
        db.session.commit()

    return redirect("/user_profile/%d" % user_id)


@app.route('/group_form/<int:user_id>')
def show_group_form(user_id):
    """Create a new group form"""

    user = User.query.get(user_id)

    return render_template("group_form.html", user=user)


@app.route('/create_group/<int:user_id>', methods=['POST'])
def create_group(user_id):
    """Handle submission of new group form"""

    user = User.query.get(user_id)
    group_name = request.form.get("group_name")
    group_image= request.form.get("group_image")
    pattern_image = request.form.get("pattern_image")
    pattern_link = request.form.get("pattern_link")

    group = Group(group_name=group_name, 
                  group_image=group_image, 
                  pattern_image=pattern_image, 
                  pattern_link=pattern_link)

    db.session.add(group)
    db.session.commit()
    
    user_group= UserGroup(group_id=group.group_id,
                          user_id=user_id)

    db.session.add(user_group)
    db.session.commit()

    return redirect("/group_home/%d" % (group.group_id))


@app.route('/group_home/<int:group_id>')
def show_group_page(group_id):
    """Show group's homepage"""

    group = Group.query.get(group_id)

    group_users = group.users

    user = session["user_id"]

    comments =  Comment.query.filter_by(group_id=group_id)


    return render_template("group_page.html", 
                            group=group, 
                            group_users=group_users, 
                            user=user,
                            comments=comments)


@app.route('/comment_form/<int:group_id>')
def show_comment_form(group_id):
    """Show form for adding a comment"""

    group = Group.query.get(group_id)

    return render_template("comment_form.html", group=group)


@app.route('/comment_add/<int:group_id>', methods=['POST'])
def add_comment(group_id):
    """Handle comment form submissions"""

    group = Group.query.get(group_id)

    comment_text = request.form.get("comment_text")
    comment_image= request.form.get("comment_image")

    comment = Comment(comment_text=comment_text, 
                      comment_image=comment_image, 
                      comment_timestamp=datetime.now(),
                      user_id=session["user_id"],
                      group_id=group_id)

    db.session.add(comment)
    db.session.commit()

    return redirect("/group_home/%d" % (group_id))


@app.route('/user_public_profile/<int:user_id>')
def show_other_user_profile(user_id):
    """Show public profile info for other users"""

    user = User.query.get(user_id)

    return render_template("user_public_profile.html", user=user)


@app.route('/invite_form/<int:group_id>')
def show_invite_form(group_id):
    """Show group invite form"""

    group = Group.query.get(group_id)

    return render_template("invite_form.html", group=group)


@app.route('/send_invite/<int:group_id>', methods=['POST'])
def send_invitation(group_id):
    """Send email invitation, store invite in databse"""

    group = Group.query.get(group_id)
    user=User.query.get(session["user_id"])

    invite_name = request.form.get("name")

    invite_email = request.form.get("email")
    invite_text= request.form.get("text")


    send_email(invite_email, invite_name, user.first_name, group.group_name, invite_text, group_id)

    invite = Invite(invite_email=invite_email, 
                    invite_text=invite_text, 
                    invite_timestamp=datetime.now(),
                    group_id=group_id,
                    user_id=session["user_id"],
                    )

    db.session.add(invite)
    db.session.commit()
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
