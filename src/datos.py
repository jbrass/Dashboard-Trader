import pandas as pd



df_diarios_ES = pd.read_csv("./Operativa/processed/Diarios-ES.csv")
df_diarios_ES['dia'] = pd.to_datetime(df_diarios_ES['dia'], format='%m/%d/%Y', errors = 'coerce')
df_diarios_ES['dia'] = df_diarios_ES['dia'].dt.date

df_diarios_NQ = pd.read_csv("./Operativa/processed/Diarios-NQ.csv")
df_diarios_NQ['dia'] = pd.to_datetime(df_diarios_NQ['dia'], format='%m/%d/%Y', errors = 'coerce')
df_diarios_NQ['dia'] = df_diarios_NQ['dia'].dt.date

df_semanal_ES = pd.read_csv("./Operativa/processed/Semanal-ES.csv")
df_semanal_ES['dia'] = pd.to_datetime(df_semanal_ES['dia'], errors = 'coerce')
df_semanal_ES['dia'] = df_semanal_ES['dia'].dt.date

df_semanal_NQ = pd.read_csv("./Operativa/processed/Semanal-NQ.csv")
df_semanal_NQ['dia'] = pd.to_datetime(df_semanal_NQ['dia'], errors = 'coerce')
df_semanal_NQ['dia'] = df_semanal_NQ['dia'].dt.date


df_vivienda = pd.read_csv("./Operativa/processed/indicadores_del_mercado_inmobiliario.csv", delimiter=";")

df_volatilidad = pd.read_csv("./Operativa/processed/spx_quotedata.csv", on_bad_lines='skip', delimiter=",")
df_volatilidad_nq = pd.read_csv("./Operativa/processed/ndx_quotedata.csv", on_bad_lines='skip', delimiter=",")
df_volatilidad_vix = pd.read_csv("./Operativa/processed/vix_quotedata.csv", on_bad_lines='skip', delimiter=",")

#Teska
df_tesla = pd.read_csv("./Operativa/processed/tsla_quotedata.csv", on_bad_lines='skip', delimiter=",")

df_dix = pd.read_csv("./Operativa/processed/DIX.csv", on_bad_lines='skip', delimiter=",")


#Squeeze metrics
# Cargar el archivo
df_squeeze = pd.read_csv("./Operativa/processed/DIX.csv")




#Datos CBOE
#SPX
data = pd.read_csv('./Operativa/processed/spx_quotedata.csv')
#SPY
data_spy = pd.read_csv('./Operativa/processed/spy_quotedata.csv')
#CBOE Acciones
data_apple = pd.read_csv('./Operativa/processed/aapl_quotedata.csv')
data_goog = pd.read_csv('./Operativa/processed/goog_quotedata.csv')
data_meta = pd.read_csv('./Operativa/processed/meta_quotedata.csv')
data_msft = pd.read_csv('./Operativa/processed/msft_quotedata.csv')
data_amzn = pd.read_csv('./Operativa/processed/amzn_quotedata.csv')
data_nvda = pd.read_csv('./Operativa/processed/nvda_quotedata.csv')
data_amd = pd.read_csv('./Operativa/processed/amd_quotedata.csv')
#Union Acciones 
df_acciones = pd.concat([data_apple, data_goog, data_meta, data_msft, data_amzn, data_nvda, data_amd, df_tesla], ignore_index=True)


#Union Indices
df_index = pd.concat([data, data_spy, df_volatilidad_nq], ignore_index=True)



#Otras acciones esporadicas
data_otros = pd.read_csv('./Operativa/processed/ko_quotedata.csv')

#DIccionario de Acciones e Indices
data_files = {
    "spx_quotedata.csv": df_volatilidad,
    "ndx_quotedata.csv": df_volatilidad_nq,
    "aapl_quotedata.csv": data_apple,
    "goog_quotedata.csv": data_goog,
    "meta_quotedata.csv": data_meta,
    "msft_quotedata.csv": data_msft,
    "amzn_quotedata.csv": data_amzn,
    "vix_quotedata.csv": df_volatilidad_vix,
    "ko_quotedata.csv": data_otros,
    "spy_quotedata.csv": data_spy,
    "tsla_quotedata.csv": df_tesla,
    "nvda_quotedata.csv": data_nvda,
    "amd_quotedata.csv": data_amd
}






#CotReport
data_cot = pd.read_csv('./Operativa/processed/cot-report.csv')
data_cot_noncommercial = pd.read_csv('./Operativa/processed/cot-report-noncommercial.csv')




inflacion_df = pd.read_csv('./Operativa/processed/inflacion.csv', names=['Date', 'Inflation'])
tipos_interes_df = pd.read_csv('./Operativa/processed/tipos-interes.csv', names=['Date', 'Tax'])
m2_df = pd.read_csv('./Operativa/processed/m2.csv', names=['Date', 'Dato'])
empleo_df = pd.read_csv('./Operativa/processed/empleo.csv', names=['Date', 'Tax'])
dolar_df = pd.read_csv('./Operativa/processed/dolar.csv', names=['Date', 'Price'])
dolaresEmergentes_df = pd.read_csv('./Operativa/processed/dolares-emergentes.csv', names=['Date', 'Cant'])

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
    "./Operativa/processed/Diarios-ES.csv": "Mini S&P500 daily data",
    "./Operativa/processed/Diarios-NQ.csv": "Daily mini NASDAQ100 data",
    "./Operativa/processed/Semanal-ES.csv": "Mini S&P500 Weekly data",
    "./Operativa/processed/Semanal-NQ.csv": "Weekly mini NASDAQ100 data"
}


