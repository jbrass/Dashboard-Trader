import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import io


# Cargar la base de datos
df = pd.read_csv("datos-diarios.csv")
df['dia'] = pd.to_datetime(df['dia'], format='%m/%d/%Y')

with open("fintra-logo.png", 'rb') as img:
    st.image(img.read(), width=200)


tab1, tab2, tab3 = st.tabs(["Estadísticas", "Gráficos", "Forecast"])


with tab1:
   st.header("Estadísticas")
   # Mostrar la tabla completa al iniciar el programa
   st.dataframe(df.drop("Unnamed: 0", axis=1))
   # Crear campos de entrada de fecha
   fecha_inicio = st.date_input("Selecciona una fecha de inicio")
   fecha_fin = st.date_input("Selecciona una fecha de fin")

    # Crear un botón para aplicar el filtro
   if st.button("Aplicar filtro"):
        # Filtrar la base de datos
        df_filtrado = df.drop("Unnamed: 0", axis=1)[(df["dia"] >= fecha_inicio.strftime("%m/%d/%Y")) & (df["dia"] <= fecha_fin.strftime("%m/%d/%Y"))]
        # Mostrar la tabla con los datos filtrados
        st.dataframe(df_filtrado)
        
    
st.header("Correlaciones")
st.header("Heatmap")
st.write("Heatmap of correlation matrix")

fig, ax = plt.subplots(figsize=(15,10))
sns.heatmap(df.corr(), annot=True, ax=ax)

buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)
st.image(buf, width=800)



with tab2:
    st.header("Gráficos")
    variable = st.selectbox("Seleccione una variable", ["high", "low", "close", "vol", "range", "vix_close", "vwap", "vol_vpoc", "vol_vah", "vol_val"])
    tipo_grafico = st.selectbox("Seleccione un tipo de gráfico", ["Línea", "Dispersión", "Barras"])

    color_scale = alt.Scale(domain=['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes'],
                        range=["#e7ba52", "#a7a7a7", "#aec7e8", "#1f77b4", "#9467bd"])

    base = alt.Chart(df).encode(
        x=alt.X('dia:T', axis=alt.Axis(title='Fecha')),
    )


    if tipo_grafico == 'Línea':
        grafico = base.mark_line().encode(
            y=variable+':Q',
            color=alt.Color('dia_semanal', scale=color_scale, legend=alt.Legend(title='Día de la semana'))
        ).properties(
            width=800,
            height=600
        )
        st.altair_chart(grafico)
    elif tipo_grafico == 'Dispersión':
        grafico = base.mark_point().encode(
            y=variable+':Q',
            color=alt.Color('dia_semanal', scale=color_scale, legend=alt.Legend(title='Día de la semana'))
        ).properties(
            width=800,
            height=600
        )
        st.altair_chart(grafico)
    else:
        grafico = base.mark_bar().encode(
            y=variable+':Q',
            color=alt.Color('dia_semanal', scale=color_scale, legend=alt.Legend(title='Día de la semana'))
        ).properties(
            width=800,
            height=600
        )
        st.altair_chart(grafico)

with tab3:
    st.header("Predicciones ES")
    df = df.set_index("dia")
    # Seleccionar variable a analizar
    variable = st.selectbox("Seleccione una variable", ["high", "low", "close", "vol", "range", "vix_close", "vwap", "vol_vpoc", "vol_vah", "vol_val"], key='select_variable')
    base = alt.Chart(df).encode(
    x=alt.X('dia:T', axis=alt.Axis(title='Fecha')),
    )

    # Calcular estadísticas básicas
    mean = df[variable].mean()
    min_value = df[variable].min()
    max_value = df[variable].max()
    std = df[variable].std()
    
    # Mostrar estadísticas en tablero
    st.write("Promedio: ", mean)
    st.write("Valor mínimo: ", min_value)
    st.write("Valor máximo: ", max_value)
    st.write("Desviación estándar: ", std)
    
    # Mostrar gráfico de la variable seleccionada
    st.line_chart(df[variable])











        
