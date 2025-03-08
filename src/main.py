import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import time
from streamlit_gsheets import GSheetsConnection
#Title
st.title("Dashboard")
#Refresh
if st.button("Refrescar"):
    st.cache_resource.clear()
#Conditional
text_input = st.text_input("Contraseña",value="", placeholder="Password")
if text_input==st.secrets["db_password"]:
    with st.status("Cargando Data"):
        time.sleep(1)
        #DataBase
        conn1 = st.connection("gsheets_preregistro", type=GSheetsConnection)
        df = conn1.read(worksheet="RespuestasPRegistro").query("Duplicados != 'Duplicado'")
        conn2 = st.connection("gsheets_pagosregistrados", type=GSheetsConnection)
        df2 = conn2.read(worksheet="RespuestasPago").query("Confirmado == 'si'")
        time.sleep(1)
else:
    st.stop()
#General Tabs
numRegistros = df["Procedencia Final"].count()
numMandV = df["¿Miembro o Visitante?"].value_counts()
numHospedaje = df["¿Necesitas Hospedaje?"].value_counts()
pagos = df2["Confirmado"].count()
tab1, tab2, tab3, tab4, tab5 = st.columns(5, border=True)
tab1.subheader(numRegistros)
tab1.text("Total de Registros")
tab2.subheader(numMandV[0])
tab2.text("Miembros")
tab3.subheader(numMandV[1])
tab3.text("Visitantes")
tab4.subheader(numHospedaje[0])
tab4.text("Requieren Hospedaje")
tab5.subheader(pagos)
tab5.text("Pagos Confirmados")
#PIE
conteo = df['Procedencia Final'].value_counts()
fig = go.Figure(data=[go.Pie(labels=conteo.index, values=conteo.values, hole=.3)])
fig.update_traces(textposition='inside',textinfo='label',insidetextorientation='radial',hoverinfo='label+percent+value')
fig.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')
fig.update(layout_showlegend=True)
fig.update_layout(title="Procedencia")
containerPie = st.container(border=True)
containerPie.plotly_chart(fig)
#Trendline
interacciones = pd.to_datetime(df["Marca temporal"].values, format="%d/%m/%Y %H:%M:%S")
interacionesLimpias = interacciones.strftime("%Y-%m-%d")
data_interaction  = pd.DataFrame({
    'Fechas': interacionesLimpias
})
fechaInicial = pd.to_datetime(interacionesLimpias.min())
fechaFinal = pd.to_datetime(interacionesLimpias.max())
fechas = pd.date_range(fechaInicial,fechaFinal).strftime("%Y-%m-%d")
date_range = pd.DataFrame({
    'Fechas': fechas
})
interaction_counts = data_interaction['Fechas'].value_counts().sort_index()
date_range['Registros'] = date_range['Fechas'].map(interaction_counts).fillna(0).astype(int)
date_range["Fechas"] = pd.to_datetime(date_range["Fechas"])
x = np.arange(len(date_range))  # Numeric indices for dates
y = date_range["Registros"].values
coefficients = np.polyfit(x, y, deg=1)  # Fit linear regression (degree 1)
trendline = np.polyval(coefficients, x)  # Generate trendline values
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=date_range['Fechas'], y=date_range['Registros'], mode='lines+markers', name="Registros"))
# Add the trendline
fig2.add_trace(go.Scatter(x=date_range['Fechas'], y=trendline, mode='lines', name="Tendencia", line=dict(dash="dot")))
# Customize layout
fig2.update_layout(title="Tendencia de Registros",
                  xaxis_title="Fechas",
                  yaxis_title="Registros")
# Show the chart
containerTrend = st.container(border=True)
containerTrend.plotly_chart(fig2)
#Age Info
maximo = df["Edad"].max()
minimo = df["Edad"].min()
mediana = df["Edad"].median()
moda = df["Edad"].mode()
promedio = df["Edad"].mean().round(2)
left, middle1, middle2, middle3, right = st.columns(5, border=True)
left.subheader(maximo)
left.text("Edad Máxima registrada")
middle1.subheader(minimo)
middle1.text("Edad Mínima registrada")
middle2.subheader(mediana)
middle2.text("Mediana")
middle3.subheader(moda[0])
middle3.text("Moda")
right.subheader(promedio)
right.text("Promedio")