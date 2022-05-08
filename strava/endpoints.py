from . import utils
from . import constants


def get_authenticated_athlete():
	"""Returns the currently authenticated athlete."""
	endpoint = f"{constants.STRAVA_BASE_URL}/api/v3/athlete"
	response = utils.make_request(endpoint)
	return response


def get_athlete_activities(before=None, after=None, page=None, per_page=30):
	"""Returns the activities of an athlete for a specific identifier."""
	endpoint = f"{constants.STRAVA_BASE_URL}/api/v3/athlete/activities"
	params = {
		'per_page': per_page
	}
	if before:
		params['before'] = before
	if after:
		params['after'] = after
	if page:
		params['page'] = page
	response = utils.make_request(endpoint, params)
	return response


def get_athlete_activities_paginated(before=None, after=None):
	athlete_activities = []
	resp = get_athlete_activities(before=before, after=after, per_page=200)
	athlete_activities.append(resp)
	page = 2
	while len(resp) != 0:
		resp = get_athlete_activities(before=before, after=after, page=page, per_page=200)
		if resp:
			athlete_activities.append(resp)
			page += 1

	# concatenate all the results from all the pages
	athlete_activities = sum(athlete_activities, [])
	return athlete_activities


def get_zones():
	"""Returns the authenticated athlete's heart rate and power zones."""
	endpoint = f"{constants.STRAVA_BASE_URL}/api/v3/athlete/zones"
	response = utils.make_request(endpoint)
	return response
