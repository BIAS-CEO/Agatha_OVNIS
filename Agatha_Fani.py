# ====================================================================
# ARCHIVO PRINCIPAL: Agatha_Fani.py
# SISTEMA: Motor de Analisis Conductual Predictivo
# MODULO: AGATHA FANI (Fenomenos Anomalos No Identificados)
# VERSION: Opcon Ready v4.4 (Datos de ejemplo integrados)
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

# --- CARGA DE CREDENCIALES ---
def obtener_credencial(nombre_var, nombre_secrets=None):
    nombre_secrets = nombre_secrets or nombre_var
    try:
        if hasattr(st, "secrets") and nombre_secrets in st.secrets:
            return st.secrets[nombre_secrets]
    except Exception:
        pass
    return os.environ.get(nombre_var)

deepseek_token = obtener_credencial("DEEPSEEK_API_KEY")

# --- DATOS DE EJEMPLO (SIEMPRE DISPONIBLES) ---
@st.cache_data
def crear_datos_ejemplo():
    """Crea un DataFrame con los 15 avistamientos originales."""
    data = {
        'ID': list(range(15)),
        'CIUDAD': ['Shermans Dale', 'North Richland Hills', 'Houma', 'Painted Post', 'Porterville',
                   'Lakewood', 'Manheim', 'Antwerp', 'Huntington', 'Windham',
                   'Athens', 'Lakeview', 'Spearfish', 'Salem', 'Reef Station'],
        'ESTADO': ['PA', 'TX', 'LA', 'NY', 'CA', 'CO', 'PA', 'Flanders', 'NY', 'NH',
                   'GA', 'OR', 'SD', 'IN', 'CA'],
        'PAIS': ['USA', 'USA', 'USA', 'USA', 'USA', 'USA', 'USA', 'BELGIUM', 'USA', 'USA',
                 'USA', 'USA', 'USA', 'USA', 'USA'],
        'FORMA': ['Unknown', 'Triangle', 'Unknown', 'Orb/Disk', 'Polyhedron',
                  'Triangle', 'Cylindrical', 'Unknown', 'Orb/Disk', 'Triangle',
                  'Polyhedron', 'Unknown', 'Chevron', 'Triangle', 'Cylindrical'],
        'RESUMEN': [
            'Bright light shining out of our woods, then moved over my mother-in-laws house',
            'Large black triangle shaped object the size of a football field with pale green lights',
            'Clearly witnessed a tear shaped ufo over our airbase',
            'black disk, no lights',
            'Octahedron, dark metallic, 600-900ft away, followed parallel w vehicle, turned 90 degrees',
            'A large triangular craft with an X shaped cross structure, followed by a helicopter',
            'Oblong cigar shaped, extremely bright white flashing. Hovering',
            'Metallic, cylindrical UFO hovered for 30 sec then vanished at high speed',
            'Blackhawk helicopter pursuing a brilliant white orb',
            'Two football field wide triangle objects floating or slowly moving',
            'Huge upside-down Pyramid rotating glowing red on bottom',
            'Bright white light moving at very high speeds, Mach 3, pilot sighting',
            'Chevron-shaped craft, estimated speed 523,440 mph, astrophotographer sighting',
            'Black triangular-shaped object, shot an intense blue and white beam',
            'Gray cylinder passing 10ft underneath military aircraft, Mach 4'
        ],
        'AÑO': [2025, 2025, 2025, 2025, 2024, 2024, 2024, 2024, 2024, 2024,
                2024, 2023, 2023, 2023, 2023],
        'MES': [5, 5, 5, 5, 4, 3, 3, 3, 2, 2, 1, 11, 9, 8, 9],
        'DIA': [7, 7, 5, 2, 4, 28, 19, 8, 24, 14, 27, 1, 28, 22, 17]
    }
    df = pd.DataFrame(data)

    # Crear fecha y día de la semana
    df['FECHA'] = pd.to_datetime(df['AÑO'].astype(str) + '-' + df['MES'].astype(str) + '-' + df['DIA'].astype(str))
    df['DIA_SEMANA'] = df['FECHA'].dt.day_name()
    df['DECADA'] = (df['AÑO'] // 10) * 10

    # Asignar coordenadas aproximadas por país
    def coord_pais(pais):
        centroides = {
            'USA': (39.8, -98.5),
            'BELGIUM': (50.5, 4.5)
        }
        lat, lon = centroides.get(pais.upper(), (20.0, 0.0))
        # Añadir variación
        rng = np.random.default_rng(hash(pais) % 2**32)
        lat += rng.normal(0, 2.0)
        lon += rng.normal(0, 2.0)
        return lat, lon

    df['lat'] = df['PAIS'].apply(lambda p: coord_pais(p)[0])
    df['lon'] = df['PAIS'].apply(lambda p: coord_pais(p)[1])

    # Paleta neón
    def color_neon(forma):
        f = forma.lower()
        if any(x in f for x in ["triangulo", "triangular", "delta"]):
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

    df['COLOR_RGBA'] = df['FORMA'].apply(color_neon)
    df['COLOR_STR'] = df['COLOR_RGBA'].apply(lambda c: f'rgba({c[0]},{c[1]},{c[2]},{c[3]/255})')
    return df

# --- CARGA DE RELACIONES (OPCIONAL) ---
def cargar_relaciones(df_nodos):
    if df_nodos.empty:
        return pd.DataFrame()

    ids_validos = set(df_nodos['ID'].unique())
    rutas = ["agatha_ufo_relationships_sample.csv", "agatha_ufo_relationships.csv"]
    dfs = []

    for ruta in rutas:
        if os.path.exists(ruta):
            try:
                df = pd.read_csv(ruta, encoding='utf-8', on_bad_lines='skip')
                df.columns = [str(c).strip().upper() for c in df.columns]
                col_src = [c for c in df.columns if 'SOURCE' in c or 'ORIGEN' in c][0]
                col_tgt = [c for c in df.columns if 'TARGET' in c or 'DESTINO' in c][0]
                df.rename(columns={col_src: 'SRC_ID', col_tgt: 'TGT_ID'}, inplace=True)

                df['SRC_ID'] = pd.to_numeric(df['SRC_ID'], errors='coerce')
                df['TGT_ID'] = pd.to_numeric(df['TGT_ID'], errors='coerce')
                df = df.dropna(subset=['SRC_ID', 'TGT_ID'])
                df = df[df['SRC_ID'].isin(ids_validos) & df['TGT_ID'].isin(ids_validos)]
                df['TIPO'] = df.get('RELATIONSHIP', 'Desconocida').fillna('Desconocida')
                df['PESO'] = pd.to_numeric(df.get('WEIGHT', 0.5), errors='coerce').fillna(0.5)
                dfs.append(df)
            except Exception as e:
                st.sidebar.write(f"Error cargando {ruta}: {e}")

    if not dfs:
        return pd.DataFrame()

    df_rel = pd.concat(dfs, ignore_index=True)
    df_coords = df_nodos.set_index('ID')[['lat', 'lon', 'CIUDAD', 'PAIS']]
    df_rel['origen_lat'] = df_rel['SRC_ID'].map(df_coords['lat'])
    df_rel['origen_lon'] = df_rel['SRC_ID'].map(df_coords['lon'])
    df_rel['destino_lat'] = df_rel['TGT_ID'].map(df_coords['lat'])
    df_rel['destino_lon'] = df_rel['TGT_ID'].map(df_coords['lon'])
    df_rel['origen_ciudad'] = df_rel['SRC_ID'].map(df_coords['CIUDAD'])
    df_rel['destino_ciudad'] = df_rel['TGT_ID'].map(df_coords['CIUDAD'])
    df_rel = df_rel.dropna(subset=['origen_lat', 'origen_lon', 'destino_lat', 'destino_lon'])
    return df_rel

# --- DATOS PRINCIPALES (SIEMPRE LOS DE EJEMPLO) ---
df_maestro = crear_datos_ejemplo()
df_grafos = cargar_relaciones(df_maestro)

# --- SIDEBAR: FILTROS ---
st.sidebar.markdown("### Centro de Comando AGATHA")

# Regiones para el mapa
regiones = {
    "Vista Orbital Global": {"lat": 20.0, "lon": 0.0},
    "Norteamérica": {"lat": 39.8, "lon": -98.5},
    "Europa": {"lat": 50.0, "lon": 10.0}
}
filtro_region = st.sidebar.selectbox("Ámbito Geopolítico", list(regiones.keys()))

# Filtros
st.sidebar.markdown("---")
st.sidebar.markdown("### Filtros Avanzados")

# Décadas
decadas = sorted(df_maestro['DECADA'].unique())
decadas_sel = st.sidebar.multiselect("Década", decadas, default=decadas)

# Países
paises = sorted(df_maestro['PAIS'].unique())
paises_sel = st.sidebar.multiselect("País", paises, default=paises)

# Formas
formas = sorted(df_maestro['FORMA'].unique())
formas_sel = st.sidebar.multiselect("Forma", formas, default=formas)

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
]

