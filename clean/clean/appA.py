# Data
import pandas as pd
import pickle
import numpy as np
# Graphing
import plotly.graph_objects as go
import plotly.express as px
# Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import dash_table
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

structure_options = ['Proportions of Branches Stage group',
                    'Proportions of Branches by OAM by Stage group',
                    'Proportions of Stage group by OAM',
                    'Proportions of Stage group by Customer']

interactiveA1 = html.Div([
    dcc.Dropdown(id='dropdownA1structure',
        options=[{'label':k, 'value':k} for k in structure_options],
        value='Proportions of Branches Stage group'),
    dcc.Dropdown(id='dropdownA1astages',
                    options=[
                        {'label': 'All', 'value': 'All'},
                        {'label': 'W vs L', 'value': 'W vs L'},
                        {'label': 'W vs O vs L', 'value': 'W vs O vs L'}
                    ],
                    value = 'All',
                    #labelStyle={'display': 'inline-block'},
                    className="dcc_control",
                    ),
    dcc.RadioItems(id='radioA1anumerical',
                    options=[
                        {'label': 'Sum', 'value': 'Sum'},
                        {'label': 'Count', 'value': 'Count'},
                    ],
                    value = 'Sum',
                    #labelStyle={'display': 'inline-block'},
                    className="dcc_control",
                    ),
])

outputA1 = html.Div(id='outputA1', children=[],)

#-------------------------------------------------------------------------------------
optionsA2scale = [{'label': "By Branch", 'value': "By Branch"},
{'label': "A Whole", 'value': "As Whole"}]

dropdownA2scale = html.Div(dcc.Dropdown(
    id='dropdownA2scale',
    options=optionsA2scale,
    value='By Branch'
))

outputA2 = html.Div(id='outputA2',children=[],)

#-------------------------------------------------------------------------------------

all_options = {
    'sum': ["PotentialValue","ExpectedValue"],
    'mean': ["PotentialValue","ExpectedValue","ProbPercent"],
    'median': ["PotentialValue","ExpectedValue","ProbPercent"],
    'std': ["PotentialValue","ExpectedValue","ProbPercent"],
    'count':["PotentialValue"]
}

group_options = ['Div','Branch','OAM','LeadType','Customer',
    'Type','New','City, St','KeyVendor','Stage','UpdateDate']


dropdownA3agg = dcc.Dropdown(id='dropdownA3agg', options=[{'label': k, 'value': k} for k in all_options.keys()],value='sum')

dropdownA3numgroup = dcc.Dropdown(id='dropdownA3numgroup')

dropdownA3group = dcc.Dropdown(id='dropdownA3group', 
                               options = [{'label': l, 'value': l} for l in group_options],
                               value='Type')

outputA3 = html.Div(id='outputA3',children=[],)
#-------------------------------------------------------------------------------------


datatable = html.Div(id="A4", children=[],)

#-------------------------------------------------------------------------------------
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}





#LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT 
body = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([interactiveA1],width=3),
                dbc.Col([outputA1],width=9),
            ]),
        ],width=6),
        dbc.Col([
            dropdownA2scale,
            outputA2 
        ],width=6),
    ]),

            
    dbc.Row([
        html.Div(className='row', children=[
            html.Div([
                html.P("""testing"""),
                html.Pre(id='selected-data', style=styles['pre']),
                #datatable
            ])
            #], className='three columns'),
        ]),
    ],justify="center", align="center"),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dropdownA3agg,
                ]),
                dbc.Col([
                    dropdownA3numgroup,
                ]),
                dbc.Col([
                    dropdownA3group,
                ]),
            ]),
            dbc.Row([
                outputA3
                ],justify="center", align="center")
        ]),
    ]),
])





def AppA():
    layout = html.Div([
        nav,
        body,
    ])

    return layout


#GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH GRAPH 
def build_graphA1():

    
    
    x_axis ="ProbPercent"

    y_axis= "PotentialValue"

    dff = df_num
    fig = go.Figure()

    dimensions = [dict(values=dff[label], label=label) for label in ["New","Type"]]

    # Build colorscale
    color = np.zeros(len(dff), dtype='uint8')
    colorscale = [[0, 'gray'], [1, 'firebrick']]

    fig.add_trace(go.Scatter(x=dff[x_axis], y=dff[y_axis],
            marker={'color': 'gray'}, mode='markers', selected={'marker': {'color': 'firebrick'}},
            unselected={'marker': {'opacity': 0.3}}))


    fig.update_layout(
        margin=dict(l=0, r=15, t=0, b=10),
        #paper_bgcolor="lightcyan",
        #plot_bgcolor='lightsteelblue' #gainsboro, lightsteelblue lightsalmon lightgreen lightpink lightcyan lightblue black
    )

    graph = dcc.Graph(id='scatter', figure = fig)
    
    return graph

def build_graphA11(path_mode, included, numerical, df_num):
    values = 'PotentialValue' if numerical == 'Sum' else [1]*len(df_num)
    dff = df_num
    if included == 'All':
        dff = df_num
    if included == 'Win vs Lose':
        dff= df_num[df_num["Stage"].isin(['Won','Lost (why?)'])]
    if included == 'Win vs Ongoing vs Lose':
        dff = df_num
        dff["Stage"] = df_num["Stage"].replace(['Quoting','Discovery (S.P.I.N.)','Working',
                                    'On Hold','Solution Development'], 'Ongoing')
    
    if path_mode == 'Proportions of Branches Stage group':
        fig = px.sunburst(data_frame = dff, path=['Branch','Stage'], values=values, color='Stage')
        title = "Proportions of Branches by {} according to {}".format(included, numerical)
    elif path_mode == 'Proportions of Branches by OAM by Stage group':
        fig = px.sunburst(data_frame = dff, path=['Branch','OAM','Stage'], values=values, color='Stage')
        title = "Proportions of Branches by OAM by {} according to {}".format(included, numerical)
    elif path_mode == 'Proportions of Stage group by OAM':
        fig = px.sunburst(data_frame = dff, path=['Stage','OAM'], values=values, color='Stage')
        title = "Proportions of {} by OAM according to {}".format(included, numerical)
    elif path_mode == 'Proportions of Stage group by Customer':
        fig = px.sunburst(data_frame = dff, path=['Stage','Customer'], values=values, color='Stage')
        title="Proportions of OAM by {} according to {}".format(included, numerical)

    fig.update_layout(title = title,
#                    width=700,
#                   height=700,
                    font=dict(
                        #family="Courier New, monospace",
                        size=12,
                        color="#000000"
                            )
                    )

    fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=20),
            paper_bgcolor='lightcyan',
            #plot_bgcolor='gainsboro' #gainsboro, lightsteelblue lightsalmon lightgreen lightpink lightcyan lightblue black
        )

    graph = dcc.Graph(figure = fig )
        
    return graph



