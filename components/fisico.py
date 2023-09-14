from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from globals import *
from app import app

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 25,
    "margin": "auto",
}

graph_margin=dict(l=25, r=25, t=25, b=0)

# =========  Layout  =========== #
layout = dbc.Col([
        dbc.Row([
            # Prev Acum
            dbc.Col([
                dbc.CardGroup([
                    dbc.Card([
                        html.H5("Prev Acum"),
                        html.H6(id='prev-acum-fisico',style={'font-size':'20px'}),
                    ], style={"padding-left": "20px", "padding-top": "10px"}),
                    dbc.Card(
                        html.Div(className="fa fa-percent d-inline", style=card_icon),
                        color="primary",
#                        style={'maxWidth': '75px', 'height': '100px', 'margin-left': '-10px'},
                    )])
                ], lg=4,sm=12),
            # Real Acum
            dbc.Col([
                dbc.CardGroup([
                    dbc.Card([
                        html.H5("Real Acum"),
                        html.H6(id='real-acum-fisico',style={'font-size':'20px'}),
                    ], style={"padding-left": "20px", "padding-top": "10px"}),
                    dbc.Card(
                        html.Div(className="fa fa-percent d-inline", style=card_icon),
                        color="success",
#                        style={'maxWidth': '75px', 'height': '100px', 'margin-left': '-10px'},
                    )])
                ], lg=4,sm=12),
            # Desvio
            dbc.Col([
                dbc.CardGroup([
                    dbc.Card([
                        html.H5("Desvio"),
                        html.H6(id='desvio', style={'font-size': '20px'}),
                    ], style={"padding-left": "20px", "padding-top": "10px"}),
                    dbc.Card(
                        html.Div(className="fa fa-percent d-inline", style=card_icon),
                        color="primary",
#                        style={'maxWidth': '75px', 'height': '100px', 'margin-left': '-10px'},
                    )])
            ], lg=4, sm=12),
        ], style={"margin": "10px"}),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='graph1', className='dbc', config={"displayModeBar": False, "showTips": False})
                    ])
                ], style={"margin": "10px","margin-top":'1px'}),
            ], lg=12,sm=12),
        ], style={"margin": "10px"}),
        dbc.Row([
            dbc.Col([
                dbc.CardGroup([
                    dbc.Card([
                        html.H5("Prev Mensal"),
                        html.H6(id="previsto-mensal-fisico", style={'font-size':'20px'}),
                    ], style={"padding-left": "20px", "padding-top": "10px"}),
                    dbc.Card(
                        html.Div(className="fa fa-percent d-inline", style=card_icon),
                        color="primary",
#                        style={'maxWidth': '75px', 'height': '100px', 'margin-left': '-10px'},
                    )])
                ], lg=4, sm=12),
            dbc.Col([
                dbc.CardGroup([
                    dbc.Card([
                        html.H5("Real Mensal"),
                        html.H6(id="realizado-mensal-fisico",style={'font-size':'20px'}),
                        ], style={"padding-left": "20px", "padding-top": "10px"}),
                    dbc.Card(
                        html.Div(className="fa fa-percent d-inline", style=card_icon),
                        color="success",
#                        style={'maxWidth': '75px', 'height': '100px', 'margin-left': '-10px'},
                    )])
                ], lg=4,sm=12),
            dbc.Col([
                dbc.CardGroup([
                    dbc.Card([
                        html.H5('Desvio Mensal'),
                        html.H6(id='desvio-mes', style={'font-size':'20px'}),
                    ], style={'padding-left':'20px','padding-top':'10px'}),
                    dbc.Card(
                        html.Div(className="fa fa-percent d-inline", style=card_icon),
                        color='primary',
#                        style={'maxWidth': '75px', 'height': '100px', 'margin-left': '-10px'},
                    )
                ])
            ],lg=4,sm=12),

        ], style={"margin": "10px"}),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='graph2',className='dbc', config={"displayModeBar": False, "showTips": False})
                    ])
                ], style={"margin": "10px","margin-top":'1px'})
            ],lg=12,sm=12)
        ], style={"margin": "10px"})
])


@app.callback(
    Output('graph1','figure'),
    Output('graph2','figure'),
    Input('store-fis','data'),
)