# Controles de visualización
st.sidebar.markdown("---")
mostrar_puntos = st.sidebar.toggle("Puntos de Contacto", value=True)
mostrar_arcos = st.sidebar.toggle("Grafos de Trayectoria", value=True)

if not df_grafos.empty:
    tipos_relacion = st.sidebar.multiselect(
        "Tipos de relación",
        df_grafos['TIPO'].unique(),
        default=df_grafos['TIPO'].unique()
    )
else:
    tipos_relacion = []

# --- ENCABEZADO ---
st.markdown("<h1>Motor de Análisis Conductual Predictivo</h1>", unsafe_allow_html=True)
st.markdown("<h3>Módulo FANI: Fenómenos Anómalos No Identificados</h3>", unsafe_allow_html=True)

# --- MÉTRICAS ---
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Registros Activos", f"{len(df_filtrado):,}")
col_m2.metric("Tipología Predominante", df_filtrado['FORMA'].mode().iloc[0] if not df_filtrado.empty else "N/A")
col_m3.metric("Zonas de Interés", len(df_filtrado[['lat', 'lon']].drop_duplicates()))
col_m4.metric("Conexiones Activas", len(df_grafos) if mostrar_arcos else 0)

st.markdown("---")

# --- PESTAÑAS ---
tab_visor, tab_datos, tab_analisis = st.tabs(["Visor Orbital", "Registros", "NLP Forense"])

