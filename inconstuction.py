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