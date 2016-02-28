
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

def example_data():
    """Create some sample data for test file."""

    # In case this is run more than once, empty out existing data
    # User.query.delete()
    # Group.query.delete()
    # UserGroup.query.delete()
    # Comment.query.delete()
    # Invite.query.delete()
    
    


    ua = User( 
              user_id=1,
              email = "usera@gmail.com", 
              password = "test", 
              first_name = "Bob", 
              last_name = "Smith",
              user_photo = "static/images/sewing_machine.jpg",
              user_descrip = "Knitting Rules!")

    ub = User(
              user_id=2, 
              email = "userb@gmail.com", 
              password = "test", 
              first_name = "Jane", 
              last_name = "Doe",
              user_photo = "static/images/glue_gun.jpg",
              user_descrip = "Sewing Rocks!")


    uc = User( 
              user_id=3,
              email = "userc@gmail.com", 
              password = "test", 
              first_name ="Betty", 
              last_name = "Sue",
              user_photo = "static/images/crafter.jpg",
              user_descrip = "DIY to the rescue!")
  

    ga = Group(
               group_id=1,
               group_name = "Knit Knit Knit",
               group_descrip = "Lets knit some stuff!",
               group_image = "static/images/knitting_group_default.jpg", 
               admin_id = 1, 
               vote_timestamp = datetime.now(),
               hashtag= "#test",
               vote_days = 3)

    gb = Group(
               group_id=2,
               group_name = "Sew Sew Sew",
               group_descrip = "Lets sew some stuff!",
               group_image = "static/images/sewing_group_default.jpg",
               admin_id = 1, 
               vote_timestamp = datetime.now(),
               hashtag= "#testtwo",
               vote_days = 5)


    ca = Comment(
                 comment_text = "I live for this pattern!",
                 comment_image = "static/images/balloonicorn.jpg",
                 comment_timestamp = datetime.now(),
                 user_id = 1,
                 group_id = 1)

    cb = Comment(
                 comment_text = "Can't stop, wont stop!",
                 comment_image = "static/images/tiger.jpeg",
                 comment_timestamp = datetime.now(),
                 user_id = 2,
                 group_id = 2)

    ia = Invite(invite_email = "friend@gmail.com", 
                    invite_text = "come sew with me", 
                    invite_timestamp = datetime.now(),
                    group_id = 2,
                    user_id = 3)

    ib = Invite(invite_email = "friendb@gmail.com", 
                    invite_text = "come knit with me", 
                    invite_timestamp = datetime.now(),
                    group_id = 1,
                    user_id = 1)

    # uga = UserGroup(group_id = 1, user_id = 1)
    # ugb = UserGroup(group_id = 1, user_id = 2)
    # ugc = UserGroup(group_id = 1, user_id = 3)
    # ugd = UserGroup(group_id = 2, user_id = 1)
    # uge = UserGroup(group_id = 2, user_id = 2)
    # ugf = UserGroup(group_id = 2, user_id = 3)
    db.session.add_all([ ca, cb, ia, ib])
    # db.session.add_all([ua, ub, uc, ga, gb, uga, ugb, ugc, ugd, uge, ugf, ca, cb, ia, ib])
    db.session.commit()





def connect_to_db(app, db_uri="postgresql:///virtcraft"):
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