def build_graphA2(mode):
    fig = go.Figure()
    if mode == "By Branch":
        stage_list = ["Discovery (S.P.I.N.)","Solution Development","Quoting","Working","On Hold","Won"]
        fig.add_trace(go.Funnel(
            name = 'Austin',
            y = stage_list,
            x = [noncumun_dfs["Austin"].loc[i,"PV_sum"] for i in stage_list],
            textinfo = "value+percent initial"))

        fig.add_trace(go.Funnel(
            name = 'Midland',
            orientation = "h",
            y = ["Discovery (S.P.I.N.)","Solution Development","Quoting","Working","On Hold","Won"],
            x = [noncumun_dfs["Midland"].loc[i,"PV_sum"] for i in stage_list],
            textposition = "inside",
            textinfo = "value+percent previous"))

        fig.add_trace(go.Funnel(
            name = 'OKC',
            orientation = "h",
            y = ["Discovery (S.P.I.N.)","Solution Development","Quoting","Working","On Hold","Won"],
            x = [noncumun_dfs["OKC"].loc[i,"PV_sum"] for i in stage_list],
            textposition = "inside",
            textinfo = "value+percent total"))

        fig.add_trace(go.Funnel(
            name = 'San Antonio',
            orientation = "h",
            y = ["Discovery (S.P.I.N.)","Solution Development","Quoting","Working","On Hold","Won"],
            x = [noncumun_dfs["San Antonio"].loc[i,"PV_sum"] for i in stage_list],
            textposition = "inside",
            textinfo = "value+percent total"))

        fig.add_trace(go.Funnel(
            name = 'Houston NOV',
            orientation = "h",
            y = ["Discovery (S.P.I.N.)","Solution Development","Quoting","Working","On Hold","Won"],
            x = [noncumun_dfs["Houston NOV"].loc[i,"PV_sum"] for i in stage_list],
            textposition = "inside",
            textinfo = "value+percent total"))

        fig.add_trace(go.Funnel(
            name = 'Corpus Christi',
            orientation = "h",
            y = ["Discovery (S.P.I.N.)","Solution Development","Quoting","Working","On Hold","Won"],
            x = [noncumun_dfs["Corpus Christi"].loc[i,"PV_sum"] for i in stage_list],
            textposition = "inside",
            textinfo = "value+percent total"))

        fig.add_trace(go.Funnel(
            name = 'Houston OEM',
            orientation = "h",
            y = ["Discovery (S.P.I.N.)","Solution Development","Quoting","Working","On Hold","Won"],
            x = [noncumun_dfs["Houston OEM"].loc[i,"PV_sum"] for i in stage_list],
            textposition = "inside",
            textinfo = "value+percent total"))
        
        title = "Sales Funnel by Branch"

        graph = dcc.Graph(figure = fig )

        fig.update_layout(title = title,
#                    width=700,
#                   height=700,
                    font=dict(
                        #family="Courier New, monospace",
                        size=12,
                        color="#000000"
                            )
                    )

        fig.update_layout(
            margin=dict(l=5, r=5, t=30, b=25),
            paper_bgcolor="lightcyan",
            #plot_bgcolor='gainsboro' #gainsboro, lightsteelblue lightsalmon lightgreen lightpink lightcyan lightblue black
        )

        return graph



    elif mode == "As Whole":
        stage_list = ["Discovery (S.P.I.N.)","Solution Development","Quoting","Working","On Hold","Won"]
        fig.add_trace(go.Funnel(
            name = 'Whole',
            y = stage_list,
            x = [df_noncumun_whole.loc[i,"PV_sum"] for i in stage_list],
            textinfo = "value+percent initial"))

        title = "Sales Funnel as Whole"

        fig.update_layout(title = title,
#                    width=700,
#                   height=700,
                    font=dict(
                        #family="Courier New, monospace",
                        size=12,
                        color="#000000"
                            )
                    )

        fig.update_layout(
            margin=dict(l=5, r=5, t=30, b=25),
            paper_bgcolor="lightcyan",
            #plot_bgcolor='gainsboro' #gainsboro, lightsteelblue lightsalmon lightgreen lightpink lightcyan lightblue black
        )

        graph = dcc.Graph(figure = fig)

        return graph


