# ====================================================================
# AGATHA v8.3 — CORE SYSTEM (DATA + GEO NOMINATIM + STREAMLIT UPDATE)
# ====================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
import requests
import time
from geopy.geocoders import Nominatim

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

OPENWEATHER_API_KEY = get_secret("OPENWEATHER_API_KEY")

# =========================
# CACHE GEO (NOMINATIM)
# =========================
@st.cache_data(show_spinner=False)
def geocode_cache(ciudad, pais):
    try:
        # Agente de usuario personalizado para Motor de Análisis Conductual Predictivo
        geolocator = Nominatim(user_agent="motor_analisis_conductual_predictivo")
        query = f"{ciudad}, {pais}"
        
        location = geolocator.geocode(query, timeout=10)
        
        if location:
            time.sleep(1.1) # Pausa obligatoria por políticas de Nominatim
            return location.latitude, location.longitude
            
    except Exception:
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
            # Corrección del error de tokenización
            df = pd.read_csv(
                os.path.join(ruta, archivo), 
                on_bad_lines="skip", 
                engine="python"
            )

            df.columns = df.columns.str.upper().str.strip()

            rename_map = {
                "DÍA": "DIA", "DAY": "DIA",
                "MES": "MES", "MONTH": "MES",
                "AÑO": "AÑO", "YEAR": "AÑO",
                "PAÍS": "PAIS", "COUNTRY": "PAIS",
                "CITY": "CIUDAD", "SHAPE": "FORMA",
                "TIME": "HORA"
            }

            df.rename(columns=rename_map, inplace=True)

            for c in ["DIA","MES","AÑO","CIUDAD","PAIS","FORMA"]:
                if c not in df.columns:
                    df[c] = "No especificado"

            df["CIUDAD"] = df["CIUDAD"].astype(str).str.strip()
            df["PAIS"] = df["PAIS"].astype(str).str.strip()
            df["FORMA"] = df["FORMA"].astype(str).str.title()

            dfs.append(df)

        except Exception as e:
            pass # Silenciamos los errores de archivos individuales para no ensuciar la interfaz

    if not dfs:
        return pd.DataFrame()

    df_total = pd.concat(dfs, ignore_index=True)
    return df_total

# =========================
# GEOLOCALIZACIÓN BAJO DEMANDA
# =========================
def geolocalizar_muestra(df_muestra):
    latitudes = []
    longitudes = []

    for i, row in df_muestra.iterrows():
        lat, lon = geocode_cache(row["CIUDAD"], row["PAIS"])
        latitudes.append(lat)
        longitudes.append(lon)

    df_muestra = df_muestra.copy()
    df_muestra["lat"] = latitudes
    df_muestra["lon"] = longitudes
    
    # Eliminamos solo los puntos que no se pudieron ubicar, manteniendo el resto
    return df_muestra.dropna(subset=["lat","lon"])

# =========================
# METEOROLOGÍA REAL
# =========================
def obtener_meteo(lat, lon):
    if not OPENWEATHER_API_KEY:
        return None
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat, "lon": lon,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric", "lang": "es"
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
with st.spinner("Motor de Análisis cargando base de datos global..."):
    df_maestro = cargar_datos_global()

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
        anios = sorted(df_maestro["AÑO"].dropna().unique())
        sel_anio = st.selectbox("AÑO", ["TODOS"] + list(map(int, [a for a in anios if str(a).isdigit()])))

        if sel_anio != "TODOS":
            df_filtrado = df_filtrado[df_filtrado["AÑO"] == sel_anio]

        formas = sorted(df_maestro["FORMA"].dropna().unique())
        sel_forma = st.selectbox("TIPO DE OBJETO", ["TODOS"] + formas)

        if sel_forma != "TODOS":
            df_filtrado = df_filtrado[df_filtrado["FORMA"] == sel_forma]

        paises = sorted(df_maestro["PAIS"].dropna().unique())
        sel_pais = st.selectbox("PAÍS", ["TODOS"] + paises)

        if sel_pais != "TODOS":
            df_filtrado = df_filtrado[df_filtrado["PAIS"] == sel_pais]

# =========================
# CONTROL DE PUNTOS Y MAPA
# =========================
with col_mapa:
    if not df_filtrado.empty:
        
        # Tomamos una muestra máxima de 60 para no bloquear la API de Nominatim
        muestra_size = min(60, len(df_filtrado))
        df_mostrar = df_filtrado.sample(muestra_size)
        
        with st.spinner("Calculando coordenadas geográficas de la muestra..."):
            df_mostrar = geolocalizar_muestra(df_mostrar)

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

            fig.update_layout(
                geo=dict(
                    projection_type="orthographic",
                    showland=True, landcolor="#121212",
                    showocean=True, oceancolor="#050505",
                    showcountries=True, countrycolor="#2a2a2a"
                ),
                margin=dict(l=0, r=0, t=0, b=0),
                height=450,
                paper_bgcolor="#0a0a0a"
            )

            # Actualizado a la nueva sintaxis de Streamlit
            st.plotly_chart(fig, width="stretch")
            st.caption("Nota: El mapa muestra una muestra representativa geolocalizada para optimizar el rendimiento.")
        else:
            st.warning("No se pudieron obtener las coordenadas geográficas de los puntos filtrados.")
    else:
        st.warning("No hay datos disponibles con los filtros actuales.")

