from dash import html


# ======= Layout ===========
layout = html.Div([
    html.H1("Sobre a Plataforma", style={'textAlign': 'left'}),

    html.H2("Descrição"),
    html.P("Bem-vindo a plataforma projetada para auxiliar no acompanhamento e gerenciamento dos prazos de suas obras de maneira eficiente."),

    html.H2("Recursos Principais"),
    html.Ul([
        html.Li("Acompanhamento detalhado dos prazos de cada etapa da obra."),
        html.Li("Gráficos para analisar o progresso da obra."),
        html.Li("Gráficos para acompanhamento: mensal e acumulado."),
        html.Li("Relatórios do projeto com percentual acumulado executado."),
        html.Li("Relatório de medições."),
        html.Li("Permite o lançamento de medições diárias, semanais, quinzenais, mensais."),
        html.Li("Medições com valores acumulados: fechamentos mensais.")
        # Adicione mais itens conforme necessário.
    ]),

    html.H2("Resultados atualizados após medições"),
    html.Ul([
        html.Li('Percentual Previsto e Realizado Mensal.'),
        html.Li('Percentual Previsto e Realizado Acumulado.'),
        html.Li('Desvio do Projeto.'),
        html.Li('Relatórios: status do projeto e ações para manutenção do projeto conforme planejado.'),
    ]),

    html.H2("Como usar a plataforma"),
    html.Div([
        html.Div([
        html.P("Basta clicar no botão 'Lançar Medições':", style={'text-align': 'left'}),
        ], style={'flex': '1'}),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),
    html.Div([
        html.Div([
        html.P("1- Selecione a atividade,"),
        html.P("2- Informe a data da medição,"),
        html.P("3- Informe o número da medição,"),
        html.P("4- Lançar o percentual acumulado separados por PONTO ( . ), ex: 90.5, 35.5"),
        ], style={'flex': '1'}),
        ], style={'display': 'flex', 'justify-content': 'space-between'}),
], style={'margin': '25px'})