def build_graphA3(agg_method, numerical_group, group, df_num):
    fig = go.Figure()
    for t in df_num[group].unique():
        #for future filtering with date range
        df_num = df_num[df_num["ExpectedOrderDate"] >= pd.to_datetime('2020-1-1')]

        if agg_method == "sum":
            Ys= df_num[df_num[group]==t].groupby("ExpectedOrderDate").sum()[[numerical_group]]
            Xs = Ys.index
            customdata = []
            for date in Ys.index:
                dff = df_num[(df_num["ExpectedOrderDate"] == date) & (df_num[group] == t)]
                customdata.append([i for i in dff.index])
            fig.add_trace(go.Bar(x=df_num[df_num[group]==t].groupby("ExpectedOrderDate").sum()[[numerical_group]].index,
                                 y=list(df_num[df_num[group]==t].groupby("ExpectedOrderDate").sum()[numerical_group]),
                                 customdata=customdata,#[t]*len(df_num[df_num[group]==t].groupby("ExpectedOrderDate").mean()[[numerical_group]].index),
                                 name=t))
        if agg_method == "mean":
            Ys= df_num[df_num[group]==t].groupby("ExpectedOrderDate").mean()[[numerical_group]]
            Xs = Ys.index
            customdata = []
            for date in Ys.index:
                dff = df_num[(df_num["ExpectedOrderDate"] == date) & (df_num[group] == t)]
                customdata.append([i for i in dff.index])
            fig.add_trace(go.Bar(x=df_num[df_num[group]==t].groupby("ExpectedOrderDate").mean()[[numerical_group]].index,
                                 y=list(df_num[df_num[group]==t].groupby("ExpectedOrderDate").mean()[numerical_group]),
                                 customdata=customdata,#[t]*len(df_num[df_num[group]==t].groupby("ExpectedOrderDate").mean()[[numerical_group]].index),
                                 name=t))
        if agg_method == "median":
            Ys= df_num[df_num[group]==t].groupby("ExpectedOrderDate").median()[[numerical_group]]
            Xs = Ys.index
            customdata = []
            for date in Ys.index:
                dff = df_num[(df_num["ExpectedOrderDate"] == date) & (df_num[group] == t)]
                customdata.append([i for i in dff.index])
            fig.add_trace(go.Bar(x=df_num[df_num[group]==t].groupby("ExpectedOrderDate").median()[[numerical_group]].index,
                                 y=list(df_num[df_num[group]==t].groupby("ExpectedOrderDate").median()[numerical_group]),
                                 customdata=customdata,#[t]*len(df_num[df_num[group]==t].groupby("ExpectedOrderDate").mean()[[numerical_group]].index),
                                 name=t))
        if agg_method == "std":
            Ys= df_num[df_num[group]==t].groupby("ExpectedOrderDate").std()[[numerical_group]]
            Xs = Ys.index
            customdata = []
            for date in Ys.index:
                dff = df_num[(df_num["ExpectedOrderDate"] == date) & (df_num[group] == t)]
                customdata.append([i for i in dff.index])
            fig.add_trace(go.Bar(x=df_num[df_num[group]==t].groupby("ExpectedOrderDate").std()[[numerical_group]].index,
                                 y=list(df_num[df_num[group]==t].groupby("ExpectedOrderDate").std()[numerical_group]),
                                 customdata=customdata,#[t]*len(df_num[df_num[group]==t].groupby("ExpectedOrderDate").mean()[[numerical_group]].index),
                                 name=t))
        if agg_method == "count":
            Ys= df_num[df_num[group]==t].groupby("ExpectedOrderDate").count()[[numerical_group]]
            Xs = Ys.index
            customdata = []
            for date in Ys.index:
                dff = df_num[(df_num["ExpectedOrderDate"] == date) & (df_num[group] == t)]
                customdata.append([i for i in dff.index])
            fig.add_trace(go.Bar(x=df_num[df_num[group]==t].groupby("ExpectedOrderDate").count()[[numerical_group]].index,
                                 y=list(df_num[df_num[group]==t].groupby("ExpectedOrderDate").count()[numerical_group]),
                                 customdata=customdata,#[t]*len(df_num[df_num[group]==t].groupby("ExpectedOrderDate").mean()[[numerical_group]].index),
                                 name=t))

    fig.update_layout(title = "{} of {} grouped by {}".format(agg_method,numerical_group,group),
                      barmode='stack',
                      width=1400,
                      height=600,
                      xaxis={'categoryorder':'category ascending'},
                      legend_title_text= group,
                      xaxis_title="Date",
                      yaxis_title="{} {}".format(numerical_group, agg_method),
                      font=dict(
                          #family="Courier New, monospace",
                          size=14,
                          color="#000000"
                        ))

    fig.update_layout(
    #margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="lightcyan",
    plot_bgcolor='gainsboro' #gainsboro, lightsteelblue lightsalmon lightgreen lightpink lightcyan lightblue black
    )

    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        ),
    )

    graph = dcc.Graph(id='timeline', figure = fig) #could add on id property

    return graph


#A4
operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3