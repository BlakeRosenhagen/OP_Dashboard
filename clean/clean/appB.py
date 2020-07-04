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
# Top Components
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


# Layout A Components
dropdown_optionsBA1 = ["PotentialValue", "ProbPercent", "ExpectedValue", "EOD_delta"]

dropdownBAx = dcc.Dropdown(id='dropdownBAx', options=[{'label': i, 'value': i} for i in dropdown_optionsBA1],value='ProbPercent')

dropdownBAy = dcc.Dropdown(id='dropdownBAy', options=[{'label': i, 'value': i} for i in dropdown_optionsBA1],value='PotentialValue')


group_options = ['New','LeadType','Type','Branch', 'Stage','OAM']

checklistBA = dcc.Checklist(
        id = 'checklistBA',
        options=[ {'label':i, 'value':i} for i in group_options],
        value=['New','Type',"Branch"]),

dropdownBAdimension = dcc.Dropdown(id='dropdownBAdimension', children=[],)

outputBA1 = html.Div(id='outputBA1', children=[],)

radioBA2group = dcc.RadioItems(options=[id='radioBA2group'
    {'label': 'Positional/Source Info', 'value': 'Positional/Source Info'},
    {'label': 'Customer/Vendor Info', 'value': 'Customer/Vendor Info'}],
    value='Positional/Source Info'
)
radioBA2numerical = dcc.RadioItems(options=[id='radioBA2numerical'
    {'label': 'Count', 'value': 'Count'},
    {'label': 'PV Sum', 'value': 'PV Sum'},
    {'label': 'EV Sum', 'value': 'EV Sum'}],
    value='Count'
)

outputBA2 = html.Div(id='outputBA2', children=[],)

dropdown_optionsBA3color = ["None",'New','Type','Branch','LeadType','Stage', 'PotentialValue','ProbPercent','EOD_delta']
dropdown_optionsBA3size = ["None",'New','Type','Branch','LeadType','Stage', 'PotentialValue','ProbPercent','EOD_delta']
dropdown_optionsBA3symbol = ["None",'New','Type','Branch','LeadType','Stage']

dropdownBAcolor = dcc.Dropdown(id='dropdownBA3color', options=[{'label': i, 'value': i} for i in dropdown_optionsBA3color],value='Branch')
dropdownBAsize = dcc.Dropdown(id='dropdownBA3size', options=[{'label': i, 'value': i} for i in dropdown_optionsBA3size],value='None')
dropdownBAsymbol = dcc.Dropdown(id='dropdownBA3symbol', options=[{'label': i, 'value': i} for i in dropdown_optionsBA3symbol],value='New')

outputBA3 = html.Div(id='outputBA3', children=[],)




# Layout B Components








def ccore_layoutB():
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



switch_layout = html.Div(id="layout_output", children=[],)
#-------------------------------------------------------------------------------------
#LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT LAYOUT 


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
        dbc.Col([dropdownBAcolor,dropdownBAsize,dropdownBAsymbol],width=2), #right band
    ])

    body2 = html.Div([])

    return body1, body2


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


