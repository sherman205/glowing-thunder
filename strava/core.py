from datetime import datetime, timedelta
from collections import defaultdict
from utils.config import cache
from utils import helpers
from strava.constants import Cache
from strava import endpoints


def get_activities_data(start_date, end_date, activity_type=None):
	"""
	Returns a dictionary of date strings to number of Strava activities for
	each date, bounded by start_date and end_date.
	i.e. {'2022-01-01': 2}
	"""
	# epoch_before = helpers.timestamp_to_unix(str(end_date))
	# epoch_after = helpers.timestamp_to_unix(str(start_date))
	# athlete_activities = []
	# resp = endpoints.get_athlete_activities(before=epoch_before, after=epoch_after, per_page=200)
	# athlete_activities.append(resp)
	# page = 2
	# while len(resp) != 0:
	# 	resp = endpoints.get_athlete_activities(before=epoch_before, after=epoch_after, page=page, per_page=200)
	# 	if resp:
	# 		athlete_activities.append(resp)
	# 		page += 1
	#
	# # concatenate all the results from all the pages
	# athlete_activities = sum(athlete_activities, [])

	# athlete_activities = [
	# 	{
	# 		"resource_state": 2,
	# 		"athlete": {
	# 			"id": 31856783,
	# 			"resource_state": 1
	# 		},
	# 		"name": "Evening Walk",
	# 		"distance": 1630.1,
	# 		"moving_time": 1291,
	# 		"elapsed_time": 1291,
	# 		"total_elevation_gain": 17.1,
	# 		"type": "Walk",
	# 		"id": 7094804084,
	# 		"start_date": "2022-05-05T22:55:11Z",
	# 		"start_date_local": "2022-05-05T18:55:11Z",
	# 		"timezone": "(GMT-05:00) America/New_York",
	# 		"utc_offset": -14400.0,
	# 		"location_city": None,
	# 		"location_state": None,
	# 		"location_country": "United States",
	# 		"achievement_count": 0,
	# 		"kudos_count": 1,
	# 		"comment_count": 0,
	# 		"athlete_count": 1,
	# 		"photo_count": 0,
	# 		"map": {
	# 			"id": "a7094804084",
	# 			"summary_polyline": "mg`lFjywvMEiADWB}Ab@qAZYd@I`@?TEPBb@AZBj@Ep@Fh@Ct@Jl@?t@D`@Ar@HXAj@Dr@?FBHJKnABl@DV?h@Ml@Bf@IdAFx@GX?RUn@{@t@WDe@Ii@]q@Qm@U{@c@iAYm@_@kAc@e@MAG?MPmA?c@Ji@A[EGKGK@KHAF@VNX@J_@vBCBG@_@IODi@BIIC]IU?SEOCc@AYH]@o@EEC?MDEJMfA?j@XtAD\\Dn@HRLKBOAo@GM",
	# 			"resource_state": 2
	# 		},
	# 		"trainer": False,
	# 		"commute": False,
	# 		"manual": False,
	# 		"private": False,
	# 		"visibility": "everyone",
	# 		"flagged": False,
	# 		"gear_id": "g9876935",
	# 		"start_latlng": [
	# 			38.836555341258645,
	# 			-77.29573150165379
	# 		],
	# 		"end_latlng": [
	# 			38.83646280504763,
	# 			-77.29593585245311
	# 		],
	# 		"average_speed": 1.263,
	# 		"max_speed": 2.176,
	# 		"has_heartrate": True,
	# 		"average_heartrate": 91.4,
	# 		"max_heartrate": 115.0,
	# 		"heartrate_opt_out": False,
	# 		"display_hide_heartrate_option": True,
	# 		"elev_high": 133.7,
	# 		"elev_low": 122.0,
	# 		"upload_id": 7552862600,
	# 		"upload_id_str": "7552862600",
	# 		"external_id": "3ED05F0B-1F5F-4BB7-BF9D-C1BC298785A4.fit",
	# 		"from_accepted_tag": False,
	# 		"pr_count": 0,
	# 		"total_photo_count": 0,
	# 		"has_kudoed": False,
	# 		"suffer_score": 2.0
	# 	},
	# 	{
	# 		"resource_state": 2,
	# 		"athlete": {
	# 			"id": 31856783,
	# 			"resource_state": 1
	# 		},
	# 		"name": "Morning Ride",
	# 		"distance": 24294.6,
	# 		"moving_time": 3825,
	# 		"elapsed_time": 3925,
	# 		"total_elevation_gain": 127.4,
	# 		"type": "Ride",
	# 		"workout_type": 0,
	# 		"id": 7092139115,
	# 		"start_date": "2022-05-05T12:46:14Z",
	# 		"start_date_local": "2022-05-05T08:46:14Z",
	# 		"timezone": "(GMT-05:00) America/New_York",
	# 		"utc_offset": -14400.0,
	# 		"location_city": None,
	# 		"location_state": None,
	# 		"location_country": "United States",
	# 		"achievement_count": 4,
	# 		"kudos_count": 1,
	# 		"comment_count": 0,
	# 		"athlete_count": 1,
	# 		"photo_count": 0,
	# 		"map": {
	# 			"id": "a7092139115",
	# 			"summary_polyline": "uuflF`gkvMAa@O|A@t@]b@Ib@o@`COHe@W}As@yGkCaEiBkAKwCRiB@_Dg@}G_@aIg@oAQm@?iAQwAAOGu@AyCYQU}@cDUgAc@cD]qBKe@MOUCgMdBaB@mAKs@[kB_B}@_@sC}@MK{@QmE}AaHsBeHcCe@W}AIQtAQh@uA|HiAnHgApFWhBOr@aA~FMh@{Hte@m@xCg@~Cu@xCY`AkA`De@fAiAtBmExGs@^sA~Be@p@eApB{@rAiAdDcA|Dm@pEc@|EOpCKtCFvFJpCJdBl@zENzBJ|BBzEClBWhFQh@BTTX@JKTWZYfAo@hDAhAe@nAMl@{AbFmBlFoA|Ce@t@eBbDcCzDwCbE}AdBuCfD}ApB}A|AiFlGuEhF{AlBuCjDo@j@qBbC_CdCmB`Ca@\\_AdAmI~JeBrCqBhEc@jA]b@w@~AeBtCgC|C{A|A}BhBiAv@_DfBsI`DoGzBw@PsExB}EpDs@x@a@Z{@hAkClEmAfCkG|PiCxHw@nByHtTw@xCi@fCMdAi@nEi@bJ_@lCKZ`@{Bx@kLd@aEr@}Db@eBnCgIbCaHpBmFn@uB|@_C~@wCnAeDtAaEfCaGjBgDnA_BtBwBrEmDdB{@bT{HrCmAhBeA`CcBrAkAjCmCv@}@nB_DlAeCf@w@dAgC~CwFxDuElHmIv@aApC}CzDoEzIqKn@o@|EuFr@_Ap@k@x@}@z@iA|AeBv@gA|BgCdD}E`@}@lBuC|@sB\\g@DUf@eAz@eCr@gBjAsDf@mBr@{BAcAXyAX{@^}A`@o@?OSUEUNk@FeCLyB@kAI_GSsDg@aES}BQ_FAiEPcFTiDXkCT{A@c@J_@NgAb@kAx@yCp@eBv@gAfDeGR[TMXEHM|B}Dv@iAXm@\\]f@aA`A}BtAuEh@uBJq@FONgAJ]ZcCp@}DDIp@qEzBqNZyAj@{Dj@}Cz@kEvAyIZyABa@b@aDbA}E~@sFJWjANtN~E`Cn@nLzD|@`@|BdBt@TdAFx@CfK}At@AbALRNJVx@vDRjA\\rAPvA^bAjALXL`AJfA\\fCI`ERtHv@NApCRlBTfB^rH?lAVpAb@rFxBfGdBPKDMl@eDGUcAi@o@UMODSJeA@w@Fw@?wADSHC^Jl@A~CLFJBr@p@|FcA|EILgAa@qAm@eC{@MMAGTqAdA\\p@LDFP?PKACRc@VeALU",
	# 			"resource_state": 2
	# 		},
	# 		"trainer": False,
	# 		"commute": False,
	# 		"manual": False,
	# 		"private": False,
	# 		"visibility": "everyone",
	# 		"flagged": False,
	# 		"gear_id": "b10036826",
	# 		"start_latlng": [
	# 			38.869554,
	# 			-77.231368
	# 		],
	# 		"end_latlng": [
	# 			38.86943,
	# 			-77.231104
	# 		],
	# 		"average_speed": 6.352,
	# 		"max_speed": 10.55,
	# 		"average_watts": 74.9,
	# 		"kilojoules": 286.4,
	# 		"device_watts": False,
	# 		"has_heartrate": True,
	# 		"average_heartrate": 140.0,
	# 		"max_heartrate": 172.0,
	# 		"heartrate_opt_out": False,
	# 		"display_hide_heartrate_option": True,
	# 		"elev_high": 130.7,
	# 		"elev_low": 69.3,
	# 		"upload_id": 7549971696,
	# 		"upload_id_str": "7549971696",
	# 		"external_id": "438F4E9C-B13F-4F99-9A5F-0953FB6BA55F",
	# 		"from_accepted_tag": False,
	# 		"pr_count": 0,
	# 		"total_photo_count": 0,
	# 		"has_kudoed": False,
	# 		"suffer_score": 54.0
	# 	}
	# ]

	epoch_before = helpers.timestamp_to_unix(str(end_date))
	epoch_after = helpers.timestamp_to_unix(str(start_date))

	activities_cache_key = Cache.athlete_activities_cache_key
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
