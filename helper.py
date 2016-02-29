
from delorean import Delorean
from datetime import datetime, timedelta

def calculate_vote_time_left(start_timestamp, vote_days):
    """Calculate seconds left to vote in group pattern poll"""

    clock_start = Delorean(datetime=start_timestamp, timezone='UTC')
    time_in_hours  = vote_days * 24
    clock_end = clock_start + timedelta(hours = time_in_hours)
    current_day_time = Delorean()
    days_remaining =  clock_end - current_day_time
    seconds_remaining = int(days_remaining.total_seconds())

    return seconds_remaining
