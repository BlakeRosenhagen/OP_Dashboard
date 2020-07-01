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
import dash_daq as daq
# Sub Modules
from navbar import Navbar
from prep import get_data
from datafilter import filter_data_master

df, df_num, df_noncumun_whole, noncumun_dfs = get_data()

nav = Navbar()

#COMPONENTS COMPONENTS COMPONENTS COMPONENTS COMPONENTS COMPONENTS COMPONENTS COMPONENTS 
#-------------------------------------------------------------------------------------

switch = html.Div([
    dbc.Col([dcc.Input(id="inputBPVmin", type="number", placeholder="PV Min")]),
    dbc.Col([dcc.Input(id="inputBPVmax", type="number", placeholder="PV Max")]),
    dbc.Col([dcc.Input(id="inputBPPmin", type="number", placeholder="PP Min")]),
    dbc.Col([dcc.Input(id="inputBPPmax", type="number", placeholder="PP Max")]),
    dbc.Col([daq.ToggleSwitch(id='toggle',value=False)]),
    dbc.Col([dcc.Input(id="inputBEODmin", type="number", placeholder="EOD Min")]),
    dbc.Col([dcc.Input(id="inputBEODmin", type="number", placeholder="EOD Max")]),
    dbc.Col([dcc.Input(id="inputBEODmin", type="number", placeholder="EOD Min")]),
    dbc.Col([dcc.Input(id="inputBEODmin", type="number", placeholder="EOD Max")]),
    ])




dropdown_options = ["PotentialValue", "ProbPercent", "ExpectedValue", "EOD_delta"]

dcc.Dropdown(id='dropdownBAx', options=[{'label': i, 'value': i} for i in dropdown_options],value='PotentialValue')

dcc.Dropdown(id='dropdownBAy', options=[{'label': i, 'value': i} for i in dropdown_options],value='PotentialValue')


group_options = ['New','LeadType','Type','Branch', 'Stage','OAM']

checklistBA = dcc.Checklist(
        id = 'checklistBA',
        options=[ {'label':i, 'value':i} for i in group_options],
        value=['New','Type',"Branch"]),








def core_layoutB():
    body1 = html.Div([
        dbc.Col([dcc.Markdown("""left graph""")], 
        width=6),
        dbc.Col([
            dbc.Row([dcc.Markdown("""top right graph""")]),
            dbc.Row([dcc.Markdown("""bottom right graph""")]),
            ],width=6),
    ])

    body2 = html.Div([
        dbc.Row([dcc.Markdown("""top graph""")]),
        dbc.Row([
            dbc.Col([dcc.Markdown("""bottom left graph""")],
            width=6),
            dbc.Col([dcc.Markdown("""bottom right graph""")],
            width=6),
        ]),
    ])

    return body1, body2



def core_layoutB():
    body1 = html.Div([
        dbc.Col([],width=2), #left band
        dbc.Col([
            dbc.Row([
                dbc.Col([],width=7), #scatterparcat
                dbc.Col([
                    dbc.Row([]), #pie charts
                    dbc.Row([]), # 3d-scatter
                ],width=5),
            ]),
            dbc.Row([]), # datatable or plotly table
        ],width=8), 
        dbc.Col([],width=2), #right band
    ])

    return body1, body2






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

switch_layout = html.Div(id="layout_output", children=[],)
#-------------------------------------------------------------------------------------
#LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT 


body = html.Div([
    dbc.Col([left_band], width=2),
#    dbc.Col([dcc.Markdown("""hop[e""")]

),
    dbc.Col([dbc.Row([switch_layout],),],width=10),
    dbc.Col([])
])


def AppB():
    layout = html.Div([
        nav,
        switch,
        switch_layout,
    ])

    return layout


#GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH 


def build_graphBA1(x_axis,y_axis,PV_min,PV_max,PP_min,PP_max,EOD_min,EOD_max,categorical_dimensions):

    dff = filter_data_master(PV_min,PV_max,PP_min,PP_max,EV_min,EV_max,EOD_min,EOD_max,df_num):


    dimensions = [dict(values=dff[label], label=label) for label in categorical_dimensions]

    # Build colorscale
    color = np.zeros(len(dff), dtype='uint8')
    colorscale = [[0, 'gray'], [1, 'firebrick']]

    # Build figure as FigureWidget
    fig = go.FigureWidget(
        data=[go.Scatter(x=dff[x_axis], y=dff[y_axis],
        marker={'color': 'gray'}, mode='markers', selected={'marker': {'color': 'firebrick'}},
        unselected={'marker': {'opacity': 0.3}}), go.Parcats(
            domain={'y': [0, 0.4]}, dimensions=dimensions,
            line={'colorscale': colorscale, 'cmin': 0,
                'cmax': 1, 'color': color, 'shape': 'hspline'})
        ])

    fig.update_layout(
            height=800, xaxis={'title': '{}'.format(x_axis)},
            yaxis={'title': '{}'.format(y_axis), 'domain': [0.6, 1]},
            dragmode='lasso', hovermode='closest',)

    # Update color callback
    def update_color(trace, points, state):
        # Update scatter selection
        fig.data[0].selectedpoints = points.point_inds

        # Update parcats colors
        new_color = np.zeros(len(dff), dtype='uint8')
        new_color[points.point_inds] = 1
        fig.data[1].line.color = new_color

    # Register callback on scatter selection...
    fig.data[0].on_selection(update_color)
    # and parcats click
    fig.data[1].on_click(update_color)

    fig.update_layout(
        margin=dict(l=0, r=15, t=0, b=10),
        #paper_bgcolor="lightcyan",
        #plot_bgcolor='lightsteelblue' #gainsboro, lightsteelblue lightsalmon lightgreen lightpink lightcyan lightblue black
    )

    graph = dcc.Graph(id='scatterparcat', figure = fig) #could add on id property

    return graph














def build_graphBA2(group, numerical, dff):
    if numerical == "Count": values = [1]*len(dff)
    elif numerical == "Sum": values = 'PotentialValue'
    fig = px.pie(dff, values=values, names=group,
                    title='Proportion',
                )#hover_data=['PotentialValue'], labels={'lifeExp':'life expectancy'})
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    graph = dcc.Graph(figure = fig )
        
    return graph