# --- TAB 1: MAPA ---
with tab_visor:
    if df_filtrado.empty:
        st.warning("No hay datos para los filtros seleccionados.")
    else:
        df_filtrado['RESUMEN_CORTO'] = df_filtrado['RESUMEN'].apply(lambda x: x[:100] + "...")
        fig = go.Figure()

        if mostrar_puntos:
            fig.add_trace(go.Scattergeo(
                lon=df_filtrado['lon'],
                lat=df_filtrado['lat'],
                mode='markers',
                marker=dict(
                    size=8,
                    color=df_filtrado['COLOR_STR'],
                    line=dict(width=0.5, color='white'),
                    opacity=0.9
                ),
                text=df_filtrado['CIUDAD'] + ', ' + df_filtrado['PAIS'] + '<br>' +
                     'Forma: ' + df_filtrado['FORMA'] + '<br>' +
                     'Año: ' + df_filtrado['AÑO'].astype(str) + '<br>' +
                     'Día: ' + df_filtrado['DIA_SEMANA'] + '<br>' +
                     df_filtrado['RESUMEN_CORTO'],
                hoverinfo='text',
                name='Avistamientos'
            ))

        if mostrar_arcos and not df_grafos.empty:
            df_rel_filt = df_grafos.copy()
            if tipos_relacion:
                df_rel_filt = df_rel_filt[df_rel_filt['TIPO'].isin(tipos_relacion)]

            for _, row in df_rel_filt.iterrows():
                fig.add_trace(go.Scattergeo(
                    lon=[row['origen_lon'], row['destino_lon'], None],
                    lat=[row['origen_lat'], row['destino_lat'], None],
                    mode='lines',
                    line=dict(width=row['PESO']*2, color='rgba(0,255,255,0.3)'),
                    hoverinfo='text',
                    text=f"{row['TIPO']} ({row['PESO']})<br>{row['origen_ciudad']} → {row['destino_ciudad']}",
                    showlegend=False
                ))

        region = regiones[filtro_region]
        fig.update_layout(
            geo=dict(
                projection_type='orthographic',
                showland=True,
                landcolor='rgb(30,30,30)',
                oceancolor='rgb(10,10,10)',
                countrycolor='rgb(80,80,80)',
                coastlinecolor='rgb(100,100,100)',
                projection_rotation=dict(lon=region['lon'], lat=region['lat'])
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='#0a0a0a',
            height=700
        )
        st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: TABLA ---
with tab_datos:
    st.markdown("#### Registros Forenses")
    if df_filtrado.empty:
        st.warning("Sin datos")
    else:
        cols = ['ID', 'AÑO', 'PAIS', 'CIUDAD', 'FORMA', 'RESUMEN']
        st.dataframe(df_filtrado[cols], use_container_width=True, hide_index=True)

# --- TAB 3: NLP ---
with tab_analisis:
    st.markdown("#### Análisis NLP Forense")
    if df_filtrado.empty:
        st.warning("Seleccione datos")
    else:
        caso = st.selectbox("Expediente", df_filtrado['CIUDAD'] + " | " + df_filtrado['AÑO'].astype(str))
        resumen = df_filtrado[df_filtrado['CIUDAD'] + " | " + df_filtrado['AÑO'].astype(str) == caso]['RESUMEN'].iloc[0]
        st.text(resumen)

        if st.button("Analizar con DeepSeek"):
            st.info("Análisis simulado (conecta tu API key para resultados reales)")

# --- FOOTER ---
st.markdown("---")
st.markdown(f"<div style='text-align:center;color:#333;'>Sistema AGATHA v4.4 | Operador {OPERADOR_ID}</div>", unsafe_allow_html=True)
