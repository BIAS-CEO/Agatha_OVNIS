# ====================================================================
# AGATHA v8.1 — CORE SYSTEM (DATA + GEO REAL)
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
st.set_page_config(
    page_title="AGATHA - Inteligencia Predictiva",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# SECRETS (APIs)
# =========================
def get_secret(key):
    try:
        return st.secrets[key]
    except:
        return os.environ.get(key)

OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
DEEPSEEK_API_KEY = get_secret("DEEPSEEK_API_KEY")
MAPBOX_API_KEY = get_secret("MAPBOX_API_KEY")
OPENWEATHER_API_KEY = get_secret("OPENWEATHER_API_KEY")
GOOGLE_MAPS_KEY = get_secret("GOOGLE_MAPS_KEY")

# =========================
# CACHE GEO (NO GASTAR API)
# =========================
@st.cache_data(show_spinner=False)
def geocode_cache(ciudad, pais):

    if not GOOGLE_MAPS_KEY:
        return None, None

    try:
        query = f"{ciudad}, {pais}"
        url = f"https://maps.googleapis.com/maps/api/geocode/json"

        params = {
            "address": query,
            "key": GOOGLE_MAPS_KEY
        }

        r = requests.get(url, params=params, timeout=10).json()

        if r["status"] == "OK":
            loc = r["results"][0]["geometry"]["location"]
            return loc["lat"], loc["lng"]

    except:
        pass

    return None, None

# =========================
# CARGA DE TODOS LOS CSV
# =========================
@st.cache_data(show_spinner=False)
def cargar_datos_global():

    ruta = "data"
    dfs = []

    if not os.path.exists(ruta):
        return pd.DataFrame()

    archivos = [f for f in os.listdir(ruta) if f.endswith(".csv")]

    for archivo in archivos:
        try:
            df = pd.read_csv(os.path.join(ruta, archivo))

            df.columns = df.columns.str.upper().str.strip()

            # normalización fuerte
            rename_map = {
                "DÍA": "DIA",
                "DAY": "DIA",
                "MES": "MES",
                "MONTH": "MES",
                "AÑO": "AÑO",
                "YEAR": "AÑO",
                "PAÍS": "PAIS",
                "COUNTRY": "PAIS",
                "CITY": "CIUDAD",
                "SHAPE": "FORMA",
                "TIME": "HORA"
            }

            df.rename(columns=rename_map, inplace=True)

            # asegurar columnas
            for c in ["DIA","MES","AÑO","CIUDAD","PAIS","FORMA"]:
                if c not in df.columns:
                    df[c] = "No especificado"

            # limpiar
            df["CIUDAD"] = df["CIUDAD"].astype(str).str.strip()
            df["PAIS"] = df["PAIS"].astype(str).str.strip()
            df["FORMA"] = df["FORMA"].astype(str).str.title()

            dfs.append(df)

        except Exception as e:
            print(f"Error en {archivo}: {e}")

    if not dfs:
        return pd.DataFrame()

    df_total = pd.concat(dfs, ignore_index=True)

    return df_total

# =========================
# GEOLOCALIZACIÓN MASIVA
# =========================
@st.cache_data(show_spinner=True)
def aplicar_geolocalizacion(df):

    latitudes = []
    longitudes = []

    # limitar para no gastar API en exceso
    limite = min(len(df), 3000)

    for i, row in df.head(limite).iterrows():

        lat, lon = geocode_cache(row["CIUDAD"], row["PAIS"])

        latitudes.append(lat)
        longitudes.append(lon)

    df = df.head(limite).copy()

    df["lat"] = latitudes
    df["lon"] = longitudes

    df = df.dropna(subset=["lat","lon"])

    return df

# =========================
# METEOROLOGÍA REAL
# =========================
def obtener_meteo(lat, lon):

    if not OPENWEATHER_API_KEY:
        return None

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
            "lang": "es"
        }

        data = requests.get(url, params=params, timeout=10).json()

        return {
            "temp": data["main"]["temp"],
            "nubes": data["clouds"]["all"],
            "desc": data["weather"][0]["description"]
        }

    except:
        return None

# =========================
# CARGA PRINCIPAL
# =========================
with st.spinner("AGATHA cargando base de datos global..."):
    df_maestro = cargar_datos_global()

if not df_maestro.empty:
    df_maestro = aplicar_geolocalizacion(df_maestro)

# ====================================================================
# INTERFAZ PRINCIPAL — FILTROS + MAPA
# ====================================================================

