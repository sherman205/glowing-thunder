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


def get_zones():
	"""Returns the authenticated athlete's heart rate and power zones."""
	endpoint = f"{constants.STRAVA_BASE_URL}/api/v3/athlete/zones"
	response = utils.make_request(endpoint)
	return response
