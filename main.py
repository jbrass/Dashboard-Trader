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
tab1, tab2, tab3, tab4, tab5= st.tabs(["Markets Report", "Statistics", "Charts/Forecast", "Volatilidad", "Volatility Calculator stocks"])

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

    # Mostrar tabla de datos con 2 inputs
    # Mostrar gráfico de dispersión de dos columnas
    col_x = st.selectbox('Select a column for the X axis', df.drop("Unnamed: 0", axis=1).columns)
    col_y = st.selectbox('Select a column for the Y axis', df.drop("Unnamed: 0", axis=1).columns)
    scatter_plot = alt.Chart(df).mark_circle().encode(
        x=col_x,
        y=col_y,
        tooltip=[col_x, col_y]
    ).interactive()
    st.write("### Scatterplot " + col_x + " vs " + col_y)
    st.altair_chart(scatter_plot, use_container_width=True)


    st.subheader("Linear Regression Model to make different predictions to one day")

    x_name = st.selectbox("Select the independent input", ["Closing Price", "VIX Closing Price", "Volume", "Opening", "Day's High", "Day's Low", "Vpoc", "Vwap", "Range in ticks"])

    y_name = st.selectbox("Select the input to predict", ["Closing Price", "VIX Closing Price", "Volume", "Opening", "Day's High", "Day's Low", "Vpoc", "Vwap", "Range in ticks"])
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

    # Select para elegir el archivo
    archivo_seleccionado = st.selectbox(
        "Seleccionar archivo",
        ["spx_quotedata.csv", "ndx_quotedata.csv"]
    )

    # Cargar el archivo seleccionado
    if archivo_seleccionado == "spx_quotedata.csv":
        df = pd.DataFrame(df_volatilidad)
    else:
        df = pd.DataFrame(df_volatilidad_nq)

    # Mostrar la tabla completa al iniciar el programa
    st.subheader('Volatilidad')
    st.dataframe(df)

    # Crear lista de fechas únicas en la columna "Expiration Date"
    fechas_unicas = df['Expiration Date'].unique()

    # Selectbox para seleccionar la fecha de vencimiento
    fecha_seleccionada = st.selectbox(
        "Seleccionar fecha de vencimiento",
        fechas_unicas
    )

    # Filtrar el DataFrame para seleccionar solo las filas que corresponden a la fecha de vencimiento seleccionada
    df_filtrado = df[df['Expiration Date'] == fecha_seleccionada]

    # Selección de la variable a graficar
    selected_vars = st.multiselect(
        "Seleccionar variables a graficar",
        [
            'Calls', 'Calls Last Sale', 'Calls Net','Calls Bid', 'Calls Ask','Calls Volume', 'Calls IV','Calls Delta',
            'Calls Gamma', 'Calls Open Interest', 'Strike', 'Puts', 'Puts Net', 'Puts Bid', 'Puts Ask', 'Puts Volume',
            'Puts IV','Puts Delta', 'Puts Gamma', 'Puts Open Interest'
        ],
        default=["Calls Volume","Puts Volume"]
    )

    # Selección del tipo de gráfico
    tipo_grafico2 = st.selectbox(
        "Seleccionar tipo de gráfico",
        ["Bars", "Scatter"],
        key='tipo_grafico2',
        index=0
    )

    if len(selected_vars) > 0:
        fig = go.Figure()

        for variable in selected_vars:
            # Si el tipo de gráfico es línea
            if tipo_grafico2 == 'Bars':
                fig.add_trace(go.Bar(x=df_filtrado['Strike'], y=df_filtrado[variable],  name=variable))
            else:
                fig.add_trace(go.Scatter(x=df_filtrado['Strike'], y=df_filtrado[variable],  mode='markers', name=variable))

        # Personaliza los títulos y ejes del gráfico
        fig.update_layout(
            title=f'Gráfico de {", ".join(selected_vars)} para la fecha {fecha_seleccionada}',
            xaxis_title= 'Strike',
            yaxis_title= variable
        )

        # Muestra el gráfico en la página
        st.plotly_chart(fig)
    else:
        st.warning("Por favor seleccionar al menos una variable")
        
        
        
with tab5:
    
    st.subheader("Volatility Calculator stocks")

    ticker = st.text_input("Please enter a ticker symbol", value="AAPL", max_chars=5, key="ticker")

    # Descargar los datos más recientes del activo
    stock_data = yf.download(ticker, period="max")
    stock_data.dropna(inplace=True)
    stock_data.reset_index(inplace=True)

    # Calcular el promedio móvil de 21 días y la volatilidad implícita
    stock_data["MA"] = stock_data["Adj Close"].rolling(window=21).mean()
    stock_data["volatility"] = ta.volatility.BollingerBands(stock_data["Adj Close"]).bollinger_mavg()

    # Crear un gráfico con los datos históricos del activo
    fig = go.Figure(data=[go.Candlestick(x=stock_data['Date'],
                open=stock_data['Open'],
                high=stock_data['High'],
                low=stock_data['Low'],
                close=stock_data['Adj Close'])])
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data["MA"], mode="lines", name="21 Day Moving Average"))
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data["volatility"], mode="lines", name="Bollinger Bands"))
    fig.update_layout(title=f"{ticker} Historical Data with Bollinger Bands and 21-day Moving Average",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    template="plotly_dark")
    st.plotly_chart(fig)

    # Crear un gráfico de la distribución de retornos
    log_returns = np.log(stock_data["Adj Close"]).diff().dropna()
    fig2 = go.Figure(data=[go.Histogram(x=log_returns, nbinsx=30)])
    fig2.update_layout(title=f"{ticker} Returns Distribution",
                    xaxis_title="Log Returns",
                    yaxis_title="Frequency",
                    template="plotly_dark")
    st.plotly_chart(fig2)

    # Calcular la volatilidad implícita
    annual_volatility = log_returns.std() * np.sqrt(252)
    st.write(f"Annualized Volatility: {round(annual_volatility*100, 2)}%")

    # Calcular los percentiles de los retornos
    percentiles = [1, 5, 10]
    values = [f"{round(np.percentile(log_returns, p), 4)}" for p in percentiles]
    result = dict(zip(percentiles, values))
    st.write(f"Percentiles of Log Returns (1%, 5%, 10%): {result}")
