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
movies['Released_Year'] = movies['Released_Year'].astype(int)

# Setup app and layout/frontend
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    html.H1('IMDB Statistics Benchmarking Dashboard'),
    dbc.Row([
        dbc.Col([ html.Label('Select the Baseline Year:'),
            dcc.Dropdown(
                id='year1',
                value=2016,  
                options=[{'label': yr1, 'value': yr1} for yr1 in movies['Released_Year']),
            html.Label('Select the Second Year:'),
            dcc.Dropdown(
                id='year2',
                value=2017,  
                options=[{'label': yr2, 'value': yr2} for yr2 in movies['Released_Year'])
                ],
                md=4),
        dbc.Col([
            dbc.Row([
                dbc.Col()]),
            html.Iframe(
                id='boxplot',
                style={'border-width': '0', 'width': '100%', 'height': '400px'})])])])


# Set up callbacks/backend
@app.callback(
    Output('boxplot', 'srcDoc'),
    Input('year1', 'value'),
    Input('year2', 'value')
    )
def plot_altair(year1, year2):

    mo

    scatter = alt.Chart(movies).mark_point().encode(
        x=alt.X(xcol, scale=alt.Scale(domain=[x_min, x_max])),
        y=alt.Y(ycol, scale=alt.Scale(domain=[y_min, y_max])),
        tooltip=['Series_Title','Genre','Released_Year', 'Runtime','IMDB_Rating'])
    scatter = scatter.properties(title = 'Scatter Plot of ' + xcol + ' and ' + ycol)
    output = scatter + text + scatter.transform_regression(xcol,ycol).mark_line(color = 'red')
    return output.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)

