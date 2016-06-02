
from delorean import Delorean
from datetime import datetime, timedelta
from model import User, Group, UserGroup, Comment, Invite, Pattern, Vote, connect_to_db, db
from flask import request, session
# from server import photos, manuals
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import re
from urlparse import urlparse


def calculate_vote_time_left(start_timestamp, vote_days):
    """Calculate seconds left to vote in group pattern poll

        >>> current = datetime.now()
        >>> calculate_vote_time_left(current, 5)
        406799

        >>> calculate_vote_time_left(current, 1)
        61199

    """

    # Flip clock needs remaining seconds in poll. First convert timestamp to a
    # Delorean object for ease of calculation. Next calculate end time by converting
    # vote days to hours and adding those hours to the clock start.
    clock_start = Delorean(datetime=start_timestamp, timezone='UTC')
    time_in_hours  = vote_days * 24
    clock_end = clock_start + timedelta(hours = time_in_hours)

    # Get current day and time and calculate seconds remaining in poll.
    current_day_time = Delorean()
    days_remaining =  clock_end - current_day_time
    seconds_remaining = int(days_remaining.total_seconds())

    return seconds_remaining


def create_group_messages(group):
    """Create dictionary for user messages by group if admin has logged in"""

    # This dictionary feeds the message section on the user homepage
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

    if session.get('chosen_pattern'):
        if session['chosen_pattern'][0] == group.group_id:
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
    """Add a group pattern if only one was chosen"""

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
    # disabled for demo
    # db.session.add(pattern)
    # db.session.commit()


def add_poll_pattern(name, link, pdf, group_id):
    """Add a individual poll pattern if a poll was created"""

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
    # disabled for demo
    # db.session.add(pattern)
    # db.session.commit()


def create_patterns_for_poll(group_id):
    """Create all the patterns for a poll when group poll is created"""

    if request.form.get("pattern_name_a"):
        add_poll_pattern("pattern_name_a", "pattern_link_a","pattern_pdf_a", group_id)


    if request.form.get("pattern_name_b"):
        add_poll_pattern("pattern_name_b", "pattern_link_b","pattern_pdf_b", group_id)


    if request.form.get("pattern_name_c"): 
        add_poll_pattern("pattern_name_c", "pattern_link_c","pattern_pdf_c", group_id)



def find_comment_url(comment_text):
    """Parse through text inputs to find links and video ids

        >>> find_comment_url('This is a comment that contains no links')
        ['This is a comment that contains no links', None]

        >>> find_comment_url('This is a comment that contains some text and a url https://www.ravelry.com')
        ["This is a comment that contains some text and a url <a href='https://www.ravelry.com'>https://www.ravelry.com</a>", None]
        
        >>> find_comment_url('This is a comment that contains some text and a youtube link https://www.youtube.com/watch?v=z_rtwaPpUW8')
        ["This is a comment that contains some text and a youtube link <a href='https://www.youtube.com/watch?v=z_rtwaPpUW8'>https://www.youtube.com/watch?v=z_rtwaPpUW8</a>", 'z_rtwaPpUW8']
    
    """

    # Regular expression to find links in text
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', comment_text)

    # url exists check for youtube links and insert link tag for the link 
    # around the link in the comment text

    if url:
        video_id = find_youtube(url)
        allowed = find_allowed_url(url[0])
        if allowed:
            position = comment_text.index(url[0])
            link_length = len(url[0])
            new_comment = (comment_text[0:position]+"<a href='" + url[0] + "'>" 
                          + comment_text[position:position+link_length] + "</a>" 
                          + comment_text[position+link_length:]) 
        else:
            new_comment = comment_text
        if len(url) > 1:
            for u in url[1:]:
                allowed = find_allowed_url(u)
                if allowed:
                    position = new_comment.index(u)
                    link_length = len(u)
                    new_comment = (new_comment[0:position]+"<a href='" + u + "'>" 
                                   + new_comment[position:position+link_length] 
                                   + "</a>" + new_comment[position+link_length:]) 
    else:
        new_comment = comment_text
        video_id = None

    result = [new_comment, video_id]

    return result


def find_youtube(url_list):
    """Identify youtube ids

        >>> find_youtube(['https://www.youtube.com/watch?v=z_rtwaPpUW8'])
        'z_rtwaPpUW8'

        >>> find_youtube(['https://www.ravelry.com'])
        >>>

    """

    # Using python url parser to check if any link source is from youtube.
    # Result after using url parse method is as follows: 
    # ParseResult(scheme='https', netloc='www.youtube.com', 
    # path='/watch', params='', query='v=z_rtwaPpUW8', fragment='')
    # Youtube id for iframe window is after the "v" in query.    

    if len(url_list) == 1:
        parsed_url = urlparse(url_list[0])
        if parsed_url.netloc == 'www.youtube.com':
            video_id = parsed_url.query[2:]
        else:
            video_id = None
    elif len(url_list) > 1:
        for i in range(0,len(url_list),2):
            parsed_url = urlparse(url_list[i])
            if parsed_url.netloc == 'www.youtube.com':
                video_id = parsed_url.query[2:]
                break
            else:
                video_id = None

    return video_id

def find_allowed_url(url):
    """Identify accepted urls"""

    # Using python url parser to check if any link source is from an accepted website. 
    whitelist = ['www.raverly.com',
                 'www.youtube.com', 
                 'www.etsy.com', 
                 'www.fabric.com', 
                 'www.pinterest.com']

    
    parsed_url = urlparse(url)
    if parsed_url.netloc in whitelist:
        return True
    else:
        return False
    




