from datetime import datetime
from dash import Dash, html, dcc, Input, Output
from visualizations import plots
from utils.config import cache


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_URL': 'redis://localhost:6379',
    'CACHE_DEFAULT_TIMEOUT': 0
}

cache.init_app(app.server, config=CACHE_CONFIG)

_, activity_types = plots.calendar_heatmap()

app.layout = html.Div(children=[
    html.H1(children='Strava Stats', style={'textAlign': 'center'}),
    html.Div(children='A visualization for your workout data', style={'textAlign': 'center'}),
    html.Div(children=[
        html.Div(children=[
            html.Label('Year'),
            dcc.Dropdown(
                options=[2018, 2019, 2020, 2021, 2022],
                value=datetime.today().year,
                id='year-dropdown'
            )
        ], style={'width': '10%', 'padding': 10}),
        html.Div(children=[
            html.Label('Activity Type'),
            dcc.Dropdown(
                options=list(activity_types),
                value='',
                id='activity-type-dropdown'
            )
        ], style={'width': '10%', 'padding': 10})
    ], style={'padding': 10, 'display': 'flex'}),
    dcc.Graph(
        id='heatmap'
    )
])


@app.callback(
    Output('heatmap', 'figure'),
    Input('activity-type-dropdown', 'value'),
    Input('year-dropdown', 'value')
)
def update_graph(activity_type, year):
    fig, _ = plots.calendar_heatmap(activity_type, year)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
