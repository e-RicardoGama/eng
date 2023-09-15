import pandas as pd
import os
df = pd.read_csv('orc.csv',index_col=0)
df['Início'] = pd.to_datetime(df['Início'])
df['Termino'] = pd.to_datetime(df['Termino'])

x = df["Total"].sum()

df_plan_fis = pd.read_csv('plan_fis.csv',index_col=0)
df_plan_fis = df_plan_fis.round(2)

def date_parser(date):
    return pd.to_datetime(date, format='%Y-%m-%d')

if ('df_fis.csv' in os.listdir()):
    df = pd.read_csv('df_fis.csv', index_col=0, parse_dates=True, date_parser=date_parser)
    df_fis['Data'] = pd.to_datetime(df_fis['Data'])
    df_fis['Data'] = df_fis['Data'].apply(lambda x: x.date())

else:
    fis_structure = {
        'Atividade':[],
        'Data':[],
        'Medição':[],
        '% Acum':[]
    }

    df_fis = pd.DataFrame(fis_structure)
    df_fis.to_csv('df_fis.csv')
