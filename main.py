# Importar las librerías necesarias
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import altair as alt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from bokeh.plotting import figure
import yfinance as yf
import datetime as dt



# Cargar la imagen de logo
with open("fintra-logo.png", 'rb') as img:
    st.image(img.read(), width=200)

df_diarios_ES = pd.read_csv("./Operativa/Diarios-ES.csv")
df_diarios_ES['dia'] = pd.to_datetime(df_diarios_ES['dia'], format='%m/%d/%Y')

df_diarios_NQ = pd.read_csv("./Operativa/Diarios-NQ.csv")
df_diarios_NQ['dia'] = pd.to_datetime(df_diarios_NQ['dia'], format='%m/%d/%Y')

df_semanal_ES = pd.read_csv("./Operativa/Semanal-ES.csv")
df_semanal_ES['dia'] = pd.to_datetime(df_semanal_ES['dia'])

df_semanal_NQ = pd.read_csv("./Operativa/Semanal-NQ.csv")
df_semanal_NQ['dia'] = pd.to_datetime(df_semanal_NQ['dia'])

renombre = {
    "./Operativa/Diarios-ES.csv": "Datos diarios mini S&P500",
    "./Operativa/Diarios-NQ.csv": "Datos diarios mini NASDAQ100",
    "./Operativa/Semanal-ES.csv": "Datos semanales mini S&P500",
    "./Operativa/Semanal-NQ.csv": "Datos semanales mini NASDAQ 100"
}

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


# Utilizar una estructura de control de flujo más clara
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Estadísticas", "Gráficos", "Forecast", "Resultados Operativa","Ficheros Descargas/Subidas", "Acciones"])

with tab1:

    st.title("Resumen de la jornada de trading")

    st.markdown("### Subtítulo")

    st.markdown('Streamlit is Streamlit isStreamlit isStreamlit isStreamlit isStreamlit isStreamlit is **_really_ cool**.')

   
    
    
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

    def graficar_maximo_drawdown(df):
        # Obtener el máximo valor acumulado hasta cada fila
        max_acumulado = df['close'].cummax()
        
        # Restar el máximo valor acumulado a cada valor del dataframe
        caida = df['close'] - max_acumulado
        
        # Obtener el mínimo valor de la caída
        min_caida = caida.min()
        
        # Calcular el máximo drawdown en términos porcentuales
        maximo_drawdown = min_caida / max_acumulado.max() * 100
        
        # Crear un gráfico con dos ejes y
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        
        # Añadir el máximo drawdown al primer eje y
        ax1.plot(df.index, maximo_drawdown, 'b-')
        
        # Añadir el precio de cierre y el número de día al segundo eje y
        ax2.plot(df.index, df['close'], 'r-').reshape(1,-1)
        ax2.plot(df.index, df['vol'], 'g-')
        
        # Mostrar el gráfico
        st.pyplot()




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


            


with tab3:

    # Cargar los dataframes
    df_diarios_ES = pd.read_csv('./Operativa/Diarios-ES.csv')
    df_diarios_NQ = pd.read_csv('./Operativa/Diarios-NQ.csv')
    df_semanal_ES = pd.read_csv('./Operativa/Semanal-ES.csv')
    df_semanal_NQ = pd.read_csv('./Operativa/Semanal-NQ.csv')

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









