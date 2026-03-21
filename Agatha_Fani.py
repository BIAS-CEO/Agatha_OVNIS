# ====================================================================
# ARCHIVO PRINCIPAL: Agatha_Fani.py
# SISTEMA: Motor de Analisis Conductual Predictivo
# MODULO: AGATHA (Intelligent Neural Network)
# SUB-MODULO: MÓDULO CONTACT (Fenómeno Anómalo No Identificado)
# VERSION: Opcon Ready v6.3 (Full Muscle Recovery & Syntax Shield)
# OPERADOR: DIR-74 | NIVEL 4 - INTELIGENCIA ESTRATEGICA
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

# --- CONFIGURACION DE PAGINA ---
st.set_page_config(
    page_title="AGATHA - Inteligencia Predictiva",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS CORPORATIVO MATE CON COLORES ELÉCTRICOS (Blueprint Aesthetic) ---
CSS_MATE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@300;400;600;700&family=Montserrat:wght@700&family=Share+Tech+Mono&display=swap');

.stApp { 
    background-color: #0a0a0a !important; 
    font-family: 'Titillium Web', sans-serif !important; 
    color: #e2e8f0 !important; 
}
[data-testid="stHeader"], footer, [data-testid="collapsedControl"] { display: none !important; }
.block-container { 
    padding-top: 2rem !important; 
    padding-bottom: 2rem !important; 
    max-width: 98% !important; 
}

/* Identidad Visual AGATHA */
h1 { 
    font-family: 'Montserrat', sans-serif !important; 
    text-transform: uppercase; 
    letter-spacing: -0.5px; 
    font-size: 2.2rem !important; 
    color: #ffffff !important; 
    border-bottom: 2px solid #334155; 
    padding-bottom: 10px; 
    margin-bottom: 0.5rem !important;
}
.agatha-title-acc { color: #00d4ff !important; }
.agatha-subtitle { color: #ffffff !important; font-family: 'Share Tech Mono', monospace; font-size: 1.1rem; letter-spacing: 2px; }

/* Inyección de Cian Eléctrico */
.expander-title-acc { color: #00d4ff !important; font-weight: 600 !important; letter-spacing: 1px; text-transform: uppercase; }

/* Métricas Tácticas */
[data-testid="stMetric"] { background-color: #1a1a1a !important; border: 1px solid #333333 !important; border-left: 3px solid #00d4ff !important; padding: 15px !important; border-radius: 0px !important; box-shadow: none !important; }
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.75rem !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.5px; }
[data-testid="stMetricValue"] { color: #ffffff !important; font-family: 'Share Tech Mono', monospace !important; font-size: 2rem !important; font-weight: 400 !important; }

/* Botones y UI */
.stButton > button { border: 1px solid #333333 !important; background-color: #1a1a1a !important; color: #e2e8f0 !important; border-radius: 0px !important; font-family: 'Montserrat', sans-serif !important; font-weight: 600 !important; text-transform: uppercase; font-size: 0.75rem !important; letter-spacing: 1px; padding: 0.8rem 1.5rem !important; transition: all 0.2s ease; width: 100%; }
.stButton > button:hover { border-color: #00d4ff !important; color: #ffffff !important; background-color: #0f172a !important; }

/* Estilo para imágenes en expander (zoom forense) */
[data-testid="stExpander"] img { width: 100% !important; height: auto !important; cursor: zoom-in; }
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

# --- MOTOR DE DATOS Y CARGA ---
def obtener_credencial(nombre_var):
    try:
        if hasattr(st, "secrets") and nombre_var in st.secrets:
            return st.secrets[nombre_var]
    except Exception: pass
    return os.environ.get(nombre_var)

DEEPSEEK_API_KEY = obtener_credencial("DEEPSEEK_API_KEY")

def encontrar_archivo(nombres_posibles):
    for nombre in nombres_posibles:
        rutas = [nombre, os.path.join("data", nombre), os.path.join(".", nombre)]
        for r in rutas:
            if os.path.exists(r): return r
    return None

def simular_coordenadas(df):
    np.random.seed(42)
    # Centroid mapping for key regions
    centroides = {
        "ESPAÑA": (40.46, -3.75), "MEXICO": (23.6, -102.5), "MÉXICO": (23.6, -102.5),
        "USA": (39.8, -98.5), "ESTADOS UNIDOS": (39.8, -98.5), "UK": (55.3, -3.4), 
        "CANADA": (56.1, -106.3), "PORTUGAL": (39.39, -8.22), "FRANCIA": (46.22, 2.21)
    }
    
    pai = df['PAIS'].astype(str).str.upper().str.strip()
    df['lat_base'] = pai.map(centroides).apply(lambda x: x[0] if isinstance(x, tuple) else 0.0)
    df['lon_base'] = pai.map(centroides).apply(lambda x: x[1] if isinstance(x, tuple) else 0.0)
    
    # Deterministic jitter based on city name to avoid point overlapping
    df['jitter'] = df['CIUDAD'].astype(str).apply(lambda x: sum(ord(c) for c in x))
    df['lat'] = df['lat_base'] + ((df['jitter'] % 100) - 50) / 40.0
    df['lon'] = df['lon_base'] + (((df['jitter'] // 10) % 100) - 50) / 40.0
    
    return df.drop(columns=['lat_base', 'lon_base', 'jitter'])

@st.cache_data(show_spinner=False)
def cargar_nodos():
    nombres = ["agatha_ufo_nodes_full.csv", "agatha_ufo_master.csv", "agatha_ufo_nodes.csv"]
    ruta = encontrar_archivo(nombres)
    if not ruta: return pd.DataFrame(), ["Error crítico: No se localizaron archivos fuente."]
    try:
        df = pd.read_csv(ruta, encoding='utf-8', on_bad_lines='skip')
        df.columns = df.columns.str.upper().str.strip()
        
        col_map = {
            'YEAR': 'AÑO', 'MONTH': 'MES', 'DAY': 'DIA', 'DÍA': 'DIA',
            'CITY': 'CIUDAD', 'COUNTRY': 'PAIS', 'PAÍS': 'PAIS',
            'SHAPE': 'FORMA', 'SUMMARY': 'RESUMEN', 'TIME': 'HORA'
        }
        df.rename(columns=col_map, inplace=True, errors='ignore')
        
        # Sanitize text fields
        for c in ['CIUDAD', 'PAIS', 'FORMA', 'RESUMEN']:
            if c in df.columns: df[c] = df[c].fillna("No especificado").astype(str)
            else: df[c] = "No especificado"
            
        # Time processing
        df['AÑO'] = pd.to_numeric(df['AÑO'], errors='coerce').fillna(2026).astype(int)
        df['MES'] = pd.to_numeric(df['MES'], errors='coerce').fillna(0).astype(int).astype(str).replace('0', 'No especificado')
        df['DIA'] = pd.to_numeric(df['DIA'], errors='coerce').fillna(0).astype(int).astype(str).replace('0', 'No especificado')
        
        if 'HORA' not in df.columns: df['HORA'] = "No especificada"
        def clean_time(h):
            val = str(h).strip()
            if ":" not in val or len(val) < 3: return "No especificada"
            parts = val.split(":")
            return f"{parts[0].zfill(2)}:{parts[1].zfill(2)}"
        df['HORA'] = df['HORA'].apply(clean_time)
        
        df['FORMA'] = df['FORMA'].str.title()
        df = simular_coordenadas(df)
        df['COLOR_STR'] = '#00d4ff' # Default electric blue
        
        return df, [f"Matriz Detectada: {ruta}", f"Nodos Operativos: {len(df)}"]
    except Exception as e: return pd.DataFrame(), [f"Error de proceso: {str(e)}"]

# --- ARRANQUE DE SISTEMA ---
with st.status("Inicializando Motor de Inteligencia AGATHA...", expanded=True) as status_boot:
    df_maestro, diagn_mensajes = cargar_nodos()
    status_boot.update(label="Sistemas AGATHA v6.3 en línea. Acceso Nivel 4 Concedido.", state="complete", expanded=False)


# --- INTERFAZ PRINCIPAL ---

col_header, col_btn = st.columns([3.5, 1.5], gap="medium")
with col_header:
    st.markdown("<h1 class='agatha-title-acc'>AGATHA</h1>", unsafe_allow_html=True)
    st.markdown("<div class='agatha-subtitle'>INTELLIGENT NEURAL NETWORK</div>", unsafe_allow_html=True)
    st.markdown("<span style='color:#ffffff; font-weight:600; text-transform:uppercase; font-size:0.85rem; letter-spacing:1px;'>Sistema UAP \"Unidentified Anomalous Phenomenon\"</span>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:5px; color:#94a3b8;'>MÓDULO CONTACT - Fenómeno Anómalo No Identificado</h3>", unsafe_allow_html=True)
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("RECARGAR MATRICES"):
        st.cache_data.clear()
        st.rerun()

st.markdown("<div style='text-align:center; color:#94a3b8; font-family:Share Tech Mono; font-size:0.85rem; border-top:1px solid #334155; padding-top:12px; margin-top:15px; font-style:italic;'>\"El Universo es enorme. Y si solo estamos nosotros, cuánto espacio desaprovechado\" - Contact.</div>", unsafe_allow_html=True)


# --- MODULO 1: REPORTE CIUDADANO (NOVEDAD ESPAÑA) ---
st.markdown("---")
with st.expander("<span class='expander-title-acc'>NOTIFICA TU AVISTAMIENTO UAP - REPORTE CIUDADANO DIRECTO</span>", expanded=False):
    st.markdown("<div style='background:#1a1a1a; padding:15px; border-left:4px solid #f59e0b; margin-bottom:15px; font-size:0.85rem;'>Módulo de notificación pública para España. AGATHA integrará su reporte en el análisis predictivo global tras validación forense.</div>", unsafe_allow_html=True)
    c_r1, c_r2, c_r3 = st.columns(3)
    r_fecha = c_r1.date_input("FECHA")
    r_hora = c_r2.time_input("HORA")
    r_pais = c_r3.selectbox("PAÍS", ["España", "México", "Portugal", "USA", "Otros"])
    r_ciudad = st.text_input("CIUDAD / ZONA DE CONTACTO")
    r_tipo = st.selectbox("TIPO DE OBJETO", ["Esfera", "Triángulo", "Disco", "Cigarro", "Luz", "Cilíndrico", "Cambiante", "Flash", "Otros"])
    r_obs = st.text_area("DETALLES DEL AVISTAMIENTO (Mínimo 50 caracteres)", height=100)
    
    c_check, c_send = st.columns([3, 1])
    r_acepto = c_check.checkbox("Acepto el procesamiento de estos datos por la red neuronal AGATHA.")
    if c_send.button("ENVIAR A AGATHA"):
        if r_acepto and len(r_obs) > 50:
            st.success("Reporte enviado correctamente. AGATHA está analizando su testimonio.")
        else:
            st.error("Error en reporte. Revise la extensión del texto y los términos.")

# --- MODULO 2: KPIs TÁCTICOS ---
st.markdown("---")
df_filtrado = df_maestro.copy() # Base para métricas iniciales
m1, m2, m3 = st.columns(3)
m1.metric("REGISTROS ACTIVOS", f"{len(df_filtrado):,}")
m2.metric("TIPOLOGÍA PREDOMINANTE", df_filtrado['FORMA'].mode().iloc[0] if not df_filtrado.empty else "N/A")
m3.metric("ZONAS DE INTERÉS (NODOS)", f"{len(df_filtrado['CIUDAD'].unique()) if not df_filtrado.empty else 0:,}")

# --- MODULO 3: CATÁLOGO DE IDENTIFICACIÓN VISUAL (REUBICADO) ---
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("<span class='expander-title-acc'>CATÁLOGO UAP IDENTIFICACIÓN VISUAL DE OBJETOS - MANUAL TÁCTICO</span>", expanded=True):
    st.markdown("<div style='color:#94a3b8; font-size:0.75rem; margin-bottom:10px;'>Activo de referencia visual clasificado. Use la imagen para identificación morfológica en campo.</div>", unsafe_allow_html=True)
    if not os.path.exists("assets"): os.makedirs("assets")
    ruta_img = os.path.join("assets", "catalogo_morfologico_completo.png")
    if os.path.exists(ruta_img):
        st.image(ruta_img, use_container_width=True, caption="Pinche para zoom conductual")
    else:
        st.info("Archivo 'catalogo_morfologico_completo.png' no localizado en /assets.")

# --- MODULO 4: VISUALIZACION PRINCIPAL (MAPA Y FILTROS) ---
st.markdown("---")
col_map, col_filt = st.columns([2.5, 1.5], gap="large")

with col_filt:
    st.markdown("#### Parámetros de Filtrado")
    cf1, cf2 = st.columns(2)
    s_anio = cf1.selectbox("AÑO", ["TODOS"] + sorted(list(df_maestro['AÑO'].unique()), reverse=True))
    s_mes = cf2.selectbox("MES", ["TODOS"] + sorted(list(df_maestro['MES'].unique())))
    
    cf3, cf4 = st.columns(2)
    s_dia = cf3.selectbox("DÍA", ["TODOS"] + sorted(list(df_maestro['DIA'].unique())))
    s_hora = cf4.selectbox("HORA", ["TODAS"] + sorted(list(df_maestro['HORA'].unique())))

    s_forma = st.selectbox("TIPO DE OBJETO UAP", ["TODOS"] + sorted(list(df_maestro['FORMA'].unique())))
    s_pais = st.selectbox("PAÍS", ["TODOS"] + sorted(list(df_maestro['PAIS'].unique())))

    # Filtrado en tiempo real
    if s_anio != "TODOS": df_filtrado = df_filtrado[df_filtrado['AÑO'] == s_anio]
    if s_mes != "TODOS": df_filtrado = df_filtrado[df_filtrado['MES'] == s_mes]
    if s_dia != "TODOS": df_filtrado = df_filtrado[df_filtrado['DIA'] == s_dia]
    if s_hora != "TODAS": df_filtrado = df_filtrado[df_filtrado['HORA'] == s_hora]
    if s_forma != "TODOS": df_filtrado = df_filtrado[df_filtrado['FORMA'] == s_forma]
    if s_pais != "TODOS": df_filtrado = df_filtrado[df_filtrado['PAIS'] == s_pais]

with col_map:
    cm1, cm2 = st.columns(2)
    m_visor = cm1.radio("MODO TÁCTICO", ["Nodos Base UAP", "Red de Trayectorias"], horizontal=True)
    m_proy = cm2.radio("PROYECCIÓN", ["Globo 3D", "Plano 2D"], horizontal=True)
    
    if not df_filtrado.empty:
        placeholder_mapa = st.empty()
        with st.spinner("Sincronizando Red Neuronal AGATHA..."):
            fig = go.Figure()
            
            if m_visor == "Nodos Base UAP":
                df_view = df_filtrado.head(8000)
                fig.add_trace(go.Scattergeo(
                    lon=df_view['lon'], lat=df_view['lat'], mode='markers',
                    marker=dict(size=6, color='#00d4ff', opacity=0.8),
                    text=df_view['CIUDAD'] + " | " + df_view['HORA'] + " (" + df_view['FORMA'] + ")", hoverinfo='text'
                ))
            else:
                # Rutas y Puentes
                df_net = df_filtrado.sort_values(by=['AÑO','MES','DIA','HORA']).head(250)
                formas_net = df_net['FORMA'].unique()
                for f in formas_net:
                    df_f = df_net[df_net['FORMA'] == f]
                    if len(df_f) > 1:
                        fig.add_trace(go.Scattergeo(
                            lon=df_f['lon'], lat=df_f['lat'], mode='lines',
                            line=dict(width=1.5, color='#00d4ff'), opacity=0.35, hoverinfo='none'
                        ))
                fig.add_trace(go.Scattergeo(
                    lon=df_net['lon'], lat=df_net['lat'], mode='markers',
                    marker=dict(size=6, color='#ffffff', opacity=0.9),
                    text=df_net['CIUDAD'] + " (" + df_net['FORMA'] + ")", hoverinfo='text'
                ))
            
            fig.update_layout(
                geo=dict(projection_type='orthographic' if m_proy == "Globo 3D" else 'equirectangular',
                         showland=True, landcolor='#121212', oceancolor='#050505', showocean=True, bgcolor='#0a0a0a', resolution=50),
                margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='#0a0a0a', height=550, showlegend=False
            )
            placeholder_mapa.plotly_chart(fig, use_container_width=True)

# --- MODULO 5: EXPANSION DE INTELIGENCIA (ORBITAL Y DB) ---
st.markdown("---")
with st.expander("<span class='expander-title-acc'>REPORTE ORBITAL (SATÉLITES) Y BASES DE DATOS ADICIONALES</span>", expanded=False):
    st.markdown("<div style='color:#cbd5e1; font-size:0.85rem; line-height:1.5; background:#1a1a1a; padding:15px; border-left:3px solid #00d4ff;'>Integración técnica de fuentes externas analizadas por AGATHA para descarte de satélites o correlación de reportes históricos.</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    ei1, ei2, ei3 = st.columns(3)
    ei1.markdown("**RED ORBITAL IN-THE-SKY** \nMonitorización de Starlink e Iridium en tiempo real.  \n[ACCEDER A MAPA DE SATÉLITES](https://in-the-sky.org/satmap_worldmap.php?gps=1)")
    ei2.markdown("**BASE DE DATOS NUFORC** \nArchivo histórico global con campo de explicación técnico.  \n[ACCEDER A BASE DE DATOS](https://nuforc.org/databank/)")
    ei3.markdown("**INTELIGENCIA GLOBAL X** \nRedes de reporte ciudadano monitorizadas por AGATHA.  \n[MONITORIZAR REDES](https://x.com/Marc296134/status/2034826362926612919)")

# --- MODULO 6: PROCESADO FORENSE NLP (SINTAXIS BLINDADA) ---
st.markdown("---")
with st.expander("<span class='expander-title-acc'>PROCESADO FORENSE - INTELIGENCIA AGATHA</span>", expanded=False):
    if not df_filtrado.empty:
        df_nlp = df_filtrado.copy()
        df_nlp['TAG'] = df_nlp['CIUDAD'] + " | " + df_nlp['FORMA'] + " | " + df_nlp['AÑO'].astype(str)
        exp_sel = st.selectbox("Seleccionar Expediente Forense para Análisis Conductual", df_nlp['TAG'].unique()[:300])
        resumen_txt = str(df_nlp[df_nlp['TAG'] == exp_sel].iloc[0]['RESUMEN'])
        st.markdown(f"<div style='background:#111; padding:20px; border-left:4px solid #00d4ff; color:#e2e8f0;'>{resumen_txt}</div>", unsafe_allow_html=True)
        
        if st.button("EJECUTAR ANÁLISIS DE INTELIGENCIA"):
            if DEEPSEEK_API_KEY:
                with st.spinner("AGATHA analizando patrones de comportamiento..."):
                    try:
                        headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
                        payload = {
                            "model": "deepseek-chat",
                            "messages": [
                                {"role": "system", "content": "Analiza y responde solo en JSON: {comportamiento, credibilidad, indice_anomalia, hipotesis}"},
                                {"role": "user", "content": resumen_txt}
                            ],
                            "response_format": {"type": "json_object"}
                        }
                        r = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload, timeout=20)
                        
                        # Extracción segura de la respuesta de la IA
                        data_json = r.json()
                        content = data_json["choices"][0]["message"]["content"]
                        
                        # Limpieza de bloques de código markdown si los hubiera
                        if "```json" in content:
                            content = content.split("```json")[1].split("```")[0]
                        elif "```" in content:
                            content = content.split("```")[1].split("```")[0]
                        
                        st.json(json.loads(content.strip()))
                    except Exception as e:
                        st.error("Error en conexión con el nodo de inteligencia central de AGATHA.")
            else:
                st.warning("Nodo de inteligencia AGATHA no configurado en los secretos del sistema.")

# --- MODULO 7: TABLA DE DATOS ---
with st.expander(f"REGISTROS FORENSES UAP ({len(df_filtrado)} ACTIVOS)", expanded=False):
    cols_tabla = ['AÑO', 'MES', 'DIA', 'HORA', 'CIUDAD', 'PAIS', 'FORMA', 'RESUMEN']
    st.dataframe(df_filtrado[cols_tabla].sort_values(by=['AÑO','MES','DIA'], ascending=False).head(1000), width='stretch', hide_index=True)

# Pie de página técnico final
st.markdown("<div style='font-family:Share Tech Mono; color:#334155; font-size:0.7rem; text-align:right; margin-top:40px;'>AGATHA OS v6.3 | OPERADOR: DIR-74 | ENCRYPTION: AES-256 | CUARTO MILENIO OPS</div>", unsafe_allow_html=True)
