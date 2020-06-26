import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_daq as daq


from prep import get_data

from homepage import Homepage
from appA import AppA, build_graphA1, build_graphA2, build_graphA3
from appB import AppB, core_layoutB

from interact import AppC

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

app.config.suppress_callback_exceptions = True

df, df_num, df_noncumun_whole, noncumun_dfs = get_data()

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])

#NavBar
@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/Pipe-dreams':
        return AppA()
    if pathname == '/Scattergories':
        return AppB()
    if pathname == '/Interact':
        return AppC()
    else:
        return Homepage()



#appA appA appA appA appA appA appA appA appA appA appA appA appA appA
#A1
@app.callback(
    dash.dependencies.Output('outputA1', 'children'),
    [dash.dependencies.Input('dropdownA1structure', 'value'),
     dash.dependencies.Input('radioA1astages', 'value'),
     dash.dependencies.Input('radioA1anumerical','value')])
def update_graphA1(path_mode, included, numerical):
    graph = build_graphA1(path_mode, included, numerical, df_num)
    return graph


#A2
@app.callback(
    Output('outputA2', 'children'),
    [Input('dropdownA2scale', 'value')]
)
def update_graph(mode):
    graph = build_graphA2(mode)
    return graph




#A3

all_options = {
    'sum': ["PotentialValue","ExpectedValue"],
    'mean': ["PotentialValue","ExpectedValue","ProbPercent"],
    'median': ["PotentialValue","ExpectedValue","ProbPercent"],
    'std': ["PotentialValue","ExpectedValue","ProbPercent"],
    'count':["PotentialValue"]
}

@app.callback(
    dash.dependencies.Output('dropdownA3numgroup', 'options'),
    [dash.dependencies.Input('dropdownA3agg', 'value')])
def set_optionsA3a(selected_agg):
    return [{'label': i, 'value': i} for i in all_options[selected_agg]]

@app.callback(
    dash.dependencies.Output('dropdownA3numgroup', 'value'),
    [dash.dependencies.Input('dropdownA3numgroup', 'options')])
def set_optionsA3b(available_options):
    return available_options[0]['value']

@app.callback(
    dash.dependencies.Output('dropdownA3group', 'value'),
    [dash.dependencies.Input('dropdownA3group', 'options')])
def set_optionsA1c(available_options):
        return available_options[0]['value']


@app.callback(
    dash.dependencies.Output('outputA3', 'children'),
    [dash.dependencies.Input('dropdownA3agg', 'value'),
     dash.dependencies.Input('dropdownA3numgroup', 'value'),
     dash.dependencies.Input('dropdownA3group','value')])
def update_graphA3(agg_method, numerical_group,group):
    #return "ag{}nu{}gr{}df{}".format(agg_method,numerical_group,group,type(df_num))
    graph = build_graphA3(agg_method, numerical_group, group,df_num)
    return graph


#appB appB appB appB appB appB appB appB appB appB appB appB appB appB appB


#@app.callback(
#    Output("number-out", "children"),
#    [Input("", "value"),]

@app.callback(
    dash.dependencies.Output('dropdownBdimension', 'options'),
    [dash.dependencies.Input('checklistB', 'value')])
def set_optionsBdimension(checked):
    return [{'label': i, 'value': i} for i in checked]




@app.callback(
    dash.dependencies.Output("layout_output", 'children'),
    [dash.dependencies.Input('toggle', 'value')])
def update_layout(value):
    body1, body2 = core_layoutB()

    if value == False:
        return body1
    if value == True:
        return body2


if __name__ == '__main__':
    app.run_server(debug=True)












"""
#@app.callback(
#    dash.dependencies.Output('sliderBx', 'children'),
#    [dash.dependencies.Input('dropdownBx', 'options')])
#def set_optionsBx(options):
#    selected = options[0]['value']
#    max_value = df_num[selected].max()
#    rangesliderx = html.Div([
#        dcc.RangeSlider(
#            id = 'sliderBxx',
#            min=0,
#            max=max_value,
#            step=max_value / 100,
#            marks={
#                0: '0',
#                max_value *(1/4) : '{}'.format(str(max_value/4)), #'{}'.format(max_value *(1/4)),
#                max_value *(2/4) : '{}'.format(str(max_value *(2/4))),
#                max_value *(3/4) : '{}'.format(str(max_value *(3/4))),
#                max_value  : '{}'.format(str(max_value)),
#            },
#            value=[0,max_value]
#        )
#    ])
#    return rangesliderx




@app.callback(Output(component_id='sliderBx', component_property='min'),
               Output(component_id='sliderBx', component_property='max'),
               Output(component_id='sliderBx', component_property='step'),
               #Output(component_id='sliderBx', component_property='marks')
               [Input(component_id='dropdownBx', component_property='options')])
def set_optionsBx(options):
    selected = options[0]['value']
    max_value = df_num[selected].max()

    minimum = 0
    maximum = max_value
    step = max_value / 100
    
    return minimum, maximum, step
    




@app.callback(
    dash.dependencies.Output('dropdownA3numgroup', 'value'),
    [dash.dependencies.Input('dropdownA3numgroup', 'options')])
def set_optionsA3b(available_options):
    return available_options[0]['value']
"""