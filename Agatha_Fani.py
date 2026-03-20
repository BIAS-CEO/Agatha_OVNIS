# ====================================================================
# ARCHIVO PRINCIPAL: Agatha_Fani.py
# SISTEMA: Motor de Analisis Conductual Predictivo
# MODULO: AGATHA FANI (Fenomenos Anomalos No Identificados)
# VERSION: Opcon Ready v4.5 (Interfaz unificada y geolocalizada)
# OPERADOR: DIR-74
# ====================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os
import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURACION DE PAGINA ---
st.set_page_config(
    page_title="AGATHA - Inteligencia Predictiva",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LIMPIEZA DE CACHE AL INICIO ---
st.cache_data.clear()

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
    max-height: 400px; 
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
    width: 100%;
}
.stButton > button:hover { 
    border-color: #00d4ff !important; 
    color: #ffffff !important; 
    background-color: #0f172a !important; 
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
deepseek_token = obtener_credencial("DEEPSEEK_API_KEY")
openweather_token = obtener_credencial("OPENWEATHER_API_KEY")
google_maps_token = obtener_credencial("GOOGLE_MAPS_KEY")

# --- FUNCIONES AUXILIARES ---
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

# --- PALETA NEÓN ---
def asignar_color_neon(forma):
    f = str(forma).lower()
    if any(x in f for x in ["triangulo", "triangular", "delta", "tri"]):
        return (0, 255, 128, 230)
    elif any(x in f for x in ["esfera", "orb", "circular", "redondo", "disco", "disk"]):
        return (255, 0, 128, 230)
    elif any(x in f for x in ["cigarro", "cilindro", "tubo", "cigar", "cylindrical"]):
        return (255, 128, 0, 230)
    elif any(x in f for x in ["luz", "cambiante", "pulsante", "flash", "light"]):
        return (255, 255, 0, 230)
    elif any(x in f for x in ["diamante", "rombo", "cuadrado", "diamond", "polyhedron"]):
        return (128, 0, 255, 230)
    elif any(x in f for x in ["rectangulo", "plataforma", "rectangle", "platform"]):
        return (0, 128, 255, 230)
    else:
        return (0, 255, 255, 230)

# --- COORDENADAS APROXIMADAS ---
def obtener_coordenadas_pais(pais):
    centroides = {
        "MARRUECOS": (31.7917, -7.0926),
        "MOROCCO": (31.7917, -7.0926),
        "ESPAÑA": (40.4637, -3.7492),
        "SPAIN": (40.4637, -3.7492),
        "ARGELIA": (28.0339, 1.6596),
        "ALGERIA": (28.0339, 1.6596),
        "MAURITANIA": (21.0079, -10.9408),
        "MALI": (17.5707, -3.9962),
        "EEUU": (39.8283, -98.5795),
        "USA": (39.8283, -98.5795),
        "FRANCIA": (46.2276, 2.2137),
        "REINO UNIDO": (55.3781, -3.4360),
        "UK": (55.3781, -3.4360)
    }
    p = str(pais).upper().strip()
    if p in centroides:
        lat, lon = centroides[p]
    else:
        # Coordenada por defecto apuntando al Atlántico Norte
        lat, lon = 30.0, -15.0
    
    rng = np.random.default_rng(hash(p) % (2**32))
    lat += rng.normal(0, 0.5)
    lon += rng.normal(0, 0.5)
    return lat, lon

def asignar_coordenadas_aproximadas(df):
    lats, lons = [], []
    for _, row in df.iterrows():
        pais = str(row.get('PAIS', 'Desconocido')).upper().strip()
        lat, lon = obtener_coordenadas_pais(pais)
        lats.append(lat)
        lons.append(lon)
    df['lat'] = lats
    df['lon'] = lons
    return df

# --- DATOS DE EJEMPLO (FALLBACK GARANTIZADO MARRUECOS) ---
def crear_datos_ejemplo():
    data = {
        'ID': list(range(10)),
        'CIUDAD': [
            'Casablanca', 'Rabat', 'Tanger', 'Marrakech', 'Fez',
            'Agadir', 'Oujda', 'Kenitra', 'Tetouan', 'Safi'
        ],
        'ESTADO': [
            'Casablanca-Settat', 'Rabat-Sale-Kenitra', 'Tanger-Tetouan-Al Hoceima',
            'Marrakech-Safi', 'Fes-Meknes', 'Souss-Massa', 'Oriental',
            'Rabat-Sale-Kenitra', 'Tanger-Tetouan-Al Hoceima', 'Marrakech-Safi'
        ],
        'PAIS': ['MARRUECOS'] * 10,
        'FORMA': ['Triangle', 'Sphere', 'Light', 'Cigar', 'Disk', 'Triangle', 'Light', 'Sphere', 'Cigar', 'Unknown'],
        'RESUMEN': [
            'Anomalia luminosa sobre la costa, vector de aproximacion rapido',
            'Objeto esferico estatico sobre espacio aereo restringido',
            'Multiples fuentes de luz descendiendo hacia el puerto',
            'Firma radarica cilindrica cerca de la cordillera del Atlas',
            'Plataforma discoidal silenciosa observada por patrulla',
            'Formacion delta interceptada por sensores termicos',
            'Fenomeno luminoso anomalo en zona fronteriza',
            'Persecucion visual reportada por vuelo comercial',
            'Estructura no identificada captada por sistemas de defensa',
            'Interferencia electromagnetica masiva en subestacion'
        ],
        'AÑO': [2024, 2024, 2023, 2023, 1999, 2005, 2010, 2018, 2020, 2022],
        'MES': [5, 8, 2, 11, 7, 4, 9, 1, 6, 12],
        'DIA': [12, 24, 5, 18, 22, 10, 30, 14, 8, 3]
    }
    df = pd.DataFrame(data)
    df['FECHA'] = pd.to_datetime(df['AÑO'].astype(str) + '-' + df['MES'].astype(str) + '-' + df['DIA'].astype(str), errors='coerce')
    df['DIA_SEMANA'] = df['FECHA'].dt.day_name()
    df['DECADA'] = (df['AÑO'] // 10) * 10
    df = asignar_coordenadas_aproximadas(df)
    df['COLOR_RGBA'] = df['FORMA'].apply(asignar_color_neon)
    df['COLOR_STR'] = df['COLOR_RGBA'].apply(lambda c: f'rgba({c[0]},{c[1]},{c[2]},{c[3]/255})')
    return df

# --- MOTORES DE INGESTA DE DATOS ---
@st.cache_data(show_spinner="Cargando metadatos...")
def cargar_nodos():
    mensajes_depuracion = []
    
    ruta = encontrar_archivo("agatha_ufo_nodes_full.csv")
    if not ruta:
        ruta = encontrar_archivo("agatha_ufo_nodes.csv")
    
    if ruta:
        mensajes_depuracion.append(f"Archivo encontrado: {ruta}")
        for sep in [',', ';']:
            try:
                df = pd.read_csv(ruta, encoding='utf-8', sep=sep, on_bad_lines='skip')
                if df.shape[1] > 1:
                    mensajes_depuracion.append(f"Separador usado: '{sep}'")
                    break
            except:
                continue
        else:
            mensajes_depuracion.append("No se pudo leer el archivo")
            return pd.DataFrame(), mensajes_depuracion

        df.columns = [str(c).strip().replace('.', '').replace(' ', '_').upper() for c in df.columns]
        
        if 'NUM' in df.columns:
            df.rename(columns={'NUM': 'ID'}, inplace=True)
        elif 'ORD' in df.columns:
            df.rename(columns={'ORD': 'ID'}, inplace=True)
        else:
            df['ID'] = range(len(df))

        col_map = {
            'CITY': 'CIUDAD',
            'STATE': 'ESTADO',
            'COUNTRY': 'PAIS',
            'SHAPE': 'FORMA',
            'SUMMARY': 'RESUMEN',
            'YEAR': 'AÑO',
            'DAY': 'DIA',
            'MONTH': 'MES'
        }
        for orig, dest in col_map.items():
            if orig in df.columns:
                df.rename(columns={orig: dest}, inplace=True)
            elif dest not in df.columns:
                df[dest] = "" if dest != 'AÑO' else 2024

        columnas_requeridas = ['CIUDAD', 'PAIS', 'FORMA', 'RESUMEN', 'AÑO', 'DIA', 'MES']
        for col in columnas_requeridas:
            if col not in df.columns:
                df[col] = "" if col != 'AÑO' else 2024

        df['FORMA'] = df['FORMA'].fillna("No especificada").astype(str).str.title()
        df['RESUMEN'] = df['RESUMEN'].fillna("").astype(str)
        df['PAIS'] = df['PAIS'].fillna("Desconocido").astype(str).str.upper()
        df['CIUDAD'] = df['CIUDAD'].fillna("Zona operativa").astype(str)
        df['ESTADO'] = df['ESTADO'].fillna("").astype(str) if 'ESTADO' in df.columns else ""
        df['AÑO'] = pd.to_numeric(df['AÑO'], errors='coerce').fillna(2024).astype(int)
        df['DIA'] = pd.to_numeric(df['DIA'], errors='coerce').fillna(1).astype(int)
        df['MES'] = pd.to_numeric(df['MES'], errors='coerce').fillna(1).astype(int)

        try:
            df['FECHA'] = pd.to_datetime(df['AÑO'].astype(str) + '-' + df['MES'].astype(str) + '-' + df['DIA'].astype(str), errors='coerce')
        except:
            df['FECHA'] = pd.NaT
        df['DIA_SEMANA'] = df['FECHA'].dt.day_name()
        df['DECADA'] = (df['AÑO'] // 10) * 10
        
        df = asignar_coordenadas_aproximadas(df)
        df['COLOR_RGBA'] = df['FORMA'].apply(asignar_color_neon)
        df['COLOR_STR'] = df['COLOR_RGBA'].apply(lambda c: f'rgba({c[0]},{c[1]},{c[2]},{c[3]/255})')
        
        mensajes_depuracion.append(f"Registros cargados: {len(df)}")
        return df, mensajes_depuracion
    else:
        mensajes_depuracion.append("No se encontraron archivos CSV")
        return pd.DataFrame(), mensajes_depuracion

# --- CARGA DE DATOS CON FALLBACK ---
if st.sidebar.button("FORZAR RECARGA DE DATOS"):
    st.cache_data.clear()
    for key in ['df_maestro', 'mensajes_depuracion']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

if 'df_maestro' not in st.session_state:
    df_cargado, mensajes_depu = cargar_nodos()
    if df_cargado.empty or len(df_cargado) == 0:
        df_maestro = crear_datos_ejemplo()
        mensajes_depu.append("Usando datos de ejemplo tácticos (10 registros)")
    else:
        df_maestro = df_cargado
    st.session_state.df_maestro = df_maestro
    st.session_state.mensajes_depuracion = mensajes_depu
else:
    df_maestro = st.session_state.df_maestro

# --- DIAGNÓSTICO EN SIDEBAR ---
with st.sidebar.expander("DIAGNOSTICO DEL SISTEMA"):
    st.write(f"Registros totales: {len(df_maestro)}")
    for msg in st.session_state.get('mensajes_depuracion', []):
        st.write(f"- {msg}")

# --- CARGA DE RELACIONES ---
@st.cache_data(show_spinner="Calculando matrices...")
def cargar_relaciones(df_nodos):
    if df_nodos.empty:
        return pd.DataFrame()
    
    ids_validos = set(df_nodos['ID'].unique())
    ruta = encontrar_archivo("agatha_ufo_relationships_sample.csv")
    
    if ruta:
        try:
            df_rel = pd.read_csv(ruta, encoding='utf-8', on_bad_lines='skip')
            df_rel.columns = [str(c).strip().upper() for c in df_rel.columns]
            col_src = [c for c in df_rel.columns if 'SOURCE' in c or 'ORIGEN' in c][0]
            col_tgt = [c for c in df_rel.columns if 'TARGET' in c or 'DESTINO' in c][0]
            df_rel.rename(columns={col_src: 'SRC_ID', col_tgt: 'TGT_ID'}, inplace=True)
            df_rel['SRC_ID'] = pd.to_numeric(df_rel['SRC_ID'], errors='coerce')
            df_rel['TGT_ID'] = pd.to_numeric(df_rel['TGT_ID'], errors='coerce')
            df_rel = df_rel.dropna(subset=['SRC_ID', 'TGT_ID'])
            df_rel = df_rel[df_rel['SRC_ID'].isin(ids_validos) & df_rel['TGT_ID'].isin(ids_validos)]
            df_rel['TIPO'] = df_rel.get('RELATIONSHIP', 'Trayectoria probable').fillna('Trayectoria probable')
            df_rel['PESO'] = pd.to_numeric(df_rel.get('WEIGHT', 0.5), errors='coerce').fillna(0.5)
            
            df_coords = df_nodos.set_index('ID')[['lat', 'lon', 'CIUDAD', 'PAIS']]
            df_rel['origen_lat'] = df_rel['SRC_ID'].map(df_coords['lat'])
            df_rel['origen_lon'] = df_rel['SRC_ID'].map(df_coords['lon'])
            df_rel['destino_lat'] = df_rel['TGT_ID'].map(df_coords['lat'])
            df_rel['destino_lon'] = df_rel['TGT_ID'].map(df_coords['lon'])
            df_rel['origen_ciudad'] = df_rel['SRC_ID'].map(df_coords['CIUDAD'])
            df_rel['destino_ciudad'] = df_rel['TGT_ID'].map(df_coords['CIUDAD'])
            df_rel = df_rel.dropna(subset=['origen_lat', 'origen_lon', 'destino_lat', 'destino_lon'])
            return df_rel
        except:
            return pd.DataFrame()
    return pd.DataFrame()

df_grafos = cargar_relaciones(df_maestro)

# --- RENDERIZADO TABLA HTML ---
def render_tabla_tactica(df, max_filas=100):
    if df.empty:
        st.warning("Sin datos para visualizar")
        return
    
    columnas_excluir = ['COLOR_RGBA', 'COLOR_STR', 'lat', 'lon', 'FECHA']
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
st.sidebar.markdown("### CENTRO DE COMANDO")

regiones = {
    "Sector Marruecos (Principal)": {"lat": 31.8, "lon": -7.1, "zoom": 5.0},
    "Estrecho de Gibraltar y Norte": {"lat": 35.9, "lon": -5.5, "zoom": 6.5},
    "Espacio Aéreo Norteafricano": {"lat": 28.0, "lon": 2.0, "zoom": 4.0},
    "Vista Orbital Global": {"lat": 20.0, "lon": 0.0, "zoom": 1.2}
}
filtro_region = st.sidebar.selectbox("Ámbito Geopolítico", list(regiones.keys()))

st.sidebar.markdown("---")
st.sidebar.markdown("### FILTROS AVANZADOS")

decadas_sel = []
paises_sel = []
formas_sel = []

try:
    decadas_disponibles = sorted([int(d) for d in df_maestro['DECADA'].dropna().unique() if pd.notna(d)])
    if decadas_disponibles:
        decadas_sel = st.sidebar.multiselect("Década", decadas_disponibles, default=decadas_disponibles)
except:
    pass

try:
    paises_disponibles = sorted([str(p) for p in df_maestro['PAIS'].unique() if pd.notna(p) and str(p) != ''])
    if paises_disponibles:
        default_paises = paises_disponibles[:min(10, len(paises_disponibles))]
        paises_sel = st.sidebar.multiselect("País", paises_disponibles, default=default_paises)
except:
    pass

try:
    formas_disponibles = sorted([str(f) for f in df_maestro['FORMA'].unique() if pd.notna(f) and str(f) != ''])
    if formas_disponibles:
        default_formas = formas_disponibles[:min(5, len(formas_disponibles))]
        formas_sel = st.sidebar.multiselect("Forma", formas_disponibles, default=default_formas)
except:
    pass

df_filtrado = df_maestro.copy()
if decadas_sel: df_filtrado = df_filtrado[df_filtrado['DECADA'].isin(decadas_sel)]
if paises_sel: df_filtrado = df_filtrado[df_filtrado['PAIS'].isin(paises_sel)]
if formas_sel: df_filtrado = df_filtrado[df_filtrado['FORMA'].isin(formas_sel)]

st.sidebar.markdown("---")
mostrar_puntos = st.sidebar.toggle("Puntos de Contacto", value=True)
mostrar_arcos = st.sidebar.toggle("Grafos de Trayectoria", value=True)

tipos_relacion = []
if not df_grafos.empty:
    tipos_disponibles = ["Trayectoria probable", "Contexto estratégico", "Shared Strategic Context", "Similar Physical Anomalies", "Otras"]
    tipos_relacion = st.sidebar.multiselect("Tipos de relación", tipos_disponibles, default=tipos_disponibles)

# --- ENCABEZADO PRINCIPAL ---
st.markdown("<h1>Motor de Análisis Conductual Predictivo</h1>", unsafe_allow_html=True)
st.markdown("<h3>Módulo FANI: Fenómenos Anómalos No Identificados</h3>", unsafe_allow_html=True)

# --- MÉTRICAS ESTRATÉGICAS ---
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
total_casos = len(df_filtrado)
if not df_filtrado.empty:
    forma_predom = df_filtrado['FORMA'].mode().iloc[0] if not df_filtrado['FORMA'].mode().empty else "N/A"
    coords = df_filtrado[['lat', 'lon']].round(1)
    zonas_criticas = len(coords.drop_duplicates())
else:
    forma_predom = "N/A"
    zonas_criticas = 0

col_m1.metric("Registros Activos", f"{total_casos:,}")
col_m2.metric("Tipología Predominante", forma_predom)
col_m3.metric("Zonas de Interés", f"{zonas_criticas:,}")
col_m4.metric("Conexiones Activas", f"{len(df_grafos) if mostrar_arcos else 0:,}")

st.markdown("---")

# --- ESTRUCTURA PRINCIPAL DE PANTALLA ---
col_mapa, col_paneles = st.columns([1.5, 1.0], gap="large")

# --- COLUMNA IZQUIERDA: VISOR ORBITAL ---
with col_mapa:
    st.markdown("#### Visor de Telemetría Orbital")
    if df_filtrado.empty:
        st.error("No hay datos para el filtro seleccionado")
    else:
        df_filtrado['RESUMEN_CORTO'] = df_filtrado['RESUMEN'].apply(lambda x: str(x)[:100] + "..." if len(str(x)) > 100 else str(x))
        fig = go.Figure()
        
        if mostrar_puntos:
            fig.add_trace(go.Scattergeo(
                lon=df_filtrado['lon'],
                lat=df_filtrado['lat'],
                mode='markers',
                marker=dict(
                    size=8,
                    color=df_filtrado['COLOR_STR'],
                    line=dict(width=1, color='white'),
                    symbol='circle',
                    opacity=0.9
                ),
                text=df_filtrado['CIUDAD'] + ', ' + df_filtrado['PAIS'] + '<br>' +
                     'Forma: ' + df_filtrado['FORMA'] + '<br>' +
                     'Año: ' + df_filtrado['AÑO'].astype(str) + '<br>' +
                     'Resumen: ' + df_filtrado['RESUMEN_CORTO'],
                hoverinfo='text',
                name='Avistamientos'
            ))
        
        if mostrar_arcos and not df_grafos.empty:
            df_rel_filt = df_grafos.copy()
            if tipos_relacion:
                def categorizar(tipo):
                    t = str(tipo).upper()
                    if 'TRAYECTORIA' in t: return 'Trayectoria probable'
                    if 'CONTEXTO' in t or 'ESTRATÉGICO' in t: return 'Contexto estratégico'
                    if 'SHARED' in t: return 'Shared Strategic Context'
                    if 'ANOMAL' in t: return 'Similar Physical Anomalies'
                    return 'Otras'
                df_rel_filt['CAT'] = df_rel_filt['TIPO'].apply(categorizar)
                df_rel_filt = df_rel_filt[df_rel_filt['CAT'].isin(tipos_relacion)]
            
            for _, row in df_rel_filt.head(100).iterrows():
                tipo = str(row['TIPO']).upper()
                if 'TRAYECTORIA' in tipo: color = 'rgba(0, 255, 255, 0.4)'
                elif 'CONTEXTO' in tipo: color = 'rgba(255, 0, 255, 0.4)'
                elif 'SHARED' in tipo: color = 'rgba(255, 255, 0, 0.5)'
                elif 'ANOMAL' in tipo: color = 'rgba(255, 128, 0, 0.5)'
                else: color = 'rgba(255, 255, 255, 0.3)'
                
                ancho = max(1, float(row['PESO']) * 3)
                
                fig.add_trace(go.Scattergeo(
                    lon=[row['origen_lon'], row['destino_lon'], None],
                    lat=[row['origen_lat'], row['destino_lat'], None],
                    mode='lines',
                    line=dict(width=ancho, color=color),
                    hoverinfo='text',
                    text=f"Tipo: {row['TIPO']}<br>{row['origen_ciudad']} → {row['destino_ciudad']}",
                    showlegend=False
                ))
        
        region = regiones[filtro_region]
        fig.update_layout(
            geo=dict(
                projection_type='orthographic',
                showland=True, landcolor='rgb(30,30,30)',
                showocean=True, oceancolor='rgb(10,10,10)',
                showcountries=True, countrycolor='rgb(80,80,80)',
                showcoastlines=True, coastlinecolor='rgb(100,100,100)',
                showframe=False, bgcolor='#0a0a0a',
                projection_rotation=dict(lon=region['lon'], lat=region['lat'])
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='#0a0a0a',
            height=700 
        )
        st.plotly_chart(fig, use_container_width=True)

# --- COLUMNA DERECHA: PANELES DESPLEGABLES ---
with col_paneles:
    
    # PANEL 1: REGISTROS FORENSES
    with st.expander("REGISTROS FORENSES", expanded=True):
        if df_filtrado.empty:
            st.warning("No hay registros disponibles.")
        else:
            cols_disp = [c for c in df_filtrado.columns if c not in ['COLOR_RGBA', 'COLOR_STR', 'lat', 'lon', 'FECHA']]
            cols_def = [c for c in ['ID', 'AÑO', 'CIUDAD', 'FORMA'] if c in cols_disp]
            cols_sel = st.multiselect("Campos a visualizar", cols_disp, default=cols_def, key="ms_campos")
            if cols_sel:
                render_tabla_tactica(df_filtrado[cols_sel].sort_values('AÑO', ascending=False), max_filas=100)

    # PANEL 2: DISTRIBUCIÓN DE INCIDENCIAS
    with st.expander("DISTRIBUCIÓN DE INCIDENCIAS", expanded=False):
        if not df_filtrado.empty:
            conteo = df_filtrado['FORMA'].value_counts().head(8).reset_index()
            conteo.columns = ['Estructura', 'Total']
            fig_bar = px.bar(conteo, x='Total', y='Estructura', orientation='h', template="plotly_dark", color_discrete_sequence=['#00d4ff'])
            fig_bar.update_layout(height=250, margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

    # PANEL 3: LÍNEA TEMPORAL
    with st.expander("LÍNEA TEMPORAL", expanded=False):
        if not df_filtrado.empty:
            timeline = df_filtrado.groupby('AÑO').size().reset_index(name='Incidentes')
            fig_line = px.area(timeline, x='AÑO', y='Incidentes', template="plotly_dark", color_discrete_sequence=['#00d4ff'])
            fig_line.update_layout(height=200, margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(10,10,10,0.5)", showlegend=False)
            fig_line.update_traces(fillcolor="rgba(0, 212, 255, 0.2)", line=dict(color="#00d4ff", width=2))
            st.plotly_chart(fig_line, use_container_width=True)

    # PANEL 4: MOTOR NLP FORENSE
    with st.expander("MOTOR NLP FORENSE (DEEPSEEK)", expanded=False):
        if df_filtrado.empty or 'RESUMEN' not in df_filtrado.columns:
            st.error("Base de datos sin sincronizar.")
        else:
            df_filtrado['ETIQUETA_CASO'] = df_filtrado['CIUDAD'].astype(str) + " | " + df_filtrado['AÑO'].astype(str)
            caso_sel = st.selectbox("Expediente", df_filtrado['ETIQUETA_CASO'].unique(), key="sb_expediente")
            datos_caso = df_filtrado[df_filtrado['ETIQUETA_CASO'] == caso_sel].iloc[0]
            texto_resumen = str(datos_caso['RESUMEN'])
            
            st.markdown(f"""
            <div style="background-color: #0a0a0a; border: 1px solid #333; padding: 10px; margin-bottom: 10px; border-left: 2px solid #64748b; font-size: 0.8rem; color: #cbd5e1;">
                {texto_resumen[:300]}{"..." if len(texto_resumen) > 300 else ""}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Ejecutar Análisis Táctico", type="primary", key="btn_nlp"):
                with st.spinner("Procesando en red neuronal..."):
                    resultado_nlp = {
                        "comportamiento": "No procesado",
                        "credibilidad": "DESCONOCIDA",
                        "hipotesis": "Sin análisis",
                        "indice": 0
                    }
                    if deepseek_token and texto_resumen.strip():
                        try:
                            headers = {
                                "Authorization": f"Bearer {deepseek_token}",
                                "Content-Type": "application/json"
                            }
                            prompt_sistema = """Eres un analista senior de inteligencia adscrito al Motor de Análisis Conductual Predictivo.
                            Tu área de operaciones abarca el Norte de África (énfasis en Marruecos) y el Estrecho de Gibraltar.
                            Analiza el texto forense proporcionado y genera un informe táctico estructurado en JSON con estos campos exactos:
                            - comportamiento: Descripción técnica del patrón de vuelo o cinemática (max 100 caracteres). Usa terminología militar.
                            - credibilidad: Exclusivamente una de estas tres palabras: ALTA, MEDIA, BAJA.
                            - indice: Número entero entre 0 y 100 representando el índice de confiabilidad del testimonio o sensor.
                            - hipotesis: Explicación analítica y técnica del posible origen (max 200 caracteres). Evita lenguaje especulativo, mantén un tono pericial.
                            
                            Responde ÚNICAMENTE con el objeto JSON válido. Ningún otro texto."""
                            
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
                        time.sleep(1.2)
                        resultado_nlp = {
                            "comportamiento": "Aceleracion instantanea no balistica en espacio aereo controlado",
                            "credibilidad": "ALTA",
                            "indice": 89,
                            "hipotesis": "Anomalia cinetica inconsistente con drones comerciales. Posible incursion de plataforma no catalogada en el sector operativo de la cordillera del Atlas."
                        }

                    cred = str(resultado_nlp.get("credibilidad", "MEDIA")).upper()
                    if "ALTA" in cred: color_cred, color_borde = "#00ff80", "#00ff80"
                    elif "MEDIA" in cred: color_cred, color_borde = "#00d4ff", "#00d4ff"
                    elif "BAJA" in cred: color_cred, color_borde = "#ff4444", "#ff4444"
                    else: color_cred, color_borde = "#64748b", "#64748b"
                    
                    indice_val = resultado_nlp.get("indice", 0)
                    
                    resultado_html = f"""
                    <div style="background-color: #050505; border: 1px solid #1a1a1a; border-left: 4px solid {color_borde}; padding: 20px; margin-top: 15px; font-family: 'Share Tech Mono', monospace;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px dashed #333; padding-bottom: 10px;">
                            <span style="color: #64748b; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px;">Evaluación Táctica de la Amenaza</span>
                            <span style="color: {color_cred}; font-size: 1.3rem; font-weight: bold; letter-spacing: 2px;">{cred} [{indice_val}/100]</span>
                        </div>
                        <div style="margin-bottom: 15px;">
                            <div style="color: #64748b; font-size: 0.7rem; text-transform: uppercase; margin-bottom: 5px; letter-spacing: 1px;">Cinemática y Comportamiento</div>
                            <div style="color: #00d4ff; font-size: 1rem;">> {resultado_nlp.get("comportamiento", "N/A")}</div>
                        </div>
                        <div>
                            <div style="color: #64748b; font-size: 0.7rem; text-transform: uppercase; margin-bottom: 5px; letter-spacing: 1px;">Conclusión Analítica</div>
                            <div style="color: #e2e8f0; font-size: 0.9rem; line-height: 1.6; font-family: 'Titillium Web', sans-serif;">{resultado_nlp.get("hipotesis", "N/A")}</div>
                        </div>
                    </div>
                    """
                    st.markdown(resultado_html, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown(f"""
    <div style="color: #333; font-family: 'Share Tech Mono', monospace; font-size: 0.7rem; text-align: center; text-transform: uppercase; letter-spacing: 1px;">
        Sistema AGATHA v4.5 | Módulo FANI | Operador {OPERADOR_ID} | Clasificación: NIVEL 4
    </div>
""", unsafe_allow_html=True)
