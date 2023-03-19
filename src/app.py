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

