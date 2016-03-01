
"""Models and database functions for Leilani's project."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    user_photo = db.Column(db.String(255), nullable=False)
    user_descrip = db.Column(db.String(255), nullable=True)

    groups = db.relationship("Group", 
                             secondary='usergroups', 
                             backref=db.backref("users", order_by=user_id))

    def __repr__(self):
        """Provide user information when printed."""

        return "<User: %s %s Email: %s>" %(self.first_name, self.last_name, self.email)


class UserGroup(db.Model):
    """Association table for linking users and groups"""

    __tablename__ = "usergroups"

    usergroup_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    
    def __repr__(self):
        """Provide usergroup information when printed."""

        return "<Group name: %s User name: %s>" %(self.group_name, self.user_name)


class Group(db.Model):
    """Group information, groups contain many users"""

    __tablename__ = "groups"

    group_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    group_name = db.Column(db.String(64), nullable=False)
    group_descrip = db.Column(db.String(255), nullable=True)
    group_image = db.Column(db.String(255), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    vote_timestamp = db.Column(db.DateTime, nullable=True) 
    vote_days = db.Column(db.Integer, nullable=True)
    hashtag = db.Column(db.String(64), nullable=True)
    admin = db.relationship("User", backref=db.backref("group", order_by=group_id))

    def __repr__(self):
        """Provide group information when printed."""

        return "<Group Id: %s Group name: %s>" %(self.group_id, self.group_name)

    def is_user_in_group(self, user_id):
        """ Check if a user is in a group"""

        if user_id in [user.user_id for user in self.users]:
            return True
        else:
            return False


class Comment(db.Model):
    """Comment information for each comment in a group"""

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    comment_text = db.Column(db.String(255), nullable=False)
    comment_image = db.Column(db.String(255), nullable=True) 
    comment_timestamp = db.Column(db.DateTime, nullable=False)   
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False) 
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=False)

    group = db.relationship("Group", backref=db.backref("comments", order_by=comment_id))     
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
    invite_confirm = db.Column(db.Boolean, nullable=False, default=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=False)   
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    group = db.relationship("Group", backref=db.backref("invites", order_by=invite_id))
    user = db.relationship("User", backref=db.backref("invites", order_by=invite_id))

    def __repr__(self):
        """Provide invite information when printed."""

        return "<Invite Id: %s From user: %s To: %s>" %(self.invite_id, self.user_id, self.invite_email)


class Pattern(db.Model):
    """"Pattern information for poll and ultimately group"""

    __tablename__= "patterns"

    pattern_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    pattern_name = db.Column(db.String(255), nullable=False)
    pattern_link = db.Column(db.String(255), nullable=True) 
    pattern_pdf = db.Column(db.String(255), nullable=True)
    chosen = db.Column(db.Boolean, nullable=False, default=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=False)   
    
    group = db.relationship("Group", backref=db.backref("patterns", order_by=pattern_id))
    
    def __repr__(self):
        """Provide invite information when printed."""

        return "<Pattern Id: %s Pattern Name: %s>" %(self.pattern_id, self.pattern_name)


class Vote(db.Model):
    """Vote information for group patttern polls"""

    __tablename__ = "votes"
    __table_args__ = (db.UniqueConstraint('group_id', 'user_id'),)

    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    pattern_id = db.Column(db.Integer, db.ForeignKey('patterns.pattern_id'), nullable=False)

    group = db.relationship("Group", backref=db.backref("votes"))
    user = db.relationship("User", backref=db.backref("votes"))
    pattern = db.relationship("Pattern", backref=db.backref("votes"))

    def __repr__(self):
        """Provide invite information when printed."""

        return "<Vote = Group Id: %d User Id: %d Pattern Id: %d>" % (self.group_id, self.user_id, self.pattern_id)

##############################################################################
# Helper functions

def connect_to_db(app, db_uri="postgresql:///virtcraft"):

# def connect_to_db(app, db_uri="postgresql:///testdb"):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."