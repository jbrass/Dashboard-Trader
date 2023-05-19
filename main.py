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
import datetime as dt
import ta
from textos import *
from sklearn.preprocessing import StandardScaler
from datetime import timedelta
import datetime
import plotly.express as px
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
tab1, tab2, tab3, tab4, tab5= st.tabs(["Reporte de Mercado", "Estadísticas", "Gráficos/Predicciones", "Opciones 0DTE", "Estadísticas Macroeconómicas"])

with tab1:

    def mostrar_sidebar():
        data_source = st.sidebar.selectbox("Selecciona un fichero de datos", list(renombre.values()))

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

    st.sidebar.title("Fuente de datos")
    df = mostrar_sidebar()





    # Título de la sección
    st.header('Día 16/05/2023')

    # Introducción
    st.write(txt_comentario)
    st.image("./img/16Mayo/premercado.png")
    #ppner imagen
    #st.image("./img/5Mayo/cme-liquidez.jpeg")
    st.image("./img/16Mayo/gamma.png")  
    # Gráfico de precios de la semana
    st.subheader('Niveles importantes')
    st.write(txt_niveles)
    st.write(txt_sentiment)
    st.image("./img/16Mayo/premercado_neto.png")

    
    # Análisis de los principales movimientos del mercado
    st.subheader('Planteamiento y escenarios operativos')
    st.write(txt_esperamos)
    st.image("./img/16Mayo/estructura_premercado.png")
    
    # Volatilidad
    st.subheader('Volatilidad')
    st.write(txt_volatilidad)
    st.image("./img/16Mayo/volatilidad.png") 

            


    st.info(title_esta_semana, icon="ℹ️")
    st.caption(esta_semana1)
    st.caption(esta_semana2)
    st.caption(esta_semana3)
    st.caption(esta_semana4)
    st.caption(esta_semana5)


    
    
with tab2: 
    
    st.subheader("Últimos 2 días")
    # Mostrar la tabla completa al iniciar el programa
    st.dataframe(df.drop("Unnamed: 0", axis=1).tail(2))
    
    st.subheader("Estadísticas generales")
    # Mostrar la tabla completa al iniciar el programa
    st.dataframe(df.drop("Unnamed: 0", axis=1))
    
    st.subheader("Estadísticas por rango de fechas")
    # Crear campos de entrada de fecha
    fecha_inicio = st.date_input("Selecciona una fecha de inicio")
    fecha_fin = st.date_input("Selecciona una fecha de fin")
    df["Date"] = pd.to_datetime(df["Date"])
    


    try:
        # Crear un botón para aplicar el filtro
        if st.button("Aplicar filtro"):
            # Filtrar la base de datos
            df_filtrado = df.drop("Unnamed: 0", axis=1)[(df["Date"].dt.date >= fecha_inicio) & (df["Date"].dt.date <= fecha_fin)]
            # Mostrar la tabla con los datos filtrados
            st.dataframe(df_filtrado)

        st.subheader("Estadísticas descriptivas")
        st.write(df.describe()) 

        st.subheader("Mapa de correlaciones")
        # Utilizar comentarios para explicar el propósito de cada sección de código
        # Crear un gráfico de correlación utilizando la librería específica
        fig = go.Figure(data=go.Heatmap(
            z=df.corr(),
            x=df.drop("Unnamed: 0", axis=1).columns,
            y=df.drop("Unnamed: 0", axis=1).columns))
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error: {e}")





   

