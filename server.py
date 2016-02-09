

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Group, UserGroup, Comment, Invite, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""

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

    return render_template("group_page.html", 
                            group=group, 
                            group_users=group_users, 
                            user=user)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
