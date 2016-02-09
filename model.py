"""Models and database functions for Leilani's project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    
    def __repr__(self):
        """Provide user information when printed."""

        return "<User: %s %s Email: %s>" %(self.first_name, self.last_name, self.email)


class Group(db.Model):
    """Group information, groups contain many users"""

    __tablename__ = "groups"

    group_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    group_name = db.Column(db.String(64), nullable=False)
    group_image = db.Column(db.String(255), nullable=False) # need to add default image
    pattern_image = db.Column(db.String(255), nullable=True)
    pattern_image = db.Column(db.String(255), nullable=True)    
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.comment_id'), nullable=True)

    comment = db.relationship("Comment", backref=db.backref("groups", order_by=group_id))

    def __repr__(self):
        """Provide group information when printed."""

        return "<Group Id: %s Group name: %s>" %(self.group_id, self.group_name)


class UserGroup(db.Model):
    """Association table for linking users and groups"""

    __tablename__ = "usergroups"

    usergroup_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)

    group = db.relationship("Group", backref=db.backref("usergroups", order_by=usergroup_id))
    user = db.relationship("User", backref=db.backref("usergroups", order_by=usergroup_id))

    def __repr__(self):
        """Provide usergroup information when printed."""

        return "<Group name: %s User name: %s>" %(self.group_name, self.user_name)


class Comment(db.Model):
    """Comment information for each comment in a group"""

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    comment_text = db.Column(db.String(255), nullable=False)
    comment_image = db.Column(db.String(255), nullable=True) 
    comment_timestamp = db.Column(db.DateTime, nullable=False)   
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
     
    user = db.relationship("User", backref=db.backref("comments", order_by=comment_id))

    def __repr__(self):
        """Provide comment information when printed."""

        return "<Comment Id: %s User: %s>" %(self.comment_id, self.user_id)


class Invite(db.Model):
    """"Invite information for each invite that a user sends"""

    __tablename__= "invites"

    invite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    invite_email = db.Column(db.String(255), nullable=False)
    invite_text = db.Column(db.String(255), nullable=False) 
    invite_timestamp = db.Column(db.DateTime, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=False)   
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    group = db.relationship("Group", backref=db.backref("invites", order_by=invite_id))
    user = db.relationship("User", backref=db.backref("invites", order_by=invite_id))

    def __repr__(self):
        """Provide invite information when printed."""

        return "<Invite Id: %s From user: %s To: %s>" %(self.invite_id, self.user_id, self.invite_email)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/virtcraft'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
