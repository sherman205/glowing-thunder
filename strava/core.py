from datetime import datetime
from collections import defaultdict

from utils import helpers
from strava import endpoints


def get_activities_count_per_day(start_date, end_date):
	"""
	Returns a dictionary of date strings to number of Strava activities for
	each date, bounded by start_date and end_date.
	i.e. {'2022-01-01': 2}
	"""
	epoch_before = helpers.timestamp_to_unix(str(end_date))
	epoch_after = helpers.timestamp_to_unix(str(start_date))
	athlete_activities = []
	resp = endpoints.get_athlete_activities(before=epoch_before, after=epoch_after, per_page=100)
	athlete_activities.append(resp)
	page = 2
	while len(resp) != 0:
		resp = endpoints.get_athlete_activities(before=epoch_before, after=epoch_after, page=page, per_page=100)
		if resp:
			athlete_activities.append(resp)
			page += 1

	# concatenate all the results from all the pages
	athlete_activities = sum(athlete_activities, [])

	date_to_count_map = defaultdict(int)
	for activity in athlete_activities:
		# Format of '2022-04-29T12:38:43Z' but we only care about the date
		date_timestamp = activity.get('start_date').split('T')[0]
		date_to_count_map[date_timestamp] += 1

	return date_to_count_map
