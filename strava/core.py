from datetime import datetime, timedelta
from collections import defaultdict
from utils.config import cache
from utils import helpers
from strava.constants import Cache
from strava import endpoints


def get_activities_data(start_date, end_date, activity_type=None, year=None):
	"""
	Returns a dictionary of date strings to an object of data points for
	each date, bounded by start_date and end_date.
	i.e. {'2022-01-01': {'activity_count': 2, 'suffer_score': 50.0}}
	"""
	epoch_before = helpers.timestamp_to_unix(str(end_date))
	epoch_after = helpers.timestamp_to_unix(str(start_date))

	activities_cache_key = Cache.athlete_activities_year_cache_key.format(str(year))
	last_synced_cache_key = Cache.last_synced_cache_key

	cache_last_synced = cache.get(last_synced_cache_key)
	cached_athlete_activities = cache.get(activities_cache_key) or []

	athlete_activities = []
	if not cached_athlete_activities or not cache_last_synced:
		athlete_activities = endpoints.get_athlete_activities_paginated(before=epoch_before, after=epoch_after)
	else:
		if cache_last_synced and cache_last_synced != datetime.today().date():
			cache_last_synced = cache_last_synced - timedelta(hours=12)
			cache_last_synced = helpers.timestamp_to_unix(str(cache_last_synced))
			new_athlete_activities = endpoints.get_athlete_activities_paginated(before=epoch_before, after=cache_last_synced)
			athlete_activities = cached_athlete_activities + new_athlete_activities

	athlete_activities = cached_athlete_activities or athlete_activities
	date_data_map = defaultdict(lambda: defaultdict(int))
	activity_types = set()

	activities = athlete_activities
	if activity_type:
		activities = [d for d in athlete_activities if d['type'] == activity_type]
	for activity in activities:
		# Generate activity types
		workout_type = activity.get('type')
		activity_types.add(workout_type)

		# Format of '2022-04-29T12:38:43Z' but we only care about the date
		date_timestamp = activity.get('start_date').split('T')[0]

		date_data_map[date_timestamp]['activity_count'] += 1
		date_data_map[date_timestamp]['suffer_score'] += activity.get('suffer_score', 0)

	cache.set(activities_cache_key, athlete_activities)
	cache.set(last_synced_cache_key, datetime.today().date())

	return {
		'activity_types': activity_types,
		'date_data_map': date_data_map
	}