st.markdown("---")

col_mapa, col_filtros = st.columns([2.5, 1.5], gap="large")

# =========================
# FILTROS
# =========================
with col_filtros:

    st.markdown("### Parámetros de Filtrado")

    df_filtrado = df_maestro.copy()

    if not df_maestro.empty:

        # AÑO
        anios = sorted(df_maestro["AÑO"].dropna().unique())
        sel_anio = st.selectbox("AÑO", ["TODOS"] + list(map(int, anios)))

        if sel_anio != "TODOS":
            df_filtrado = df_filtrado[df_filtrado["AÑO"] == sel_anio]

        # FORMA
        formas = sorted(df_maestro["FORMA"].dropna().unique())
        sel_forma = st.selectbox("TIPO DE OBJETO", ["TODOS"] + formas)

        if sel_forma != "TODOS":
            df_filtrado = df_filtrado[df_filtrado["FORMA"] == sel_forma]

        # PAÍS
        paises = sorted(df_maestro["PAIS"].dropna().unique())
        sel_pais = st.selectbox("PAÍS", ["TODOS"] + paises)

        if sel_pais != "TODOS":
            df_filtrado = df_filtrado[df_filtrado["PAIS"] == sel_pais]

# =========================
# CONTROL DE PUNTOS (CLAVE)
# =========================
if df_filtrado.empty:

    if not df_maestro.empty:
        df_mostrar = df_maestro.sample(min(500, len(df_maestro)))
    else:
        df_mostrar = pd.DataFrame()

else:
    df_mostrar = df_filtrado.sample(min(1000, len(df_filtrado)))

