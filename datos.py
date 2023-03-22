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


df_volatilidad = pd.read_csv("./Operativa/spx_quotedata.csv", on_bad_lines='skip', delimiter=",")
df_volatilidad_nq = pd.read_csv("./Operativa/ndx_quotedata.csv", on_bad_lines='skip', delimiter=",")
df_volatilidad_vix = pd.read_csv("./Operativa/vix_quotedata.csv", on_bad_lines='skip', delimiter=",")

df_dix = pd.read_csv("./Operativa/DIX.csv", on_bad_lines='skip', delimiter=",")



inflacion_df = pd.read_csv('./Operativa/inflacion.csv', names=['Date', 'Inflation'])
tipos_interes_df = pd.read_csv('./Operativa/tipos-interes.csv', names=['Date', 'Tax'])
m2_df = pd.read_csv('./Operativa/m2.csv', names=['Date', 'Dato'])
empleo_df = pd.read_csv('./Operativa/empleo.csv', names=['Date', 'Tax'])
dolar_df = pd.read_csv('./Operativa/dolar.csv', names=['Date', 'Price'])
dolaresEmergentes_df = pd.read_csv('./Operativa/dolares-emergentes.csv', names=['Date', 'Cant'])

#elimino la fila 0
# Eliminar la fila 0 de inflacion_df
inflacion_df = inflacion_df.drop(0)

# Eliminar la fila 0 de tipos_interes_df
tipos_interes_df = tipos_interes_df.drop(0)

# Eliminar la fila 0 de m2_df
m2_df = m2_df.drop(0)

# Eliminar la fila 0 de empleo_df
empleo_df = empleo_df.drop(0)


# Eliminar la fila 0 de dolar_df
empleo_df = dolar_df.drop(0)

# Eliminar la fila 0 de dolaresEmergentes_df
empleo_df = dolaresEmergentes_df.drop(0)

#df_inflacion = pd.read_csv("./Operativa/inflacion.csv", on_bad_lines='skip', delimiter=",")

## Renombro algunas columnas 
def rename_columns(df):
    df = df.rename(columns={
        "high": "Day's High",
        "low": "Day's Low",
        "close": "Closing Price",
        "vol": "Volume",
        "range": "Range in ticks",
        "vix_close": "VIX Closing Price",
        "vwap": "Vwap",
        "vol_vpoc": "Volume in Vpoc Zone",
        "vol_val": "Volume Value Area Low",
        "vol_vah": "Volume Value Area High",
        "open": "Opening",
        "vpoc": "Vpoc",
        "dia": "Date",
        "vah": "Value Area High",
        "val": "Value Area Low",
        "poc_naked": "Naked Open Poc",
        "rango_area": "Range of Area in points",
        "delta": "Delta",
        "dia_semanal": "Weekday",
        "tendencia": "Trend",
        "cot_commercial": "Cot Commercial",
        "cot_noncommercial": "Cot Non Commercial",
        "cot_dealer": "Cot Dealer",
        "cot_institutional": "Cot Institutional",
        "cot_leveragedfunds": "Cot Leveraged Funds",
        "cot_other": "Cot Other"
        
    })
    return df

df_diarios_ES = rename_columns(df_diarios_ES)
df_diarios_NQ = rename_columns(df_diarios_NQ)
df_semanal_ES = rename_columns(df_semanal_ES)
df_semanal_NQ = rename_columns(df_semanal_NQ)




renombre = {
    "./Operativa/Diarios-ES.csv": "Mini S&P500 daily data",
    "./Operativa/Diarios-NQ.csv": "Daily mini NASDAQ100 data",
    "./Operativa/Semanal-ES.csv": "Mini S&P500 Weekly data",
    "./Operativa/Semanal-NQ.csv": "Weekly mini NASDAQ100 data"
}


