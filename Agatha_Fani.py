# ====================================================================
# ARCHIVO PRINCIPAL: Agatha_Fani.py
# SISTEMA: Motor de Analisis Conductual Predictivo
# MODULO: AGATHA FANI (Fenomenos Anomalos No Identificados)
# VERSION: Opcon Ready v4.0 (Mapa Tactico Mejorado)
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
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

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
mapbox_token = obtener_credencial("MAPBOX_API_KEY")      # Ya no se usa, pero se mantiene por compatibilidad
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

# --- GEOCODIFICACION CON CACHE ---
@st.cache_data(show_spinner="Geocodificando ubicaciones (puede tomar varios minutos)...")
def geocodificar_ciudades(df, col_ciudad, col_estado, col_pais):
    """
    Añade columnas 'lat' y 'lon' al DataFrame usando geocodificación real con caché en disco.
    """
    if df.empty:
        return df

    # Intentar cargar caché previa
    cache_file = "geocode_cache.csv"
    if os.path.exists(cache_file):
        cache_df = pd.read_csv(cache_file)
        cache = dict(zip(cache_df['query'], zip(cache_df['lat'], cache_df['lon'])))
    else:
        cache = {}

    geolocator = Nominatim(user_agent="agatha_fani")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    lats, lons = [], []
    nuevas_consultas = []

    for _, row in df.iterrows():
        ciudad = str(row[col_ciudad]).strip()
        estado = str(row[col_estado]).strip() if col_estado else ""
        pais = str(row[col_pais]).strip() if col_pais else ""
        query = f"{ciudad}, {estado}, {pais}" if estado else f"{ciudad}, {pais}"
        query = query.strip(", ")

        if query in cache:
            lat, lon = cache[query]
        else:
            try:
                location = geocode(query)
                if location:
                    lat, lon = location.latitude, location.longitude
                else:
                    # Fallback: centroide del país
                    lat, lon = obtener_coordenadas_pais(pais)
                cache[query] = (lat, lon)
                nuevas_consultas.append({'query': query, 'lat': lat, 'lon': lon})
            except Exception:
                lat, lon = obtener_coordenadas_pais(pais)
                cache[query] = (lat, lon)

        lats.append(lat)
        lons.append(lon)

    df['lat'] = lats
    df['lon'] = lons

    # Guardar nuevas consultas en caché
    if nuevas_consultas:
        nuevas_df = pd.DataFrame(nuevas_consultas)
        if os.path.exists(cache_file):
            antiguas = pd.read_csv(cache_file)
            todas = pd.concat([antiguas, nuevas_df]).drop_duplicates(subset=['query'])
        else:
            todas = nuevas_df
        todas.to_csv(cache_file, index=False)

    return df

def obtener_coordenadas_pais(pais):
    """Devuelve coordenadas aproximadas de un país (centroide)."""
    centroides = {
        "EEUU": (39.8283, -98.5795),
        "USA": (39.8283, -98.5795),
        "MEXICO": (23.6345, -102.5528),
        "CANADA": (56.1304, -106.3468),
        "ESPAÑA": (40.4637, -3.7492),
        "SPAIN": (40.4637, -3.7492),
        "FRANCIA": (46.2276, 2.2137),
        "FRANCE": (46.2276, 2.2137),
        "REINO UNIDO": (55.3781, -3.4360),
        "UK": (55.3781, -3.4360),
        "ALEMANIA": (51.1657, 10.4515),
        "ITALIA": (41.8719, 12.5674),
        "AUSTRALIA": (-25.2744, 133.7751),
        "JAPON": (36.2048, 138.2529),
        "CHINA": (35.8617, 104.1954),
        "RUSIA": (61.5240, 105.3188),
        "BRASIL": (-14.2350, -51.9253),
        "ARGENTINA": (-38.4161, -63.6167),
        "SUDAFRICA": (-30.5595, 22.9375),
        "EGIPTO": (26.8206, 30.8025),
        "INDIA": (20.5937, 78.9629),
        "INDONESIA": (-0.7893, 113.9213),
    }
    p = pais.upper().strip()
    if p in centroides:
        lat, lon = centroides[p]
    else:
        lat, lon = 20.0, 0.0  # Default: África central
    # Añadir pequeña variación aleatoria para no superponer
    rng = np.random.default_rng(hash(p) % 2**32)
    lat += rng.normal(0, 1.0)
    lon += rng.normal(0, 1.0)
    return lat, lon

