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
                initial_sidebar_state="expanded"                
                )
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
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(["Reporte de Mercado", "Estadísticas", "Gráficos/Predicciones", "Opciones 0DTE", "Charts Índices", "Charts Acciones", "Meme Stocks", "Gamma", "Estadísticas Macroeconómicas"])

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
    st.header('Día 30/05/2023')

    # Introducción
    st.write(txt_comentario)
    st.image("./img/30Mayo/premercado.png")
    #ppner imagen
    #st.image("./img/5Mayo/cme-liquidez.jpeg")
    st.image("./img/30Mayo/gamma.png")  
    # Gráfico de precios de la semana
    st.subheader('Niveles importantes')
    st.write(txt_niveles)
    st.write(txt_sentiment)
    st.image("./img/30Mayo/premercado_neto.png")
    st.image("./img/30Mayo/premercado_delta.png")
    
    # Análisis de los principales movimientos del mercado
    st.subheader('Planteamiento y escenarios operativos')
    st.write(txt_esperamos)
    st.image("./img/30Mayo/estructura.png")
    
    # Volatilidad
    st.subheader('Volatilidad')
    st.write(txt_volatilidad)
    st.image("./img/30Mayo/volatilidad.png") 




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
        # Excluir columnas no numéricas
        numeric_columns = df.select_dtypes(include=[float, int]).columns
        df_numeric2 = df[numeric_columns]
        df_numeric2 = df_numeric2.drop("Unnamed: 0", axis=1)
        st.write(df_numeric2.describe().round(2))

        st.subheader("HeatMap")
        # Excluir columnas no numéricas
        numeric_columns = df.select_dtypes(include=[float, int]).columns
        df_numeric = df[numeric_columns]
        # Eliminar la columna "Unnamed:"
        df_numeric = df_numeric.drop("Unnamed: 0", axis=1)
        # Calcular la matriz de correlaciones
        correlation_matrix = df_numeric.corr().reset_index().melt('index')

        # Crear el heatmap con Altair
        heatmap = alt.Chart(correlation_matrix).mark_rect().encode(
            x='index:O',
            y='variable:O',
            color='value:Q'
        ).properties(
            width=1000,
            height=800,
            title='Mapa de correlaciones'
        )

        # Mostrar el gráfico en Streamlit
        st.altair_chart(heatmap)


    except Exception as e:
        st.error(f"Error: {e}")







