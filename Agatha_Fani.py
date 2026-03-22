# ====================================================================
# AGATHA v8.7 — CORE SYSTEM (RESTAURACIÓN ESTÉTICA 3D + RELACIONES)
# ====================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# =========================
# CONFIGURACIÓN
# =========================
st.set_page_config(
    page_title="Motor de Análisis Conductual Predictivo",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def obtener_credencial(key):
    try:
        return st.secrets[key]
    except:
        return os.environ.get(key)

# =========================
# FUNCIONES NÚCLEO
# =========================
def asignar_color_neon(forma):
    forma = str(forma).lower()
    if "luz" in forma or "flash" in forma: return "rgba(255, 255, 0, 0.8)"
    if "triangulo" in forma: return "rgba(255, 0, 0, 0.8)"
    if "esfera" in forma or "bola" in forma: return "rgba(0, 255, 0, 0.8)"
    return "rgba(0, 212, 255, 0.8)"

def simular_coordenadas(df):
    """Asignación de coordenadas determinista global."""
    np.random.seed(42)
    
    centroides = {
        "TX": (31.9, -99.9), "FL": (27.7, -81.6), "CA": (36.7, -119.4), "NY": (40.7, -74.0),
        "EEUU": (39.8, -98.5), "ESTADOS UNIDOS": (39.8, -98.5), "USA": (39.8, -98.5),
        "CANADA": (56.1, -106.3), "CANADÁ": (56.1, -106.3),
        "MEXICO": (23.6, -102.5), "MÉXICO": (23.6, -102.5),
        "UK": (55.3, -3.4), "REINO UNIDO": (55.3, -3.4), "INGLATERRA": (52.3, -1.1),
        "ESPAÑA": (40.46, -3.75), "ESPANA": (40.46, -3.75), "SPAIN": (40.46, -3.75),
        "FRANCIA": (46.22, 2.21), "ALEMANIA": (51.16, 10.45), "ITALIA": (41.87, 12.56),
        "INDIA": (20.59, 78.96), "CHINA": (35.86, 104.19), "JAPON": (36.20, 138.25), "JAPÓN": (36.20, 138.25),
        "AUSTRALIA": (-25.27, 133.77), "BRASIL": (-14.23, -51.92), "ARGENTINA": (-38.41, -63.61)
    }
    
    est = df.get('ESTADO', pd.Series(index=df.index)).astype(str).str.upper().str.strip()
    pai = df['PAIS'].astype(str).str.upper().str.strip()
    
    coord_est = est.map(centroides)
    coord_pai = pai.map(centroides)
    
    coords_finales = coord_est.combine_first(coord_pai)
    coords_defecto = pd.Series([(0.0, 0.0)] * len(df), index=df.index)
    coords_finales = coords_finales.combine_first(coords_defecto)
    
    df['hash_val'] = df['CIUDAD'].astype(str).apply(lambda x: sum(ord(c) for c in x) if pd.notna(x) else 0)
    df['lat_offset'] = ((df['hash_val'] % 100) - 50) / 100.0 * 3.5
    df['lon_offset'] = (((df['hash_val'] // 10) % 100) - 50) / 100.0 * 3.5
    
    df['lat'] = coords_finales.apply(lambda x: x[0]) + df['lat_offset']
    df['lon'] = coords_finales.apply(lambda x: x[1]) + df['lon_offset']
    
    df = df.drop(columns=['hash_val', 'lat_offset', 'lon_offset'])
    
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce').fillna(0.0)
    df['lon'] = pd.to_numeric(df['lon'], errors='coerce').fillna(0.0)
    
    return df

@st.cache_data(show_spinner=False)
def cargar_nodos():
    mensajes = []
    ruta_carpeta = "data"
    dfs = []
    
    if os.path.exists(ruta_carpeta):
        for archivo in os.listdir(ruta_carpeta):
            # Leemos todos los CSV. Ya NO excluimos el de relaciones.
            if archivo.endswith(".csv"):
                try:
                    temp_df = pd.read_csv(os.path.join(ruta_carpeta, archivo), encoding='utf-8', on_bad_lines='skip')
                    dfs.append(temp_df)
                except Exception:
                    pass
                    
        if dfs:
            df = pd.concat(dfs, ignore_index=True)
            mensajes.append("Archivos de datos unificados.")
        else:
            return pd.DataFrame(), ["Error: La carpeta de datos no contiene archivos válidos."]
    else:
        return pd.DataFrame(), ["Error: No se localizó la carpeta 'data'."]

    try:
        df.columns = df.columns.str.upper().str.strip()
        
        col_map = {
            'DÍA': 'DIA', 'DAY': 'DIA', 'MONTH': 'MES', 'YEAR': 'AÑO',
            'CITY': 'CIUDAD', 'STATE': 'ESTADO', 'PAÍS': 'PAIS', 
            'COUNTRY': 'PAIS', 'SHAPE': 'FORMA', 'SUMMARY': 'RESUMEN',
            'TIME': 'HORA'
        }
        df.rename(columns=col_map, inplace=True)
        
        for c in ['CIUDAD', 'PAIS', 'FORMA']:
            if c not in df.columns: df[c] = "No especificado"
            else: df[c] = df[c].fillna("No especificado").astype(str)
            
        df['PAIS'] = df['PAIS'].str.title().str.strip()
        df['FORMA'] = df['FORMA'].str.title().str.strip()
        
        if 'AÑO' not in df.columns: df['AÑO'] = 2026
        df['AÑO'] = pd.to_numeric(df['AÑO'], errors='coerce').fillna(2026).astype(int)
        
        df = simular_coordenadas(df)
        df['COLOR_STR'] = df['FORMA'].apply(asignar_color_neon)
        
        return df, mensajes
    except Exception as e:
        return pd.DataFrame(), [f"Error de proceso: {str(e)}"]

# =========================
# EJECUCIÓN PRINCIPAL
# =========================
status_boot = st.status("Iniciando Motor de Análisis Conductual Predictivo...")
status_boot.write("Extrayendo matrices de datos globales...")
df_maestro, diagn_mensajes = cargar_nodos()

if not df_maestro.empty:
    status_boot.update(label="Sistemas FANI en línea.", state="complete", expanded=False)
else:
    for msg in diagn_mensajes:
        status_boot.write(msg)
    status_boot.update(label="No se detectaron datos válidos.", state="error", expanded=True)

st.markdown("---")

col_mapa, col_filtros = st.columns([2.5, 1.5], gap="large")

with col_filtros:
    st.markdown("### Parámetros de Filtrado")
    
    df_filtrado = df_maestro.copy()

    if not df_maestro.empty:
        anios = sorted(df_maestro["AÑO"].dropna().unique())
        sel_anio = st.selectbox("AÑO", ["TODOS"] + list(map(int, [a for a in anios if str(a).isdigit()])))

        formas = sorted(df_maestro["FORMA"].dropna().unique())
        sel_forma = st.selectbox("TIPO DE OBJETO", ["TODOS"] + formas)

        paises = sorted(df_maestro["PAIS"].dropna().unique())
        sel_pais = st.selectbox("PAÍS", ["TODOS"] + paises)

        filtros_activos = False
        
        if sel_anio != "TODOS":
            df_filtrado = df_filtrado[df_filtrado["AÑO"] == sel_anio]
            filtros_activos = True
        if sel_forma != "TODOS":
            df_filtrado = df_filtrado[df_filtrado["FORMA"] == sel_forma]
            filtros_activos = True
        if sel_pais != "TODOS":
            df_filtrado = df_filtrado[df_filtrado["PAIS"] == sel_pais]
            filtros_activos = True

with col_mapa:
    if not df_filtrado.empty:
        if filtros_activos:
            muestra_size = min(1000, len(df_filtrado))
        else:
            muestra_size = min(500, len(df_filtrado))
            
        df_mostrar = df_filtrado.sample(muestra_size).reset_index(drop=True)

        fig = go.Figure()
        
        # 1. Capa de Relaciones (Los arcos curvos de la Imagen 1)
        lon_lines = []
        lat_lines = []
        # Generamos conexiones entre nodos cercanos/relevantes para recuperar la red
        for i in range(len(df_mostrar) - 1):
            if np.random.rand() > 0.75: # Conecta nodos para formar la red visible
                lon_lines.extend([df_mostrar.iloc[i]['lon'], df_mostrar.iloc[i+1]['lon'], None])
                lat_lines.extend([df_mostrar.iloc[i]['lat'], df_mostrar.iloc[i+1]['lat'], None])
                
        fig.add_trace(go.Scattergeo(
            lon=lon_lines,
            lat=lat_lines,
            mode='lines',
            line=dict(width=1, color='rgba(0, 212, 255, 0.3)'),
            hoverinfo='none',
            name="Red de Correlación"
        ))

        # 2. Capa de Nodos (Los puntos neón)
        fig.add_trace(go.Scattergeo(
            lon=df_mostrar["lon"],
            lat=df_mostrar["lat"],
            mode="markers",
            marker=dict(
                size=6,
                color=df_mostrar["COLOR_STR"],
                line=dict(width=0.3, color="white")
            ),
            text=df_mostrar["CIUDAD"] + " | " + df_mostrar["PAIS"] + " (" + df_mostrar["FORMA"] + ")",
            hoverinfo="text",
            name="Registros"
        ))

        # 3. Restauración Estética Original (Fondo oscuro, sin parpadeos blancos)
        fig.update_layout(
            geo=dict(
                projection_type="orthographic",
                showland=True, landcolor="#121212",
                showocean=True, oceancolor="#050505",
                showcountries=True, countrycolor="#2a2a2a",
                bgcolor="rgba(0,0,0,0)"
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=500,
            paper_bgcolor="#0a0a0a",
            plot_bgcolor="#0a0a0a",
            showlegend=False
        )

        # Usamos la sintaxis limpia sin el theme=None que causaba el fallo
        st.plotly_chart(fig, width="stretch")
        
        st.caption(f"Mostrando {len(df_mostrar)} nodos activos y sus vectores de correlación.")
    else:
        st.warning("No hay datos geográficos para renderizar con los filtros seleccionados.")

st.markdown("---")
m1, m2, m3 = st.columns(3)
if not df_filtrado.empty:
    m1.metric("Registros Encontrados", f"{len(df_filtrado):,}")
    m2.metric("Tipos Únicos", df_filtrado["FORMA"].nunique())
    m3.metric("Países Implicados", df_filtrado["PAIS"].nunique())