# --- MOTORES DE INGESTA DE DATOS ---
@st.cache_data(show_spinner="Sincronizando base de datos táctica...")
def cargar_nodos():
    """Carga el archivo maestro agatha_ufo_nodes_full.csv y normaliza."""
    # Buscar el archivo maestro completo
    ruta = encontrar_archivo("agatha_ufo_nodes_full.csv")
    if not ruta:
        # Fallback al archivo de nodos pequeño
        ruta = encontrar_archivo("agatha_ufo_nodes.csv")
        if not ruta:
            st.error("CRITICO: No se localiza archivo de nodos (agatha_ufo_nodes_full.csv o agatha_ufo_nodes.csv)")
            return pd.DataFrame()

    try:
        df = pd.read_csv(ruta, encoding='utf-8', on_bad_lines='skip')
    except Exception as e:
        st.error(f"Error al leer nodos: {e}")
        return pd.DataFrame()

    # Normalizar nombres de columnas (a mayúsculas, sin puntos)
    df.columns = [str(c).strip().replace('.', '').replace(' ', '_').upper() for c in df.columns]

    # Identificar columna ID
    if 'NUM' in df.columns:
        df.rename(columns={'NUM': 'ID'}, inplace=True)
    elif 'ORD' in df.columns:
        df.rename(columns={'ORD': 'ID'}, inplace=True)
    else:
        st.error("No se encontró columna de identificación (NUM/ORD)")
        return pd.DataFrame()

    # Mapeo de columnas
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

    # Limpieza de datos
    df['FORMA'] = df['FORMA'].fillna("No especificada").astype(str).str.title()
    df['RESUMEN'] = df['RESUMEN'].fillna("").astype(str)
    df['PAIS'] = df['PAIS'].fillna("Desconocido").astype(str).str.upper()
    df['CIUDAD'] = df['CIUDAD'].fillna("Zona operativa").astype(str)
    df['ESTADO'] = df['ESTADO'].fillna("").astype(str)
    df['AÑO'] = pd.to_numeric(df['AÑO'], errors='coerce').fillna(2024).astype(int)
    df['DIA'] = pd.to_numeric(df['DIA'], errors='coerce').fillna(1).astype(int)
    df['MES'] = pd.to_numeric(df['MES'], errors='coerce').fillna(1).astype(int)

    # Crear fecha y día de la semana
    try:
        df['FECHA'] = pd.to_datetime(df['AÑO'].astype(str) + '-' + 
                                      df['MES'].astype(str) + '-' + 
                                      df['DIA'].astype(str), errors='coerce')
    except:
        df['FECHA'] = pd.NaT
    df['DIA_SEMANA'] = df['FECHA'].dt.day_name()  # Monday, Tuesday...
    df['DECADA'] = (df['AÑO'] // 10) * 10

    # Geocodificar (si no hay columnas de lat/lon preexistentes)
    if 'LAT' not in df.columns or 'LON' not in df.columns:
        df = geocodificar_ciudades(df, 'CIUDAD', 'ESTADO', 'PAIS')
    else:
        df.rename(columns={'LAT': 'lat', 'LON': 'lon'}, inplace=True)

    # Paleta neón
    def asignar_color_neon(forma):
        f = forma.lower()
        if any(x in f for x in ["triangulo", "triangular", "delta"]):
            return (0, 255, 128, 230)        # verde neón
        elif any(x in f for x in ["esfera", "orb", "circular", "redondo", "disco"]):
            return (255, 0, 128, 230)        # magenta neón
        elif any(x in f for x in ["cigarro", "cilindro", "tubo", "cigar"]):
            return (255, 128, 0, 230)        # naranja neón
        elif any(x in f for x in ["luz", "cambiante", "pulsante", "flash"]):
            return (255, 255, 0, 230)        # amarillo neón
        elif any(x in f for x in ["diamante", "rombo", "cuadrado"]):
            return (128, 0, 255, 230)        # violeta neón
        elif any(x in f for x in ["rectangulo", "plataforma"]):
            return (0, 128, 255, 230)        # azul neón
        else:
            return (0, 255, 255, 230)        # cian neón

    df['COLOR_RGBA'] = df['FORMA'].apply(asignar_color_neon)
    df['COLOR_STR'] = df['COLOR_RGBA'].apply(lambda c: f'rgba({c[0]},{c[1]},{c[2]},{c[3]/255})')
    df['ID'] = df['ID'].astype(int)

    return df

@st.cache_data(show_spinner="Calculando matrices de relación...")
def cargar_relaciones(df_nodos):
    """Carga relaciones desde los archivos sample y pequeño, filtrando por IDs existentes."""
    if df_nodos.empty:
        return pd.DataFrame()

    ids_validos = set(df_nodos['ID'].unique())

    # Cargar relaciones del sample
    ruta_sample = encontrar_archivo("agatha_ufo_relationships_sample.csv")
    if ruta_sample:
        try:
            df_sample = pd.read_csv(ruta_sample, encoding='utf-8', on_bad_lines='skip')
            df_sample.columns = [str(c).strip().upper() for c in df_sample.columns]
            # Renombrar columnas de origen/destino
            col_src = [c for c in df_sample.columns if 'SOURCE' in c or 'ORIGEN' in c][0]
            col_tgt = [c for c in df_sample.columns if 'TARGET' in c or 'DESTINO' in c][0]
            df_sample.rename(columns={col_src: 'SRC_ID', col_tgt: 'TGT_ID'}, inplace=True)

            df_sample['SRC_ID'] = pd.to_numeric(df_sample['SRC_ID'], errors='coerce')
            df_sample['TGT_ID'] = pd.to_numeric(df_sample['TGT_ID'], errors='coerce')
            df_sample = df_sample.dropna(subset=['SRC_ID', 'TGT_ID'])
            df_sample = df_sample[df_sample['SRC_ID'].isin(ids_validos) & df_sample['TGT_ID'].isin(ids_validos)]
            df_sample['TIPO'] = df_sample.get('RELATIONSHIP', 'Trayectoria probable').fillna('Trayectoria probable')
            df_sample['PESO'] = pd.to_numeric(df_sample.get('WEIGHT', 0.5), errors='coerce').fillna(0.5)
        except Exception as e:
            st.warning(f"Error al cargar relaciones sample: {e}")
            df_sample = pd.DataFrame()
    else:
        df_sample = pd.DataFrame()

    # Cargar relaciones del archivo pequeño
    ruta_peq = encontrar_archivo("agatha_ufo_relationships.csv")
    if ruta_peq:
        try:
            df_peq = pd.read_csv(ruta_peq, encoding='utf-8', on_bad_lines='skip')
            df_peq.columns = [str(c).strip().upper() for c in df_peq.columns]
            col_src_p = [c for c in df_peq.columns if 'SOURCE' in c or 'ORIGEN' in c][0]
            col_tgt_p = [c for c in df_peq.columns if 'TARGET' in c or 'DESTINO' in c][0]
            df_peq.rename(columns={col_src_p: 'SRC_ID', col_tgt_p: 'TGT_ID'}, inplace=True)

            df_peq['SRC_ID'] = pd.to_numeric(df_peq['SRC_ID'], errors='coerce')
            df_peq['TGT_ID'] = pd.to_numeric(df_peq['TGT_ID'], errors='coerce')
            df_peq = df_peq.dropna(subset=['SRC_ID', 'TGT_ID'])
            df_peq = df_peq[df_peq['SRC_ID'].isin(ids_validos) & df_peq['TGT_ID'].isin(ids_validos)]
            df_peq['TIPO'] = df_peq.get('RELATIONSHIP_TYPE', 'Desconocida').fillna('Desconocida')
            df_peq['PESO'] = pd.to_numeric(df_peq.get('WEIGHT', 0.3), errors='coerce').fillna(0.3)
        except Exception as e:
            st.warning(f"Error al cargar relaciones pequeñas: {e}")
            df_peq = pd.DataFrame()
    else:
        df_peq = pd.DataFrame()

    # Combinar ambas
    df_rel = pd.concat([df_sample, df_peq], ignore_index=True)

    if df_rel.empty:
        return pd.DataFrame()

    # Añadir coordenadas de origen y destino
    df_coords = df_nodos.set_index('ID')[['lat', 'lon', 'CIUDAD', 'PAIS']]
    df_rel['origen_lat'] = df_rel['SRC_ID'].map(df_coords['lat'])
    df_rel['origen_lon'] = df_rel['SRC_ID'].map(df_coords['lon'])
    df_rel['destino_lat'] = df_rel['TGT_ID'].map(df_coords['lat'])
    df_rel['destino_lon'] = df_rel['TGT_ID'].map(df_coords['lon'])
    df_rel['origen_ciudad'] = df_rel['SRC_ID'].map(df_coords['CIUDAD'])
    df_rel['destino_ciudad'] = df_rel['TGT_ID'].map(df_coords['CIUDAD'])

    # Eliminar filas con coordenadas faltantes
    df_rel = df_rel.dropna(subset=['origen_lat', 'origen_lon', 'destino_lat', 'destino_lon'])

    return df_rel

# --- RENDERIZADO TABLA TACTICA HTML ---
def render_tabla_tactica(df, max_filas=200):
    if df.empty:
        st.warning("Sin datos para visualizar")
        return

    columnas_excluir = ['COLOR_RGBA', 'COLOR_STR', 'lat', 'lon', 'ID', 'FECHA']
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

# --- CARGA DE DATOS ---
df_maestro = cargar_nodos()
df_grafos = cargar_relaciones(df_maestro)

# --- SIDEBAR: TERMINAL DE OPERACIONES ---
st.sidebar.markdown("### Centro de Comando AGATHA")

# Filtro geopolitico (solo afecta vista inicial del globo, no filtrado de datos)
regiones = {
    "Vista Orbital Global": {"lat": 20.0, "lon": 0.0, "zoom": 1.2},
    "Marruecos y España": {"lat": 35.0, "lon": -5.0, "zoom": 5},
    "Norteamérica": {"lat": 39.8, "lon": -98.5, "zoom": 3.5},
    "Europa Occidental": {"lat": 48.0, "lon": 10.0, "zoom": 4.5}
}
filtro_region = st.sidebar.selectbox("Ámbito Geopolítico", list(regiones.keys()))

# --- FILTROS AVANZADOS (MULTISELECT) ---
st.sidebar.markdown("---")
st.sidebar.markdown("### Filtros Avanzados")

if not df_maestro.empty:
    # Décadas
    decadas_disponibles = sorted(df_maestro['DECADA'].dropna().unique())
    decadas_sel = st.sidebar.multiselect("Década", decadas_disponibles, default=decadas_disponibles)

    # Países
    paises_disponibles = sorted(df_maestro['PAIS'].unique())
    paises_sel = st.sidebar.multiselect("País", paises_disponibles, default=paises_disponibles[:10])

    # Formas
    formas_disponibles = sorted(df_maestro['FORMA'].unique())
    formas_sel = st.sidebar.multiselect("Forma", formas_disponibles, default=formas_disponibles[:5])

    # Días de la semana
    dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dias_disponibles = [d for d in dias_orden if d in df_maestro['DIA_SEMANA'].unique()]
    dias_sel = st.sidebar.multiselect("Día de la semana", dias_disponibles, default=dias_disponibles)

    # Aplicar filtros
    df_filtrado = df_maestro[
        (df_maestro['DECADA'].isin(decadas_sel)) &
        (df_maestro['PAIS'].isin(paises_sel)) &
        (df_maestro['FORMA'].isin(formas_sel)) &
        (df_maestro['DIA_SEMANA'].isin(dias_sel))
    ].copy()
else:
    df_filtrado = pd.DataFrame()
    decadas_sel = paises_sel = formas_sel = dias_sel = []

# Controles de visualización
st.sidebar.markdown("---")
mostrar_puntos = st.sidebar.toggle("Puntos de Contacto", value=True)
mostrar_arcos = st.sidebar.toggle("Grafos de Trayectoria", value=True)

# Filtro de tipos de relación
if not df_grafos.empty:
    tipos_relacion = st.sidebar.multiselect(
        "Tipos de relación a mostrar",
        ["Trayectoria probable", "Contexto estratégico", "Shared Strategic Context", "Similar Physical Anomalies", "Otras"],
        default=["Trayectoria probable", "Contexto estratégico", "Shared Strategic Context", "Similar Physical Anomalies"]
    )
else:
    tipos_relacion = []

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

# --- PESTAÑAS PRINCIPALES ---
tab_visor, tab_datos, tab_analisis = st.tabs([
    "Visor de Telemetría Orbital",
    "Registros Forenses",
    "Procesador NLP Forense"
])

# --- TAB 1: VISOR GLOBO TERRAQUEO INTERACTIVO (Plotly) ---
with tab_visor:
    if df_filtrado.empty:
        st.warning("No hay datos para el filtro seleccionado.")
    else:
        # Preparar datos para Plotly
        df_filtrado['RESUMEN_CORTO'] = df_filtrado['RESUMEN'].apply(lambda x: x[:100] + "..." if len(x) > 100 else x)

        # Crear figura base
        fig = go.Figure()

        # Capa de puntos
        if mostrar_puntos:
            # Tamaño de punto variable según número de registros en la misma ubicación
            # (para evitar apelotonamiento, usamos transparencia y tamaño pequeño)
            punto_size = 6
            fig.add_trace(go.Scattergeo(
                lon=df_filtrado['lon'],
                lat=df_filtrado['lat'],
                mode='markers',
                marker=dict(
                    size=punto_size,
                    color=df_filtrado['COLOR_STR'],
                    line=dict(width=0.3, color='white'),
                    symbol='circle',
                    opacity=0.8
                ),
                text=df_filtrado['CIUDAD'] + ', ' + df_filtrado['PAIS'] + '<br>' +
                     'Forma: ' + df_filtrado['FORMA'] + '<br>' +
                     'Año: ' + df_filtrado['AÑO'].astype(str) + '<br>' +
                     'Día: ' + df_filtrado['DIA_SEMANA'] + '<br>' +
                     'Resumen: ' + df_filtrado['RESUMEN_CORTO'],
                hoverinfo='text',
                name='Avistamientos'
            ))

        # Capa de arcos (relaciones)
        if mostrar_arcos and not df_grafos.empty:
            # Filtrar relaciones por tipo seleccionado
            df_rel_filt = df_grafos.copy()
            if tipos_relacion:
                def categorizar(tipo):
                    t = tipo.upper()
                    if 'TRAYECTORIA' in t:
                        return 'Trayectoria probable'
                    if 'CONTEXTO' in t or 'ESTRATÉGICO' in t:
                        return 'Contexto estratégico'
                    if 'SHARED' in t:
                        return 'Shared Strategic Context'
                    if 'ANOMAL' in t:
                        return 'Similar Physical Anomalies'
                    return 'Otras'
                df_rel_filt['CAT'] = df_rel_filt['TIPO'].apply(categorizar)
                df_rel_filt = df_rel_filt[df_rel_filt['CAT'].isin(tipos_relacion)]

            for _, row in df_rel_filt.iterrows():
                # Determinar color según tipo
                tipo = row['TIPO'].upper()
                if 'TRAYECTORIA' in tipo:
                    color = 'rgba(0, 255, 255, 0.3)'  # cian
                elif 'CONTEXTO' in tipo or 'ESTRATÉGICO' in tipo:
                    color = 'rgba(255, 0, 255, 0.3)'  # magenta
                elif 'SHARED' in tipo:
                    color = 'rgba(255, 255, 0, 0.4)'  # amarillo
                elif 'ANOMAL' in tipo:
                    color = 'rgba(255, 128, 0, 0.4)'  # naranja
                else:
                    color = 'rgba(255, 255, 255, 0.2)'  # blanco tenue

                ancho = max(1, row['PESO'] * 3)

                fig.add_trace(go.Scattergeo(
                    lon=[row['origen_lon'], row['destino_lon'], None],
                    lat=[row['origen_lat'], row['destino_lat'], None],
                    mode='lines',
                    line=dict(width=ancho, color=color),
                    hoverinfo='text',
                    text=f"Tipo: {row['TIPO']}<br>Peso: {row['PESO']}<br>{row['origen_ciudad']} → {row['destino_ciudad']}",
                    showlegend=False
                ))

        # Configurar layout del globo
        region = regiones[filtro_region]
        fig.update_layout(
            geo=dict(
                projection_type='orthographic',
                showland=True,
                landcolor='rgb(30,30,30)',
                showocean=True,
                oceancolor='rgb(10,10,10)',
                showcountries=True,
                countrycolor='rgb(80,80,80)',
                showcoastlines=True,
                coastlinecolor='rgb(100,100,100)',
                showframe=False,
                bgcolor='#0a0a0a',
                projection_rotation=dict(lon=region['lon'], lat=region['lat'])
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='#0a0a0a',
            height=700
        )

        st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: Registros Forenses ---
with tab_datos:
    st.markdown("#### Archivos de Inteligencia Extraídos")

    if df_filtrado.empty:
        st.warning("No hay registros que coincidan con los criterios de filtrado")
    else:
        cols_disponibles = [c for c in df_filtrado.columns if c not in ['COLOR_RGBA', 'COLOR_STR', 'lat', 'lon', 'FECHA']]
        cols_default = [c for c in ['ID', 'AÑO', 'PAIS', 'CIUDAD', 'FORMA', 'RESUMEN'] if c in cols_disponibles]

        cols_seleccionadas = st.multiselect(
            "Campos de Visualización",
            cols_disponibles,
            default=cols_default[:6]
        )

        if cols_seleccionadas:
            df_display = df_filtrado[cols_seleccionadas].sort_values('AÑO', ascending=False)
            render_tabla_tactica(df_display, max_filas=250)
        else:
            st.info("Seleccione campos para visualizar")

# --- TAB 3: Procesador NLP Forense (DeepSeek) ---
with tab_analisis:
    col_nlp, col_stats = st.columns([1, 1])

    with col_nlp:
        st.markdown("#### Motor de Análisis NLP Forense")
        st.markdown("<p style='color: #64748b; font-size:0.85rem; margin-top:-10px;'>"
        "Seleccione un expediente para generar perfilamiento táctico automatizado.</p>",
        unsafe_allow_html=True)

        if df_filtrado.empty or 'RESUMEN' not in df_filtrado.columns:
            st.error("Base de datos no sincronizada o sin campo RESUMEN")
        else:
            # Crear selector de casos
            df_filtrado['ETIQUETA_CASO'] = (
                df_filtrado['CIUDAD'].astype(str) + " | " +
                df_filtrado['FORMA'].astype(str) + " | " +
                df_filtrado['AÑO'].astype(str)
            )

            caso_sel = st.selectbox("Expediente Operativo", df_filtrado['ETIQUETA_CASO'].unique())

            datos_caso = df_filtrado[df_filtrado['ETIQUETA_CASO'] == caso_sel].iloc[0]
            texto_resumen = str(datos_caso['RESUMEN'])

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

            if st.button("Ejecutar Análisis Forense", type="primary"):
                with st.spinner("Procesando mediante red neuronal DeepSeek..."):

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

                            prompt_sistema = """Eres un analista de inteligencia militar especializado en fenómenos aéreos no identificados.
                            Analiza el texto proporcionado y genera un informe táctico estructurado en JSON con estos campos exactos:
                            - comportamiento: Descripción técnica del patrón de vuelo/cinemática (max 100 caracteres)
                            - credibilidad: Una de ALTA, MEDIA, BAJA
                            - indice: Número entero 0-100 representando confiabilidad del testimonio
                            - hipotesis: Explicación analítica técnica del origen (max 200 caracteres)

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
                        # Simulación si no hay API
                        time.sleep(1.2)
                        resultado_nlp = {
                            "comportamiento": "Maniobra no balística con vector ascendente",
                            "credibilidad": "ALTA",
                            "indice": 87,
                            "hipotesis": "Firma electromagnética inconsistente con aeronaves convencionales. Probable plataforma de propulsión gravítica no catalogada."
                        }

                    # Determinar color según credibilidad
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

                    # HTML para el resultado
                    resultado_html = f"""
                    <div style="background-color: #0a0a0a; border: 1px solid #333; 
                    border-left: 4px solid {color_borde}; padding: 20px; margin-top: 20px;">

                        <div style="display: flex; justify-content: space-between; align-items: center; 
                        margin-bottom: 15px; border-bottom: 1px solid #222; padding-bottom: 10px;">
                            <span style="color: #64748b; font-size: 0.7rem; text-transform: uppercase; 
                            font-weight: 600;">Resultado del Análisis</span>
                            <span style="color: {color_cred}; font-family: 'Share Tech Mono', monospace; 
                            font-size: 1.2rem; font-weight: bold;">{cred} [{indice_val}/100]</span>
                        </div>

                        <div style="margin-bottom: 15px;">
                            <div style="color: #64748b; font-size: 0.7rem; text-transform: uppercase; 
                            margin-bottom: 5px; font-weight: 600;">Patrón Comportamental</div>
                            <div style="color: #00d4ff; font-family: 'Share Tech Mono', monospace; 
                            font-size: 0.95rem;">{resultado_nlp.get("comportamiento", "N/A")}</div>
                        </div>

                        <div>
                            <div style="color: #64748b; font-size: 0.7rem; text-transform: uppercase; 
                            margin-bottom: 5px; font-weight: 600;">Hipótesis Operativa</div>
                            <div style="color: #e2e8f0; font-size: 0.85rem; line-height: 1.5; 
                            text-align: justify;">{resultado_nlp.get("hipotesis", "N/A")}</div>
                        </div>

                    </div>
                    """

                    st.markdown(resultado_html, unsafe_allow_html=True)

    with col_stats:
        st.markdown("#### Distribución de Incidencias")

        if not df_filtrado.empty:
            # Gráfico de barras horizontal
            conteo_formas = df_filtrado['FORMA'].value_counts().head(10).reset_index()
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
            st.plotly_chart(fig, use_container_width=True)

            # Timeline de incidentes
            st.markdown("#### Línea Temporal")
            timeline = df_filtrado.groupby('AÑO').size().reset_index(name='Incidentes')

            fig2 = px.area(
                timeline,
                x='AÑO',
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
            st.plotly_chart(fig2, use_container_width=True)

# --- FOOTER TÁCTICO ---
st.markdown("---")
st.markdown(f"""
    <div style="color: #333; font-family: 'Share Tech Mono', monospace; font-size: 0.7rem; 
    text-align: center; text-transform: uppercase; letter-spacing: 1px;">
        Sistema AGATHA v4.0 | Módulo FANI | Operador {OPERADOR_ID} | Clasificación: NIVEL 4
    </div>
""", unsafe_allow_html=True)    font-family: 'Titillium Web', sans-serif !important; 
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
mapbox_token = obtener_credencial("MAPBOX_API_KEY")      # Ya no se usa, pero se mantiene por compatibilidad
deepseek_token = obtener_credencial("DEEPSEEK_API_KEY")
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

    # Paleta Neon con TUPLAS (hashables)
    def asignar_color_neon(forma):
        f = str(forma).lower()
        if any(x in f for x in ["triangulo", "triangular", "delta", "tri"]):
            return (0, 255, 128, 230)        # verde neón
        elif any(x in f for x in ["esfera", "orb", "circular", "redondo", "disco"]):
            return (255, 0, 128, 230)        # magenta neón
        elif any(x in f for x in ["cigarro", "cilindro", "tubo", "cigar"]):
            return (255, 128, 0, 230)        # naranja neón
        elif any(x in f for x in ["luz", "cambiante", "pulsante", "flash"]):
            return (255, 255, 0, 230)        # amarillo neón
        elif any(x in f for x in ["diamante", "rombo", "cuadrado"]):
            return (128, 0, 255, 230)        # violeta neón
        elif any(x in f for x in ["rectangulo", "plataforma"]):
            return (0, 128, 255, 230)        # azul neón
        else:
            return (0, 255, 255, 230)        # cian neón
    
    df['Color Rgba'] = df['Forma'].apply(asignar_color_neon)
    df['Color Str'] = df['Color Rgba'].apply(lambda c: f'rgba({c[0]},{c[1]},{c[2]},{c[3]/255})')
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
                'origen_lon': float(nodo_a['Longitud']), 
                'origen_lat': float(nodo_a['Latitud']),
                'destino_lon': float(nodo_b['Longitud']), 
                'destino_lat': float(nodo_b['Latitud']),
                'color_origen': nodo_a.get('Color Str', 'rgba(0,255,255,0.9)'),
                'peso': float(row.get('Weight', 1)) if 'Weight' in df_rel.columns else 1.0
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
    
    columnas_excluir = ['Color Rgba', 'Color Str', 'Latitud', 'Longitud', 'Id Caso']
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

# Filtro geopolitico (solo afecta vista inicial del globo, no filtrado de datos)
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

if not df_maestro.empty:
    min_year_global = int(df_maestro['Ano'].min())
    max_year_global = int(df_maestro['Ano'].max())
else:
    min_year_global, max_year_global = 1900, 2024

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
    
    # Aplicar filtros al dataframe principal
    df_filtrado = df_maestro[
        (df_maestro['Forma'].isin(filtro_forma)) & 
        (df_maestro['Ano'].between(rango_anos[0], rango_anos[1]))
    ].copy()
else:
    df_filtrado = pd.DataFrame()
    filtro_forma = []

# Controles de visualizacion (solo puntos y arcos, eliminado heatmap)
st.sidebar.markdown("---")
mostrar_puntos = st.sidebar.toggle("Puntos de Contacto", value=True)
mostrar_arcos = st.sidebar.toggle("Grafos de Trayectoria", value=True)

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

# --- TAB 1: VISOR GLOBO TERRAQUEO INTERACTIVO (Plotly) ---
with tab_visor:
    # Filtro de franja temporal encima del mapa
    if not df_maestro.empty:
        col_filtro1, col_filtro2, col_filtro3 = st.columns([2, 2, 2])
        
        with col_filtro1:
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
                st.session_state.franja_rapida = "Todas"
                st.rerun()
        
        # Aplicar filtro rápido
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
        # Preparar datos para Plotly
        df_mapa['Resumen_corto'] = df_mapa['Resumen'].apply(lambda x: x[:100] + "..." if len(x) > 100 else x)
        
        # Crear figura base
        fig = go.Figure()

        # 1. Capa de puntos
        if mostrar_puntos:
            fig.add_trace(go.Scattergeo(
                lon=df_mapa['Longitud'],
                lat=df_mapa['Latitud'],
                mode='markers',
                marker=dict(
                    size=8,
                    color=df_mapa['Color Str'],
                    line=dict(width=0.5, color='white'),
                    symbol='circle'
                ),
                text=df_mapa['Ciudad'] + ', ' + df_mapa['Pais'] + '<br>' + 
                     'Forma: ' + df_mapa['Forma'] + '<br>' +
                     'Año: ' + df_mapa['Ano'].astype(str) + '<br>' +
                     'Resumen: ' + df_mapa['Resumen_corto'],
                hoverinfo='text',
                name='Puntos de contacto'
            ))

        # 2. Capa de arcos (relaciones)
        if mostrar_arcos and not df_grafos.empty:
            # Crear una línea por cada relación (conectar origen y destino)
            for _, row in df_grafos.iterrows():
                fig.add_trace(go.Scattergeo(
                    lon=[row['origen_lon'], row['destino_lon'], None],
                    lat=[row['origen_lat'], row['destino_lat'], None],
                    mode='lines',
                    line=dict(width=1, color='rgba(255,255,255,0.3)'),
                    hoverinfo='none',
                    showlegend=False
                ))

        # Configurar layout del globo
        fig.update_layout(
            geo=dict(
                projection_type='orthographic',
                showland=True,
                landcolor='rgb(30,30,30)',
                showocean=True,
                oceancolor='rgb(10,10,10)',
                showcountries=True,
                countrycolor='rgb(80,80,80)',
                showcoastlines=True,
                coastlinecolor='rgb(100,100,100)',
                showframe=False,
                bgcolor='#0a0a0a'
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='#0a0a0a',
            height=700
        )

        # Ajustar vista inicial según región seleccionada
        region = regiones[filtro_region]
        # Plotly no permite fijar lat/lon/zoom directamente en orthographic? 
        # Podemos usar `geo.projection.rotation` y `geo.projection.distance`
        # Para simplificar, dejamos la vista por defecto (rotación inicial) y el usuario puede rotar.
        # Si se quiere centrar en una región, se puede usar `geo.projection.rotation` con `lon` y `lat`.
        # Ajustamos rotación según región:
        fig.update_geos(
            projection_rotation=dict(lon=region['lon'], lat=region['lat'])
        )

        st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: Registros Forenses ---
with tab_datos:
    st.markdown("#### Archivos de Inteligencia Extraidos")
    
    if df_filtrado.empty:
        st.warning("No hay registros que coincidan con los criterios de filtrado")
    else:
        cols_disponibles = [c for c in df_filtrado.columns if c not in ['Color Rgba', 'Color Str', 'Latitud', 'Longitud']]
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
                    
                    # HTML CORREGIDO para el resultado
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
        Sistema AGATHA v3.0 | Modulo FANI | Operador {OPERADOR_ID} | Clasificacion: NIVEL 4
    </div>
""", unsafe_allow_html=True)
