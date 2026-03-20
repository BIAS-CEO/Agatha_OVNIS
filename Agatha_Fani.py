# ====================================================================
# ARCHIVO PRINCIPAL: Agatha_Fani.py
# SISTEMA: Motor de Analisis Conductual Predictivo
# MODULO: AGATHA FANI (Fenomenos Anomalos No Identificados)
# VERSION: Opcon Ready v5.0 (Carga Optimizada y Filtros en Cascada)
# OPERADOR: DIR-74
# ====================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os
import json
import requests
import unicodedata
from datetime import datetime

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

# --- SISTEMA DE GESTION DE CREDENCIALES ---
def obtener_credencial(nombre_var):
    try:
        if hasattr(st, "secrets") and nombre_var in st.secrets:
            return st.secrets[nombre_var]
    except Exception:
        pass
    valor = os.environ.get(nombre_var)
    if valor: return valor
    return None

# Carga de las claves requeridas
OPENAI_API_KEY = obtener_credencial("OPENAI_API_KEY")
MAPBOX_API_KEY = obtener_credencial("MAPBOX_API_KEY")
OPENWEATHER_API_KEY = obtener_credencial("OPENWEATHER_API_KEY")
GOOGLE_MAPS_KEY = obtener_credencial("GOOGLE_MAPS_KEY")
DEEPSEEK_API_KEY = obtener_credencial("DEEPSEEK_API_KEY")

# --- FUNCIONES AUXILIARES ---
def encontrar_archivo(nombres_posibles):
    for nombre in nombres_posibles:
        rutas_posibles = [
            nombre,
            os.path.join("data", nombre),
            os.path.join(".", nombre),
            os.path.join("..", "data", nombre)
        ]
        for ruta in rutas_posibles:
            if os.path.exists(ruta):
                return ruta
    return None

def asignar_color_neon(forma):
    f = str(forma).lower()
    if any(x in f for x in ["triangulo", "triangular", "delta", "tri"]): return (0, 255, 128, 230)
    elif any(x in f for x in ["esfera", "orb", "circular", "redondo", "disco", "disk"]): return (255, 0, 128, 230)
    elif any(x in f for x in ["cigarro", "cilindro", "tubo", "cigar", "cylindrical"]): return (255, 128, 0, 230)
    elif any(x in f for x in ["luz", "cambiante", "pulsante", "flash", "light"]): return (255, 255, 0, 230)
    elif any(x in f for x in ["diamante", "rombo", "cuadrado", "diamond"]): return (128, 0, 255, 230)
    elif any(x in f for x in ["rectangulo", "plataforma", "rectangle", "galones"]): return (0, 128, 255, 230)
    else: return (0, 255, 255, 230)

def simular_coordenadas(df):
    """Genera coordenadas base usando el estado (USA) o país para dispersión visual en el mapa."""
    np.random.seed(42)
    lats, lons = [], []
    
    centroides = {
        "TX": (31.9, -99.9), "FL": (27.7, -81.6), "CA": (36.7, -119.4), "NY": (40.7, -74.0),
        "SC": (33.8, -81.1), "PA": (41.2, -77.1), "LA": (30.9, -91.9), "CO": (39.5, -105.7),
        "EEUU": (39.8, -98.5), "CANADA": (56.1, -106.3), "JAPON": (36.2, 138.2)
    }

    for _, row in df.iterrows():
        estado = str(row.get('ESTADO', '')).upper().strip()
        pais = str(row.get('PAIS', '')).upper().strip()
        
        lat_base, lon_base = 39.8, -98.5 # Centro EEUU por defecto
        
        if estado in centroides:
            lat_base, lon_base = centroides[estado]
        elif pais in centroides:
            lat_base, lon_base = centroides[pais]
            
        # Añadir ruido aleatorio para que no se superpongan en el mismo punto exacto
        lats.append(lat_base + np.random.normal(0, 1.5))
        lons.append(lon_base + np.random.normal(0, 1.5))
        
    df['lat'] = lats
    df['lon'] = lons
    return df

