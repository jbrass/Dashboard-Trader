import pandas as pd

df_diarios_ES = pd.read_csv("./Operativa/Diarios-ES.csv")
df_diarios_ES['dia'] = pd.to_datetime(df_diarios_ES['dia'], format='%m/%d/%Y', errors = 'coerce')
df_diarios_ES['dia'] = df_diarios_ES['dia'].dt.date

df_diarios_NQ = pd.read_csv("./Operativa/Diarios-NQ.csv")
df_diarios_NQ['dia'] = pd.to_datetime(df_diarios_NQ['dia'], format='%m/%d/%Y', errors = 'coerce')
df_diarios_NQ['dia'] = df_diarios_NQ['dia'].dt.date

df_semanal_ES = pd.read_csv("./Operativa/Semanal-ES.csv")
df_semanal_ES['dia'] = pd.to_datetime(df_semanal_ES['dia'], errors = 'coerce')
df_semanal_ES['dia'] = df_semanal_ES['dia'].dt.date

df_semanal_NQ = pd.read_csv("./Operativa/Semanal-NQ.csv")
df_semanal_NQ['dia'] = pd.to_datetime(df_semanal_NQ['dia'], errors = 'coerce')
df_semanal_NQ['dia'] = df_semanal_NQ['dia'].dt.date



## Renombro algunas columnas 
def rename_columns(df):
    df = df.rename(columns={
        "high": "Máximo del día",
        "low": "Mínimo del día",
        "close": "Precio de cierre",
        "vol": "Volumen",
        "range": "Rango en ticks",
        "vix_close": "Precio cierre de VIX",
        "vwap": "Vwap",
        "vol_vpoc": "Volumen en zona de Vpoc",
        "vol_val": "Volumen Value Area Low",
        "vol_vah": "Volumen Value Area High",
        "open": "Apertura",
        "vpoc": "Vpoc"
    })
    return df

df_diarios_ES = rename_columns(df_diarios_ES)
df_diarios_NQ = rename_columns(df_diarios_NQ)
df_semanal_ES = rename_columns(df_semanal_ES)
df_semanal_NQ = rename_columns(df_semanal_NQ)




renombre = {
    "./Operativa/Diarios-ES.csv": "Datos diarios mini S&P500",
    "./Operativa/Diarios-NQ.csv": "Datos diarios mini NASDAQ100",
    "./Operativa/Semanal-ES.csv": "Datos semanales mini S&P500",
    "./Operativa/Semanal-NQ.csv": "Datos semanales mini NASDAQ 100"
}


