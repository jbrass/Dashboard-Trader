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
import ta
from textos import *
from sklearn.preprocessing import StandardScaler
from datetime import timedelta
import datetime
import plotly.express as px
import scipy
from scipy.stats import norm
import matplotlib.pyplot as plt
import yfinance as yf


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
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Markets Report", "Statistics", "Charts/Forecast", "Track Record", "Gamma"])

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






    with st.expander(titulo_semanal):
            st.caption(resumen_semanal)
            st.markdown(titulo_cuerpo)
            st.markdown(cuerpo_semanal)

            

    with st.expander(title_renta_variable):
            st.caption(renta_variable)
            st.image("./img/renta_variable.png")
            
            
    with st.expander(title_renta_fija):
            st.caption(renta_fija)
            st.image("./img/renta_fija.png")
            
            
    with st.expander(title_divisa_mater):
            st.caption(divisa_materia)
            st.image("./img/materias_divisas.png")
            


    st.info(title_esta_semana, icon="ℹ️")
    st.caption(esta_semana1)
    st.caption(esta_semana2)
    st.caption(esta_semana3)
    st.caption(esta_semana4)
    st.caption(esta_semana5)


    
    
with tab2: 
    
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




with tab3:

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

    y_name = st.selectbox("Select the variable to predict", ["Closing Price", "VIX Closing Price", "Volume", "Opening", "Day's High", "Day's Low", "Vpoc", "Vwap", "Range in ticks"])
    latest_date = df['Date'].max() - timedelta(days=1)
    latest_row = df[df['Date'] == latest_date][x_name]
    if not latest_row.empty:
        predict_value = st.number_input("Last value of the independent variable in yesterday or enter the data you want to make a relationship and with it you will have a prediction(" + x_name + "):", value=latest_row.values[0])
    else:
        predict_value = st.number_input("Last value of the independent variable in yesterday or enter the data you want to make a relationship and with it you will have a prediction(" + x_name + "):")


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

with tab4:


    st.subheader('Sube el archivo estadísticas de tus operaciones')
    # Carga el archivo
    archivo = st.file_uploader("Elige un archivo CSV o Excel", type=["csv", "xlsx"])
    


    # Si se seleccionó un archivo
    if archivo is not None:
        # Lee el archivo en un dataframe de pandas
        df = pd.read_csv(archivo, delimiter=";", parse_dates=["Period"]) if archivo.type == "text/csv" else pd.read_excel(archivo, engine='openpyxl', parse_dates=["Period"])
        # Convierte la columna "Period" a formato de fecha sin hora
        df['Period'] = pd.to_datetime(df['Period']).dt.date

        # Reemplazar comas con puntos en todo el dataframe
        df = df.apply(lambda x: x.str.replace(',', '.') if x.dtype == "object" and x.name != "Period" else x)


        # Muestra el dataframe en una tabla
        st.write(df)

        # Define las opciones para el select
        opciones = ['Cum. net profit', 'Net profit', 'Gross profit', 'Gross loss', 'Commission',
                    'Cum. max. drawdown', 'Max. drawdown', '% Win', 'Avg. trade', 'Avg. winner', 'Avg. loser', 'Lrg. winner',
                    'Lrg. loser', 'MTR', 'Avg. MAE', 'Avg. MFE', 'Avg. ETD', '% Trade']

        # Crea el cuadro de selección
        variable_eje_y = st.selectbox("Selecciona una variable para el eje Y", opciones)
        
        # Define las opciones para el select de tipo de gráfico
        opciones_graficos = ['Area', 'Barras', 'Puntos']
        
        # Crea el cuadro de selección para el tipo de gráfico
        tipo_grafico = st.selectbox("Selecciona el tipo de gráfico", opciones_graficos)

        # Crea el gráfico de acuerdo al tipo seleccionado
        if tipo_grafico == 'Area':
            fig = px.area(df, x='Period', y=variable_eje_y)
        elif tipo_grafico == 'Barras':
            fig = px.bar(df, x='Period', y=variable_eje_y)  
        else:
            fig = px.scatter(df, x='Period', y=variable_eje_y)

        # Configura el gráfico
        fig.update_layout(
            xaxis=dict(title='Period', tickformat='%Y-%m-%d'), # Formato de fecha en el eje X
            yaxis_title=variable_eje_y,
            title={
                'text': f'{variable_eje_y} vs Period',
                'x': 0.5,
                'xanchor': 'center'
            }
        )
        
        # Muestra el gráfico
        st.plotly_chart(fig)


    st.subheader('Muestra tu resumen operativo')
    uploaded_file = st.file_uploader("Seleccione un archivo CSV o Excel", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
            st.write(df.dropna())
        except Exception as e:
            st.write("Error: ", e)
            
            
with tab5:

    st.subheader('Gamma')

   
