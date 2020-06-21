# Data
import pandas as pd
import pickle
# Graphing
import plotly.graph_objects as go
import plotly.express as px
# Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
# Sub Modules
from navbar import Navbar
from prep import get_data

df, df_num, df_noncumun_whole, noncumun_dfs = get_data()

#df = pd.read_csv('https://gist.githubusercontent.com/joelsewhere/f75da35d9e0c7ed71e5a93c10c52358d/raw/d8534e2f25495cc1de3cd604f952e8cbc0cc3d96/population_il_cities.csv')
#df.set_index(df.iloc[:, 0], drop=True, inplace=True)
#df = df.iloc[:, 1:]

nav = Navbar()

#COMPONENTS COMPONENTS COMPONENTS COMPONENTS COMPONENTS COMPONENTS COMPONENTS COMPONENTS 
#-------------------------------------------------------------------------------------
left_band = html.Div([
    dcc.RangeSlider(
    min=0,
    max=10,
    step=None,
    marks={
        0: '0 °F',
        3: '3 °F',
        5: '5 °F',
        7.65: '7.65 °F',
        10: '10 °F'
    },
    value=[3, 7.65]
)  
])

left_graphs = []

right_top_graph = []

right_bottom_graph = []
#-------------------------------------------------------------------------------------
#LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT 


body = html.Div([
    dbc.Col([left_band]),
    dbc.Col([]),
    dbc.Col([])
])


def AppB():
    layout = html.Div([
        nav,
        body,
    ])

    return layout


#GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH 