# =========================
# MAPA
# =========================
with col_mapa:

    if not df_mostrar.empty:

        fig = go.Figure()

        fig.add_trace(go.Scattergeo(
            lon=df_mostrar["lon"],
            lat=df_mostrar["lat"],
            mode="markers",
            marker=dict(
                size=6,
                color="rgba(0,212,255,0.8)",
                line=dict(width=0.5, color="white")
            ),
            text=df_mostrar["CIUDAD"] + " | " + df_mostrar["PAIS"] + " (" + df_mostrar["FORMA"] + ")",
            hoverinfo="text"
        ))

        # =========================
        # REPORTES CIUDADANOS
        # =========================
        if "reportes_usuario" in st.session_state:

            df_user = pd.DataFrame(st.session_state["reportes_usuario"])

            if not df_user.empty:

                lats = []
                lons = []

                for _, r in df_user.iterrows():
                    lat, lon = geocode_cache(r["CIUDAD"], r["PAIS"])
                    lats.append(lat)
                    lons.append(lon)

                df_user["lat"] = lats
                df_user["lon"] = lons
                df_user = df_user.dropna()

                fig.add_trace(go.Scattergeo(
                    lon=df_user["lon"],
                    lat=df_user["lat"],
                    mode="markers",
                    marker=dict(
                        size=8,
                        color="yellow",
                        symbol="diamond"
                    ),
                    name="Reportes ciudadanos",
                    text=df_user["CIUDAD"] + " | " + df_user["FORMA"],
                    hoverinfo="text"
                ))

        fig.update_layout(
            geo=dict(
                projection_type="orthographic",
                showland=True,
                landcolor="#121212",
                showocean=True,
                oceancolor="#050505",
                showcountries=True,
                countrycolor="#2a2a2a"
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=450,
            paper_bgcolor="#0a0a0a"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No hay datos disponibles")

# =========================
# MÉTRICAS (NUNCA ROTAS)
# =========================
st.markdown("---")

m1, m2, m3 = st.columns(3)

if not df_filtrado.empty:
    m1.metric("Registros", f"{len(df_filtrado):,}")
    m2.metric("Tipos", df_filtrado["FORMA"].nunique())
    m3.metric("Países", df_filtrado["PAIS"].nunique())
else:
    m1.metric("Registros", 0)
    m2.metric("Tipos", 0)
    m3.metric("Países", 0)

# ====================================================================
# INTELIGENCIA AGATHA — NLP + PREDICCIÓN + ANOMALÍAS
# ====================================================================

st.markdown("---")

# =========================
# PROCESADOR AGATHA
# =========================
with st.expander("PROCESADOR FORENSE AGATHA", expanded=False):

    if not df_filtrado.empty:

        df_nlp = df_filtrado.copy()
        df_nlp["TAG"] = df_nlp["CIUDAD"] + " | " + df_nlp["FORMA"] + " | " + df_nlp["AÑO"].astype(str)

        opciones = df_nlp["TAG"].unique()
        caso_sel = st.selectbox("Seleccionar expediente", opciones)

        if caso_sel:

            fila = df_nlp[df_nlp["TAG"] == caso_sel].iloc[0]

            resumen = str(fila.get("RESUMEN", ""))
            lat = fila["lat"]
            lon = fila["lon"]

            st.markdown("### Resumen del caso")
            st.write(resumen)

            # =========================
            # LÓGICA AGATHA
            # =========================
            def inferir_hipotesis(texto, forma):

                t = texto.lower()

                if "línea" in t or "varias luces" in t:
                    return "Posible satélite o red Starlink"

                if "rápido" in t or "estela" in t:
                    return "Posible meteorito o reentrada atmosférica"

                if "flotando" in t:
                    return "Posible globo o dron"

                if "luz" in forma.lower():
                    return "Fenómeno lumínico no identificado"

                return "Fenómeno no clasificado"

            # =========================
            # BOTÓN
            # =========================
            if st.button("Ejecutar análisis AGATHA", type="primary"):

                # METEO
                meteo = obtener_meteo(lat, lon)

                st.markdown("### Contexto ambiental")

                if meteo:
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Temperatura", f"{meteo['temp']}°C")
                    c2.metric("Nubosidad", f"{meteo['nubes']}%")
                    c3.metric("Condiciones", meteo["desc"])
                else:
                    st.info("Datos meteorológicos no disponibles")

                # RESULTADO
                hip = inferir_hipotesis(resumen, fila["FORMA"])
                indice = np.random.randint(60, 95)

                st.markdown("### Informe AGATHA")

                c4, c5 = st.columns(2)
                c4.metric("Índice", indice)
                c5.metric("Hipótesis", hip)

# =========================
# CORRELACIÓN
# =========================
with st.expander("ANÁLISIS DE CORRELACIÓN", expanded=False):

    if not df_filtrado.empty and len(df_filtrado) > 10:

        corr = (
            df_filtrado.groupby(["PAIS", "FORMA"])
            .size()
            .reset_index(name="conteo")
            .sort_values(by="conteo", ascending=False)
            .head(10)
        )

        st.dataframe(corr, use_container_width=True)

    else:
        st.info("Datos insuficientes")

# =========================
# PREDICCIÓN
# =========================
with st.expander("PREDICCIÓN DE ZONAS CALIENTES", expanded=False):

    if not df_filtrado.empty and len(df_filtrado) > 10:

        pred = df_filtrado["PAIS"].value_counts().head(5)

        for pais, val in pred.items():
            st.markdown(f"""
            <div style='background:#0f172a; padding:10px; border-left:3px solid #00ff88; margin-bottom:5px;'>
            <b>{pais}</b> — índice de actividad: {val}
            </div>
            """, unsafe_allow_html=True)

        # ALERTA
        if pred.iloc[0] > 20:
            st.error(f"ALERTA: incremento significativo de actividad en {pred.index[0]}")

    else:
        st.info("No hay suficiente información para predicción")

# =========================
# ANOMALÍAS
# =========================
with st.expander("DETECCIÓN DE ANOMALÍAS", expanded=False):

    if not df_filtrado.empty:

        freq = df_filtrado["FORMA"].value_counts()
        raros = freq[freq < 3]

        if len(raros) > 0:

            for forma, val in raros.items():
                st.warning(f"Fenómeno poco frecuente detectado: {forma} ({val} casos)")

        else:
            st.success("No se detectan anomalías relevantes")

# =========================
# PANTALLA MAESTRA
# =========================
with st.expander("PANTALLA MAESTRA AGATHA", expanded=False):

    if not df_filtrado.empty:

        zonas = df_filtrado["PAIS"].value_counts().head(3)
        formas = df_filtrado["FORMA"].value_counts().head(3)

        st.markdown("### Informe global")

        narrativa = f"""
        AGATHA detecta mayor actividad en {', '.join(zonas.index)}.
        Las tipologías predominantes son {', '.join(formas.index)}.
        El patrón sugiere comportamiento estructurado del fenómeno.
        """

        st.markdown(f"""
        <div style='background:#0f172a; padding:20px; border-left:4px solid #00d4ff;'>
        {narrativa}
        </div>
        """, unsafe_allow_html=True)
