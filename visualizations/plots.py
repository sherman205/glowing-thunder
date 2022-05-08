import datetime
import plotly.graph_objects as go
import numpy as np

from collections import OrderedDict
from strava import core as strava_core


def calendar_heatmap(activity_type=None):
	"""Create calendar heatmap"""
	year = datetime.datetime.now().year
	d1 = datetime.date(year, 1, 1)
	d2 = datetime.date(year, 12, 31)
	delta = d2 - d1

	number_of_days = (d2 - d1).days + 1

	month_obj = {
		'Jan': 31,
		'Feb': 29 if number_of_days == 366 else 28,
		'Mar': 31,
		'Apr': 30,
		'May': 31,
		'Jun': 30,
		'Jul': 31,
		'Aug': 31,
		'Sept': 30,
		'Oct': 31,
		'Nov': 30,
		'Dec': 31
	}
	month_positions = (np.cumsum(list(month_obj.values())) - 15) / 7

	# list with datetimes for each day a year
	dates_in_year = [d1 + datetime.timedelta(i) for i in range(delta.days + 1)]
	# maps integer (0-6) to weekdays for ticktext in xaxis
	weekdays_in_year = [i.weekday() for i in dates_in_year]
	weeknumber_of_dates = []

	activities_data = strava_core.get_activities_data(d1, d2, activity_type)
	date_data_map = activities_data.get('date_data_map')
	for date in dates_in_year:
		# %V is the week number in a year (1-52)
		inferred_week_no = int(date.strftime("%V"))
		if inferred_week_no >= 52 and date.month == 1:
			weeknumber_of_dates.append(0)
		elif inferred_week_no == 1 and date.month == 12:
			weeknumber_of_dates.append(53)
		else:
			weeknumber_of_dates.append(inferred_week_no)

		# create data points
		value = ''
		if str(date) not in date_data_map:
			date_data_map[str(date)]['suffer_score'] = 0
			date_data_map[str(date)]['activity_count'] = 0
			value = 'activity_count'

	sorted_date_data_map = OrderedDict(sorted(date_data_map.items()))

	vals = list(sorted_date_data_map.values())
	z = map(lambda x: x.get(value), vals)
	z = np.array(list(z))

	# Format YYYY-MM-DD for hovertext
	text = [str(i) for i in dates_in_year]
	colorscale = [[False, '#eeeeee'], [True, '#76cf63']]

	data = [
		go.Heatmap(
			x=weeknumber_of_dates,
			y=weekdays_in_year,
			z=z,
			text=text,
			hoverinfo='text+z',
			xgap=3,
			ygap=3,
			colorscale=colorscale
		)
	]
	layout = go.Layout(
		title='Number of workouts per day',
		yaxis=dict(
			showline=False, showgrid=False, zeroline=False,
			tickmode='array',
			ticktext=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
			tickvals=[0, 1, 2, 3, 4, 5, 6],
			autorange="reversed",
		),
		xaxis=dict(
			showline=False, showgrid=False, zeroline=False,
			tickmode='array',
			ticktext=list(month_obj.keys()),
			tickvals=month_positions
		),
		font={'size': 10, 'color': '#9e9e9e'},
		plot_bgcolor='#fff',
		showlegend=False,
	)

	fig = go.Figure(data=data, layout=layout)
	return fig, activities_data.get('activity_types')
