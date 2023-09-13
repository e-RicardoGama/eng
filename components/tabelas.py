from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from globals import *
from app import app
from dash import dash_table
import locale
from datetime import datetime


card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

graph_margin=dict(l=25, r=25, t=25, b=0)

# ==================Localização
# Defina a localização para o formato brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        dbc.Card([
            dbc.CardBody([
                html.Legend('Atualização Diária do Status das Atividades')
            ])
        ])
    ],style={'padding':'10px'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5('Planilha de Orçamento e Percentual Executado'),
                    html.Div(id='orc-perc',className='dbc')
                ])
            ]),
            ],lg=6,sm=12),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5('Relatório Medições'),
                    html.Div(id='tabela-medicao',className='dbc')
                ])
            ])
        ],lg=6,sm=12)
        ],style={'padding':'5px'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5('Atividades Atrasadas'),
                    html.Div(id='atrasada',className='dbc')
                ])
            ], style={"margin": "10px","margin-top":'1px'})
        ], lg=6, sm=12),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5('Atividades em execução'),
                    html.Div(id='exec-hoje',className='dbc')
                ])
            ],style={'margin':'10px','margin-top':'1px'})
        ],lg=6,sm=12)
    ],style={'padding':'5px'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5('Atividades que iniciam hoje'),
                    html.Div(id='inicio-hoje',className='dbc')
                ])
            ],style={'margin':'10px','margin-top':'1px'})
        ],lg=6,sm=12),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5('Atividades que devem ser concluídas hoje'),
                    html.Div(id='termino-hoje',className='dbc')
                ])
            ],style={'margin':'10px','margin-top':'1px'})
        ],lg=6,sm=12),
    ],style={'padding':'5px'})
])


@app.callback(
    Output('orc-perc','children'),
    Input('store-fis','data')
)

def tabela_orc_medido(data):
    df1 = pd.DataFrame(data)
    df1['Data'] = pd.to_datetime(df1['Data'])
    df1 = df1.groupby('Atividade')['% Acum'].max().reset_index()


    df = pd.read_csv('orc.csv',index_col=0)
    df['Início'] = pd.to_datetime(df['Início']).dt.date
    df['Termino'] = pd.to_datetime((df['Termino'])).dt.date
    df = df.drop(columns=['Obra'])

    df = df.merge(df1[['Atividade', '% Acum']], on='Atividade', how='left')
    df = df.drop(columns=['Atividade','Total','Duracao'])
    df['% Acum'] = df['% Acum'].apply(lambda x: min(x, 100))
    df = df.fillna(0)

    data_de_referencia = datetime(2019,4,25).date()

    def calcular_status(row):
        df['% Acum'] = df['% Acum'].astype(float)

        if row['% Acum'] == 100:
            return 'Concluída'
        elif row['% Acum'] < 100 and row['Início'] < data_de_referencia and row['Termino'] < data_de_referencia:
            return 'Atrasada'
        elif row['% Acum'] < 100 and row['Início'] <= data_de_referencia < row['Termino']:
            return 'Em Execução'
        else:
            return 'Atividade Futura'

    df['Status'] = df.apply(calcular_status, axis=1)

    orc_medido = dash_table.DataTable(style_data={'whiteSpace': 'normal','height': 'auto',},
                                     data=df.to_dict('records'),
                                     columns=[{'name':i, 'id':i} for i in df.columns],
                                     fixed_rows={'headers': True},
                                     style_table={'height': '200px', 'overflowY': 'auto'},
                                     style_cell_conditional = [
                                         {'if': {'column_id': 'Etapa'},
                                          'width': '5%', 'textAlign': 'left'},
                                         {'if': {'column_id': 'Sub Etapa'},
                                          'width': '5%','textAlign':'left'},
                                         {'if': {'column_id': 'Início'},
                                          'width':'3%'},
                                         {'if': {'column_id': 'Termino'},
                                          'width': '3%'},
                                         {'if': {'column_id': '% Acum'},
                                          'width': '1%','textAlign':'center'},
                                         {'if': {'column_id': 'Status'},
                                          'width': '1%','textAlign':'center'}
                                                ]
                                                   ),

    return orc_medido

@app.callback(
    Output('tabela-medicao','children'),
    Input('store-fis','data'),
)

def tabela_medicao(data):

    df= pd.DataFrame(data)
    df = df.drop_duplicates()
    df['Data'] = pd.to_datetime(df['Data']).dt.date
    df['% Acum'] = df['% Acum'].apply(lambda x: min(x, 100))
    df = df.fillna('-')
    df.sort_values(by='Data',ascending=False)

    relatorio = dash_table.DataTable(style_data={'whiteSpace': 'normal','height': 'auto',},
                                     data=df.to_dict('records'),
                                     columns=[{'name':i, 'id':i} for i in df.columns],
                                     fixed_rows={'headers': True},
                                     style_table={'height': '200px', 'overflowY': 'auto'},
                                     style_cell_conditional = [
                                         {'if': {'column_id': 'Medição'},
                                          'width': '12%'},
                                         {'if': {'column_id': '% Acum'},
                                          'width': '10%'},
                                         {'if': {'column_id': 'Data'},
                                          'width': '20%'},
                                         {'if': {'column_id': 'Atividade'},
                                          'textAlign': 'left'}
                                                ]),
    return relatorio

@app.callback(
    Output('atrasada','children'),
    Output('inicio-hoje','children'),
    Output('termino-hoje','children'),
    Output('exec-hoje','children'),
    Input('store-fis','data'),
)

