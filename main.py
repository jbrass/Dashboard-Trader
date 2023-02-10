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
from datetime import timedelta
import datetime

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
tab1, tab2 = st.tabs(["Statistics", "Charts/Forecast"])

with tab1:

    def mostrar_sidebar():
        data_source = st.sidebar.selectbox("Select a data source", list(renombre.values()))

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
        return df

    st.sidebar.title("Data selection")
    df = mostrar_sidebar()





    
    
    st.subheader(titulo_semanal)
    st.markdown(subtitulo_semanal)
    st.markdown(resumen_semanal)
    st.markdown(titulo_cuerpo)
    st.markdown(cuerpo_semanal)

   
    
    
    st.subheader("Last 2 Days Statistics")
    # Mostrar la tabla completa al iniciar el programa
    st.dataframe(df.drop("Unnamed: 0", axis=1).tail(2))
    
    st.subheader("General Statistics")
    # Mostrar la tabla completa al iniciar el programa
    st.dataframe(df.drop("Unnamed: 0", axis=1))
    
    st.subheader("Statistics by Date Range")
    # Crear campos de entrada de fecha
    fecha_inicio = st.date_input("Select a Start Date")
    fecha_fin = st.date_input("Select an End Date")
    df["Date"] = pd.to_datetime(df["Date"])
    


    # Crear un botón para aplicar el filtro
    if st.button("Apply Filter"):
            # Filtrar la base de datos
            df_filtrado = df.drop("Unnamed: 0", axis=1)[(df["Date"].dt.date >= fecha_inicio) & (df["Date"].dt.date <= fecha_fin)]
            # Mostrar la tabla con los datos filtrados
            st.dataframe(df_filtrado)
    

    st.subheader("General statistics")
    st.write(df.describe()) 
              
    st.subheader("Correlation Heatmap")
    # Utilizar comentarios para explicar el propósito de cada sección de código
    # Crear un gráfico de correlación utilizando la librería específica
    fig = go.Figure(data=go.Heatmap(
            z=df.corr(),
            x=df.drop("Unnamed: 0", axis=1).columns,
            y=df.drop("Unnamed: 0", axis=1).columns))
    st.plotly_chart(fig)




with tab2:

    # Selección de la variable a graficar
    selected_vars = st.multiselect("Select multiple inputs", ["Day's High", "Day's Low", "Closing Price", "Volume", "Range in ticks", "VIX Closing Price", "Vwap", "Volume in Vpoc Zone", "Volume Value Area Low", "Volume Value Area High"], default=["Closing Price"])
    # Selección del tipo de gráfico
    tipo_grafico = st.selectbox("Select a Chart Type", ["Line", "Scatter", "Bars"], key='tipo_grafico', index=0)
    if len(selected_vars) > 0:
        fig = go.Figure()
        
        for variable in selected_vars:
            # Si el tipo de gráfico es línea
            if tipo_grafico == 'Line':
                fig.add_trace(go.Scatter(x=df['Date'], y=df[variable], mode='lines', name=variable))
            # Si el tipo de gráfico es dispersión
            elif tipo_grafico == 'Scatter':
                fig.add_trace(go.Scatter(x=df['Date'], y=df[variable], mode='markers', name=variable))
            # Si el tipo de gráfico es barras
            else:
                fig.add_trace(go.Bar(x=df['Date'], y=df[variable], name=variable))
        
        # Personaliza los títulos y ejes del gráfico
        fig.update_layout(
            title=f'Chart of {", ".join(selected_vars)}',
            xaxis_title='Date',
            yaxis_title='Value'
        )
        
        # Muestra el gráfico en la página
        st.plotly_chart(fig)
    else:
        st.warning("Please select at least one variable")



    @st.cache
    def model(x_name, y_name, predict_value, num_days):
        x = df[x_name].dropna().values.reshape(-1, 1)
        y = df[y_name].dropna().values.reshape(-1, 1)

        sc_x = StandardScaler()
        sc_y = StandardScaler()

        x_std = sc_x.fit_transform(x)
        y_std = sc_y.fit_transform(y)

        slr = LinearRegression()
        slr.fit(x_std, y_std)

        predict_values_std = sc_x.transform(np.array([predict_value + i for i in range(num_days)]).reshape(-1, 1))
        predictions = slr.predict(predict_values_std)
        predictions = sc_y.inverse_transform(predictions)
            
        return x_std, y_std, slr, predictions


    st.subheader("Linear Regression Model to make different predictions to one day")

    x_name = st.selectbox("Select the independent variable", ["Closing Price", "VIX Closing Price", "Volume", "Opening", "Day's High", "Day's Low", "Vpoc", "Vwap", "Range in ticks"])
    predict_value = st.number_input("Last value of the independent variable in yesterday or enter the data you want to make a relationship and with it you will have a prediction(" + x_name + "):", value=df[df['Date'] == df['Date'].max() - timedelta(days=1)][x_name].values[0])
    y_name = st.selectbox("Select the variable to predict", ["Closing Price", "VIX Closing Price", "Volume", "Opening", "Day's High", "Day's Low", "Vpoc", "Vwap", "Range in ticks"])


    x_std, y_std, slr, prediction = model(x_name, y_name, predict_value, 1)

    scatter = alt.Chart(pd.DataFrame({
        "x": x_std.flatten(),
        "y": y_std.flatten()
    })).mark_circle().encode(
        x='x',
        y='y'
    )

    line = alt.Chart(pd.DataFrame({
        "x": x_std.flatten(),
        "y": slr.predict(x_std).flatten()
    })).mark_line(color='orange').encode(
        x='x',
        y='y'
    )

    st.altair_chart(scatter + line, use_container_width=True)


    variable_dependiente = y_name

    st.write("The prediction for the variable: ", variable_dependiente, "es", prediction[0][0])

    




