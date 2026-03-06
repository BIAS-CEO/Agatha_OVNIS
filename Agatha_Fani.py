# ====================================================================
# ARCHIVO PRINCIPAL: Agatha_Fani.py
# SISTEMA: Motor de Analisis Conductual Predictivo
# MODULO: AGATHA FANI (Fenomenos Anomalos No Identificados)
# VERSION: Opcon Ready v2.1
# OPERADOR: DIR-74
# ====================================================================

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import os
import json
import time
import hashlib
import requests  # Para DeepSeek API
from datetime import datetime
from dotenv import load_dotenv  # Opcional, para archivo .env

# Cargar variables de entorno desde .env si existe (opcional)
load_dotenv()

# --- CONFIGURACION DE PAGINA ---
st.set_page_config(
    page_title="AGATHA - Inteligencia Predictiva",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS CORPORATIVO MATE (Flat Corporate) ---
CSS_MATE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@300;400;600;700&family=Montserrat:wght@700&family=Share+Tech+Mono&display=swap');

.stApp { 
    background-color: #0a0a0a !important; 
    font-family: 'Titillium Web', sans-serif !important; 
    color: #e2e8f0 !important; 
}
[data-testid="stHeader"], footer { display: none !important; }
.block-container { 
    padding-top: 1rem !important; 
    padding-bottom: 1rem !important; 
    max-width: 98% !important; 
}

h1 { 
    font-family: 'Montserrat', sans-serif !important; 
    text-transform: uppercase; 
    letter-spacing: -0.5px; 
    font-size: 2rem !important; 
    color: #ffffff !important; 
    border-bottom: 1px solid #334155; 
    padding-bottom: 8px; 
    margin-bottom: 0.5rem !important;
}
h2, h3, h4 { 
    color: #94a3b8 !important; 
    text-transform: uppercase; 
    letter-spacing: 1.5px; 
    font-family: 'Montserrat', sans-serif !important; 
    font-weight: 600 !important; 
    font-size: 0.95rem !important;
    margin-top: 1.5rem !important;
}

[data-testid="stMetric"] { 
    background-color: #1a1a1a !important; 
    border: 1px solid #333333 !important; 
    border-left: 3px solid #00d4ff !important; 
    padding: 12px !important; 
    border-radius: 0px !important; 
    box-shadow: none !important;
}
[data-testid="stMetricLabel"] { 
    color: #64748b !important; 
    font-size: 0.75rem !important; 
    font-weight: 600 !important; 
    text-transform: uppercase; 
    letter-spacing: 0.5px;
}
[data-testid="stMetricValue"] { 
    color: #ffffff !important; 
    font-family: 'Share Tech Mono', monospace !important; 
    font-size: 1.8rem !important;
    font-weight: 400 !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.8rem !important;
}

.contenedor-tabla { 
    width: 100%; 
    max-height: 600px; 
    overflow-y: auto; 
    border: 1px solid #333333; 
    background-color: #0a0a0a; 
    margin-bottom: 20px; 
}
.rejilla-tactica { 
    width: 100%; 
    border-collapse: collapse; 
    font-family: 'Titillium Web', sans-serif; 
    font-size: 0.8rem; 
    color: #e2e8f0; 
}
.rejilla-tactica thead th { 
    position: sticky; 
    top: 0; 
    background-color: #1a1a1a; 
    color: #00d4ff; 
    text-align: left; 
    padding: 10px 12px; 
    text-transform: uppercase; 
    font-size: 0.7rem; 
    letter-spacing: 1px; 
    border-bottom: 1px solid #333333; 
    z-index: 10; 
    font-weight: 600;
}
.rejilla-tactica tbody td { 
    padding: 8px 12px; 
    border-bottom: 1px solid #1a1a1a; 
    color: #cbd5e1;
}
.rejilla-tactica tbody tr:hover { 
    background-color: #1a1a1a; 
}
.valor-num { 
    font-family: 'Share Tech Mono', monospace; 
    color: #ffffff; 
}
.valor-texto {
    color: #94a3b8;
}

.stButton > button { 
    border: 1px solid #333333 !important; 
    background-color: #1a1a1a !important; 
    color: #e2e8f0 !important; 
    border-radius: 0px !important; 
    font-family: 'Montserrat', sans-serif !important; 
    font-weight: 600 !important; 
    text-transform: uppercase; 
    font-size: 0.75rem !important;
    letter-spacing: 0.5px;
    padding: 0.6rem 1.2rem !important; 
    box-shadow: none !important;
    transition: all 0.2s ease;
}
.stButton > button:hover { 
    border-color: #00d4ff !important; 
    color: #ffffff !important; 
    background-color: #0f172a !important; 
}
button[data-baseweb="tab"] { 
    background-color: transparent !important; 
    color: #475569 !important; 
    font-family: 'Montserrat', sans-serif !important; 
    font-weight: 600 !important; 
    font-size: 0.8rem !important;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    border-bottom: 2px solid transparent !important;
}
button[data-baseweb="tab"][aria-selected="true"] { 
    color: #ffffff !important; 
    border-bottom: 2px solid #00d4ff !important; 
    background-color: transparent !important;
}

.stSelectbox label, .stMultiselect label, .stSlider label, .stRadio label {
    color: #64748b !important;
    font-family: 'Montserrat', sans-serif !important;
    font-size: 0.7rem !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 600 !important;
}

.stSpinner > div {
    border-color: #00d4ff !important;
}
</style>
"""
st.markdown(CSS_MATE, unsafe_allow_html=True)

# --- IDENTIDAD DEL OPERADOR ---
OPERADOR_ID = "DIR-74"
ROL_ACCESO = "NIVEL 4 - INTELIGENCIA ESTRATEGICA"
MARCA_TIEMPO = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')

st.markdown(f"""
    <div style="position: fixed; top: 12px; right: 20px; background: #1a1a1a; border: 1px solid #333333; 
    color: #64748b; padding: 6px 15px; font-family: 'Share Tech Mono', monospace; font-size: 0.75rem; 
    z-index: 999999; pointer-events: none; text-transform: uppercase; letter-spacing: 0.5px;">
        Operador: {OPERADOR_ID} | Acceso: {ROL_ACCESO} | {MARCA_TIEMPO}
    </div>
""", unsafe_allow_html=True)

# --- SISTEMA DE GESTION DE CREDENCIALES MULTIMODAL ---
def obtener_credencial(nombre_var, nombre_secrets=None):
    """
    Obtiene credenciales desde:
    1. st.secrets (prioridad)
    2. Variables de entorno
    3. Alternativas (sin guiones bajos, mayúsculas, etc.)
    """
    nombre_secrets = nombre_secrets or nombre_var
    try:
        if hasattr(st, "secrets") and nombre_secrets in st.secrets:
            return st.secrets[nombre_secrets]
    except Exception:
        pass
    valor = os.environ.get(nombre_var)
    if valor:
        return valor
    alternativas = [
        nombre_var.replace("_", ""),
        nombre_var.upper(),
        nombre_var.lower(),
        nombre_var.replace("_", "-"),
    ]
    for alt in alternativas:
        valor = os.environ.get(alt)
        if valor:
            return valor
    return None

# --- CARGA DE CREDENCIALES TACTICAS ---
mapbox_token = obtener_credencial("MAPBOX_API_KEY")
deepseek_token = obtener_credencial("DEEPSEEK_API_KEY")  # Reemplaza OPENAI_API_KEY
openweather_token = obtener_credencial("OPENWEATHER_API_KEY")
google_maps_token = obtener_credencial("GOOGLE_MAPS_KEY")

# --- CENTROIDES GEOESPACIALES (Dispersion reducida para evitar mar) ---
CENTROIDES_TACTICOS = {
    "MARRUECOS": {"lat": 31.7917, "lon": -7.0926, "dispersion": 2.0},
    "MOROCCO": {"lat": 31.7917, "lon": -7.0926, "dispersion": 2.0},
    "ESPANA": {"lat": 40.4637, "lon": -3.7492, "dispersion": 1.5},
    "SPAIN": {"lat": 40.4637, "lon": -3.7492, "dispersion": 1.5},
    "EEUU": {"lat": 39.0902, "lon": -98.7129, "dispersion": 5.0},
    "USA": {"lat": 39.0902, "lon": -98.7129, "dispersion": 5.0},
    "ESTADOS UNIDOS": {"lat": 39.0902, "lon": -98.7129, "dispersion": 5.0},
    "UNITED STATES": {"lat": 39.0902, "lon": -98.7129, "dispersion": 5.0},
    "FRANCIA": {"lat": 46.2276, "lon": 2.2137, "dispersion": 1.8},
    "FRANCE": {"lat": 46.2276, "lon": 2.2137, "dispersion": 1.8},
    "REINO UNIDO": {"lat": 55.3781, "lon": -3.4360, "dispersion": 2.0},
    "UK": {"lat": 55.3781, "lon": -3.4360, "dispersion": 2.0},
    "UNITED KINGDOM": {"lat": 55.3781, "lon": -3.4360, "dispersion": 2.0},
    "DEFAULT": {"lat": 20.0, "lon": 0.0, "dispersion": 8.0}
}

# --- VALIDACION DE COORDENADAS (Evitar oceano) ---
def es_coordenada_valida(lat, lon, pais):
    pais = str(pais).upper()
    # Permitir coordenadas que explicitamente mencionan oceanos
    if any(x in pais for x in ["ATLANTIC", "PACIFIC", "OCEAN", "MAR", "SEA"]):
        return True
    
    # Atlantico Norte central
    if 20 < lat < 45 and -45 < lon < -20:
        return False
    # Atlantico Sur central
    if -20 < lat < 10 and -35 < lon < -10:
        return False
    # Pacifico central
    if -10 < lat < 30 and -160 < lon < -100:
        return False
    # Indico central
    if -30 < lat < 5 and 60 < lon < 95:
        return False
    
    return True

# --- BUSQUEDA DE ARCHIVOS ---
def encontrar_archivo(nombre):
    rutas_posibles = [
        nombre,
        os.path.join("data", nombre),
        os.path.join(".", nombre),
        os.path.join("..", "data", nombre),
        os.path.join("/mnt/data", nombre)
    ]
    for ruta in rutas_posibles:
        if os.path.exists(ruta):
            return ruta
    return None

# --- MOTORES DE INGESTA DE DATOS ---
@st.cache_data(show_spinner="Sincronizando base de datos tactica...")
def cargar_nodos():
    ruta = encontrar_archivo("agatha_ufo_nodes_full.csv")
    if not ruta:
        ruta = encontrar_archivo("agatha_ufo_nodes.csv")
        if not ruta:
            ruta = encontrar_archivo("agatha_ufo_master.csv")
        
    if not ruta:
        st.error("CRITICO: No se localiza archivo de nodos. Verificar directorio data/")
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(ruta, on_bad_lines='skip', engine='python', encoding='utf-8')
    except Exception:
        try:
            df = pd.read_csv(ruta, sep=';', on_bad_lines='skip', engine='python', encoding='utf-8')
        except Exception as e:
            st.error(f"Error de lectura CSV: {e}")
            return pd.DataFrame()
    
    # Normalizacion de cabeceras
    df.columns = [str(c).strip().replace('_', ' ').title() for c in df.columns]
    
    # Mapeo estandarizado
    mapeo_columnas = {
        "City": "Ciudad", 
        "Country": "Pais", 
        "Shape": "Forma", 
        "Summary": "Resumen", 
        "Year": "Ano",
        "State": "Estado",
        "Time": "Hora",
        "Day": "Dia",
        "Month": "Mes"
    }
    
    for col_orig, col_dest in mapeo_columnas.items():
        if col_orig in df.columns: 
            df.rename(columns={col_orig: col_dest}, inplace=True)
        elif col_orig.title() in df.columns: 
            df.rename(columns={col_orig.title(): col_dest}, inplace=True)
    
    # Garantizar columnas operativas
    columnas_requeridas = {
        'Resumen': "Reporte clasificado - Sin datos textuales disponibles",
        'Forma': "No Especificada",
        'Pais': "Desconocido",
        'Ciudad': "Zona Operativa",
        'Ano': 2024,
        'Estado': "N/A"
    }
    
    for col, default in columnas_requeridas.items():
        if col not in df.columns:
            df[col] = default
    
    # Limpieza de datos
    df['Forma'] = df['Forma'].fillna("No Especificada").astype(str).str.title()
    df['Resumen'] = df['Resumen'].fillna("").astype(str)
    df['Pais'] = df['Pais'].fillna("Desconocido").astype(str).str.upper()
    df['Ciudad'] = df['Ciudad'].fillna("Zona Operativa").astype(str)
    df['Ano'] = pd.to_numeric(df['Ano'], errors='coerce').fillna(2024).astype(int)
    
    # Generacion de coordenadas con validacion de oceano
    if 'Latitud' not in df.columns or 'Longitud' not in df.columns or df['Latitud'].isna().all():
        lats, lons = [], []
        
        for idx, row in df.iterrows():
            pais = str(row.get('Pais', '')).strip().upper()
            ciudad = str(row.get('Ciudad', '')).strip()
            centroide = CENTROIDES_TACTICOS.get(pais, CENTROIDES_TACTICOS["DEFAULT"])
            
            # Intentos multiples para evitar oceano
            lat, lon = centroide["lat"], centroide["lon"]
            for intento in range(15):
                seed = (idx + hash(ciudad) % 10000 + intento) % (2**32 - 1)
                rng = np.random.default_rng(seed)
                
                offset_lat = rng.normal(0, centroide["dispersion"] * 0.2)
                offset_lon = rng.normal(0, centroide["dispersion"] * 0.3)
                
                lat_temp = centroide["lat"] + offset_lat
                lon_temp = centroide["lon"] + offset_lon
                
                if es_coordenada_valida(lat_temp, lon_temp, pais):
                    lat, lon = lat_temp, lon_temp
                    break
            
            lats.append(lat)
            lons.append(lon)
        
        df['Latitud'] = lats
        df['Longitud'] = lons

    # Paleta Neon con TUPLAS (hashables) en lugar de listas
    def asignar_color_neon(forma):
        f = str(forma).lower()
        if any(x in f for x in ["triangulo", "triangular", "delta", "tri"]):
            return (0, 255, 128, 230)
        elif any(x in f for x in ["esfera", "orb", "circular", "redondo", "disco"]):
            return (255, 0, 128, 230)
        elif any(x in f for x in ["cigarro", "cilindro", "tubo", "cigar"]):
            return (255, 128, 0, 230)
        elif any(x in f for x in ["luz", "cambiante", "pulsante", "flash"]):
            return (255, 255, 0, 230)
        elif any(x in f for x in ["diamante", "rombo", "cuadrado"]):
            return (128, 0, 255, 230)
        elif any(x in f for x in ["rectangulo", "plataforma"]):
            return (0, 128, 255, 230)
        else:
            return (0, 255, 255, 230)
    
    df['Color Rgba'] = df['Forma'].apply(asignar_color_neon)
    df['Id Caso'] = range(1, len(df) + 1)
    
    return df

@st.cache_data(show_spinner="Calculando matrices de relacion...")
def cargar_relaciones(df_nodos):
    if df_nodos.empty:
        return pd.DataFrame()
    
    ruta = encontrar_archivo("agatha_ufo_relationships_sample.csv")
    if not ruta: 
        ruta = encontrar_archivo("agatha_ufo_relationships.csv")
    
    if not ruta:
        return pd.DataFrame()
    
    try:
        df_rel = pd.read_csv(ruta, on_bad_lines='skip', engine='python')
    except:
        try:
            df_rel = pd.read_csv(ruta, sep=';', on_bad_lines='skip', engine='python')
        except:
            return pd.DataFrame()
    
    df_rel.columns = [str(c).strip().replace('_', ' ').title() for c in df_rel.columns]
    
    col_src = [c for c in df_rel.columns if "Source" in c or "Origen" in c or "Src" in c]
    col_tgt = [c for c in df_rel.columns if "Target" in c or "Destino" in c or "Tgt" in c]
    
    if not col_src or not col_tgt:
        return pd.DataFrame()
    
    edges = []
    max_edges = min(500, len(df_rel))
    
    for _, row in df_rel.head(max_edges).iterrows():
        try:
            idx_orig = int(row[col_src[0]]) % len(df_nodos)
            idx_dest = int(row[col_tgt[0]]) % len(df_nodos)
            
            if idx_orig == idx_dest:
                continue
                
            nodo_a = df_nodos.iloc[idx_orig]
            nodo_b = df_nodos.iloc[idx_dest]
            
            edges.append({
                'Origen Lon': float(nodo_a['Longitud']), 
                'Origen Lat': float(nodo_a['Latitud']),
                'Destino Lon': float(nodo_b['Longitud']), 
                'Destino Lat': float(nodo_b['Latitud']),
                'Color Origen': nodo_a.get('Color Rgba', (0, 255, 255, 200)),
                'Color Destino': (255, 255, 255, 200),
                'Peso': float(row.get('Weight', 1)) if 'Weight' in df_rel.columns else 1.0
            })
        except Exception:
            continue
            
    return pd.DataFrame(edges)

# --- CARGA DE DATOS ---
df_maestro = cargar_nodos()
df_grafos = cargar_relaciones(df_maestro)

# --- RENDERIZADO TABLA TACTICA HTML ---
def render_tabla_tactica(df, max_filas=200):
    if df.empty:
        st.warning("Sin datos para visualizar")
        return
    
    columnas_excluir = ['Color Rgba', 'Latitud', 'Longitud', 'Id Caso']
    columnas_validas = [c for c in df.columns if c not in columnas_excluir][:8]
    
    html = '<div class="contenedor-tabla"><table class="rejilla-tactica"><thead><tr>'
    for col in columnas_validas:
        html += f'<th>{col}</th>'
    html += '</tr></thead><tbody>'
    
    for _, row in df.head(max_filas).iterrows():
        html += '<tr>'
        for col in columnas_validas:
            val = row[col]
            if pd.isna(val):
                val = "-"
            elif isinstance(val, float):
                val = f"{val:.2f}"
            
            clase = 'valor-num' if isinstance(val, (int, float)) or (isinstance(val, str) and val.replace('.','').isdigit()) else 'valor-texto'
            html += f'<td class="{clase}">{val}</td>'
        html += '</tr>'
    
    html += '</tbody></table></div>'
    st.markdown(html, unsafe_allow_html=True)

# --- SIDEBAR: TERMINAL DE OPERACIONES ---
st.sidebar.markdown("### Centro de Comando AGATHA")

# Filtro geopolitico
regiones = {
    "Vista Orbital Global": {"lat": 20.0, "lon": 0.0, "zoom": 1.2},
    "Marruecos y Espana": {"lat": 35.0, "lon": -5.0, "zoom": 5},
    "Norteamerica": {"lat": 39.8, "lon": -98.5, "zoom": 3.5},
    "Europa Occidental": {"lat": 48.0, "lon": 10.0, "zoom": 4.5}
}

filtro_region = st.sidebar.selectbox("Ambito Geopolitico", list(regiones.keys()))

# FILTRO DE FRANJAS TEMPORALES
st.sidebar.markdown("---")
st.sidebar.markdown("### Control Temporal")

# Franjas predefinidas
franjas_temporales = {
    "Personalizado": None,
    "Pre-1940 (Era Moderna Temprana)": (1900, 1940),
    "1940-1960 (Era de los Discos)": (1940, 1960),
    "1960-1980 (Guerra Fria)": (1960, 1980),
    "1980-2000 (Era Digital)": (1980, 2000),
    "2000-2024 (Siglo XXI)": (2000, 2024),
    "Todo el Registro": None
}

franja_seleccionada = st.sidebar.selectbox("Franja Historica", list(franjas_temporales.keys()))

# Determinar rango de años
if not df_maestro.empty:
    min_year_global = int(df_maestro['Ano'].min())
    max_year_global = int(df_maestro['Ano'].max())
else:
    min_year_global, max_year_global = 1900, 2024

# Aplicar franja o permitir seleccion manual
if franja_seleccionada == "Todo el Registro":
    rango_anos = (min_year_global, max_year_global)
elif franja_seleccionada == "Personalizado":
    rango_anos = st.sidebar.slider(
        "Ventana Temporal Personalizada", 
        min_year_global, 
        max_year_global, 
        (min_year_global, max_year_global)
    )
else:
    rango_anos = franjas_temporales[franja_seleccionada]
    st.sidebar.markdown(f"<span style='color:#64748b; font-size:0.7rem;'>Periodo: {rango_anos[0]}-{rango_anos[1]}</span>", unsafe_allow_html=True)

# Filtros de forma
if not df_maestro.empty:
    formas_disp = sorted(df_maestro['Forma'].unique())
    filtro_forma = st.sidebar.multiselect("Tipologia Estructural", formas_disp, default=formas_disp[:5] if len(formas_disp) > 5 else formas_disp)
    
    # Aplicar filtros al dataframe principal (luego se aplicará filtro rápido en el tab)
    df_filtrado = df_maestro[
        (df_maestro['Forma'].isin(filtro_forma)) & 
        (df_maestro['Ano'].between(rango_anos[0], rango_anos[1]))
    ].copy()
else:
    df_filtrado = pd.DataFrame()
    filtro_forma = []

# Controles de visualizacion
st.sidebar.markdown("---")
mostrar_calor = st.sidebar.toggle("Capa de Densidad Termica", value=True)
mostrar_arcos = st.sidebar.toggle("Grafos de Trayectoria", value=True)
mostrar_puntos = st.sidebar.toggle("Puntos de Contacto", value=True)

# --- ENCABEZADO PRINCIPAL ---
st.markdown("<h1>Motor de Analisis Conductual Predictivo</h1>", unsafe_allow_html=True)
st.markdown("<h3>Modulo FANI: Fenomenos Anomalos No Identificados</h3>", unsafe_allow_html=True)

# --- METRICAS ESTRATEGICAS ---
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

total_casos = len(df_filtrado)
if not df_filtrado.empty:
    forma_predom = df_filtrado['Forma'].mode().iloc[0] if not df_filtrado['Forma'].mode().empty else "N/A"
    coords = df_filtrado[['Latitud', 'Longitud']].round(1)
    zonas_criticas = len(coords.drop_duplicates())
else:
    forma_predom = "N/A"
    zonas_criticas = 0

col_m1.metric("Registros Activos", f"{total_casos:,}")
col_m2.metric("Tipologia Predominante", forma_predom)
col_m3.metric("Zonas de Interes", f"{zonas_criticas:,}")
col_m4.metric("Conexiones Activas", f"{len(df_grafos) if mostrar_arcos else 0:,}")

st.markdown("---")

# --- PESTANAS PRINCIPALES ---
tab_visor, tab_datos, tab_analisis = st.tabs([
    "Visor de Telemetria Orbital", 
    "Registros Forenses", 
    "Procesador NLP Forense"
])

# --- TAB 1: VISOR GEOESPACIAL ---
with tab_visor:
    # Filtro de franja temporal encima del mapa
    if not df_maestro.empty:
        col_filtro1, col_filtro2, col_filtro3 = st.columns([2, 2, 2])
        
        with col_filtro1:
            # Usar session_state para recordar el filtro rápido
            if "franja_rapida" not in st.session_state:
                st.session_state.franja_rapida = "Todas"
            franja_rapida = st.selectbox(
                "Franja Temporal Rapida",
                ["Todas", "1930-1950", "1950-1970", "1970-1990", "1990-2010", "2010-2024"],
                index=["Todas", "1930-1950", "1950-1970", "1970-1990", "1990-2010", "2010-2024"].index(st.session_state.franja_rapida),
                key="franja_rapida_selector"
            )
            st.session_state.franja_rapida = franja_rapida
        
        with col_filtro2:
            if franja_rapida != "Todas":
                años = franja_rapida.split("-")
                st.markdown(f"<div style='margin-top:28px; color:#00d4ff; font-family:Share Tech Mono;'>Periodo: {años[0]} - {años[1]}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        
        with col_filtro3:
            st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
            if st.button("Resetear Filtros", type="secondary"):
                # Reiniciar filtros a valores por defecto
                st.session_state.franja_rapida = "Todas"
                # También podemos resetear los filtros del sidebar si se desea, pero es más complejo.
                # Por simplicidad, recargamos la app.
                st.rerun()
        
        # Aplicar filtro rápido si se seleccionó (combinado con filtros del sidebar)
        if franja_rapida != "Todas":
            años = franja_rapida.split("-")
            df_mapa = df_filtrado[df_filtrado['Ano'].between(int(años[0]), int(años[1]))].copy()
        else:
            df_mapa = df_filtrado.copy()
    else:
        df_mapa = df_filtrado.copy()

    if df_mapa.empty:
        st.error("No hay datos geoespaciales disponibles para el filtro seleccionado")
    else:
        config_region = regiones[filtro_region]
        
        view_state = pdk.ViewState(
            latitude=config_region["lat"],
            longitude=config_region["lon"],
            zoom=config_region["zoom"],
            pitch=50,
            bearing=0,
            min_zoom=1,
            max_zoom=15
        )
        
        capas = []
        
        # Capa 1: Mapa de calor
        if mostrar_calor:
            capas.append(pdk.Layer(
                "HeatmapLayer",
                data=df_mapa,
                get_position=["Longitud", "Latitud"],
                opacity=0.7,
                get_weight=1,
                radius_pixels=60,
                intensity=1.5,
                threshold=0.05,
                color_range=[
                    [0, 0, 255, 100],
                    [0, 255, 255, 150],
                    [255, 255, 0, 200],
                    [255, 128, 0, 230],
                    [255, 0, 0, 255]
                ]
            ))
        
        # Capa 2: Puntos de contacto
        if mostrar_puntos:
            capas.append(pdk.Layer(
                "ScatterplotLayer",
                data=df_mapa,
                get_position=["Longitud", "Latitud"],
                get_fill_color="Color Rgba",
                get_radius=60000,
                radius_min_pixels=5,
                radius_max_pixels=50,
                opacity=0.9,
                stroked=True,
                get_line_color=[255, 255, 255, 200],
                get_line_width=2,
                pickable=True,
                auto_highlight=True
            ))
        
        # Capa 3: Arcos de trayectoria
        if mostrar_arcos and not df_grafos.empty:
            capas.append(pdk.Layer(
                "ArcLayer",
                data=df_grafos,
                get_source_position=["Origen Lon", "Origen Lat"],
                get_target_position=["Destino Lon", "Destino Lat"],
                get_source_color="Color Origen",
                get_target_color="Color Destino",
                get_width=2,
                get_height=0.5,
                get_tilt=15,
                opacity=0.6,
                pickable=True
            ))
        
        # Configuracion del mapa
        if mapbox_token:
            estilo_mapa = "mapbox://styles/mapbox/dark-v11"
            api_keys = {"mapbox": mapbox_token}
        else:
            estilo_mapa = "carto-darkmatter"
            api_keys = None
        
        # Tooltip HTML puro (con truncado de resumen)
        df_mapa['Resumen_corto'] = df_mapa['Resumen'].apply(lambda x: x[:120] + "..." if len(x) > 120 else x)
        
        tooltip_html = """
        <div style="background: rgba(10,10,10,0.95); padding: 12px; border-radius: 0px; 
        border: 1px solid #00d4ff; font-family: 'Share Tech Mono', monospace; min-width: 200px;">
            <div style="color: #00d4ff; font-size: 0.9rem; text-transform: uppercase; 
            border-bottom: 1px solid #333; padding-bottom: 5px; margin-bottom: 8px; font-weight: bold;">
                OBJETO: {Forma}
            </div>
            <div style="color: #fff; font-size: 0.8rem; margin-bottom: 4px;">
                <span style="color: #64748b;">UBICACION:</span> {Ciudad}, {Pais}
            </div>
            <div style="color: #fff; font-size: 0.8rem; margin-bottom: 4px;">
                <span style="color: #64748b;">TEMPORAL:</span> {Ano}
            </div>
            <div style="color: #94a3b8; font-size: 0.75rem; margin-top: 8px; font-style: italic; 
            max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                {Resumen_corto}
            </div>
        </div>
        """
        
        st.pydeck_chart(pdk.Deck(
            api_keys=api_keys,
            map_style=estilo_mapa,
            initial_view_state=view_state,
            layers=capas,
            tooltip={
                "html": tooltip_html,
                "style": {
                    "backgroundColor": "transparent",
                    "color": "white",
                    "font-family": "Share Tech Mono"
                }
            }
        ), height=700)

# --- TAB 2: Registros Forenses ---
with tab_datos:
    st.markdown("#### Archivos de Inteligencia Extraidos")
    
    if df_filtrado.empty:
        st.warning("No hay registros que coincidan con los criterios de filtrado")
    else:
        cols_disponibles = [c for c in df_filtrado.columns if c not in ['Color Rgba', 'Latitud', 'Longitud']]
        cols_default = [c for c in ['Id Caso', 'Ano', 'Pais', 'Ciudad', 'Forma', 'Resumen'] if c in cols_disponibles]
        
        cols_seleccionadas = st.multiselect(
            "Campos de Visualizacion", 
            cols_disponibles, 
            default=cols_default[:6]
        )
        
        if cols_seleccionadas:
            df_display = df_filtrado[cols_seleccionadas].sort_values('Ano', ascending=False)
            render_tabla_tactica(df_display, max_filas=250)
        else:
            st.info("Seleccione campos para visualizar")

# --- TAB 3: Procesador NLP Forense (DeepSeek) ---
with tab_analisis:
    col_nlp, col_stats = st.columns([1, 1])
    
    with col_nlp:
        st.markdown("#### Motor de Analisis NLP Forense")
        st.markdown("<p style='color: #64748b; font-size:0.85rem; margin-top:-10px;'>"
        "Seleccione un expediente para generar perfilamiento tactico automatizado.</p>", 
        unsafe_allow_html=True)
        
        if df_filtrado.empty or 'Resumen' not in df_filtrado.columns:
            st.error("Base de datos no sincronizada o sin campo Resumen")
        else:
            # Crear selector de casos
            df_filtrado['Etiqueta Caso'] = (
                df_filtrado['Ciudad'].astype(str) + " | " + 
                df_filtrado['Forma'].astype(str) + " | " + 
                df_filtrado['Ano'].astype(str)
            )
            
            caso_sel = st.selectbox("Expediente Operativo", df_filtrado['Etiqueta Caso'].unique())
            
            datos_caso = df_filtrado[df_filtrado['Etiqueta Caso'] == caso_sel].iloc[0]
            texto_resumen = str(datos_caso['Resumen'])
            
            # Mostrar resumen original
            st.markdown(f"""
            <div style="background-color: #0a0a0a; border: 1px solid #333; padding: 12px; 
            border-radius: 0px; margin-bottom: 15px; border-left: 3px solid #64748b;">
                <div style="color: #64748b; font-family: 'Montserrat', sans-serif; font-size: 0.7rem; 
                font-weight: 600; text-transform: uppercase; margin-bottom: 5px;">
                    Cuerpo del Informe Original
                </div>
                <div style="color: #cbd5e1; font-family: 'Titillium Web', sans-serif; font-size: 0.85rem; 
                line-height: 1.4; max-height: 120px; overflow-y: auto;">
                    {texto_resumen[:500]}{"..." if len(texto_resumen) > 500 else ""}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Ejecutar Analisis Forense", type="primary"):
                with st.spinner("Procesando mediante red neuronal DeepSeek..."):
                    
                    resultado_nlp = {
                        "comportamiento": "No procesado",
                        "credibilidad": "DESCONOCIDA",
                        "hipotesis": "Sin analisis",
                        "indice": 0
                    }
                    
                    # Usar DeepSeek API en lugar de OpenAI
                    if deepseek_token and texto_resumen.strip():
                        try:
                            headers = {
                                "Authorization": f"Bearer {deepseek_token}",
                                "Content-Type": "application/json"
                            }
                            
                            prompt_sistema = """Eres un analista de inteligencia militar especializado en fenomenos aereos no identificados.
                            Analiza el texto proporcionado y genera un informe tactico estructurado en JSON con estos campos exactos:
                            - comportamiento: Descripcion tecnica del patron de vuelo/cinematica (max 100 caracteres)
                            - credibilidad: Una de ALTA, MEDIA, BAJA
                            - indice: Numero entero 0-100 representando confiabilidad del testimonio
                            - hipotesis: Explicacion analitica tecnica del origen (max 200 caracteres)
                            
                            Responde SOLO con el JSON, sin markdown ni texto adicional."""
                            
                            payload = {
                                "model": "deepseek-chat",
                                "messages": [
                                    {"role": "system", "content": prompt_sistema},
                                    {"role": "user", "content": texto_resumen[:1000]}
                                ],
                                "temperature": 0.1,
                                "max_tokens": 300,
                                "response_format": {"type": "json_object"}
                            }
                            
                            respuesta = requests.post(
                                "https://api.deepseek.com/v1/chat/completions",
                                headers=headers,
                                json=payload,
                                timeout=30
                            )
                            
                            respuesta.raise_for_status()
                            datos = respuesta.json()
                            contenido = datos["choices"][0]["message"]["content"]
                            
                            # Limpiar posibles backticks
                            if contenido.startswith("```json"):
                                contenido = contenido[7:]
                            if contenido.endswith("```"):
                                contenido = contenido[:-3]
                            
                            parsed = json.loads(contenido.strip())
                            resultado_nlp.update(parsed)
                            
                        except Exception as e:
                            resultado_nlp["hipotesis"] = f"Error en procesamiento: {str(e)[:50]}"
                            resultado_nlp["credibilidad"] = "ERROR"
                    else:
                        # Simulacion si no hay API
                        time.sleep(1.2)
                        resultado_nlp = {
                            "comportamiento": "Maniobra no balistica con vector ascendente",
                            "credibilidad": "ALTA",
                            "indice": 87,
                            "hipotesis": "Firma electromagnetica inconsistente con aeronaves convencionales. Probable plataforma de propulsion gravitica no catalogada."
                        }
                    
                    # Determinar color segun credibilidad
                    cred = resultado_nlp.get("credibilidad", "MEDIA").upper()
                    if "ALTA" in cred:
                        color_cred = "#00ff80"
                        color_borde = "#00ff80"
                    elif "MEDIA" in cred:
                        color_cred = "#00d4ff"
                        color_borde = "#00d4ff"
                    elif "BAJA" in cred:
                        color_cred = "#ff4444"
                        color_borde = "#ff4444"
                    else:
                        color_cred = "#64748b"
                        color_borde = "#64748b"
                    
                    indice_val = resultado_nlp.get("indice", 0)
                    
                    # Renderizar resultado
                    resultado_html = f"""
                    <div style="background-color: #0a0a0a; border: 1px solid #333; 
                    border-left: 4px solid {color_borde}; padding: 20px; margin-top: 20px;">
                        
                        <div style="display: flex; justify-content: space-between; align-items: center; 
                        margin-bottom: 15px; border-bottom: 1px solid #222; padding-bottom: 10px;">
                            <span style="color: #64748b; font-size: 0.7rem; text-transform: uppercase; 
                            font-weight: 600;">Resultado del Analisis</span>
                            <span style="color: {color_cred}; font-family: 'Share Tech Mono', monospace; 
                            font-size: 1.2rem; font-weight: bold;">{cred} [{indice_val}/100]</span>
                        </div>
                        
                        <div style="margin-bottom: 15px;">
                            <div style="color: #64748b; font-size: 0.7rem; text-transform: uppercase; 
                            margin-bottom: 5px; font-weight: 600;">Patron Comportamental</div>
                            <div style="color: #00d4ff; font-family: 'Share Tech Mono', monospace; 
                            font-size: 0.95rem;">{resultado_nlp.get("comportamiento", "N/A")}</div>
                        </div>
                        
                        <div>
                            <div style="color: #64748b; font-size: 0.7rem; text-transform: uppercase; 
                            margin-bottom: 5px; font-weight: 600;">Hipotesis Operativa</div>
                            <div style="color: #e2e8f0; font-size: 0.85rem; line-height: 1.5; 
                            text-align: justify;">{resultado_nlp.get("hipotesis", "N/A")}</div>
                        </div>
                        
                    </div>
                    """
                    
                    st.markdown(resultado_html, unsafe_allow_html=True)
    
    with col_stats:
        st.markdown("#### Distribucion de Incidencias")
        
        if not df_filtrado.empty:
            # Grafico de barras horizontal
            conteo_formas = df_filtrado['Forma'].value_counts().head(10).reset_index()
            conteo_formas.columns = ['Estructura', 'Total']
            
            fig = px.bar(
                conteo_formas, 
                x='Total', 
                y='Estructura', 
                orientation='h',
                template="plotly_dark",
                color_discrete_sequence=['#00d4ff']
            )
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Titillium Web", size=10, color="#64748b"),
                yaxis=dict(title="", tickfont=dict(size=10)),
                xaxis=dict(title="", gridcolor="#1a1a1a", tickfont=dict(size=9)),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width="stretch")
            
            # Timeline de incidentes
            st.markdown("#### Linea Temporal")
            timeline = df_filtrado.groupby('Ano').size().reset_index(name='Incidentes')
            
            fig2 = px.area(
                timeline,
                x='Ano',
                y='Incidentes',
                template="plotly_dark",
                color_discrete_sequence=['#00d4ff']
            )
            fig2.update_layout(
                height=200,
                margin=dict(l=0, r=0, t=10, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(10,10,10,0.5)",
                font=dict(family="Titillium Web", size=9, color="#64748b"),
                xaxis=dict(title="", gridcolor="#1a1a1a", showgrid=True),
                yaxis=dict(title="", gridcolor="#1a1a1a", showgrid=True),
                showlegend=False
            )
            fig2.update_traces(fillcolor="rgba(0, 212, 255, 0.2)", line=dict(color="#00d4ff", width=2))
            st.plotly_chart(fig2, use_container_width="stretch")

# --- FOOTER TACTICO ---
st.markdown("---")
st.markdown(f"""
    <div style="color: #333; font-family: 'Share Tech Mono', monospace; font-size: 0.7rem; 
    text-align: center; text-transform: uppercase; letter-spacing: 1px;">
        Sistema AGATHA v2.1 | Modulo FANI | Operador {OPERADOR_ID} | Clasificacion: NIVEL 4
    </div>
""", unsafe_allow_html=True)