def inicio_hoje(data):
    df1 = pd.DataFrame(data)
    df1['Data'] = pd.to_datetime(df1['Data'])
    df1 = df1.groupby('Atividade')['% Acum'].max().reset_index()

    df = pd.read_csv('orc.csv', index_col=0)
    df['Início'] = pd.to_datetime(df['Início']).dt.date
    df['Termino'] = pd.to_datetime((df['Termino'])).dt.date
    df = df.drop(columns=['Obra'])

    df = df.merge(df1[['Atividade', '% Acum']], on='Atividade', how='left')
    df = df.drop(columns=['Atividade'])
    df['% Acum'] = df['% Acum'].apply(lambda x: min(x, 100))
    df = df.fillna(0)

    data_de_referencia = datetime(2019,4,25).date()

    df_hoje = df.copy()
    df_hoje_fim = df.copy()
    df_hoje_ex = df.copy()
    df_atrasada = df.copy()

    # Filtrar as atividades atrasadas
    df_atrasada = df_atrasada[(df_atrasada['Início'] < data_de_referencia) &(df_atrasada['Termino']<data_de_referencia) & (df_atrasada['% Acum'] < 100)]
    df_atrasada.drop(columns=['Total', 'Duracao'], inplace=True)

    # Filtrar as atividades que começam hoje e têm '% Acum' menor que 100
    df_hoje = df_hoje[(df_hoje['Início'] == data_de_referencia) & (df_hoje['% Acum'] < 100)]
    df_hoje.drop(columns=['Total','Duracao'],inplace=True)

    # Filtrar as atividades que terminam hoje e têm '% Acum' menor que 100
    df_hoje_fim = df_hoje_fim[(df_hoje_fim['Termino'] == data_de_referencia) & (df_hoje_fim['% Acum'] < 100)]
    df_hoje_fim.drop(columns=['Total', 'Duracao'], inplace=True)

    # Filtrar as atividades em execução hoje e têm '% Acum' menor que 100
    df_hoje_ex = df_hoje_ex[(df_hoje_ex['Início'] <= data_de_referencia) & (df_hoje_ex['Termino'] >= data_de_referencia) & (df_hoje_ex['% Acum'] < 100)]
    df_hoje_ex.drop(columns=['Total', 'Duracao'], inplace=True)

    atrasada = dash_table.DataTable(style_data={'whiteSpace': 'normal', 'height': 'auto', },
                                data=df_atrasada.to_dict('records'),
                                columns=[{'name': i, 'id': i} for i in df_atrasada.columns],
                                fixed_rows={'headers': True},
                                style_table={'height': '200px', 'overflowY': 'auto'},
                                style_cell_conditional=[
                                    {'if': {'column_id': 'Etapa'},
                                     'width': '20%', 'textAlign': 'left'},
                                    {'if': {'column_id': 'Sub Etapa'},
                                     'width': '20%', 'textAlign': 'left'},
                                    {'if': {'column_id': 'Início'},
                                     'width': '12%'},
                                    {'if': {'column_id': 'Termino'},
                                     'width': '12%'},
                                    {'if': {'column_id': '% Acum'},
                                     'width': '5%', 'textAlign': 'center'}
                                ]),

    hoje = dash_table.DataTable(style_data={'whiteSpace': 'normal','height': 'auto',},
                                     data=df_hoje.to_dict('records'),
                                     columns=[{'name':i, 'id':i} for i in df_hoje.columns],
                                     fixed_rows={'headers': True},
                                     style_table={'height': '200px', 'overflowY': 'auto'},
                                     style_cell_conditional=[
                                         {'if': {'column_id': 'Etapa'},
                                          'width': '20%','textAlign':'left'},
                                         {'if': {'column_id': 'Sub Etapa'},
                                          'width': '20%','textAlign':'left'},
                                         {'if': {'column_id': 'Início'},
                                          'width': '12%'},
                                         {'if': {'column_id': 'Termino'},
                                          'width': '12%'},
                                         {'if': {'column_id': '% Acum'},
                                          'width':'5%','textAlign': 'center'}
                                     ]),

    fim_hoje = dash_table.DataTable(style_data={'whiteSpace': 'normal','height': 'auto',},
                                     data=df_hoje_fim.to_dict('records'),
                                     columns=[{'name':i, 'id':i} for i in df_hoje_fim.columns],
                                     fixed_rows={'headers': True},
                                     style_table={'height': '200px', 'overflowY': 'auto'},
                                     style_cell_conditional=[
                                         {'if': {'column_id': 'Etapa'},
                                          'width': '20%','textAlign':'left'},
                                         {'if': {'column_id': 'Sub Etapa'},
                                          'width': '20%','textAlign':'left'},
                                         {'if': {'column_id': 'Início'},
                                          'width': '12%'},
                                         {'if': {'column_id': 'Termino'},
                                          'width': '12%'},
                                         {'if': {'column_id': '% Acum'},
                                          'width':'5%','textAlign': 'center'}
                                     ]),

    execucao = dash_table.DataTable(style_data={'whiteSpace': 'normal', 'height': 'auto', },
                                    data=df_hoje_ex.to_dict('records'),
                                    columns=[{'name': i, 'id': i} for i in df_hoje_ex.columns],
                                    fixed_rows={'headers': True},
                                    style_table={'height': '200px', 'overflowY': 'auto'},
                                    style_cell_conditional=[
                                        {'if': {'column_id': 'Etapa'},
                                         'width': '20%', 'textAlign': 'left'},
                                        {'if': {'column_id': 'Sub Etapa'},
                                         'width': '20%', 'textAlign': 'left'},
                                        {'if': {'column_id': 'Início'},
                                         'width': '12%'},
                                        {'if': {'column_id': 'Termino'},
                                         'width': '12%'},
                                        {'if': {'column_id': '% Acum'},
                                         'width': '5%', 'textAlign': 'center'}
                                    ]),

    return atrasada,hoje, fim_hoje, execucao