with tab3:

    # Selección de la variable a graficar
    selected_vars = st.multiselect("Seleccione uno o múltiple variables", ["Day's High", "Day's Low", "Closing Price", "Volume", "Range in ticks", "VIX Closing Price", "Vwap", "Vpoc", "Volume in Vpoc Zone", "Volume Value Area Low", "Volume Value Area High", "vix_0dte"], default=["Closing Price"])
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



    @st.cache_data
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
    
    ticker_input = st.text_input("Ingrese el nombre, ticker del Índice o Acción:","SPX")

    archivo_seleccionado = None

    # Buscar el archivo correspondiente basado en el ticker_input
    for archivo, datos in data_files.items():
        if ticker_input.lower() in archivo.lower():
            archivo_seleccionado = archivo
            df = pd.DataFrame(datos)
            break

    if archivo_seleccionado is None:
        st.write("Ticker o acción no encontrado")
        st.stop()

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
            barmode= 'stack',
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
    df_top = df_filtrado[['Strike', 'Calls Volume', 'Calls Open Interest', 'Puts Volume', 'Puts Open Interest', 'Puts Net', 'Calls Net', 'Puts Gamma', 'Calls Gamma']]

    if archivo_seleccionado not in ["spx_quotedata.csv", "spy_quotedata.csv"]:
        st.markdown(f"**{archivo_seleccionado.replace('_quotedata.csv', '').upper()}**")
        st.dataframe(df_top)
    else:
        if archivo_seleccionado == "spx_quotedata.csv":
            df_top['Price'] = df_top['Strike'] + 10
        else:  # archivo_seleccionado == "spy_quotedata.csv"
            df_top['Price'] = df_top['Strike'] * 10

        df_top = df_top.sort_values(by=['Calls Volume', 'Calls Open Interest', 'Puts Volume', 'Puts Open Interest'], ascending=False)
        df_top = df_top.head(15)

        # Mostrar las dos tablas en dos columnas
        col1, col2 = st.columns(2)

        # En la primera columna, mostrar la tabla original con la columna "Strike"
        with col1:
            if ticker_input.upper() not in ["SPX", "SPY"]:
                st.dataframe(df_top[['Calls Volume', 'Calls Open Interest', 'Puts Volume', 'Puts Open Interest']], width=0)
            else:
                st.markdown(f"**{ticker_input.upper()}**")
                st.dataframe(df_top[['Strike', 'Calls Volume', 'Calls Open Interest', 'Puts Volume', 'Puts Open Interest']])

        # En la segunda columna, mostrar la tabla actualizada con la nueva columna "Nuevo Strike"
        with col2:
            st.write("**Futuros E-Mini S&P 500**")
            st.dataframe(df_top[['Price', 'Calls Volume', 'Calls Open Interest', 'Puts Volume', 'Puts Open Interest']])



    



    # Transformar Expiration Date a formato fecha
    data['Expiration Date'] = pd.to_datetime(data['Expiration Date'], format='%a %b %d %Y')

    # Agregar una columna para el total de deltas en cada Expiration Date
    data['Total Delta'] = data['Calls Delta'] + data['Puts Delta']

    # Crear el gráfico con Plotly Express
    fig = px.bar(data, x='Expiration Date', y='Total Delta',
                color='Total Delta',
                color_discrete_sequence=['red', 'green'],
                labels={'Total Delta': 'Deltas'},
                title=f"Delta {archivo_seleccionado.replace('_quotedata.csv', '').upper()}".upper())

    # Definir los colores para valores positivos y negativos
    fig.update_traces(marker=dict(color=data['Total Delta'].apply(lambda x: 'green' if x >= 0 else 'red')))

    # Añadir línea horizontal en y=0
    fig.add_shape(type='line', x0=min(data['Expiration Date']), y0=0, x1=max(data['Expiration Date']), y1=0,
                line=dict(color='black', width=1))

    # Configurar el tooltip para mostrar la fecha y el valor de delta
    fig.update_traces(hovertemplate='<b>%{x|%Y-%m-%d}</b><br>%{y:.0f} Deltas')



    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)









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
        fig4.add_trace(go.Bar(x=df_top['Strike'], y=df_top['Puts Net'], name='Puts Net'))
        fig4.add_trace(go.Bar(x=df_top['Strike'], y=df_top['Calls Net'], name='Calls Net'))
        
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
        fig5.add_trace(go.Bar(x=df_top['Strike'], y=df_top['Puts Gamma'], name='Puts Gamma'))
        fig5.add_trace(go.Bar(x=df_top['Strike'], y=df_top['Calls Gamma'], name='Calls GAmma'))
        
        # Personaliza los títulos y ejes del gráfico
        fig5.update_layout(
            title='Neto de opciones call y put para los 15 strikes principales',
            xaxis_title='Strike',
            yaxis_title='Puts Gamma',
            barmode='stack'
            
        )
        
        # Muestra el gráfico en la página
        st.plotly_chart(fig5)








