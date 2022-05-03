from visualizations import plots
from dash import Dash, html, dcc


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

fig = plots.calendar_heatmap()

app.layout = html.Div(children=[
    html.H1(children='Strava Stats', style={'textAlign': 'center'}),
    html.Div(children='A visualization for your workout data', style={'textAlign': 'center'}),
    dcc.Graph(
        id='heatmap',
        figure=fig
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
