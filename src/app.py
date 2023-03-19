from dash import Dash, html, dcc, Input, Output, dash_table
import altair as alt
from vega_datasets import data
import dash_bootstrap_components as dbc
import pandas as pd 
import numpy as np 

# Data Wrangling
movies = pd.read_csv("../data/imdb_top_1000.csv", dtype={'Runtime': str})
movies['Runtime'] = movies['Runtime'].str.extract('(\d+)').astype(int)
movies = movies.loc[:,['Director', 'Released_Year', 'IMDB_Rating']]
movies['Released_Year'] =movies['Released_Year'].str.extract('(\d+)')
movies = movies.dropna()
movies['Released_Year'] = movies['Released_Year'].astype(str)

# Setup app and layout/frontend
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    html.H1('IMDB Statistics Benchmarking Dashboard'),
    dbc.Row([
        dbc.Col([ html.Label('Select the Baseline Year:'),
            dcc.Dropdown(
                id='year1',
                value='2016',  
                options=[{'label': yr1, 'value': yr1} for yr1 in movies['Released_Year']]),
            html.Label('Select the Second Year:'),
            dcc.Dropdown(
                id='year2',
                value='2017',  
                options=[{'label': yr2, 'value': yr2} for yr2 in movies['Released_Year']])
                ],
                md=4),
        dbc.Col([
            dbc.Row([
                dbc.Col()]),
            html.Iframe(
                id='boxplot1',
                style={'border-width': '0', 'width': '100%', 'height': '400px'})])]),
    dbc.Row([
        dbc.Col([ html.Label('Select the Baseline Director:'),
            dcc.Dropdown(
                id='director1',
                value='Alfred Hitchcock',  
                options=[{'label': dr1, 'value': dr1} for dr1 in movies['Director']]),
            html.Label('Select the Second Director:'),
            dcc.Dropdown(
                id='director2',
                value='Steven Spielberg',  
                options=[{'label': dr2, 'value': dr2} for dr2 in movies['Director']])
                ],
                md=4),
        dbc.Col([
            dbc.Row([
                dbc.Col()]),
            html.Iframe(
                id='tickplot1',
                style={'border-width': '0', 'width': '100%', 'height': '400px'}
                )
                ])
            ])
        ])


# Set up callbacks/backend
@app.callback(
    Output('boxplot1', 'srcDoc'),
    Input('year1', 'value'),
    Input('year2', 'value')
    )
def plot_altair(year1, year2):

    boxplot1 = alt.Chart(movies.query("Released_Year == @year1 | Released_Year == @year2"), width=400, height=300).mark_boxplot().encode(
        x=alt.X('IMDB_Rating', scale=alt.Scale(domain=[7.4, 9.4])),
        y=alt.Y('Released_Year', axis=alt.Axis(title='Released year'))
    ).properties(title = 'Benchmarking Boxplot Release Year and IMDB Rating')
    output = boxplot1 + boxplot1.mark_point(size = 10)
    return output.to_html()

@app.callback(
    Output('tickplot1', 'srcDoc'),
    Input('director1', 'value'),
    Input('director2', 'value')
    )
def plot_altair(director1, director2):

    tickplot1 = alt.Chart(movies.query("Director == @director1 | Director == @director2"), width=400, height=300).mark_tick(size=50, color='orange').encode(
        x=alt.X('IMDB_Rating', scale=alt.Scale(domain=[7.4, 9.4])),
        y=alt.Y('Director')
    ).properties(title = 'Benchmarking Tickplot Director and IMDB Rating')
    output = tickplot1 + tickplot1.mark_boxplot(extent='min-max')
    return output.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)

