import json
import numpy as np
#Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_table
#Sub Modules
from prep import get_data

from homepage import Homepage
from appA import AppA, build_graphA1, build_graphA2, build_graphA3, split_filter_part
from appB import AppB, core_layoutB, build_graphBA1, build_graphBA2, build_graphBA3
#from appB import AppB, core_layoutB, build_graphBA1, build_graphBA2, build_graphBA3 #real B

from interact import AppC, build_graphC1

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
     dash.dependencies.Input('dropdownA1astages', 'value'),
     dash.dependencies.Input('radioA1anumerical','value')])
def update_graphA1(path_mode, included, numerical):
    graph = build_graphA1()#path_mode, included, numerical, df_num)
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



#Layout Master
@app.callback(
    dash.dependencies.Output("layout_output", 'children'),
    [dash.dependencies.Input('toggle', 'value')])
def update_layout(value):
    body1, body2 = core_layoutB()

    if value == False:
        return body1
    if value == True:
        return body2



#Layout BA
"""
@app.callback(
    Output('outputBA1', 'children'),
    [Input("inputBPVmin", "value"), Input("inputBPVmax", "value"),
    Input("inputBPPmin", "value"), Input("inputBPPmax", "value"),
    Input("inputBEVmin", "value"), Input("inputBEVmax", "value"),
    Input("inputBEODmin", "value"), Input("inputBEODmax", "value"),
    Input("checklistBA1", "value")]
)
def update_graphBA1(x_axis,y_axis,PV_min,PV_max,PP_min,PP_max,EOD_min,EOD_max,categorical_dimensions):
     graph = build_graphBA1()
     return graph
"""







@app.callback(
    Output('clickdatatest', 'children'),
    [Input('scatterA','clickData')]
)
def datatest1(clickData):
    return json.dumps(clickData, indent=2)




@app.callback(
    Output('selectdatatest', 'children'),
    [Input('scatterA','selectedData')]
)
def datatest2(selectedData):
    return json.dumps(selectedData, indent=2)



#BA1
@app.callback(
    Output('scatterA', 'figure'),
    [Input('radioBA2group','value'),
    Input('radioBA2numerical','value'),
    Input('scatterA', 'selectedData'),
    Input('scatterA', 'clickData')]
)
def update_graphBA1(para1,para2, selectedData,clickData):
    selected_points = []
    if selectedData:
        for selected_data in [selectedData]:
            if selected_data and selected_data['points']:
                selected_points = [p['pointIndex'] for p in selected_data['points']]
    elif clickData:
        for click_data in [clickData]:
            if clickData and clickData['points']:
                selected_points = [p['pointIndex'] for p in clickData['points']]
    fig = build_graphBA1(selected_points)
    return fig


#BA2
@app.callback(
    Output('outputBA2', 'children'),
    [Input('radioBA2group','value'),
    Input('radioBA2numerical','value')]
)
def update_graphBA2(group_sel, numerical):
    graph = build_graphBA2(group_sel, numerical)
    return graph



#BA3

@app.callback(
    dash.dependencies.Output('dropdownBA3color', 'value'),
    [dash.dependencies.Input('dropdownBA3color', 'options')])
def set_optionsA3b(available_options):
    return available_options[0]['value']

@app.callback(
    dash.dependencies.Output('dropdownBA3size', 'value'),
    [dash.dependencies.Input('dropdownBA3size', 'options')])
def set_optionsA3b(available_options):
    return available_options[0]['value']

@app.callback(
    dash.dependencies.Output('dropdownBA3symbol', 'value'),
    [dash.dependencies.Input('dropdownBA3symbol', 'options')])
def set_optionsA3b(available_options):
    return available_options[0]['value']









@app.callback(
    Output('outputBA3', 'children'),
    [Input('dropdownBA3color', 'value'),
    Input('dropdownBA3size', 'value'),
    Input('dropdownBA3symbol', 'value'),
    Input("inputBPVmin", "value"), Input("inputBPVmax", "value"),
    Input("inputBPPmin", "value"), Input("inputBPPmax", "value"),
    Input("inputBEVmin", "value"), Input("inputBEVmax", "value"),
    Input("inputBEODmin", "value"), Input("inputBEODmax", "value"),]
)
def update_graphBA3(color_sel,size_sel,symbol_sel,PV_min,PV_max,PP_min,PP_max,EV_min,EV_max,EOD_min,EOD_max):
    graph = build_graphBA3(color_sel,size_sel,symbol_sel,PV_min,PV_max,PP_min,PP_max,EV_min,EV_max,EOD_min,EOD_max)
    return graph



#Layout B
@app.callback(
    dash.dependencies.Output('dropdownBB1dimension', 'options'),
    [dash.dependencies.Input('checklistBB1', 'value')])
def set_optionsBdimension(checked):
    return [{'label': i, 'value': i} for i in checked]

#Interact

@app.callback(
    Output('selected-data', 'children'),
    [Input('timeline', 'selectedData')])
def display_selected_data(selectedData):
    idlist = []
    for i in selectedData['points']:
        idlist.append(i['customdata'])
    idlist = [val for sublist in idlist for val in sublist]
    df_table = df_num[df_num.index.isin(idlist)]
    
    if selectedData:
        return json.dumps(selectedData, indent=2)
    if not selectedData:
        return "didnt work"




@app.callback(
    Output('datatableBA', 'data'),
    [Input('datatableBA', "page_current"),
     Input('datatableBA', "page_size"),
     Input('datatableBA', 'sort_by'),
     Input('datatableBA', 'filter_query'),
     Input('scatterA', 'selectedData')])
def update_table(page_current, page_size, sort_by, filter, selectedData):
    filtering_expressions = filter.split(' && ')
    selected_points = []
    if selectedData:
        for selected_data in [selectedData]:
            if selected_data and selected_data['points']:
                selected_points = [p['pointIndex'] for p in selected_data['points']]
    dff = df_num.iloc[[*selected_points]]
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    page = page_current
    size = page_size
    return dff.iloc[page * size: (page + 1) * size].to_dict('records')






if __name__ == '__main__':
    app.run_server(debug=True)