#INDICES ALL ###

        
        
    
    st.header("Todas las expiraciones SPX")

    col1, col2 = st.columns(2)

    with col1:
        # Crear un gráfico de barras para mostrar las columnas de "Calls Volume" y "Puts Volume" para cada "Strike"
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=data_all['Strike'], y=data_all['Calls Volume'], name='Calls Volume'))
        fig2.add_trace(go.Bar(x=data_all['Strike'], y=data_all['Puts Volume'], name='Puts Volume'))

        # Personaliza los títulos y ejes del gráfico
        fig2.update_layout(
            title='Volumen de opciones call y put para todas las expiraciones',
            xaxis_title='Strike',
            yaxis_title='Volume',
            barmode='stack'
        )

        # Muestra el gráfico en la página
        st.plotly_chart(fig2)

    with col2:
        # Crear un gráfico de barras para mostrar las columnas de "Calls Open Interest" y "Puts Open Interest" para cada "Strike"
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=df_top['Strike'], y=data_all['Calls Open Interest'], name='Calls Open Interest'))
        fig3.add_trace(go.Bar(x=df_top['Strike'], y=data_all['Puts Open Interest'], name='Puts Open Interest'))

        # Personaliza los títulos y ejes del gráfico
        fig3.update_layout(
            title='Interés abierto de opciones call y put para todas las expiraciones',
            xaxis_title='Strike',
            yaxis_title='Open Interest',
            barmode='stack'
        )

        # Muestra el gráfico en la página
        st.plotly_chart(fig3)

    col1, col2 = st.columns(2)

    with col1:
        # Crear un gráfico de barras para mostrar las columnas de "Puts Net" y "Calls Net" para cada "Strike"
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(x=data_all['Strike'], y=data_all['Puts Net'], name='Puts Net'))
        fig4.add_trace(go.Bar(x=data_all['Strike'], y=data_all['Calls Net'], name='Calls Net'))

        # Personaliza los títulos y ejes del gráfico
        fig4.update_layout(
            title='Neto de opciones call y put para todas las expiraciones',
            xaxis_title='Strike',
            yaxis_title='Puts Net',
            barmode='stack'
        )

        # Muestra el gráfico en la página
        st.plotly_chart(fig4)

    with col2:
        # Crear un gráfico de barras para mostrar las columnas de "Puts Gamma" y "Calls Gamma" para cada "Strike"
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(x=data_all['Strike'], y=data_all['Puts Gamma'], name='Puts Gamma'))
        fig5.add_trace(go.Bar(x=data_all['Strike'], y=data_all['Calls Gamma'], name='Calls Gamma'))
                    
        # Personaliza los títulos y ejes del gráfico
        fig5.update_layout(
            title='Gamma de opciones call y put para todas las expiraciones',
            xaxis_title='Strike',
            yaxis_title='Puts Gamma',
            barmode='stack'
        )

        # Muestra el gráfico en la página
        st.plotly_chart(fig5)
                    