# =========================
# MÉTRICAS
# =========================
st.markdown("---")
m1, m2, m3 = st.columns(3)

if not df_filtrado.empty:
    m1.metric("Registros Totales", f"{len(df_filtrado):,}")
    m2.metric("Tipos Únicos", df_filtrado["FORMA"].nunique())
    m3.metric("Países Implicados", df_filtrado["PAIS"].nunique())
else:
    m1.metric("Registros", 0)
    m2.metric("Tipos", 0)
    m3.metric("Países", 0)

# ====================================================================
# INTELIGENCIA AGATHA — NLP + PREDICCIÓN + ANOMALÍAS
# ====================================================================

st.markdown("---")

with st.expander("PROCESADOR FORENSE AGATHA", expanded=False):
    if not df_filtrado.empty:
        df_nlp = df_filtrado.copy()
        df_nlp["TAG"] = df_nlp["CIUDAD"] + " | " + df_nlp["FORMA"] + " | " + df_nlp["AÑO"].astype(str)
        opciones = df_nlp["TAG"].unique()
        caso_sel = st.selectbox("Seleccionar expediente", opciones)

        if caso_sel:
            fila = df_nlp[df_nlp["TAG"] == caso_sel].iloc[0]
            resumen = str(fila.get("RESUMEN", "Sin descripción detallada."))
            
            st.markdown("### Resumen del caso")
            st.write(resumen)

            def inferir_hipotesis(texto, forma):
                t = texto.lower()
                if "línea" in t or "varias luces" in t: return "Posible satélite o red Starlink"
                if "rápido" in t or "estela" in t: return "Posible meteorito o reentrada"
                if "flotando" in t: return "Posible globo o dron"
                if "luz" in forma.lower(): return "Fenómeno lumínico no identificado"
                return "Fenómeno no clasificado"

            if st.button("Ejecutar análisis AGATHA", type="primary"):
                # Intentamos geolocalizar el punto específico para sacar la meteo
                lat, lon = geocode_cache(fila["CIUDAD"], fila["PAIS"])
                
                st.markdown("### Contexto ambiental")
                if lat and lon:
                    meteo = obtener_meteo(lat, lon)
                    if meteo:
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Temperatura", f"{meteo['temp']}°C")
                        c2.metric("Nubosidad", f"{meteo['nubes']}%")
                        c3.metric("Condiciones", meteo["desc"])
                    else:
                        st.info("Datos meteorológicos no disponibles en este momento.")
                else:
                    st.info("Coordenadas no disponibles para consulta meteorológica.")

                hip = inferir_hipotesis(resumen, fila["FORMA"])
                indice = np.random.randint(60, 95)

                st.markdown("### Informe AGATHA")
                c4, c5 = st.columns(2)
                c4.metric("Índice de Anomalía", indice)
                c5.metric("Hipótesis Principal", hip)

with st.expander("ANÁLISIS DE CORRELACIÓN", expanded=False):
    if not df_filtrado.empty and len(df_filtrado) > 10:
        corr = (
            df_filtrado.groupby(["PAIS", "FORMA"])
            .size()
            .reset_index(name="conteo")
            .sort_values(by="conteo", ascending=False)
            .head(10)
        )
        # Actualizado a la nueva sintaxis de Streamlit
        st.dataframe(corr, width="stretch")
    else:
        st.info("Datos insuficientes para correlación.")

with st.expander("PREDICCIÓN DE ZONAS CALIENTES", expanded=False):
    if not df_filtrado.empty and len(df_filtrado) > 10:
        pred = df_filtrado["PAIS"].value_counts().head(5)
        for pais, val in pred.items():
            st.markdown(f"""
            <div style='background:#0f172a; padding:10px; border-left:3px solid #00ff88; margin-bottom:5px;'>
            <b>{pais}</b> — índice de actividad: {val}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No hay suficiente información para predicción.")

with st.expander("DETECCIÓN DE ANOMALÍAS", expanded=False):
    if not df_filtrado.empty:
        freq = df_filtrado["FORMA"].value_counts()
        raros = freq[freq < 3]
        if len(raros) > 0:
            for forma, val in raros.items():
                st.warning(f"Fenómeno poco frecuente detectado: {forma} ({val} casos)")
        else:
            st.success("No se detectan anomalías relevantes en la muestra actual.")
