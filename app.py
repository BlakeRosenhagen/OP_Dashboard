# Data
import pandas as pd
import pickle
# Graphing
import plotly.graph_objects as go
# Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
# Navbar
from navbar import Navbar
#OPIPE
from prep import get_data


df, df_num, df_noncumun_whole, noncumun_dfs = get_data()

#df = pd.read_csv('https://gist.githubusercontent.com/joelsewhere/f75da35d9e0c7ed71e5a93c10c52358d/raw/d8534e2f25495cc1de3cd604f952e8cbc0cc3d96/population_il_cities.csv')
#df.set_index(df.iloc[:, 0], drop=True, inplace=True)
#df = df.iloc[:, 1:]



nav = Navbar()

header = html.H3(
    'Select the name of an Illinois city to see its population!'
)


options = [{'label': x.replace(', Illinois', ''), 'value': x}
                        for x in df.columns]


body = dbc.Container(
    [
       dbc.Row(
           [
               dbc.Col(
                  [
                    html.Div(dcc.Dropdown(
                        id='pop_dropdown',
                        options=options,
                        #default value
                        value='Abingdon city, Illinois'
                    ))

                    html.Div(id='output',
                            children=[],
                        )
                    ],
                  md=6,
               ),
              dbc.Col(
                 [
                     html.H2("Cumunalative"),
                     dcc.Graph(
                         figure={"data": [{"x": [1, 2, 3], "y": [1, 4, 9]}]}
                            ),
                        ]
                        md=6,
                     ),
                ]
            )
       ],
className="mt-4",
)


BODY = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                
                            ],
                            md=1,
                        ),
                        dbc.Row(
                            [

                            ],
                            md=1,
                        )
                    ],
                    md=8
                )
                dbc.Col(
                    [
                        dbc.Row(
                            [

                            ]
                        ),
                        dbc.Row(
                            [
                                
                            ]
                        )
                    ],
                    md=4,
                )
            ],
            md=5,
        )
        dbc.Row(
            [
                dbc.Col(
                    [

                    ]
                )
                dbc.Col(
                    [

                    ]
                )
            ],
            md=5,
        )

    ]
)



#funnel graph
options = [{'label': 'By Branch', 'value': 'By Branch'},
            {'label': 'As Whole', 'value': 'As Whole'}]

dropdown1 = html.Div(dcc.Dropdown(
    id='pop_dropdown',
    options=options,
    #default value
    value='By Branch'
))

output1 = html.Div(id='output',
                  children=[],
                  )






#when wrapped in function it can be easily called upon in index.py
def App():
    layout = html.Div([
        nav,
        header,
        dropdown,
        output
    ])
    return layout

#parameter will take input from dropdown menu and return plotly graph
def build_graph(setting):
    if setting == "By Branch":
        data = [go.Scatter(x=df.in,dex,
                        y=df[city]
                        marker={'color': 'orange'})]
        graph = dcc.Graph(
            figure={
                
        )
    elif setting == "As Whole"
        data = [go.Scatter(x=df.index,
                        y=df[city],
                        marker={'color': 'orange'})]
        graph = dcc.Graph(
            figure={
                'data': data,
                'layout': go.Layout(
                    title='{} Population Change'.format(city),
                    yaxis={'title': 'Population'},
                    hovermode='closest'
                )
            }
        )
    return graph