with tab3:

    # Selección de la variable a graficar
    selected_vars = st.multiselect("Seleccione uno o múltiple variables", ["Day's High", "Day's Low", "Closing Price", "Volume", "Range in ticks", "VIX Closing Price", "Vwap", "Volume in Vpoc Zone", "Volume Value Area Low", "Volume Value Area High"], default=["Closing Price"])
    # Selección del tipo de gráfico
    tipo_grafico = st.selectbox("Seleccione el tipo de gráfico", ["Linea", "Puntos", "Barras"], key='tipo_grafico', index=0)
    if len(selected_vars) > 0:
        fig = go.Figure()
        
        for variable in selected_vars:
            # Si el tipo de gráfico es línea
            if tipo_grafico == 'Linea':
                fig.add_trace(go.Scatter(x=df['Date'], y=df[variable], mode='lines', name=variable))
            # Si el tipo de gráfico es dispersión
            elif tipo_grafico == 'Puntos':
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
        st.warning("Por favor selecciona alguna variable para graficar")



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
    col_x = st.selectbox('Selecciona una columna para el eje x', df.drop("Unnamed: 0", axis=1).columns)
    col_y = st.selectbox('Selecciona una columna para el eje y', df.drop("Unnamed: 0", axis=1).columns)
    scatter_plot = alt.Chart(df).mark_circle().encode(
        x=col_x,
        y=col_y,
        tooltip=[col_x, col_y]
    ).interactive()
    st.write("### Scatterplot " + col_x + " vs " + col_y)
    st.altair_chart(scatter_plot, use_container_width=True)





    st.subheader("Regresión Linea para hacer predicciones a un día")

    x_name = st.selectbox("Selecciona la variable independiente", ["Closing Price", "VIX Closing Price", "Volume", "Opening", "Day's High", "Day's Low", "Vpoc", "Vwap", "Range in ticks"])

    y_name = st.selectbox("Selecciona la variable a predecir", ["Closing Price", "VIX Closing Price", "Volume", "Opening", "Day's High", "Day's Low", "Vpoc", "Vwap", "Range in ticks"])
    latest_date = df['Date'].max() - timedelta(days=1)
    latest_row = df[df['Date'] == latest_date][x_name]
    if not latest_row.empty:
        predict_value = st.number_input("Último valor de la variable independiente en ayer o ingresa los datos que deseas hacer una relación y con ello tendrás una predicción(" + x_name + "):", value=latest_row.values[0])
    else:
        predict_value = st.number_input("Último valor de la variable independiente en ayer o ingresa los datos que deseas hacer una relación y con ello tendrás una predicción(" + x_name + "):")


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

    st.write("La predicción para la variable: ", variable_dependiente, "es", prediction[0][0])









