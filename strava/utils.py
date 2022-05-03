import json
import requests

from . import constants


def refresh_strava_token(credentials_file):
    """
    Refresh access token to maintain access to a user's resources,
    since the refresh_token is set to expire after 6 hours.

    Args:
        :credentials_file

    Returns:
        access_token
    """

    with open(credentials_file, 'r') as r:
        api_credentials = json.load(r)
        client_id = api_credentials['client_id']
        client_secret = api_credentials['client_secret']
        refresh_token = api_credentials['refresh_token']

    req = requests.post(f"{constants.STRAVA_BASE_URL}/oauth/token?client_id={client_id}&client_secret={client_secret}"
                        f"&refresh_token={refresh_token}&grant_type=refresh_token").json()
    api_credentials['access_token'] = req['access_token']
    api_credentials['refresh_token'] = req['refresh_token']

    with open(credentials_file, 'w') as w:
        json.dump(api_credentials, w)

    access_token = api_credentials['access_token']

    return access_token


def make_request(url, params):
    """Make GET request to the Strava API"""
    access_token = refresh_strava_token('.secret/api_credentials.json')

    headers = {"Authorization": "Bearer {}".format(access_token)}
    response = requests.get(url, headers=headers, params=params).json()

    return response