##########

    with tab5:

        st.subheader("Options Data. Índices más representativos: SPX, SPY, NDX")

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
            # Ordenar el índice de forma descendente (de la fecha más reciente a la más antigua)
            df_chart.sort_index(ascending=False, inplace=False)

            # Ordenar el dataframe por Calls Net descendente
            #df_chart = df_chart.sort_values('Calls Net', ascending=True)
        

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Neto de los principales Índices: SPX, SPY, NDX"

            # Crear un gráfico de barras
            fig18 = go.Figure()
            fig18.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Net'], name='Calls Net'))
            fig18.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Net'], name='Puts Net') )

            # Personalizar el diseño del gráfico
            fig18.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Neto',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig18, container_width=1000, container_height=500)

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
            #df_chart = df_chart.sort_values('Calls Volume', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Volumen de los principales Índices: SPX, SPY, NDX"
            # Crear un gráfico de barras
            fig19 = go.Figure()
            fig19.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Volume'], name='Calls Volume'))
            fig19.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Volume'], name='Puts Volume'))

            # Personalizar el diseño del gráfico
            fig19.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Volume',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig19, container_width=1000, container_height=500)






        col1, col2 = st.columns(2)
        
        
        with col1:

            #INDICES
            #DELTA

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_index['Expiration Date'],
                'Calls Delta': df_index['Calls Delta'],
                'Puts Delta': df_index['Puts Delta']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            #df_chart = df_chart.sort_values('Calls Delta', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Delta de los principales Índices: SPX, SPY, NDX"

            # Crear un gráfico de barras
            fig10 = go.Figure()
            fig10.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Delta'], name='Calls Delta', marker=dict(color='green')))
            fig10.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Delta'], name='Puts Delta', marker=dict(color='red')))

            # Personalizar el diseño del gráfico
            fig10.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Delta',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig10, container_width=1000, container_height=500)

        with col2:
            

            # Obtener los datos del dataframe df_acciones
            # Gamma

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_index['Expiration Date'],
                'Calls Gamma': df_index['Calls Gamma'],
                'Puts Gamma': df_index['Puts Gamma']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            #df_chart = df_chart.sort_values('Calls Gamma', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Gamma de los principales índices: SPX, SPY, NDX"

            # Crear un gráfico de barras
            fig11 = go.Figure()
            fig11.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Gamma'], name='Calls Gamma'))
            fig11.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Gamma'], name='Puts Gamma'))

            # Personalizar el diseño del gráfico
            fig11.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Gamma',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig11, container_width=1000, container_height=500)







        col1, col2 = st.columns(2)
            
            
        with col1:

            #INDICES
            #Last Sale Mayor actividad en las opciones de compra (calls): La barra más alta y el color verde indican que ha habido una mayor actividad en las opciones de compra en comparación con las opciones de venta. Esto podría sugerir que los inversores tienen un mayor interés en la compra de opciones de compra en este vencimiento en particular.
            #Posible expectativa alcista: La diferencia de altura entre las barras de Calls Last Sale y Puts Last Sale puede indicar una mayor preferencia de los inversores por las posiciones alcistas. La actividad en las opciones de compra podría reflejar una expectativa de que el precio del activo subyacente aumente antes del vencimiento.

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_index['Expiration Date'],
                'Calls Last Sale': df_index['Calls Last Sale'],
                'Puts Last Sale': df_index['Puts Last Sale']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            #df_chart = df_chart.sort_values('Calls Last Sale', ascending=False)
            #df_chart.sort_values('Expiration Date', inplace=True)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Calls/Puts Last Sale de las Principales Índices: SPX, SPY, NDX"

            # Crear un gráfico de barras
            fig12 = go.Figure()
            fig12.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Last Sale'], name='Calls Last Sale', marker=dict(color='green')))
            fig12.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Last Sale'], name='Puts Last Sale', marker=dict(color='red')))

            # Personalizar el diseño del gráfico
            fig12.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Last Sale',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig12, container_width=1000, container_height=500)

        with col2:
            

            # Obtener los datos del dataframe df_acciones
            # Open Interest

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_index['Expiration Date'],
                'Calls Open Interest': df_index['Calls Open Interest'],
                'Puts Open Interest': df_index['Puts Open Interest']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            #df_chart = df_chart.sort_values('Calls Open Interest', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Open Interest de los principales índices: SPX, SPY, NDX"

            # Crear un gráfico de barras
            fig13 = go.Figure()
            fig13.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Open Interest'], name='Calls Open Interest'))
            fig13.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Open Interest'], name='Puts Open Interest'))

            # Personalizar el diseño del gráfico
            fig13.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Open Interest',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig13, container_width=1000, container_height=500)



    with tab6:
        st.subheader("Options Data. Acciones más representativas del SP500")
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
            #df_chart = df_chart.sort_values('Calls Net', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Neto de Principales Acciones: AMZN, AAPL, GOOG, MSFT, META, TSLA, NVDA, AMD"

            # Crear un gráfico de barras
            fig6 = go.Figure()
            fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Net'], name='Calls Net'))
            fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Net'], name='Puts Net'))

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
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Volumen de las principales acciones: AMZN, AAPL, GOOG, MSFT, META, TSLA, NVDA, AMD"

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

            #ACCIONES
            #DELTA

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_acciones['Expiration Date'],
                'Calls Delta': df_acciones['Calls Delta'],
                'Puts Delta': df_acciones['Puts Delta']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Delta', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Delta de las principales acciones: AMZN, AAPL, GOOG, MSFT, META, TSLA, NVDA, AMD"

            # Crear un gráfico de barras
            fig14 = go.Figure()
            fig14.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Delta'], name='Calls Delta', marker=dict(color='green')))
            fig14.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Delta'], name='Puts Delta', marker=dict(color='red')))

            # Personalizar el diseño del gráfico
            fig14.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Delta',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig14, container_width=1000, container_height=500)

        with col2:
            

            # Obtener los datos del dataframe df_acciones
            # Gamma

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_acciones['Expiration Date'],
                'Calls Gamma': df_acciones['Calls Gamma'],
                'Puts Gamma': df_acciones['Puts Gamma']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Gamma', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Gamma de las principales acciones: AMZN, AAPL, GOOG, MSFT, META, TSLA, NVDA, AMD"

            # Crear un gráfico de barras
            fig15 = go.Figure()
            fig15.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Gamma'], name='Calls Gamma'))
            fig15.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Gamma'], name='Puts Gamma'))

            # Personalizar el diseño del gráfico
            fig15.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Gamma',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig15, container_width=1000, container_height=500)







        col1, col2 = st.columns(2)
            
            
        with col1:

            #INDICES
            #Last Sale Mayor actividad en las opciones de compra (calls): La barra más alta y el color verde indican que ha habido una mayor actividad en las opciones de compra en comparación con las opciones de venta. Esto podría sugerir que los inversores tienen un mayor interés en la compra de opciones de compra en este vencimiento en particular.
            #Posible expectativa alcista: La diferencia de altura entre las barras de Calls Last Sale y Puts Last Sale puede indicar una mayor preferencia de los inversores por las posiciones alcistas. La actividad en las opciones de compra podría reflejar una expectativa de que el precio del activo subyacente aumente antes del vencimiento.

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_acciones['Expiration Date'],
                'Calls Last Sale': df_acciones['Calls Last Sale'],
                'Puts Last Sale': df_acciones['Puts Last Sale']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Last Sale', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Calls/Puts Last Sale de las principales acciones: AMZN, AAPL, GOOG, MSFT, META, TSLA, NVDA, AMD"

            # Crear un gráfico de barras
            fig16 = go.Figure()
            fig16.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Last Sale'], name='Calls Last Sale', marker=dict(color='green')))
            fig16.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Last Sale'], name='Puts Last Sale', marker=dict(color='red')))

            # Personalizar el diseño del gráfico
            fig16.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Last Sale',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig16, container_width=1000, container_height=500)

        with col2:
            

            # Obtener los datos del dataframe df_acciones
            # Open Interest

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_acciones['Expiration Date'],
                'Calls Open Interest': df_acciones['Calls Open Interest'],
                'Puts Open Interest': df_acciones['Puts Open Interest']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Open Interest', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Open Interest de las principales acciones: AMZN, AAPL, GOOG, MSFT, META, TSLA, NVDA, AMD"

            # Crear un gráfico de barras
            fig17 = go.Figure()
            fig17.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Open Interest'], name='Calls Open Interest'))
            fig17.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Open Interest'], name='Puts Open Interest'))

            # Personalizar el diseño del gráfico
            fig17.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Open Interest',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig17, container_width=1000, container_height=500)



        #Chart de tecnlogicas
        st.subheader("Acciones tecnológicas")
        col1, col2 = st.columns(2)
        
        
        with col1:

            # Obtener los datos del dataframe df_acciones
            # Supongamos que el dataframe contiene las columnas ['Expiration Date', 'Calls Net', 'Puts Net']

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_acciones_tech['Expiration Date'],
                'Calls Net': df_acciones_tech['Calls Net'],
                'Puts Net': df_acciones_tech['Puts Net']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            #df_chart = df_chart.sort_values('Calls Net', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Options Data. Neto de Principales Acciones: AAPL, GOOG, MSFT, NVDA"

            # Crear un gráfico de barras
            fig6 = go.Figure()
            fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Net'], name='Calls Net'))
            fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Net'], name='Puts Net'))

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
                'Expiration Date': df_acciones_tech['Expiration Date'],
                'Calls Volume': df_acciones_tech['Calls Volume'],
                'Puts Volume': df_acciones_tech['Puts Volume']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Volume', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Volumen de las principales acciones:AAPL, GOOG, MSFT,NVDA"

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

            #ACCIONES
            #DELTA

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_acciones_tech['Expiration Date'],
                'Calls Delta': df_acciones_tech['Calls Delta'],
                'Puts Delta': df_acciones_tech['Puts Delta']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Delta', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Delta de las principales acciones: AAPL, GOOG, MSFT, NVDA"

            # Crear un gráfico de barras
            fig14 = go.Figure()
            fig14.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Delta'], name='Calls Delta', marker=dict(color='green')))
            fig14.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Delta'], name='Puts Delta', marker=dict(color='red')))

            # Personalizar el diseño del gráfico
            fig14.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Delta',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig14, container_width=1000, container_height=500)

        with col2:
            

            # Obtener los datos del dataframe df_acciones
            # Gamma

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_acciones_tech['Expiration Date'],
                'Calls Gamma': df_acciones_tech['Calls Gamma'],
                'Puts Gamma': df_acciones_tech['Puts Gamma']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Gamma', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Gamma de las principales acciones: AAPL, GOOG, MSFT, NVDA"

            # Crear un gráfico de barras
            fig15 = go.Figure()
            fig15.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Gamma'], name='Calls Gamma'))
            fig15.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Gamma'], name='Puts Gamma'))

            # Personalizar el diseño del gráfico
            fig15.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Gamma',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig15, container_width=1000, container_height=500)







        col1, col2 = st.columns(2)
            
            
        with col1:

            #INDICES
            #Last Sale Mayor actividad en las opciones de compra (calls): La barra más alta y el color verde indican que ha habido una mayor actividad en las opciones de compra en comparación con las opciones de venta. Esto podría sugerir que los inversores tienen un mayor interés en la compra de opciones de compra en este vencimiento en particular.
            #Posible expectativa alcista: La diferencia de altura entre las barras de Calls Last Sale y Puts Last Sale puede indicar una mayor preferencia de los inversores por las posiciones alcistas. La actividad en las opciones de compra podría reflejar una expectativa de que el precio del activo subyacente aumente antes del vencimiento.

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_acciones_tech['Expiration Date'],
                'Calls Last Sale': df_acciones_tech['Calls Last Sale'],
                'Puts Last Sale': df_acciones_tech['Puts Last Sale']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Last Sale', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Calls/Puts Last Sale de las principales acciones: AAPL, GOOG, MSFT,NVDA"

            # Crear un gráfico de barras
            fig16 = go.Figure()
            fig16.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Last Sale'], name='Calls Last Sale', marker=dict(color='green')))
            fig16.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Last Sale'], name='Puts Last Sale', marker=dict(color='red')))

            # Personalizar el diseño del gráfico
            fig16.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Last Sale',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig16, container_width=1000, container_height=500)

        with col2:
            

            # Obtener los datos del dataframe df_acciones
            # Open Interest

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_acciones_tech['Expiration Date'],
                'Calls Open Interest': df_acciones_tech['Calls Open Interest'],
                'Puts Open Interest': df_acciones_tech['Puts Open Interest']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Open Interest', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Open Interest de las principales acciones: AAPL, GOOG, MSFT, NVDA"

            # Crear un gráfico de barras
            fig17 = go.Figure()
            fig17.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Open Interest'], name='Calls Open Interest'))
            fig17.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Open Interest'], name='Puts Open Interest'))

            # Personalizar el diseño del gráfico
            fig17.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Open Interest',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig17, container_width=1000, container_height=500)
    



    with tab7:
        
        #Chart de Memes Stocks
        st.subheader("Options Data. Meme Stocks")
        col1, col2 = st.columns(2)
        
        
        with col1:

            # Obtener los datos del dataframe df_acciones
            # Supongamos que el dataframe contiene las columnas ['Expiration Date', 'Calls Net', 'Puts Net']

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_memestock['Expiration Date'],
                'Calls Net': df_memestock['Calls Net'],
                'Puts Net': df_memestock['Puts Net']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            #df_chart = df_chart.sort_values('Calls Net', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Neto de Principales Memes: LCID, AMC, PLTR, RIVN"

            # Crear un gráfico de barras
            fig6 = go.Figure()
            fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Net'], name='Calls Net'))
            fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Net'], name='Puts Net'))

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
                'Expiration Date': df_memestock['Expiration Date'],
                'Calls Volume': df_memestock['Calls Volume'],
                'Puts Volume': df_memestock['Puts Volume']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Volume', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Volumen de Principales Memes: LCID, AMC, PLTR, RIVN"

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

            #ACCIONES
            #DELTA

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_memestock['Expiration Date'],
                'Calls Delta': df_memestock['Calls Delta'],
                'Puts Delta': df_memestock['Puts Delta']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Delta', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Delta de Principales Memes: LCID, AMC, PLTR, RIVN"

            # Crear un gráfico de barras
            fig14 = go.Figure()
            fig14.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Delta'], name='Calls Delta', marker=dict(color='green')))
            fig14.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Delta'], name='Puts Delta', marker=dict(color='red')))

            # Personalizar el diseño del gráfico
            fig14.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Delta',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig14, container_width=1000, container_height=500)

        with col2:
            

            # Obtener los datos del dataframe df_acciones
            # Gamma

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_memestock['Expiration Date'],
                'Calls Gamma': df_memestock['Calls Gamma'],
                'Puts Gamma': df_memestock['Puts Gamma']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Gamma', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Gamma de Principales Memes: LCID, AMC, PLTR, RIVN"

            # Crear un gráfico de barras
            fig15 = go.Figure()
            fig15.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Gamma'], name='Calls Gamma'))
            fig15.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Gamma'], name='Puts Gamma'))

            # Personalizar el diseño del gráfico
            fig15.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Gamma',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig15, container_width=1000, container_height=500)







        col1, col2 = st.columns(2)
            
            
        with col1:

            #INDICES
            #Last Sale Mayor actividad en las opciones de compra (calls): La barra más alta y el color verde indican que ha habido una mayor actividad en las opciones de compra en comparación con las opciones de venta. Esto podría sugerir que los inversores tienen un mayor interés en la compra de opciones de compra en este vencimiento en particular.
            #Posible expectativa alcista: La diferencia de altura entre las barras de Calls Last Sale y Puts Last Sale puede indicar una mayor preferencia de los inversores por las posiciones alcistas. La actividad en las opciones de compra podría reflejar una expectativa de que el precio del activo subyacente aumente antes del vencimiento.

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_memestock['Expiration Date'],
                'Calls Last Sale': df_memestock['Calls Last Sale'],
                'Puts Last Sale': df_memestock['Puts Last Sale']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Last Sale', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Calls/Puts Last Sale de los Principales Memes: LCID, AMC, PLTR, RIVN"

            # Crear un gráfico de barras
            fig16 = go.Figure()
            fig16.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Last Sale'], name='Calls Last Sale', marker=dict(color='green')))
            fig16.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Last Sale'], name='Puts Last Sale', marker=dict(color='red')))

            # Personalizar el diseño del gráfico
            fig16.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Last Sale',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig16, container_width=1000, container_height=500)

        with col2:
            

            # Obtener los datos del dataframe df_acciones
            # Open Interest

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_memestock['Expiration Date'],
                'Calls Open Interest': df_memestock['Calls Open Interest'],
                'Puts Open Interest': df_memestock['Puts Open Interest']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Open Interest', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Open Interest de Principales Memes: LCID, AMC, PLTR, RIVN"

            # Crear un gráfico de barras
            fig17 = go.Figure()
            fig17.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Open Interest'], name='Calls Open Interest'))
            fig17.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Open Interest'], name='Puts Open Interest'))

            # Personalizar el diseño del gráfico
            fig17.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Open Interest',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig17, container_width=1000, container_height=500)


    with tab8:

        st.subheader("Dark Index (DIX), Gamma Exposure (GEX)")

        # Convertir la columna 'date' en un objeto datetime
        df_squeeze['date'] = pd.to_datetime(df_squeeze['date'])

        # Seleccionar rango de fechas según el select 3 meses , 6 meses, 1 año, 1 año y medio, 2 años , 3 años, o todos los datos
        time_range = st.selectbox("Seleccionar rango de fechas", ["1 Semana" , "1 mes", "3 meses", "6 meses", "1 año", "1 año y medio", "2 años", "3 años",  "Todos los datos"])
        if time_range == "1 Semana":
            df_squeeze = df_squeeze[df_squeeze['date'] >= df_squeeze['date'].max() - pd.DateOffset(weeks=1)]
        elif time_range == "1 mes":
            df_squeeze = df_squeeze[df_squeeze['date'] >= df_squeeze['date'].max() - pd.DateOffset(months=1)]
        elif time_range == "3 meses":
            df_squeeze = df_squeeze[df_squeeze['date'] >= df_squeeze['date'].max() - pd.DateOffset(months=3)]
        elif time_range == "6 meses":
            df_squeeze = df_squeeze[df_squeeze['date'] >= df_squeeze['date'].max() - pd.DateOffset(months=6)]
        elif time_range == "1 año":
            df_squeeze = df_squeeze[df_squeeze['date'] >= df_squeeze['date'].max() - pd.DateOffset(years=1)]
        elif time_range == "1 año y medio":
            df_squeeze = df_squeeze[df_squeeze['date'] >= df_squeeze['date'].max() - pd.DateOffset(years=1)]
        elif time_range == "2 años":
            df_squeeze = df_squeeze[df_squeeze['date'] >= df_squeeze['date'].max() - pd.DateOffset(years=2)]
        elif time_range == "3 años":
            df_squeeze = df_squeeze[df_squeeze['date'] >= df_squeeze['date'].max() - pd.DateOffset(years=3)]
        elif time_range == "Todos los datos":
            df_squeeze = df_squeeze
            



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
                    

    with tab9:


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
            



    
    