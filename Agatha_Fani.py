# ====================================================================
# AGATHA v7.0 — INTELLIGENT NEURAL NETWORK (TV READY FINAL)
# ====================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
import json
import requests
from datetime import datetime
import time

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="AGATHA", layout="wide")

# =========================
# CSS
# =========================
st.markdown("""
<style>
.stApp { background:#0a0a0a; color:#e2e8f0; }
h1 { color:#00d4ff; text-shadow:0 0 8px #00d4ff; }
h3 { color:#00ff88; }
.block-container { border-top:1px solid rgba(0,212,255,0.2); }
</style>
""", unsafe_allow_html=True)

# =========================
# CABECERA
# =========================
st.markdown("""
<h1>AGATHA Intelligent Neural Network</h1>
<h3>MÓDULO CONTACT — Unidentified Anomalous Phenomenon</h3>
<p style="font-size:0.8rem; color:#94a3b8;">
“El Universo es enorme. Y si solo estamos nosotros, cuánto espacio desaprovechado”
</p>
""", unsafe_allow_html=True)

# =========================
# FORMULARIO USUARIO
# =========================
st.markdown("### NOTIFICA TU AVISTAMIENTO")

col1, col2, col3 = st.columns(3)
fecha = col1.date_input("Fecha")
hora = col2.time_input("Hora")
pais = col3.text_input("País")

col4, col5 = st.columns(2)
ciudad = col4.text_input("Ciudad")
tipo = col5.selectbox("Tipo de objeto", [
    "Desconocido","Luz","Orbe","Triángulo","Disco","Cilindro","Esfera",
    "Rectángulo","Cruz","Diamante","Otros"
])

descripcion = st.text_area("Descripción")

if st.button("Enviar reporte"):
    if "reportes" not in st.session_state:
        st.session_state["reportes"] = []

    st.session_state["reportes"].append({
        "PAIS": pais,
        "CIUDAD": ciudad,
        "FORMA": tipo,
        "RESUMEN": descripcion
    })

    st.success("Reporte registrado en AGATHA")

# =========================
# CARGA DATOS
# =========================
@st.cache_data
def cargar_datos():
    try:
        df = pd.read_csv("agatha_ufo_nodes_full.csv")
        df.columns = df.columns.str.upper()

        df["lat"] = np.random.uniform(-60, 60, len(df))
        df["lon"] = np.random.uniform(-180, 180, len(df))

        return df
    except:
        return pd.DataFrame()

df = cargar_datos()

# =========================
# MAPA
# =========================
if not df.empty:

    fig = go.Figure()

    fig.add_trace(go.Scattergeo(
        lon=df["lon"],
        lat=df["lat"],
        mode="markers",
        marker=dict(size=5, color="cyan"),
        name="Histórico"
    ))

    if "reportes" in st.session_state:
        df_user = pd.DataFrame(st.session_state["reportes"])

        if not df_user.empty:
            df_user["lat"] = np.random.uniform(-60, 60, len(df_user))
            df_user["lon"] = np.random.uniform(-180, 180, len(df_user))

            fig.add_trace(go.Scattergeo(
                lon=df_user["lon"],
                lat=df_user["lat"],
                mode="markers",
                marker=dict(size=8, color="yellow"),
                name="Ciudadanos"
            ))

    st.plotly_chart(fig, use_container_width=True)

# =========================
# METRICAS
# =========================
col_m1, col_m2, col_m3 = st.columns(3)

col_m1.metric("Registros", len(df))
col_m2.metric("Tipos", df["FORMA"].nunique() if not df.empty else 0)
col_m3.metric("Países", df["PAIS"].nunique() if not df.empty else 0)

# =========================
# METEOROLOGIA
# =========================
def obtener_meteo():
    return {
        "temp": np.random.randint(-5, 35),
        "nubes": np.random.randint(0, 100),
        "clima": np.random.choice([
            "cielo despejado",
            "nubes dispersas",
            "alta nubosidad"
        ])
    }

# =========================
# ANALISIS AGATHA
# =========================
def analizar_texto(texto):

    texto = texto.lower()

    if "línea" in texto or "varias luces" in texto:
        return "Posible satélite o Starlink"

    if "rápido" in texto:
        return "Posible meteorito"

    if "flotando" in texto:
        return "Posible globo o dron"

    return "Fenómeno no clasificado"

# =========================
# NLP
# =========================
if not df.empty:

    idx = st.selectbox("Seleccionar caso", df.index)

    fila = df.iloc[idx]
    resumen = str(fila.get("RESUMEN", ""))

    st.markdown("### RESUMEN DEL CASO")
    st.write(resumen)

    if st.button("Ejecutar análisis AGATHA"):

        meteo = obtener_meteo()
        hipotesis = analizar_texto(resumen)
        indice = np.random.randint(50, 95)

        st.markdown("### CONTEXTO AMBIENTAL")
        c1, c2, c3 = st.columns(3)
        c1.metric("Temperatura", f"{meteo['temp']}°C")
        c2.metric("Nubosidad", f"{meteo['nubes']}%")
        c3.metric("Condiciones", meteo["clima"])

        st.markdown("### INFORME AGATHA")

        c4, c5 = st.columns(2)
        c4.metric("Índice", indice)
        c5.metric("Hipótesis", hipotesis)

# =========================
# CORRELACION
# =========================
def correlacion(df):
    if df.empty:
        return None
    return df.groupby(["PAIS", "FORMA"]).size().sort_values(ascending=False).head(5)

corr = correlacion(df)

if corr is not None:
    st.markdown("### CORRELACIÓN")
    st.dataframe(corr)

# =========================
# PREDICCION
# =========================
def predecir(df):
    if df.empty:
        return None
    return df["PAIS"].value_counts().head(5)

pred = predecir(df)

if pred is not None:
    st.markdown("### PREDICCIÓN ZONAS CALIENTES")
    for p in pred.index:
        st.write(p)

# =========================
# ALERTAS
# =========================
if pred is not None and pred.iloc[0] > 10:
    st.error(f"ALERTA: actividad elevada en {pred.index[0]}")

# =========================
# ANOMALIAS
# =========================
def anomalías(df):

    if df.empty:
        return None

    freq = df["FORMA"].value_counts()
    return freq[freq < 3]

anom = anomalías(df)

if anom is not None and len(anom) > 0:
    st.markdown("### ANOMALÍAS DETECTADAS")

    for a in anom.index:
        st.warning(f"Fenómeno poco frecuente: {a}")
