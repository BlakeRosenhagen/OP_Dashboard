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

dropdown_options = ["PotentialValue", "ProbPercent", "ExpectedValue", "EOD_delta"]

group_options = ['New','LeadType','Type','Branch', 'Stage','OAM']



left_band = html.Div([
    dcc.Dropdown(id='dropdownBx', options=[{'label': i, 'value': i} for i in dropdown_options],value='PotentialValue'),
    dcc.Input(id="inputBxmin", type="number", placeholder="Minimum"),
    dcc.Input(id="inputBxmax", type="number", placeholder="Maximum"),

    dcc.Dropdown(id='dropdownBy', options=[{'label': i, 'value': i} for i in dropdown_options],value='PotentialValue'),
    
    dcc.Input(id="inputBymin", type="number", placeholder="Minimum"),
    dcc.Input(id="inputBymax", type="number", placeholder="Maximum"),

    dcc.Checklist(
        id = 'checklistB',
        options=[ {'label':i, 'value':i} for i in group_options],
        value=['New','Type',"Branch"]),
    
    #html.P("Select Dimension")
    dcc.Dropdown(id='dropdownBdimension'),

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