def build_graphBA2(group_sel, numerical):

    dff = df_num

    # Define color sets of paintings
    night_colors = ['rgb(56, 75, 126)', 'rgb(18, 36, 37)', 'rgb(34, 53, 101)',
                    'rgb(36, 55, 57)', 'rgb(6, 4, 4)']
    sunflowers_colors = ['rgb(177, 127, 38)', 'rgb(205, 152, 36)', 'rgb(99, 79, 37)',
                        'rgb(129, 180, 179)', 'rgb(124, 103, 37)']
    irises_colors = ['rgb(33, 75, 99)', 'rgb(79, 129, 102)', 'rgb(151, 179, 100)',
                    'rgb(175, 49, 35)', 'rgb(36, 73, 147)']
    cafe_colors =  ['rgb(146, 123, 21)', 'rgb(177, 180, 34)', 'rgb(206, 206, 40)',
                    'rgb(175, 51, 21)', 'rgb(35, 36, 21)']

    color_dict = {'Branch':['greenyellow', 'orange', 'hotpink', 'darkgreen','cyan','brown','blueviolet'],
                'LeadType':['yellow','darkgoldenrod','aqua','blue','blueviolet','darkgreen','aliceblue','lawngreen'],
                'Type':['Orange','green','cyan','violet'],
                'New':['cadetblue', 'burlywood', 'brown'],
                'Stage':['palegoldenrod', 'forestgreen', 'paleturquoise','orange','brown', 'palegreen', 'fuchsia'],
                'OAM':['orchid', 'palegoldenrod', 'palegreen', 'paleturquoise',
                    'tomato', 'turquoise','violet', 'darkgreen', 'peru', 'pink',
                    'plum', 'powderblue', 'purple', 'red', 'rosybrown',
                    'royalblue', 'saddlebrown', 'salmon', 'sandybrown',
                    'seagreen', 'seashell', 'gold', 'silver', 'skyblue',],
                'KeyVendor':['beige', 'bisque', 'black', 'blanchedalmond', 'blue',
                            'blueviolet', 'brown', 'burlywood', 'cadetblue',
                            'chartreuse', 'chocolate', 'coral', 'cornflowerblue',
                            'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan',
                            'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen',
                            'darkkhaki'],
                "Customer": ['mediumturquoise', 'mediumvioletred', 'midnightblue',
                            'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy',
                            'oldlace', 'olive', 'olivedrab', 'orange', 'pink',
                            'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise',
                            'black', 'papayawhip', 'orange', 'peru', 'pink',
                            'aliceblue', 'red', 'aqua', 'aquamarine', 'azure',
                            'beige', 'bisque', 'black', 'blanchedalmond', 'blue',
                            'blueviolet', 'brown', 'burlywood', 'cadetblue',
                            'chartreuse', 'chocolate', 'coral', 'cornflowerblue',
                            'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan',
                            'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen',
                            'darkkhaki']}
                
    # Create subplots, using 'domain' type for pie charts
    specs = [[{'type':'domain'}, {'type':'domain'}],
            [{'type':'domain'}, {'type':'domain'}],]
    fig = make_subplots(rows=2, cols=2, specs=specs,horizontal_spacing=0,vertical_spacing=0.1)

    groups1 = ["Branch","LeadType","OAM","Stage"] #Positional/Source Info

    groups2 = ["Customer","KeyVendor","New","Type"] #Customer/Vendor Info

    rowcol = {"1":(1,1), "2":(1,2),
            "3":(2,1), "4":(2,2)}

    groups = groups1 if group_sel == "Positional/Source Info" else groups2

    if numerical == "Count":
        for i,group in enumerate(groups):
            fig.add_trace(go.Pie(labels=df_num[group].value_counts().sort_values(ascending=False).index,
                                values=list(df_num["Stage"].value_counts().sort_values(ascending=False)), 
                                name=group,
                                title=group,
                                marker_colors=color_dict[group]), rowcol[str(i+1)][0], rowcol[str(i+1)][1])
    if numerical == "PV Sum":
        fig.add_trace(go.Pie(labels=df_num.groupby("Stage").sum()["PotentialValue"].sort_values(ascending=False).index,
                                values=list(df_num.groupby("Stage").sum()["PotentialValue"].sort_values(ascending=False)), 
                                name=group,
                                title=group,
                                marker_colors=color_dict[group]), rowcol[str(i+1)][0], rowcol[str(i+1)][1])
    if numerical == "EV Sum":
        fig.add_trace(go.Pie(labels=df_num.groupby("Stage").sum()["ExpectedValue"].sort_values(ascending=False).index,
                                values=list(df_num.groupby("Stage").sum()["ExpectedValue"].sort_values(ascending=False)), 
                                name=group,
                                title=group,
                                marker_colors=color_dict[group]), rowcol[str(i+1)][0], rowcol[str(i+1)][1])


    # Tune layout and hover info
    fig.update_traces(hoverinfo='label+percent+name', textinfo='label+value')
    fig.update(
        layout_title_text='Positional/Source Info Pie Charts' if group_sel == "Positional/Source Info" else\
                                        "Customer/Vendor Info",
            layout_showlegend=False)

    fig.update_layout(
        margin=dict(l=0, r=0, t=30,b=0),
        #paper_bgcolor="lightcyan",
        #plot_bgcolor='lightsteelblue' #gainsboro, lightsteelblue lightsalmon lightgreen lightpink lightcyan lightblue black
    )
    graph = dcc.Graph(id='fourpie', figure = fig)

    return graph

#def build_graphBA2(group, numerical, dff):
#    if numerical == "Count": values = [1]*len(dff)
#    elif numerical == "Sum": values = 'PotentialValue'
#    fig = px.pie(dff, values=values, names=group,
#                    title='Proportion',
#                )#hover_data=['PotentialValue'], labels={'lifeExp':'life expectancy'})
#    fig.update_traces(textposition='inside', textinfo='percent+label')
#    
#    graph = dcc.Graph(figure = fig )
#        
#    return graph



def build_graphBA3(color_sel,size_sel,symbol_sel,PV_min,PV_max,PP_min,PP_max,EOD_min,EOD_max):
    
    dff = filter_data_master(PV_min,PV_max,PP_min,PP_max,EOD_min,EOD_max,df_num):

    if not color_sel and not symbol_sel:
        showlegend = True
    elif color_sel and not symbol_sel:
        showlegend = True
    elif not color_sel and symbol_sel:
        showlegend = True
    elif color_sel and symbol_sel:
        if color_sel == symbol_sel:
            showlegend = True
            print("both active and same")
        elif color_sel != symbol_sel:
            print("both active and not same")
            showlegend = False

    df = px.data.iris()
    fig = px.scatter_3d(dff, x='ProbPercent', y='EOD_delta', z='PotentialValue',
                        color=color_sel,
                        size=size_sel, size_max=18,
                        symbol=symbol_sel,
                        opacity=0.6)
    
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0),
        scene = dict(
            xaxis = dict(
                backgroundcolor="rgb(245, 236, 218)",
                gridcolor="white",
                showbackground=True,
                zerolinecolor="white",),
            yaxis = dict(
                backgroundcolor="rgb(206, 240, 194)",
                gridcolor="white",
                showbackground=True,
                zerolinecolor="white"),
            zaxis = dict(
                backgroundcolor="rgb(241, 217, 252)",
                gridcolor="white",
                showbackground=True,
                zerolinecolor="white",),),
            width=700,
            showlegend=showlegend)
    
    fig.show()
    #graph = dcc.Graph(figure = fig)

    #return graph