with tab4:
    # Mostrar resumen operativo
    st.subheader('Resumen Operativo')

    # Función para leer y procesar archivos
    def read_and_process_file(file_type):
        if file_type == "resultados_operativa":
            try:
                df = pd.read_csv("./Operativa/resumen.csv", sep=',')
                df = df.fillna(0)
                df = df.drop(columns = ["Unnamed: 4"], axis = 1)
            except:
                st.error("No se puede leer el archivo de resultados operativos")
                return None
        elif file_type == "trades":
            try:
                df = pd.read_excel("./Operativa/trades-excel.xlsx", sheet_name="Sheet1")
                df = df.drop(columns = ["#"], axis = 1)
                new_columns = {
                    "Period": "Período",
                    "Instrument": "Instrumento",
                    "Side": "Lado",
                    "Quantity": "Cantidad",
                    "Price": "Precio",
                    "Commission": "Comisión",
                    "P&L": "Ganancias/Pérdidas",
                    "Cum. net profit": "Beneficio neto acumulado"
                }
                df = df.rename(columns=new_columns)
            except:
                st.error("No se puede leer el archivo de trades")
                return None
        elif file_type == "ordenes_ejecutadas":
            try:
                df = pd.read_csv("./Operativa/ordenes.csv", sep=',')
                df = df.drop(columns = ["Connection","Strategy","Unnamed: 18"], axis = 1)
            except:
                st.error("No se puede leer el archivo de órdenes ejecutadas")
                return None
        elif file_type == "ejecuciones":
            try:
                df = pd.read_csv("./Operativa/ejecuciones.csv", sep=',')
                df = df.drop(columns = ["Connection","Unnamed: 14","Commission"], axis = 1)
            except:
                st.error("No se puede leer el archivo de ejecuciones")
                return None
        else:
            st.error(f"Tipo de archivo inválido: {file_type}")
            return None
        return df

    
    # Leer y procesar archivo de resultados de operativa
    resultados_operativa = read_and_process_file("resultados_operativa")
    # Mostrar los resultados de operativa en un dataframe
    st.dataframe(resultados_operativa)

    # Leer y procesar archivo de trades
    trades = read_and_process_file("trades")
    # Mostrar los trades en un dataframe
    st.dataframe(trades)

    # Agregar un título a la sección de visualización de resultados
    st.subheader('Visualización de resultados')

    # Mostrar una lista desplegable para elegir el tipo de gráfico
    chart_type = st.selectbox("Elige el tipo de gráfico:", ["Línea", "Dispersión", "Barras"])

    # Definir la columna para el eje X como "Período"
    x_col = "Período"
    # Mostrar una lista desplegable para elegir la columna para el eje Y
    y_col = st.selectbox("Elige la columna para el eje Y:", [col for col in trades.columns if col != "Período"])

    # Verificar el tipo de gráfico seleccionado y crear el gráfico correspondiente
    if chart_type == "Línea":
        # Crear un gráfico de línea utilizando la librería altair
        line_chart = alt.Chart(trades).mark_line().encode(
            x=alt.X(x_col, type="nominal"),
            y=alt.Y(y_col, sort="descending")
        )
        # Mostrar el gráfico en la sección de visualización de resultados
        st.altair_chart(line_chart.properties(width=800, height=600))

    elif chart_type == "Dispersión":
        # Crear un gráfico de dispersión utilizando la librería altair
        scatter_chart = alt.Chart(trades).mark_point().encode(
        x=alt.X(x_col, type="nominal"),
        y=alt.Y(y_col, sort="descending")
    )
        # Mostrar el gráfico en la sección de visualización de resultados
        st.altair_chart(scatter_chart.properties(width=800, height=600))

    elif chart_type == "Barras":
        # Crear un gráfico de barras utilizando la librería altair
        bar_chart = alt.Chart(trades).mark_bar().encode(
        x=alt.X(x_col, type="nominal"),
        y=alt.Y(y_col, sort="descending")
    )
        # Mostrar el gráfico en la sección de visualización de resultados
        st.altair_chart(bar_chart.properties(width=800, height=600))


        ordenes_ejecutadas = read_and_process_file("ordenes_ejecutadas")

        ejecuciones = read_and_process_file("ejecuciones")


        
with tab5:


    def load_data():
        data = st.file_uploader("Selecciona el archivo de datos diarios (formato csv)", type="csv")
        if data is not None:
            data = pd.read_csv(data)
            data["dia"] = pd.to_datetime(data["dia"])
            return data
        else:
            st.error("No se ha seleccionado ningún archivo.")
            return None

    data = load_data()

    if data is not None:
        # Filtro de fechas
        start_date = st.date_input("Selecciona la fecha de inicio")
        end_date = st.date_input("Selecciona la fecha de fin")
        if start_date and end_date:
            data = data[(data["dia"] >= start_date) & (data["dia"] <= end_date)]
        elif start_date:
            data = data[data["dia"] >= start_date]
        elif end_date:
            data = data[data["dia"] <= end_date]

        # Tablas con estadísticos básicos
        st.subheader("Estadísticos básicos")
        st.write(data.describe())

        # Heatmap de correlaciones
        st.subheader("Heatmap de correlaciones")
        corr = data.drop("dia", axis=1).corr()
        sns.set(font_scale=1.5)
        fig, ax = plt.subplots(figsize=(10,8))
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

        
        # Crear un gráfico de líneas utilizando Altair
        chart = alt.Chart(df).mark_line().encode(
            x='dia',
            y='vol'
        )
        st.altair_chart(chart, use_container_width=True)


with tab6:
    # Función para descargar datos de cotización de un instrumento financiero específico
    def download_data(ticker, start_date, end_date):
        df = yf.download(ticker, start=start_date, end=end_date)
        info = yf.Ticker(ticker).info
        description = info.get("longBusinessSummary")
        df["Media móvil de 200 sesiones"] = df["Close"].rolling(window=200).mean()
        df["Close"].rolling(200).mean().plot(color='orange', label='Media móvil de 200 sesiones')
        df["Close"].plot(label='Precio de cierre')
        plt.legend()
       
        st.set_option('deprecation.showPyplotGlobalUse', False)

        return df, description

    # Interfaz de usuario de Streamlit
    with st.container():
        st.title("Buscador de Acciones")

        ticker = st.text_input("Ingrese el ticker de la empresa:", "AAPL")

        start_date = st.date_input("Ingrese la fecha de inicio:", dt.date(2020, 1, 1))
        end_date = st.date_input("Ingrese la fecha final:", dt.date.today())

        if st.button("Mostrar datos"):    
            df,description = download_data(ticker, start_date, end_date)
            st.markdown("**Descripción de la empresa:** \n\n" + description)
            st.line_chart(df[["Close", "Media móvil de 200 sesiones"]])

            
