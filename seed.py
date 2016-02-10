from sqlalchemy import func
from model import User
from model import Group
from model import UserGroup

from model import connect_to_db, db
from server import app

def load_users():
    """Load users from user.txt into database."""

    print "Users"

    User.query.delete()

    for row in open("seed_data/users.txt"):
        row = row.rstrip()
        user_id, email, password, first_name, last_name, user_photo, user_descrip = row.split("|")

        user = User(user_id=user_id,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    user_photo=user_photo,
                    user_descrip=user_descrip
                    )

        db.session.add(user)

    db.session.commit()


def load_groups():
    """Load groups from groups.txt into database."""

    print "Groups"

    Group.query.delete()

    for row in open("seed_data/groups.txt"):
        row = row.rstrip()
        group_id, group_name, group_descrip, group_image, pattern_image, pattern_link, pattern_name = row.split("|")

        group = Group(group_id=group_id,
                      group_name=group_name,
                      group_descrip=group_descrip,
                      group_image=group_image, 
                      pattern_image=pattern_image, 
                      pattern_link=pattern_link,
                      pattern_name=pattern_name
                      )

        db.session.add(group)

    db.session.commit()

def load_usergroups():
    """Load usergroups from usergroups.txt into database."""

    print "UserGroups"

    UserGroup.query.delete()

    for row in open("seed_data/usergroup.txt"):
        row = row.rstrip()
        usergroup_id, group_id, user_id = row.split("|")

        usergroup = UserGroup(usergroup_id=usergroup_id,
                              group_id=group_id,
                              user_id=user_id)

        db.session.add(usergroup)

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_group_id():
    """Set value for the next group_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Group.group_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('groups_group_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_groups()
    load_usergroups()
    
    set_val_user_id()
    set_val_group_id()