def imprimir_medicao_mes(data):

    df = pd.DataFrame(data)
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.round(2)
    df = df.drop_duplicates()
    df = df.fillna('')

    orc = pd.read_csv('orc.csv',index_col=0)
    orc['Início'] = pd.to_datetime(orc['Início'])
    orc['Termino'] = pd.to_datetime(orc['Termino'])

    df1 = df.merge(orc[['Atividade', 'Total']], on='Atividade', how='left')
    df1['Data'] = pd.to_datetime(df1['Data'])
    df1['Mes/Ano'] = df1['Data'].dt.strftime('%m/%Y')
    df1['% Acum'] = df1['% Acum'].apply(lambda x: min(x, 100))
    df1['% Real'] = ((df1['% Acum'] * df1['Total']) / orc['Total'].sum())
    df1 = df1.groupby('Mes/Ano')['% Real'].sum().reset_index()
    df1['% Real'] = df1['% Real'].round(2)
    df1['Real Acum'] = df1['% Real'].cumsum()
    df1['Real Acum'] = df1['Real Acum'].round(2)
    df1.sort_values(by='Mes/Ano', ascending=False)

    plan_fis = pd.read_csv('plan_fis.csv',index_col=0)
    plan_fis = plan_fis.round(2)

    df2 = pd.merge(plan_fis, df1, on='Mes/Ano', how='outer')
    df2 = df2.fillna('')


    # Definindo as cores desejadas
    cor_real_acum = 'red'  # Cinza
    cor_prev_acum = 'black'  # Preto

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df2['Mes/Ano'], y=df2['Prev Acum'],
                             mode='lines+markers',
                             name='Prev Acum',
                             line=dict(color=cor_prev_acum)))
    fig1.add_trace(go.Scatter(x=df2['Mes/Ano'], y=df2['Real Acum'],
                             mode='lines+markers',
                             name='Real Acum',
                             line=dict(color=cor_real_acum)))

    fig1.update_layout(margin=dict(l=30, r=30, t=30, b=30))
    fig1.update_layout(title='Prev x Real Acumulado',
                             xaxis_title='Mes/Ano',
                             yaxis_title='%')
    fig1.update_layout(legend=dict(x=0, y=-0.4))

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df2['Mes/Ano'], y=df2['Prev Mensal'],
                         name='Prev Mensal',
                         marker_color='black'))
    fig.add_trace(go.Bar(x=df2['Mes/Ano'], y=df2['% Real'],
                         name='Real Mensal',
                         marker_color='indianred'))
    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    fig.update_layout(title='Prev x Real Mensal',
                       xaxis_title='Mes/Ano',
                       yaxis_title='%')
    fig.update_layout(margin=dict(l=30, r=30, t=30, b=30))
    fig.update_layout(legend=dict(x=0, y=-0.4))

    return fig1, fig

@app.callback(
    [
        Output('prev-acum-fisico', 'children'),
        Output('real-acum-fisico', 'children'),
        Output('desvio','children'),
        Output('previsto-mensal-fisico', 'children'),
        Output('realizado-mensal-fisico', 'children'),
        Output('desvio-mes','children'),
    ],
    Input('store-fis', 'data')
)
def atualizar_indicadores(data):
    df = pd.DataFrame(data)
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.round(2)
    df = df.drop_duplicates()
    df = df.fillna('')

    orc = pd.read_csv('orc.csv', index_col=0)
    orc['Início'] = pd.to_datetime(orc['Início'])
    orc['Termino'] = pd.to_datetime(orc['Termino'])
    orc['Total'] = pd.to_numeric(orc['Total'], errors='coerce')

    df1 = df.merge(orc[['Atividade', 'Total']], on='Atividade', how='left')
    df1['Data'] = pd.to_datetime(df1['Data'])
    df1['Mes/Ano'] = df1['Data'].dt.strftime('%m/%Y')
    df1['% Acum'] = df1['% Acum'].apply(lambda x: min(x, 100))
    df1['% Real'] = ((df1['% Acum'] * df1['Total']) / orc['Total'].sum())
    df1 = df1.groupby('Mes/Ano')['% Real'].sum().reset_index()
    df1['% Real'] = df1['% Real'].round(2)
    df1['Real Acum'] = df1['% Real'].cumsum()
    df1['Real Acum'] = df1['Real Acum'].round(2)
    df1.sort_values(by='Mes/Ano', ascending=False)

    plan_fis = pd.read_csv('plan_fis.csv', index_col=0)
    plan_fis = plan_fis.round(2)

    df2 = pd.merge(plan_fis, df1, on='Mes/Ano', how='outer')
    df2 = df2.fillna('')

    card = df2.copy()
    card['Real Acum'] = pd.to_numeric(card['Real Acum'], errors='coerce')
    filtro = card['Real Acum'] > 0
    df_card = card[filtro]

    if df_card.empty:
        previsto_acum = 0
        real_acumulado = 0
        desvio = 0
        previsto_mensal = 0
        realizado_mensal = 0
        desvio_mes = 0
    else:
        previsto_acum = df_card['Prev Acum'].iloc[-1]
        real_acumulado = df_card['Real Acum'].iloc[-1]
        desvio = ((real_acumulado - previsto_acum) / previsto_acum) * 100
        desvio = round(desvio, 2)  # Limitar a duas casas decimais
        previsto_mensal = df_card['Prev Mensal'].iloc[-1]
        realizado_mensal = df_card['% Real'].iloc[-1]
        desvio_mes = ((realizado_mensal - previsto_mensal)/previsto_mensal) * 100
        desvio_mes = round(desvio_mes,2)

    return previsto_acum, real_acumulado, desvio, previsto_mensal, realizado_mensal, desvio_mes
