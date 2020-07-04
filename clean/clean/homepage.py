import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar










nav = Navbar()










body = dbc.Col([
    dbc.Row([dcc.Upload([
        'Drag and Drop or ',
        html.A('Select a File')
    ], style={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center'
    })]),
    dbc.Row([]),
    dbc.Row([]),
])




def Homepage():
    layout = html.Div([
    nav,
    body
    ])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.COSMO])
app.layout = Homepage()
if __name__ == "__main__":
    app.run_server()


