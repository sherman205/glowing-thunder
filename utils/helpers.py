import time
from datetime import datetime


def timestamp_to_unix(timestamp_string):
    """Convert datetime object to epoch time"""
    timestamp_datetime = datetime.strptime(timestamp_string, "%Y-%m-%d")
    datetime_tuple = timestamp_datetime.timetuple()
    unix_timestamp = int(time.mktime(datetime_tuple))
    return unix_timestamp
