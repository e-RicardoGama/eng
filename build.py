from dash import html, dcc
from dash.dependencies import Input, Output

from globals import *
from app import *
from components import sidebar, fisico,tabelas
from components.sobre import layout as sobre_layout

# =========  Layout  =========== #
content = html.Div(id="page-content")

app.layout = dbc.Container(children=[

    dcc.Store(id='store-eap', data=df.to_dict()),
    dcc.Store(id='store-fis', data=df_fis.to_dict()),

    dbc.Row([
        dbc.Col([
            dcc.Location(id="url"),
            sidebar.layout
        ], sm=12,lg=2),

        dbc.Col([
            html.Div(id="page-content")
        ], sm=12,lg=10),
    ])

], fluid=True, style={"padding": "0px"}, className="dbc")

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])

def render_page_content(pathname):
    if pathname == "/" or pathname == "/tabelas":
        return tabelas.layout
    if pathname == "/fisico":
        return fisico.layout
    if pathname == "/sobre":
        return sobre_layout

if __name__ == '__main__':
    app.run_server(debug=True)