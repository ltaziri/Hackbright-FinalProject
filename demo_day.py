from sqlalchemy import func
from model import User
from model import Group
from model import UserGroup
from model import Pattern
from model import Invite
from model import Comment
from model import Vote
from model import connect_to_db, db
from server import app


def remove_invite():
    """Remove invite to Cricut Crafters Group."""

    UserGroup.query.filter(UserGroup.user_id==1, UserGroup.group_id==9).delete()

    invite = Invite.query.filter(Invite.invite_email=='leilani@hbmail.com').first();

    invite.invite_confirm = False

    db.session.commit()

def reset_sew_page():
    """Reset votes and comments on sewing page"""

    Vote.query.filter(Vote.user_id==1, Vote.group_id==2).delete()

    # Comment.query.filter(Comment.group_id==2).delete()

    pattern = Pattern.query.filter(Pattern.group_id==2, Pattern.chosen == True).first()

    pattern.chosen = False

    db.session.commit()

def reset_knit_page():
    """Reset comments on knit page"""
    
    Comment.query.filter(Comment.group_id==1, Comment.comment_id > 27).delete()

    db.session.commit()
# def reset_wood_pattern():
#     """Update wood group to not have a chosen pattern"""

#     pattern = Pattern.query.filter(Pattern.group_id==5, Pattern.chosen == True).first()

#     pattern.chosen = False

#     db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    remove_invite()
    reset_sew_page()
    reset_knit_page()
    # reset_wood_pattern()

