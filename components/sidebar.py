from datetime import datetime, date
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash import Input, Output, State
from app import app
from globals import *

# ========= Layout ========= #
layout = dbc.Card([
        html.Img(src=r'assets/buid.png', className='perfil_avatar',
                style={'background-color': 'transparent', 'border-color': 'transparent'}),
        html.Legend("Gestão de Prazos nas Obras", className="text-primary",
                style={'margin-top':'10px'}),
        dbc.Button("Visite o Site", href="https://www.rgama.net/", target="_blank",style={'margin-top':'10px'}),
        html.Hr(),



# Seção + NOVO ------------------------
        dbc.Row([
            html.H6('Clique no botão abaixo para:', className='text-primary'),
            dbc.Button(color="dark", id="open-novo-fisico",
                    children=["Lançar Medições"],style={'margin-top':'20px'}),

            ]),

# Modal Serviços -------------------
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle('Lançamento Medições')),
            dbc.ModalBody([
                dbc.Row([
                   dbc.Col([
                       dbc.Label('Selecione a Atividade'),
                        dbc.Select(
                            id='selecione-atividade-fis',
                            options=[{'label': atividade, 'value': atividade} for atividade in df['Atividade'].unique()],
                            value=[df['Atividade'].iloc[0]],
                            style={'margin':'5px'}
                        ),
                   ],width=12, style={'padding':'10px'})
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Data Medição: '),
                        dcc.DatePickerSingle(
                            id='data-medicao',
                            min_date_allowed=date(2018, 12, 1),
                            max_date_allowed=date(2020, 1, 31),
                            date=date(2019,10,31),
                            style={'width':'100%'}
                        )
                    ],lg=3,sm=12, style={'padding':'10px'}),
                    dbc.Col([
                        dbc.Label('Medição'),
                        dbc.Input(placeholder='Ex:1, 2, 10,...',
                                  id='n-med'),
                    ],lg=4,sm=6,style={'padding':'10px'}),
                    dbc.Col([
                        dbc.Label('% Acumulado'),
                        dbc.Input(placeholder='Ex: 25.5, 50, 65,....',
                                  id='perc-servico',
                                  step=0.1,
                                  min=0.0,
                                  max=100.0),
                    ], lg=4,sm=6,style={'padding':'10px'}),
                    dbc.ModalFooter([
                            dbc.Button("Adicionar Medição", id="salvar_medicao", color="success"),
                            dbc.Popover(dbc.PopoverBody("Medição Salva"), target="salvar_medicao", placement="left", trigger="click"),
                        ]
                        )
                ],style={'margin-top':'20px'}),
            ])
        ], style={'backgroud-color':'rgba(17,140,79,0.05)'},
            id='modal-novo-servico',
        size='lg',
        is_open=False,
        centered=True,
        backdrop=True),

# Seção NAV =========================

        html.Hr(),
        html.H5('Selecione a página', className='text-primary'),
        dbc.Nav(
            [
                dbc.NavLink('Status Obra', href='/fisico', active='exact'),
                dbc.NavLink("Relatórios - Planilhas", href="/tabelas", active="exact"),
                dbc.NavLink('Sobre a plataforma', href='/sobre',active='exact'),
            ], vertical=True, pills=True, id='nav_buttons', style={"margin-bottom": "50px", "margin-top": "20px"}),
        ], style={'margin-top': '10px'}, id='sidebar_completa')

# Calbacks --------------------------
# Pop up Serviços

@app.callback(
    Output('modal-novo-servico','is_open'),
    Input('open-novo-fisico','n_clicks'),
    State('modal-novo-servico','is_open')
)

def toggle_modal(n1, is_open):
    if n1:
        return not is_open


#def toggle_modal(n1, is_open):
#    if n1:
#        return not is_open

# Preencher o dataframe de medições
@app.callback(
    Output('store-fis','data'),
    Input('salvar_medicao','n_clicks'),
    [
        State('selecione-atividade-fis','value'),
        State('data-medicao','date'),
        State('n-med','value'),
        State('perc-servico','value'),
        State('store-fis','data')
    ]
)

def salvar_medicao(n,atividade,date,med,valor,dict_df_fis):
    df_fis = pd.DataFrame(dict_df_fis)

    if n and not(valor == '' or valor == None):
        valor = round(float(valor),2)
        med = min(int(med), 100)
        date = pd.to_datetime(date).date()
        atividade = atividade[0] if isinstance(atividade, list) else atividade

        if atividade in df_fis['Atividade'].values:
            # Verifica se a atividade já foi concluída (tem % Acum = 100)
            if df_fis.loc[(df_fis['Atividade'] == atividade) & (df_fis['% Acum'] == 100)].shape[0] > 0:
                return dict_df_fis  # Não atualize se a atividade for concluída

        # Certifique-se de que% Acum permaneça dentro do intervalo [0, 100]
        valor = max(min(valor, 100), 0)

        df_fis.loc[df_fis.shape[0]] = [atividade,date,med,valor]
        df_fis.drop_duplicates()
        df_fis.to_csv('df_fis.csv')


    data_return_fis = df_fis.to_dict()
    return data_return_fis
