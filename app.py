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

figure, activity_types = plots.calendar_heatmap()

app.layout = html.Div(children=[
    html.H1(children='Strava Stats', style={'textAlign': 'center'}),
    html.Div(children='A visualization for your workout data', style={'textAlign': 'center'}),
    html.Div(children=[
        html.Label('Activity Type'),
        dcc.Dropdown(
            options=list(activity_types),
            value='',
            id='activity-type-dropdown'
        )
    ], style={'padding': 10}),
    dcc.Graph(
        id='heatmap',
        figure=figure
    )
])


@app.callback(
    Output('heatmap', 'figure'),
    Input('activity-type-dropdown', 'value')
)
def update_graph(activity_type):
    fig, _ = plots.calendar_heatmap(activity_type)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
