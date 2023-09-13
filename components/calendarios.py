from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime

from app import app

# =========  Componentes  =========== #
calendario1 = html.Div([
    dcc.DatePickerSingle(
        id='date_picker_single',
        min_date_allowed=date(2018,12,1),
        max_date_allowed=date(2020, 12, 31),
        initial_visible_month=date(2019,10,31),
        date=date(2019,10,31)
    ),
    html.Div(id='output_container_datepicker')
])


# =========  Callbacks  =========== #
@app.callback(
    Output('output_container_datepicker', 'children'),
    Input('date_picker_single', 'date'))
def update_output(date_value):
    string_prefix = 'Selecionado: '
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%d %B, %Y')
        return string_prefix + date_string