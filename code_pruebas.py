""" st.info("Para analizar el gráfico, podemos observar la distribución de las conexiones y las interacciones entre las categorías en función de la ubicación de los puntos en el gráfico", icon="ℹ️")
st.info("1. Proximidad: Si dos puntos en el gráfico están cercanos entre sí, indica una mayor interacción o relación entre las categorías que representan. Esto puede sugerir que estas categorías están influenciando o interactuando directamente en el mercado.")
st.info("2. Tendencia: Si hay una tendencia clara en la dirección de las conexiones en el gráfico (por ejemplo, una línea ascendente o descendente), puede indicar una relación sistemática entre las categorías. Esto puede ser útil para identificar patrones o comportamientos consistentes en el mercado.")
st.info("3. Concentración: Si hay una concentración de puntos alrededor de ciertas áreas del gráfico, puede indicar una interacción significativa o una mayor actividad entre esas categorías. Esto puede sugerir áreas de mayor liquidez, acumulación o distribución de posiciones.")
st.info("4. Anomalías: Si hay puntos aislados o alejados del grupo principal en el gráfico, pueden representar situaciones atípicas o anómalas en las interacciones entre las categorías. Estas anomalías podrían ser señales de cambios inesperados o eventos inusuales en el mercado.")
# Crear un subconjunto del dataframe con las variables necesarias
df_subset = df_cotSP[['cot_commercial', 'cot_noncommercial', 'cot_dealer', 'cot_institutional', 'cot_leveragedfunds', 'cot_other']]

# Calcular la matriz de correlación entre las variables
correlation_matrix = df_subset.corr()

# Crear un grafo dirigido a partir de la matriz de correlación
G = nx.from_pandas_adjacency(correlation_matrix, create_using=nx.DiGraph)

# Configurar el diseño del grafo
pos = nx.spring_layout(G, seed=42)

# Crear los nodos y las conexiones del grafo
node_trace = go.Scatter(
    x=[pos[k][0] for k in G.nodes()],
    y=[pos[k][1] for k in G.nodes()],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        size=10,
        color='blue',
    ),
    text=list(G.nodes()),
)

edge_trace = go.Scatter(
    x=[pos[k[0]][0] for k in G.edges()],
    y=[pos[k[0]][1] for k in G.edges()],
    line=dict(width=1, color='gray'),
    hoverinfo='none',
    mode='lines',
)

# Crear el layout del gráfico
layout = go.Layout(
    title='Red de Interacciones',
    showlegend=False,
    hovermode='closest',
    margin=dict(b=20, l=5, r=5, t=40),
)

# Crear la figura
fig = go.Figure(data=[edge_trace, node_trace], layout=layout)

# Mostrar el gráfico con Plotly
st.plotly_chart(fig, use_container_width=True)
"""
