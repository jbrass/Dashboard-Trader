import pandas as pd

df_diarios_ES = pd.read_csv("./Operativa/Diarios-ES.csv")
df_diarios_ES['dia'] = pd.to_datetime(df_diarios_ES['dia'], format='%m/%d/%Y')
df_diarios_ES['dia'] = df_diarios_ES['dia'].dt.date

df_diarios_NQ = pd.read_csv("./Operativa/Diarios-NQ.csv")
df_diarios_NQ['dia'] = pd.to_datetime(df_diarios_NQ['dia'], format='%m/%d/%Y')
df_diarios_NQ['dia'] = df_diarios_NQ['dia'].dt.date

df_semanal_ES = pd.read_csv("./Operativa/Semanal-ES.csv")
df_semanal_ES['dia'] = pd.to_datetime(df_semanal_ES['dia'])
df_semanal_ES['dia'] = df_semanal_ES['dia'].dt.date

df_semanal_NQ = pd.read_csv("./Operativa/Semanal-NQ.csv")
df_semanal_NQ['dia'] = pd.to_datetime(df_semanal_NQ['dia'])
df_semanal_NQ['dia'] = df_semanal_NQ['dia'].dt.date

renombre = {
    "./Operativa/Diarios-ES.csv": "Datos diarios mini S&P500",
    "./Operativa/Diarios-NQ.csv": "Datos diarios mini NASDAQ100",
    "./Operativa/Semanal-ES.csv": "Datos semanales mini S&P500",
    "./Operativa/Semanal-NQ.csv": "Datos semanales mini NASDAQ 100"
}
