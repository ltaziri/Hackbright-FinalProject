
from delorean import Delorean
from datetime import datetime, timedelta
from model import User, Group, UserGroup, Comment, Invite, Pattern, Vote, connect_to_db, db
from flask import request
from server import photos, manuals
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import re
from urlparse import urlparse


def calculate_vote_time_left(start_timestamp, vote_days):
    """Calculate seconds left to vote in group pattern poll"""

    clock_start = Delorean(datetime=start_timestamp, timezone='UTC')
    time_in_hours  = vote_days * 24
    clock_end = clock_start + timedelta(hours = time_in_hours)
    current_day_time = Delorean()
    days_remaining =  clock_end - current_day_time
    seconds_remaining = int(days_remaining.total_seconds())

    return seconds_remaining


def create_group_messages(group):
    """Create dictionary for user messages by group"""

    message_dict ={}
    users_in_group = UserGroup.query.filter_by(group_id=group.group_id).all()
    votes_for_group = Vote.query.filter_by(group_id=group.group_id).all()
    patterns_for_group = Pattern.query.filter_by(group_id =group.group_id).all()

    if group.vote_timestamp:
        message_dict['remaining_time'] = calculate_vote_time_left(
                                                                  group.vote_timestamp,
                                                                  group.vote_days)
    else:
        message_dict['remaining_time'] = False 
    
    for pattern in patterns_for_group:
        if pattern.chosen == True:
            message_dict['pattern_chosen'] = True  

    patternless = message_dict.get('pattern_chosen', False)
    if not patternless:
        message_dict['pattern_chosen'] = False

    message_dict['group_id'] = group.group_id
    message_dict['admin'] = group.admin_id
    message_dict['user_count'] = len(users_in_group)
    message_dict['vote_count'] = len(votes_for_group)

    return message_dict


def add_chosen_pattern(name, link, pdf, group_id):
    """add a group pattern or poll pattern"""

    pattern_name = request.form.get(name)
    pattern_link = request.form.get(link)

    if pdf in request.files and request.files[pdf].filename:
        pdf_filename = manuals.save(request.files[pdf])
        pattern_pdf = str(manuals.path(pdf_filename))
    else:
        pattern_pdf = None

    pattern = Pattern(pattern_name = pattern_name,
                      pattern_link = pattern_link,
                      pattern_pdf = pattern_pdf,
                      chosen = True,
                      group_id = group_id)

    db.session.add(pattern)
    db.session.commit()

def add_poll_pattern(name, link, pdf, group_id):
    """add a group pattern or poll pattern"""

    pattern_name = request.form.get(name)
    pattern_link = request.form.get(link)

    if pdf in request.files and request.files[pdf].filename:
        pdf_filename = manuals.save(request.files[pdf])
        pattern_pdf = str(manuals.path(pdf_filename))
    else:
        pattern_pdf = None

    pattern = Pattern(pattern_name = pattern_name,
                      pattern_link = pattern_link,
                      pattern_pdf = pattern_pdf,
                      chosen = False,
                      group_id = group_id)

    db.session.add(pattern)
    db.session.commit()


def create_patterns_for_poll(group_id):
    """create patterns for poll when group poll is created"""

    if request.form.get("pattern_name_a"):
        add_poll_pattern("pattern_name_a", "pattern_link_a","pattern_pdf_a", group_id)


    if request.form.get("pattern_name_b"):
        add_poll_pattern("pattern_name_b", "pattern_link_b","pattern_pdf_b", group_id)


    if request.form.get("pattern_name_c"): 
        add_poll_pattern("pattern_name_c", "pattern_link_c","pattern_pdf_c", group_id)


def find_comment_youtube(comment_text):
    """Parse through text inputs to find youtube links"""
    
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', comment_text)

    if url:
        parsed_url = urlparse(url[0])
        if parsed_url.netloc == 'www.youtube.com':
            video_id = parsed_url.query[2:]
        else:
            video_id = None
    else:
        video_id= None
            
    return video_id