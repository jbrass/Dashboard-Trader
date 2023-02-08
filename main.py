# Importar las librerías necesarias
from datos import *
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import altair as alt
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from bokeh.plotting import figure
import yfinance as yf
import datetime as dt
import streamlit as st
import requests
from bs4 import BeautifulSoup
import ta
from textos import *
from sklearn.preprocessing import StandardScaler



st.set_page_config(page_title="Mi tablero de Streamlit",
                   page_icon=":guardsman:",
                   layout="wide",
                   initial_sidebar_state="expanded")
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



    
# Cargar la imagen de logo
with open("fintra-logo.png", 'rb') as img:
    st.image(img.read(), width=200)

# Utilizar una estructura de control de flujo más clara
tab1, tab2 = st.tabs(["Estadísticas", "Gráficos/Forecast"])

with tab1:

    data_source = st.selectbox("Selecciona una fuente de datos", list(renombre.values()))

    for archivo, nombre_amigable in renombre.items():
        if data_source == nombre_amigable:
            if archivo == "./Operativa/Diarios-ES.csv":
                df = df_diarios_ES
            elif archivo == "./Operativa/Diarios-NQ.csv":
                df = df_diarios_NQ
            elif archivo == "./Operativa/Semanal-ES.csv":
                df = df_semanal_ES
            else:
                df = df_semanal_NQ
            break
    
    
    st.subheader(titulo_semanal)
    st.markdown(subtitulo_semanal)
    st.markdown(resumen_semanal)
    st.markdown(titulo_cuerpo)
    st.markdown(cuerpo_semanal)

   
    
    
    st.header("Estadísticas últimos 2 días")
    # Mostrar la tabla completa al iniciar el programa
    st.dataframe(df.drop("Unnamed: 0", axis=1).tail(2))
    
    st.subheader("Estadísticas Generales")
    # Mostrar la tabla completa al iniciar el programa
    st.dataframe(df.drop("Unnamed: 0", axis=1))
    
    st.subheader("Estadísticas por rango de fechas")
    # Crear campos de entrada de fecha
    fecha_inicio = st.date_input("Selecciona una fecha de inicio")
    fecha_fin = st.date_input("Selecciona una fecha de fin")

    # Crear un botón para aplicar el filtro
    if st.button("Aplicar filtro"):
            # Filtrar la base de datos
            df_filtrado = df.drop("Unnamed: 0", axis=1)[(df["dia"] >= fecha_inicio.strftime("%m/%d/%Y")) & (df["dia"] <= fecha_fin.strftime("%m/%d/%Y"))]
            # Mostrar la tabla con los datos filtrados
            st.dataframe(df_filtrado)
            
    st.subheader("Mapa de Correlaciones")
    # Utilizar comentarios para explicar el propósito de cada sección de código
    # Crear un gráfico de correlación utilizando la librería específica
    fig = go.Figure(data=go.Heatmap(
            z=df.corr(),
            x=df.columns,
            y=df.columns))
    st.plotly_chart(fig)




with tab2:
    
    # Encabezado para la sección de gráficos
    st.header("Gráficos")

    # Selección de la variable a graficar
    variable = st.selectbox("Seleccione una variable", ["high", "low", "close", "vol", "range", "vix_close", "vwap", "vol_vpoc", "vol_vah", "vol_val"], key='variable', index=0)

    # Selección del tipo de gráfico
    tipo_grafico = st.selectbox("Seleccione un tipo de gráfico", ["Línea", "Dispersión", "Barras"], key='tipo_grafico', index=0)

    # Verifica si la variable seleccionada es válida para un gráfico de línea, dispersión o barras
    if variable in ["high", "low", "close", "vol", "range", "vix_close", "vwap", "vol_vpoc", "vol_vah", "vol_val"]:
        # Crea un gráfico con x como el día y y como el valor de la variable seleccionada
        fig = go.Figure()

        # Si el tipo de gráfico es línea
        if tipo_grafico == 'Línea':
            fig.add_trace(go.Scatter(x=df['dia'], y=df[variable], mode='lines'))
        # Si el tipo de gráfico es dispersión
        elif tipo_grafico == 'Dispersión':
            fig.add_trace(go.Scatter(x=df['dia'], y=df[variable], mode='markers'))
        # Si el tipo de gráfico es barras
        else:
            fig.add_trace(go.Bar(x=df['dia'], y=df[variable]))

        # Personaliza los títulos y ejes del gráfico
        fig.update_layout(
            title=f'Gráfico de {variable}',
            xaxis_title='Día',
            yaxis_title=variable
        )

        # Muestra el gráfico en la página
        st.plotly_chart(fig)
    else:
        st.warning("La variable seleccionada no es válida.")

    st.subheader('Pulsa el botón de la izquierda Predecir y podrás hacer una predicción sobre la variable que desees')

    dfs = {'Diarios ES': df_diarios_ES, 'Diarios NQ': df_diarios_NQ,
        'Semanal ES': df_semanal_ES, 'Semanal NQ': df_semanal_NQ}

    # Función para realizar la regresión lineal
    def regresion_lineal(df, valor, dias):
        if 'close' not in df.columns or valor not in df.columns:
            st.error("Error: las columnas necesarias no están presentes en el dataframe.")
            return

        x = df['close'].values.reshape(-1, 1)
        y = df[valor].values.reshape(-1, 1)

        sc_x = StandardScaler()
        x_std = sc_x.fit_transform(x)

        slr = LinearRegression()
        slr.fit(x_std, y)

        x_pred = [x[-1]] + [x[-1] + i for i in range(1, dias + 1)]
        x_pred_std = sc_x.transform(np.array(x_pred).reshape(-1, 1))
        y_pred = slr.predict(x_pred_std)

        data = pd.DataFrame({'x_std': x_std.flatten(), 'y': y.flatten()})
        data_pred = pd.DataFrame({'x_pred_std': x_pred_std.flatten(), 'y_pred': y_pred.flatten()})

        st.line_chart(data)
        st.line_chart(data_pred, use_container_width=True)
        return y_pred
    

    # Usar un sidebar de Streamlit para obtener la entrada del usuario
    st.sidebar.header("Pronóstico")

        
        
    rename_values = {'close': 'Cierre', 'vol': 'Volumen', 'vpoc': 'VPOC', 'vwap': 'VWAP', 'vol_vah': 'Volumen en VAH', 'vol_vpoc': 'Volumen en VPOC', 'vol_val': 'Volumen en VAL', 'vix_close': 'VIX Cierre', 'range': 'Rango', 'high': 'Alto', 'low': 'Bajo', 'delta': 'Delta'}
    valor = st.sidebar.selectbox("Seleccione el valor a predecir", [rename_values[i] for i in rename_values.keys()])
    valor = [key for key, value in rename_values.items() if value == valor][0]

    dias = st.sidebar.number_input("Ingrese el número de días a predecir", min_value=1, max_value=365, value=30)


    # Llamar a la función con la entrada del usuario
    if st.sidebar.button("Predecir"):
        y_pred = regresion_lineal(df, valor, dias)
        st.write("Valores pronosticados:", y_pred)     