with tab4:

    # Mostrar la tabla completa al iniciar el programa
    st.subheader('Opciones con expiración diarias 0DTE')
    st.caption('Las opciones sobre acciones son importantes porque ofrecen oportunidades comerciales rápidas y pueden influir en el mercado de futuros. Los operadores de futuros deben estar atentos a estas opciones para aprovechar las oportunidades y minimizar los riesgos.')
    
    
    # Select para elegir el archivo
    archivo_seleccionado = st.selectbox(
        "Seleccione el activo a cargar: ",
        ["spx_quotedata.csv", "ndx_quotedata.csv", "aapl_quotedata.csv", "goog_quotedata.csv", "meta_quotedata.csv", "msft_quotedata.csv", "amzn_quotedata.csv", "vix_quotedata.csv", "spy_quotedata.csv", "tsla_quotedata.csv", "ko_quotedata.csv"]
    )

    # Cargar el archivo seleccionado
    if archivo_seleccionado == "spx_quotedata.csv":
        df = pd.DataFrame(df_volatilidad)
    elif archivo_seleccionado == "ndx_quotedata.csv":
        df = pd.DataFrame(df_volatilidad_nq)
        
    elif archivo_seleccionado == "aapl_quotedata.csv":
        df = pd.DataFrame(data_apple)
        
    elif archivo_seleccionado == "goog_quotedata.csv":
        df = pd.DataFrame(data_goog)
        
    elif archivo_seleccionado == "meta_quotedata.csv":
        df = pd.DataFrame(data_meta)

    elif archivo_seleccionado == "msft_quotedata.csv":
        df = pd.DataFrame(data_msft)

    elif archivo_seleccionado == "amzn_quotedata.csv":
        df = pd.DataFrame(data_amzn)
        
    elif archivo_seleccionado == "vix_quotedata.csv":
        df = pd.DataFrame(df_volatilidad_vix)
        
    elif archivo_seleccionado == "ko_quotedata.csv":
        df = pd.DataFrame(data_otros)
        
    elif archivo_seleccionado == "spy_quotedata.csv":
        df = pd.DataFrame(data_spy)
        
    elif archivo_seleccionado == "tsla_quotedata.csv":
        df = pd.DataFrame(df_tesla)                                        
    else:
        st.dataframe(df)

    # Crear lista de fechas únicas en la columna "Expiration Date"
    fechas_unicas = df['Expiration Date'].unique()

    # Selectbox para seleccionar la fecha de vencimiento
    fecha_seleccionada = st.selectbox(
        "Seleccione la fecha de vencimiento: ",
        fechas_unicas
    )

    # Filtrar el DataFrame para seleccionar solo las filas que corresponden a la fecha de vencimiento seleccionada
    df_filtrado = df[df['Expiration Date'] == fecha_seleccionada]

    # Obtener todos los valores de Strike en el DataFrame filtrado
    strikes = df_filtrado['Strike'].unique()

    # Crear un nuevo DataFrame con todos los valores de Strike y reindexar el DataFrame filtrado
    df_strikes = pd.DataFrame({'Strike': strikes})
    df_filtrado = pd.merge(df_filtrado, df_strikes, on='Strike', how='right').fillna(0)

    # Selección de la variable a graficar
    selected_vars = st.multiselect(
        "Selecciones la variable a graficar",
        [
            'Calls', 'Calls Last Sale', 'Calls Net','Calls Bid', 'Calls Ask','Calls Volume', 'Calls IV','Calls Delta',
            'Calls Gamma', 'Calls Open Interest', 'Strike', 'Puts', 'Puts Last Sale', 'Puts Net', 'Puts Bid', 'Puts Ask', 'Puts Volume',
            'Puts IV','Puts Delta', 'Puts Gamma', 'Puts Open Interest'
        ],
        default=["Calls Volume","Puts Volume", "Calls Open Interest", "Puts Open Interest"]
    )

    # Selección del tipo de gráfico
    tipo_grafico2 = st.selectbox(
        "Seleccione el tipo de gráfico",
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
            yaxis_title= variable,
            #barmode='relative',
            barmode='overlay',
            xaxis=dict(
                tickmode='linear',
                tick0=df_filtrado['Strike'].min(),
                dtick=5
            )
        )

        # Muestra el gráfico en la página
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Por favor seleccione al menos una variable")


 
 
    # Crear un DataFrame con los datos de interés
    df_top = df_filtrado[['Strike', 'Calls Volume', 'Calls Open Interest', 'Puts Volume', 'Puts Open Interest']]
    df_top['Nuevo Strike'] = df_top['Strike'] + 15 # Agregar la nueva columna "Nuevo Strike" sumando 30 a cada fila
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


    

    

 
    



    # Transformar Expiration Date a formato fecha
    data['Expiration Date'] = pd.to_datetime(data['Expiration Date'], format='%a %b %d %Y')

    # Agregar una columna para el total de deltas en cada Expiration Date
    data['Total Delta'] = data['Calls Delta'] + data['Puts Delta']

    # Crear el gráfico con Plotly Express
    fig = px.bar(data, x='Expiration Date', y='Total Delta',
                color='Total Delta',
                color_discrete_sequence=['red', 'green'],
                labels={'Total Delta': 'Deltas'},
                title='Delta Diario')

    # Definir los colores para valores positivos y negativos
    fig.update_traces(marker=dict(color=data['Total Delta'].apply(lambda x: 'green' if x >= 0 else 'red')))

    # Añadir línea horizontal en y=0
    fig.add_shape(type='line', x0=min(data['Expiration Date']), y0=0, x1=max(data['Expiration Date']), y1=0,
                line=dict(color='black', width=1))

    # Configurar el tooltip para mostrar la fecha y el valor de delta
    fig.update_traces(hovertemplate='<b>%{x|%Y-%m-%d}</b><br>%{y:.0f} Deltas')



    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)


    st.subheader('Squeezmetric')
    # Seleccionar todas las columnas numéricas excepto date
    numeric_cols = ['price', 'dix', 'gex']
    df_numeric = df_squeeze[numeric_cols]

    # Crear figura con 3 subplots
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True)


    col1, col2 = st.columns(2)

    with col1:
        st.info('**Dark Index (DIX)**, es una medida ponderada en dólares del Dark Pool Indicator (DPI) de los componentes del S&P 500. Cuando el DIX es más alto, el sentimiento del mercado en los fondos oscuros es generalmente más alcista. Cuando el DIX es más bajo, es más bajista o incierto.', icon="ℹ️")
        

    with col2:
        st.info('**Gamma Exposure (GEX)**, es una medida denominada en dólares de las obligaciones de cobertura de los creadores de mercado de opciones. Cuando GEX es alto, el mercado de opciones implica que la volatilidad será baja. Cuando GEX es bajo, la volatilidad es alta y, aunque esperamos un mercado agitado, es poco probable que se produzcan más pérdidas.', icon="ℹ️")

   
   
    # Agregar cada gráfico de línea a la figura
    fig.add_trace(go.Scatter(x=df_squeeze['date'], y=df_squeeze['price'], name='SP500'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_squeeze['date'], y=df_squeeze['dix'], name='Dark Index'), row=2, col=1)
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
    st.plotly_chart(fig, use_container_width=True)



    
    

    st.subheader('Volumen Call & Put por vencimientos')
    
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
        title='Volumen de opciones de venta por fecha de vencimiento'
    ).interactive()
    



    st.subheader('Interés abierto de opciones call y put por precio de ejercicio')
    
    # filtrar los datos para incluir solo la fecha de vencimiento más reciente
    latest_expiry = data['Expiration Date'].max()
    data = data[data['Expiration Date'] == latest_expiry]

    # crear el gráfico
    chart = alt.Chart(data).mark_line().encode(
        x='Strike',
        y='Calls Open Interest:Q',
        color=alt.value('#5b8ff9')
    ).properties(
        width=600,
        height=400
    )

    chart += alt.Chart(data).mark_line().encode(
        x='Strike',
        y='Puts Open Interest:Q',
        color=alt.value('#ff6b81')
    ).interactive()

    # mostrar el gráfico
    chart
        
       




    col1, col2 = st.columns(2)

    with col1:
        # Crear un gráfico de barras para mostrar las columnas de "Calls Volume" y "Puts Volume" para cada "Strike"
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=df_top['Strike'], y=df_top['Calls Volume'], name='Calls Volume'))
        fig2.add_trace(go.Bar(x=df_top['Strike'], y=df_top['Puts Volume'], name='Puts Volume'))

        # Personaliza los títulos y ejes del gráfico
        fig2.update_layout(
            title='Volumen de opciones call y put para los 15 strikes principales',
            xaxis_title='Strike',
            yaxis_title='Volume',
            barmode='stack'
        )

        # Muestra el gráfico en la página
        st.plotly_chart(fig2)



    with col2:
        # Crear un gráfico de barras para mostrar las columnas de "Calls Open Interest" y "Puts Open Interest" para cada "Strike"
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=df_top['Strike'], y=df_top['Calls Open Interest'], name='Calls Open Interest'))
        fig3.add_trace(go.Bar(x=df_top['Strike'], y=df_top['Puts Open Interest'], name='Puts Open Interest'))

        # Personaliza los títulos y ejes del gráfico
        fig3.update_layout(
            title='Interés abierto de opciones call y put para los 15 strikes principales',
            xaxis_title='Strike',
            yaxis_title='Open Interest',
            #bar mode stack sirve para que se apilen las barras y no se superpongan
            barmode='stack'
            
            
        )

        # Muestra el gráfico en la página
        st.plotly_chart(fig3)


    col1, col2 = st.columns(2)
        
    with col1:
        # Crear un gráfico de barras para mostrar las columnas de "Puts Net" y "Calls Net" para cada "Strike"
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(x=data['Strike'], y=data['Puts Net'], name='Puts Net'))
        fig4.add_trace(go.Bar(x=data['Strike'], y=data['Calls Net'], name='Calls Net'))
        
        # Personaliza los títulos y ejes del gráfico
        fig4.update_layout(
            title='Neto de opciones call y put para los 15 strikes principales',
            xaxis_title='Strike',
            yaxis_title='Puts Net',
            barmode='stack'
            
        )
        
        # Muestra el gráfico en la página
        st.plotly_chart(fig4)
        
        
    with col2:
         
        # Crear un gráfico de barras para mostrar las columnas de "Puts Net" y "Calls Net" para cada "Strike"
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(x=data['Strike'], y=data['Puts Gamma'], name='Puts Gamma'))
        fig5.add_trace(go.Bar(x=data['Strike'], y=data['Calls Gamma'], name='Calls GAmma'))
        
        # Personaliza los títulos y ejes del gráfico
        fig5.update_layout(
            title='Neto de opciones call y put para los 15 strikes principales',
            xaxis_title='Strike',
            yaxis_title='Puts Gamma',
            barmode='stack'
            
        )
        
        # Muestra el gráfico en la página
        st.plotly_chart(fig5)




    col1, col2 = st.columns(2)
    
    
    with col1:

        # Obtener los datos del dataframe df_acciones
        # Supongamos que el dataframe contiene las columnas ['Expiration Date', 'Calls Net', 'Puts Net']

        # Crear un nuevo dataframe para los datos del gráfico
        df_chart = pd.DataFrame({
            'Expiration Date': df_acciones['Expiration Date'],
            'Calls Net': df_acciones['Calls Net'],
            'Puts Net': df_acciones['Puts Net']
        })

        # Establecer la columna 'Expiration Date' como índice
        df_chart.set_index('Expiration Date', inplace=True)

        # Ordenar el dataframe por Calls Net descendente
        df_chart = df_chart.sort_values('Calls Net', ascending=False)

        # Limitar el número de acciones a mostrar en el gráfico
        num_acciones_mostrar = 10
        df_chart = df_chart.head(num_acciones_mostrar)

        # Título del gráfico
        titulo = "Neto de Principales Acciones: AMZN, AAPL, GOOG, MSFT, META..."

        # Crear un gráfico de barras
        fig6 = go.Figure()
        fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Net'], name='Calls Net', marker=dict(color='green')))
        fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Net'], name='Puts Net', marker=dict(color='red')))

        # Personalizar el diseño del gráfico
        fig6.update_layout(
            title=titulo,
            xaxis_title='Expiration Date',
            yaxis_title='Neto',
            barmode='group'
        )

        # Mostrar el gráfico en la página web
        st.plotly_chart(fig6, container_width=1000, container_height=500)

    with col2:
        

        # Obtener los datos del dataframe df_acciones
        # Supongamos que el dataframe contiene las columnas ['Expiration Date', 'Calls Volume', 'Puts Volume']

        # Crear un nuevo dataframe para los datos del gráfico
        df_chart = pd.DataFrame({
            'Expiration Date': df_acciones['Expiration Date'],
            'Calls Volume': df_acciones['Calls Volume'],
            'Puts Volume': df_acciones['Puts Volume']
        })

        # Establecer la columna 'Expiration Date' como índice
        df_chart.set_index('Expiration Date', inplace=True)

        # Ordenar el dataframe por Calls Net descendente
        df_chart = df_chart.sort_values('Calls Volume', ascending=False)

        # Limitar el número de acciones a mostrar en el gráfico
        num_acciones_mostrar = 10
        df_chart = df_chart.head(num_acciones_mostrar)

        # Título del gráfico
        titulo = "Volumen de los principales índices: SPX, SPY, NDX"

        # Crear un gráfico de barras
        fig6 = go.Figure()
        fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Volume'], name='Calls Volume'))
        fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Volume'], name='Puts Volume'))

        # Personalizar el diseño del gráfico
        fig6.update_layout(
            title=titulo,
            xaxis_title='Expiration Date',
            yaxis_title='Volume',
            barmode='group'
        )

        # Mostrar el gráfico en la página web
        st.plotly_chart(fig6, container_width=1000, container_height=500)





    col1, col2 = st.columns(2)
    
    
    with col1:

        #INDICES
        # Obtener los datos del dataframe df_acciones
        # Supongamos que el dataframe contiene las columnas ['Expiration Date', 'Calls Net', 'Puts Net']

        # Crear un nuevo dataframe para los datos del gráfico
        df_chart = pd.DataFrame({
            'Expiration Date': df_index['Expiration Date'],
            'Calls Net': df_index['Calls Net'],
            'Puts Net': df_index['Puts Net']
        })

        # Establecer la columna 'Expiration Date' como índice
        df_chart.set_index('Expiration Date', inplace=True)

        # Ordenar el dataframe por Calls Net descendente
        df_chart = df_chart.sort_values('Calls Net', ascending=False)

        # Limitar el número de acciones a mostrar en el gráfico
        num_acciones_mostrar = 10
        df_chart = df_chart.head(num_acciones_mostrar)

        # Título del gráfico
        titulo = "Neto de Principales Índices: SPX, SPY, NDX"

        # Crear un gráfico de barras
        fig8 = go.Figure()
        fig8.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Net'], name='Calls Net', marker=dict(color='green')))
        fig8.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Net'], name='Puts Net', marker=dict(color='red')))

        # Personalizar el diseño del gráfico
        fig8.update_layout(
            title=titulo,
            xaxis_title='Expiration Date',
            yaxis_title='Neto',
            barmode='group'
        )

        # Mostrar el gráfico en la página web
        st.plotly_chart(fig8, container_width=1000, container_height=500)

    with col2:
        

        # Obtener los datos del dataframe df_acciones
        # Supongamos que el dataframe contiene las columnas ['Expiration Date', 'Calls Volume', 'Puts Volume']

        # Crear un nuevo dataframe para los datos del gráfico
        df_chart = pd.DataFrame({
            'Expiration Date': df_index['Expiration Date'],
            'Calls Volume': df_index['Calls Volume'],
            'Puts Volume': df_index['Puts Volume']
        })

        # Establecer la columna 'Expiration Date' como índice
        df_chart.set_index('Expiration Date', inplace=True)

        # Ordenar el dataframe por Calls Net descendente
        df_chart = df_chart.sort_values('Calls Volume', ascending=False)

        # Limitar el número de acciones a mostrar en el gráfico
        num_acciones_mostrar = 10
        df_chart = df_chart.head(num_acciones_mostrar)

        # Título del gráfico
        titulo = "Volumen de las Principales Acciones: AMZN, AAPL, GOOG, MSFT, META..."

        # Crear un gráfico de barras
        fig9 = go.Figure()
        fig9.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Volume'], name='Calls Volume'))
        fig9.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Volume'], name='Puts Volume'))

        # Personalizar el diseño del gráfico
        fig9.update_layout(
            title=titulo,
            xaxis_title='Expiration Date',
            yaxis_title='Volume',
            barmode='group'
        )

        # Mostrar el gráfico en la página web
        st.plotly_chart(fig9, container_width=1000, container_height=500)



       
        


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
        