# --- MOTORES DE INGESTA DE DATOS SANITIZADOS ---
@st.cache_data(show_spinner="Sincronizando metadatos...")
def cargar_nodos():
    mensajes_depuracion = []
    
    nombres_archivos = [
        "agatha_ufo_master.csv", 
        "agatha_ufo_nodes_full.csv", 
        "agatha_ufo_nodes.csv"
    ]
    ruta = encontrar_archivo(nombres_archivos)
    
    if ruta:
        mensajes_depuracion.append(f"Archivo detectado: {ruta}")
        try:
            df = pd.read_csv(ruta, encoding='utf-8', on_bad_lines='skip')
        except Exception as e:
            return pd.DataFrame(), [f"Error de lectura: {str(e)}"]

        # Mapeo de columnas normalizado (maneja español e inglés de los archivos provistos)
        col_map = {
            'AÑO': 'AÑO', 'Year': 'AÑO',
            'MES': 'MES', 'Month': 'MES',
            'DÍA': 'DIA', 'Day': 'DIA',
            'CIUDAD': 'CIUDAD', 'City': 'CIUDAD',
            'ESTADO': 'ESTADO', 'State': 'ESTADO',
            'PAÍS': 'PAIS', 'Country': 'PAIS',
            'FORMA': 'FORMA', 'Shape': 'FORMA',
            'RESUMEN': 'RESUMEN', 'Summary': 'RESUMEN'
        }
        
        df.rename(columns=col_map, inplace=True)

        # Rellenar faltantes
        for col in ['CIUDAD', 'ESTADO', 'PAIS', 'FORMA', 'RESUMEN']:
            if col not in df.columns: df[col] = "Desconocido"
            else: df[col] = df[col].fillna("Desconocido").astype(str)
            
        if 'AÑO' not in df.columns: df['AÑO'] = 2026
        
        # Limpieza de datos numéricos
        df['AÑO'] = pd.to_numeric(df['AÑO'], errors='coerce').fillna(2026).astype(int)
        df['DECADA'] = (df['AÑO'] // 10) * 10
        df['FORMA'] = df['FORMA'].str.title()
        
        df = simular_coordenadas(df)
        df['COLOR_RGBA'] = df['FORMA'].apply(asignar_color_neon)
        df['COLOR_STR'] = df['COLOR_RGBA'].apply(lambda c: f'rgba({c[0]},{c[1]},{c[2]},{c[3]/255})')
        
        mensajes_depuracion.append(f"Registros operativos: {len(df)}")
        return df, mensajes_depuracion
    else:
        return pd.DataFrame(), ["Advertencia: No se encontraron matrices CSV en el directorio local."]

if st.sidebar.button("FORZAR RECARGA DE MATRICES"):
    st.cache_data.clear()
    st.rerun()

df_maestro, mensajes_depu = cargar_nodos()

# --- RENDERIZADO TABLA HTML ---
def render_tabla_tactica(df):
    if df.empty:
        st.warning("Sin datos para visualizar bajo estos parámetros.")
        return
    
    columnas_excluir = ['COLOR_RGBA', 'COLOR_STR', 'lat', 'lon', 'Source_File', 'FECHA AMER.', 'ORD.', 'NUM.']
    columnas_validas = [c for c in df.columns if c not in columnas_excluir]
    
    html = '<div class="contenedor-tabla"><table class="rejilla-tactica"><thead><tr>'
    for col in columnas_validas: html += f'<th>{col}</th>'
    html += '</tr></thead><tbody>'
    
    for _, row in df.iterrows():
        html += '<tr>'
        for col in columnas_validas:
            val = row[col]
            if pd.isna(val): val = "-"
            clase = 'valor-num' if isinstance(val, (int, float)) or (isinstance(val, str) and val.replace('.','').isdigit()) else 'valor-texto'
            html += f'<td class="{clase}">{val}</td>'
        html += '</tr>'
    
    html += '</tbody></table></div>'
    st.markdown(html, unsafe_allow_html=True)

# --- SIDEBAR: TERMINAL DE OPERACIONES ---
st.sidebar.markdown("### CENTRO DE COMANDO")
regiones = {
    "Vista Global / EEUU": {"lat": 39.8, "lon": -98.5, "zoom": 1.5},
    "Costa Este (EEUU)": {"lat": 35.0, "lon": -78.0, "zoom": 3.0},
    "Europa Central": {"lat": 50.0, "lon": 10.0, "zoom": 3.0}
}
filtro_region = st.sidebar.selectbox("Ámbito Geográfico", list(regiones.keys()))

with st.sidebar.expander("DIAGNOSTICO DEL SISTEMA"):
    st.write(f"Carga Inicial: {len(df_maestro)} registros")
    for msg in mensajes_depu:
        st.write(f"- {msg}")

# --- ENCABEZADO PRINCIPAL ---
st.markdown("<h1>Motor de Análisis Conductual Predictivo</h1>", unsafe_allow_html=True)
st.markdown("<h3>Módulo FANI: Fenómenos Anómalos No Identificados</h3>", unsafe_allow_html=True)

# --- PANEL 1: REGISTROS FORENSES (FILTROS EN CASCADA ESTRICTOS) ---
st.markdown("#### FILTRADO DE REGISTROS FORENSES")
st.markdown("<div style='color: #94a3b8; font-size: 0.85rem; margin-bottom: 15px;'>Para garantizar el rendimiento, seleccione primero la década. A continuación, podrá afinar por año y morfología. Se mostrarán TODOS los registros coincidentes.</div>", unsafe_allow_html=True)

df_filtrado = df_maestro.copy()

if not df_filtrado.empty:
    col_f1, col_f2, col_f3 = st.columns(3)
    
    # 1. Filtro por Década (Obligatorio para iniciar el embudo)
    decadas_disp = sorted(df_filtrado['DECADA'].dropna().unique(), reverse=True)
    decada_sel = col_f1.selectbox("1. Seleccionar Década", ["TODAS"] + [int(d) for d in decadas_disp])
    
    if decada_sel != "TODAS":
        df_filtrado = df_filtrado[df_filtrado['DECADA'] == decada_sel]
    
    # 2. Filtro por Año (Depende de la década elegida)
    anios_disp = sorted(df_filtrado['AÑO'].dropna().unique(), reverse=True)
    anio_sel = col_f2.selectbox("2. Filtrar por Año", ["TODOS"] + [int(a) for a in anios_disp])
    
    if anio_sel != "TODOS":
        df_filtrado = df_filtrado[df_filtrado['AÑO'] == anio_sel]
        
    # 3. Filtro por Forma (Depende del Año/Década elegido)
    formas_disp = sorted(df_filtrado['FORMA'].dropna().unique())
    forma_sel = col_f3.selectbox("3. Filtrar por Morfología (Objeto)", ["TODAS"] + [str(f) for f in formas_disp])
    
    if forma_sel != "TODAS":
        df_filtrado = df_filtrado[df_filtrado['FORMA'] == forma_sel]

# --- METRICAS DE CABECERA (Actualizadas según filtros) ---
st.markdown("---")
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
total_casos = len(df_filtrado)

if not df_filtrado.empty:
    forma_predom = df_filtrado['FORMA'].mode().iloc[0] if not df_filtrado['FORMA'].mode().empty else "N/A"
    zonas_criticas = len(df_filtrado['CIUDAD'].unique())
else:
    forma_predom, zonas_criticas = "N/A", 0

col_m1.metric("Registros Filtrados", f"{total_casos:,}")
col_m2.metric("Morfología Frecuente", forma_predom)
col_m3.metric("Nodos Identificados", f"{zonas_criticas:,}")
col_m4.metric("Estado de Red", "OPTIMO")
st.markdown("---")

# --- ESTRUCTURA PRINCIPAL DE PANTALLA ---
col_mapa, col_paneles = st.columns([1.2, 1.8], gap="large")

with col_mapa:
    st.markdown("#### Telemetría Espacial")
    if df_filtrado.empty:
        st.error("No hay datos para el filtro seleccionado.")
    else:
        fig = go.Figure()
        
        fig.add_trace(go.Scattergeo(
            lon=df_filtrado['lon'], lat=df_filtrado['lat'], mode='markers',
            marker=dict(size=7, color=df_filtrado['COLOR_STR'], line=dict(width=0.5, color='white'), symbol='circle', opacity=0.8),
            text=df_filtrado['CIUDAD'] + ', ' + df_filtrado['ESTADO'] + '<br>Forma: ' + df_filtrado['FORMA'] + '<br>Año: ' + df_filtrado['AÑO'].astype(str),
            hoverinfo='text', name='Avistamientos'
        ))
        
        region = regiones[filtro_region]
        fig.update_layout(
            geo=dict(
                projection_type='orthographic', showland=True, landcolor='rgb(30,30,30)',
                showocean=True, oceancolor='rgb(10,10,10)', showcountries=True, countrycolor='rgb(80,80,80)',
                showcoastlines=True, coastlinecolor='rgb(100,100,100)', showframe=False, bgcolor='#0a0a0a',
                projection_rotation=dict(lon=region['lon'], lat=region['lat']),
                center=dict(lat=region['lat'], lon=region['lon']),
            ),
            margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='#0a0a0a', height=500 
        )
        st.plotly_chart(fig, use_container_width=True)

with col_paneles:
    # TABLA DE REGISTROS (Muestra TODOS los filtrados)
    st.markdown(f"#### Base de Datos Táctica (Mostrando {total_casos} registros)")
    if not df_filtrado.empty:
        cols_defecto = ['AÑO', 'MES', 'DIA', 'CIUDAD', 'ESTADO', 'FORMA', 'RESUMEN']
        cols_existentes = [c for c in cols_defecto if c in df_filtrado.columns]
        render_tabla_tactica(df_filtrado[cols_existentes].sort_values(by=['AÑO', 'MES', 'DIA'], ascending=[False, False, False]))

st.markdown("---")

# --- PANEL INFERIOR: MOTOR NLP FORENSE ---
with st.expander("MOTOR NLP FORENSE (ANÁLISIS DE RESÚMENES)", expanded=False):
    if df_filtrado.empty or 'RESUMEN' not in df_filtrado.columns:
        st.error("Base de datos sin registros para analizar.")
    else:
        df_nlp = df_filtrado.copy()
        df_nlp['ETIQUETA_CASO'] = df_nlp['CIUDAD'].astype(str) + " | " + df_nlp['FORMA'].astype(str) + " | " + df_nlp['AÑO'].astype(str)
        
        col_nlp1, col_nlp2 = st.columns([1, 2])
        caso_sel = col_nlp1.selectbox("Expediente a evaluar", df_nlp['ETIQUETA_CASO'].unique(), key="sb_expediente")
        datos_caso = df_nlp[df_nlp['ETIQUETA_CASO'] == caso_sel].iloc[0]
        texto_resumen = str(datos_caso['RESUMEN'])
        
        col_nlp2.markdown("**Transcripción del Expediente:**")
        col_nlp2.markdown(f"""
        <div style="background-color: #1a1a1a; border: 1px solid #333; padding: 15px; border-left: 3px solid #64748b; font-size: 0.9rem; color: #cbd5e1;">
            {texto_resumen}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Ejecutar Análisis de Inteligencia", type="primary"):
            with st.spinner("Procesando patrones conductuales..."):
                if DEEPSEEK_API_KEY and texto_resumen.strip() and texto_resumen.lower() != "desconocido":
                    try:
                        headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
                        prompt_sistema = """Eres un analista senior de inteligencia.
                        Analiza el texto proporcionado y devuelve un JSON estricto con:
                        - comportamiento: Patrón de vuelo (max 100 caracteres).
                        - credibilidad: Exclusivamente ALTA, MEDIA o BAJA.
                        - indice: Número entero entre 0 y 100.
                        - hipotesis: Explicación técnica u origen probable (max 200 caracteres)."""
                        
                        payload = {
                            "model": "deepseek-chat",
                            "messages": [{"role": "system", "content": prompt_sistema}, {"role": "user", "content": texto_resumen[:1000]}],
                            "temperature": 0.1, "max_tokens": 300, "response_format": {"type": "json_object"}
                        }
                        respuesta = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload, timeout=30)
                        respuesta.raise_for_status()
                        contenido = respuesta.json()["choices"][0]["message"]["content"]
                        
                        if contenido.startswith("
http://googleusercontent.com/immersive_entry_chip/0
http://googleusercontent.com/immersive_entry_chip/1
