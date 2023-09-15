from dash import html


# ======= Layout ===========
layout = html.Div([
    html.H1("Sobre a Plataforma", style={'textAlign': 'center'}),

    html.H2("Descrição"),
    html.P("Bem-vindo a nossa plataforma de gestão de prazos de obras! "
           "Esta plataforma foi projetada para ajudá-lo a acompanhar e gerenciar os prazos de suas obras de forma eficiente."),

    html.H2("Recursos Principais"),
    html.P("A plataforma oferece uma série de recursos que podem facilitar o gerenciamento de suas obras, "
           "incluindo:"),
    html.Ul([
        html.Li("Acompanhamento detalhado dos prazos de cada etapa da obra."),
        html.Li("Gráficos e visualizações para analisar o progresso da obra."),
        html.Li("Gráficos de acompanhamento mensal e acumulado."),
        html.Li("Relatório do projeto com percentual acumulado executado."),
        html.Li("Relatório de medições."),
        html.Li("Permite o lançamento de medições diárias, semanais e etc."),
        # Adicione mais itens conforme necessário.
    ]),
    html.H2("Como usar a plataforma"),
    html.Div([
        html.Div([
        html.P("Basta clicar no botão 'Lançar Medições':", style={'text-align': 'left'}),
        ], style={'flex': '1'}),

    ], style={'display': 'flex', 'justify-content': 'space-between'}),
    html.Div([
        html.Div([
        html.P("1: Selecione a atividade,"),
        html.P("2: Informe a data da medição,"),
        html.P("3: Informe o número da medição,"),
        html.P("4: Lance o percentual acumulado, NÃO USE VÍRGULAS, quando necessário separe por PONTO, ex: 90.5"),
        ], style={'flex': '1'}),
        ], style={'display': 'flex', 'justify-content': 'space-between'}),
    html.H2("Resultado"),
    html.P("Após cada lançamento, automaticamente todos os gráficos e planilhas são atualizados com esses valores."),
    html.Li('Percentual Previsto e Realizado Mensal.'),
    html.Li('Precentual Previsto e Realizado Acumulado.'),
    html.Li('Desvio do Projeto.'),
    html.Li('Relatórios no formato de tabelas, indicando o status do projeto, e ações necessárias para manter o projeto conforme planejado.'),
], style={'margin': '25px'})


