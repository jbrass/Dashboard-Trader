# Importar las librerías necesarias
from src.datos import *
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
from sklearn.linear_model import LinearRegression
from plotly.subplots import make_subplots

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
tab1, tab2, tab3, tab4, tab5= st.tabs(["Markets Report", "Statistics", "Charts/Forecast", "Options 0DTE", "Statics Macro"])

with tab1:

    def mostrar_sidebar():
        data_source = st.sidebar.selectbox("Select a data source", list(renombre.values()))

        for archivo, nombre_amigable in renombre.items():
            if data_source == nombre_amigable:
                if archivo == "./Operativa/processed/Diarios-ES.csv":
                    df = df_diarios_ES
                elif archivo == "./Operativa/processed/Diarios-NQ.csv":
                    df = df_diarios_NQ
                elif archivo == "./Operativa/processed/Semanal-ES.csv":
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

    # Mostrar la tabla completa al iniciar el programa
    st.subheader('Options 0DTE')
    st.caption('Options on stock are important because they offer fast trading opportunities and can influence the futures market. Futures traders should keep an eye on these options to take advantage of opportunities and minimize risks.')
    
    
    # Select para elegir el archivo
    archivo_seleccionado = st.selectbox(
        "Select a file",
        ["spx_quotedata.csv", "ndx_quotedata.csv", "vix_quotedata.csv"]
    )

    # Cargar el archivo seleccionado
    if archivo_seleccionado == "spx_quotedata.csv":
        df = pd.DataFrame(df_volatilidad)
    elif archivo_seleccionado == "ndx_quotedata.csv":
        df = pd.DataFrame(df_volatilidad_nq)
    else:
        df = pd.DataFrame(df_volatilidad_vix)
    
    st.dataframe(df)

    # Crear lista de fechas únicas en la columna "Expiration Date"
    fechas_unicas = df['Expiration Date'].unique()

    # Selectbox para seleccionar la fecha de vencimiento
    fecha_seleccionada = st.selectbox(
        "Select expiration date",
        fechas_unicas
    )

    # Filtrar el DataFrame para seleccionar solo las filas que corresponden a la fecha de vencimiento seleccionada
    df_filtrado = df[df['Expiration Date'] == fecha_seleccionada]

    # Selección de la variable a graficar
    selected_vars = st.multiselect(
        "Select variables to graph",
        [
            'Calls', 'Calls Last Sale', 'Calls Net','Calls Bid', 'Calls Ask','Calls Volume', 'Calls IV','Calls Delta',
            'Calls Gamma', 'Calls Open Interest', 'Strike', 'Puts', 'Puts Net', 'Puts Bid', 'Puts Ask', 'Puts Volume',
            'Puts IV','Puts Delta', 'Puts Gamma', 'Puts Open Interest'
        ],
        default=["Calls Volume","Puts Volume"]
    )

    # Selección del tipo de gráfico
    tipo_grafico2 = st.selectbox(
        "Select chart type",
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
            title=f'Chart of {", ".join(selected_vars)} to date {fecha_seleccionada}',
            xaxis_title= 'Strike',
            yaxis_title= variable
        )

        # Muestra el gráfico en la página
        st.plotly_chart(fig)
    else:
        st.warning("Please select at least one input")
 
 
 
 
    # Crear un DataFrame con los datos de interés
    df_top = df_filtrado[['Strike', 'Calls Volume', 'Calls Open Interest', 'Puts Volume', 'Puts Open Interest']]
    df_top['Nuevo Strike'] = df_top['Strike'] + 30 # Agregar la nueva columna "Nuevo Strike" sumando 30 a cada fila
    df_top = df_top.sort_values(by=['Calls Volume', 'Calls Open Interest', 'Puts Volume', 'Puts Open Interest'], ascending=False)
    df_top = df_top.head(15)

    # Mostrar las dos tablas en dos columnas
    col1, col2 = st.columns(2)

    # En la primera columna, mostrar la tabla original con la columna "Strike"
    with col1:
        st.write("SPX")
        st.dataframe(df_top[['Strike', 'Calls Volume', 'Calls Open Interest', 'Puts Volume', 'Puts Open Interest']])

    # En la segunda columna, mostrar la tabla actualizada con la nueva columna "Nuevo Strike"
    with col2:
        st.write("ES")
        st.dataframe(df_top[['Nuevo Strike', 'Calls Volume', 'Calls Open Interest', 'Puts Volume', 'Puts Open Interest']])


    

    

 
    
    st.subheader('Squeezmetric')
    # Seleccionar todas las columnas numéricas excepto date
    numeric_cols = ['price', 'dix', 'gex']
    df_numeric = df_squeeze[numeric_cols]

    # Crear figura con 3 subplots
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True)


    col1, col2 = st.columns(2)

    with col1:
        st.info('**Dark Index (DIX)**, is a dollar-weighted measure of the Dark Pool Indicator (DPI) of the S&P 500 components. When the DIX is higher, market sentiment in dark pools is generally more bullish. When the DIX is lower, it is more bearish or uncertain.', icon="ℹ️")
        

    with col2:
        st.info('**Gamma Exposure (GEX)**, is a dollar-denominated measure of option market-makers hedging obligations. When GEX is high, the option market is implying that volatility will be low. When GEX is low, volatility is high, and while we expect a choppy market, further losses are unlikely.', icon="ℹ️")

   
   
    # Agregar cada gráfico de línea a la figura
    fig.add_trace(go.Scatter(x=df_squeeze['date'], y=df_squeeze['price'], name='SP500'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_squeeze['date'], y=df_squeeze['dix'], name='Dark Index', hovertemplate='hola'), row=2, col=1)
    fig.add_trace(go.Scatter(x=df_squeeze['date'], y=df_squeeze['gex'], name='Gamma Exposure'), row=3, col=1)

    # Personalizar la figura
    fig.update_layout(
        height=800,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Mostrar la figura utilizando st.plotly_chart()
    st.plotly_chart(fig)



 
    # Agregar una columna para el total de deltas en cada Expiration Date
    data['Total Delta'] = data['Calls Delta'] + data['Puts Delta']

    #Transformar Expiration Date a formato fecha
    data['Expiration Date'] = pd.to_datetime(data['Expiration Date'], format='%a %b %d %Y')

    # Crear un gráfico de barras con los datos de Total Delta vs Expiration Date
    chart = alt.Chart(data).mark_bar(width=15).encode(
        x=alt.X('Expiration Date', sort=None),
        y=alt.Y('Total Delta', axis=alt.Axis(title='Deltas', format='.0f')),
        color=alt.condition(
            alt.datum['Total Delta'] > 0,
            alt.value("green"),  # cuando Total Delta es mayor que 0, la barra será verde
            alt.value("red")  # cuando Total Delta es menor que 0, la barra será roja
        )
    ).properties(
        width=800,
        height=400,
        title='DEALERS MARKET DIARY'
    )


    # Agregar una línea horizontal para mostrar el nivel 0 de Delta
    hline = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(color='black', strokeWidth=1).encode(y='y')

    # Configurar las opciones del gráfico y mostrarlo en Streamlit
    st.altair_chart(chart + hline, use_container_width=True)


    st.info('The dealers current approximate total delta exposure for all expirations is a crucial metric to track. When calls are greater than zero, it indicates that the dealers are short calls, while customers are long calls. On the other hand, when puts are less than zero, it means dealers are short puts, while customers are long puts, implying they are well-hedged. The green and red lines represent the average short-term deltas, which are important indicators of market trends. Therefore, keeping an eye on the dealers delta exposure is essential to make informed trading decisions and minimize risks.', icon="ℹ️")





    col1, col2 = st.columns(2)
    
    
    with col1:
        st.subheader('Call & Put volume by maturities')
        
        # gráfico 1
        alt.Chart(df).mark_circle(size=50).encode(
            x='Calls Volume:Q',
            y='Puts Volume:Q',
            color=alt.Color('Expiration Date:N', scale=alt.Scale(scheme='category10')),
            tooltip=['Expiration Date:N']
        ).properties(
            title='Call volume vs put options'
        ).interactive()
                # gráfico 2
        alt.Chart(df).mark_bar().encode(
            x=alt.X('Expiration Date:N', axis=alt.Axis(title=None)),
            y=alt.Y('Calls Volume:Q', axis=alt.Axis(title='Volumen')),
            color=alt.value('steelblue')
        ).properties(
            title='Call volume by due date'
        ).interactive() | alt.Chart(df).mark_bar().encode(
            x=alt.X('Expiration Date:N', axis=alt.Axis(title=None)),
            y=alt.Y('Puts Volume:Q', axis=alt.Axis(title='Volumen')),
            color=alt.value('orange')
        ).properties(
            title='Put Option Volume by Expiration Date'
        ).interactive()


    with col2:

        st.subheader('Open interest of calls and put options by strike price')
        
        # filtrar los datos para incluir solo la fecha de vencimiento más reciente
        latest_expiry = data['Expiration Date'].max()
        data = data[data['Expiration Date'] == latest_expiry]

        # crear el gráfico
        chart = alt.Chart(data).mark_line().encode(
            x='Strike',
            y='Calls Open Interest:Q',
            color=alt.value('#5b8ff9')
        )

        chart += alt.Chart(data).mark_line().encode(
            x='Strike',
            y='Puts Open Interest:Q',
            color=alt.value('#ff6b81')
        ).interactive()

        # mostrar el gráfico
        chart
        
    

    

        
        
        

        
    

with tab5:


    # Dividir en dos columnas
    col1, col2, col3, col4,  = st.columns(4)

    # Tabla de inflación en la primera columna
    with col1:
        st.subheader('CPI')
        st.write(inflacion_df.tail(10))




    # Gráfico de tipos de interés en la segunda columna
    with col2:
        st.subheader('Interest Rate')
        st.write(tipos_interes_df.tail(10))
        
    # Gráfico de tipos de interés en la segunda columna
    with col3:
        st.subheader('M2')
        st.write(m2_df.tail(10))

    # Gráfico de tipos de interés en la segunda columna
    with col4:
        st.subheader('Unemployment Rate')
        st.write(empleo_df.tail(10))
        
        
    # Dividir en dos columnas
    col1, col2, col3, col4,  = st.columns(4)

    # Tabla de inflación en la primera columna
    with col1:
        st.subheader('Dollar to Euro')
        st.write(dolar_df.tail(10))

    # Gráfico de tipos de interés en la segunda columna
    with col2:
        st.subheader('Emerging Markets')
        st.write(dolaresEmergentes_df.tail(10))
        






