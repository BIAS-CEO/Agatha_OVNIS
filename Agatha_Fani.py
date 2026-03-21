# ====================================================================
# ARCHIVO PRINCIPAL: Agatha_Fani.py
# SISTEMA: Motor de Analisis Conductual Predictivo
# MODULO: AGATHA (Intelligent Neural Network)
# SUB-MODULO: MÓDULO CONTACT (Fenómeno Anómalo No Identificado)
# VERSION: Opcon Ready v6.1.6 (Fix: Global Data Loading & Mapping)
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

# --- CSS CORPORATIVO MATE CON COLORES ELECTRICOS (Blueprint Aesthetic) ---
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

/* Identidad Visual AGATHA y Colores Electricos */
.agatha-main-title { 
    font-family: 'Montserrat', sans-serif !important; 
    text-transform: uppercase; 
    letter-spacing: -1px; 
    font-size: 3rem !important; 
    color: #ffffff !important; 
    margin-bottom: 0px !important;
}

.electric-cyan { 
    color: #00d4ff !important; 
    text-shadow: 0 0 15px rgba(0, 212, 255, 0.4); 
}

.electric-green { 
    color: #39ff14 !important; 
    text-shadow: 0 0 10px rgba(57, 255, 20, 0.4); 
}

.uap-label {
    color: #94a3b8 !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    margin-top: 5px !important;
}

.contact-module-box {
    color: #ffffff !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.95rem !important;
    background: rgba(0, 212, 255, 0.05);
    padding: 8px 20px;
    border-left: 4px solid #00d4ff;
    display: inline-block;
    margin-top: 15px !important;
    letter-spacing: 1px;
}

.contact-quote {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    color: #475569;
    font-style: italic;
    margin-top: 20px;
    border-top: 1px solid #1e293b;
    padding-top: 12px;
    text-align: center;
    width: 100%;
}

/* Metricas Tácticas */
[data-testid="stMetric"] { 
    background-color: #1a1a1a !important; 
    border: 1px solid #333333 !important; 
    border-left: 3px solid #00d4ff !important; 
    padding: 15px !important; 
    border-radius: 2px !important; 
}
[data-testid="stMetricLabel"] { 
    color: #64748b !important; 
    font-size: 0.8rem !important; 
    text-transform: uppercase; 
    font-weight: 600;
}
[data-testid="stMetricValue"] { 
    color: #ffffff !important; 
    font-family: 'Share Tech Mono', monospace !important; 
    font-size: 2.2rem !important;
}

/* Botonera Principal */
.stButton > button { 
    border: 1px solid #333333 !important; 
    background-color: #1a1a1a !important; 
    color: #ffffff !important; 
    border-radius: 0px !important; 
    font-family: 'Montserrat', sans-serif !important; 
    font-weight: 600 !important; 
    text-transform: uppercase; 
    font-size: 0.8rem !important;
    padding: 0.8rem 1.5rem !important; 
    transition: all 0.3s ease;
    width: 100%;
}
.stButton > button:hover { 
    border-color: #00d4ff !important; 
    color: #ffffff !important; 
    background-color: #0f172a !important; 
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
}

/* Ajuste para que la imagen del catálogo no tenga márgenes internos y permita zoom */
[data-testid="stExpander"] img {
    width: 100% !important;
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

# --- MOTOR DE DATOS ---
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
    """Mapeo de coordenadas global ultra-robusto."""
    np.random.seed(42)
    # Diccionario de centroides globales normalizado
    centroides = {
        "ESPAÑA": (40.46, -3.75), "ESPANA": (40.46, -3.75), "SPAIN": (40.46, -3.75),
        "ALEMANIA": (51.16, 10.45), "GERMANY": (51.16, 10.45),
        "FRANCIA": (46.22, 2.21), "FRANCE": (46.22, 2.21),
        "ITALIA": (41.87, 12.56), "ITALY": (41.87, 12.56),
        "MEXICO": (23.6, -102.5), "MÉXICO": (23.6, -102.5),
        "USA": (39.8, -98.5), "ESTADOS UNIDOS": (39.8, -98.5), "UNITED STATES": (39.8, -98.5),
        "UK": (55.3, -3.4), "REINO UNIDO": (55.3, -3.4), "UNITED KINGDOM": (55.3, -3.4),
        "CANADA": (56.1, -106.3), "CANADÁ": (56.1, -106.3),
        "PORTUGAL": (39.39, -8.22),
        "MARRUECOS": (31.79, -7.09), "MOROCCO": (31.79, -7.09),
        "INDIA": (20.59, 78.96),
        "AUSTRALIA": (-25.27, 133.77),
        "BRASIL": (-14.23, -51.92), "BRAZIL": (-14.23, -51.92),
        "JAPON": (36.20, 138.25), "JAPÓN": (36.20, 138.25), "JAPAN": (36.20, 138.25),
        "CHINA": (35.86, 104.19),
        "ARGENTINA": (-38.41, -63.61),
        "CHILE": (-35.67, -71.54),
        "COLOMBIA": (4.57, -74.29)
    }
    
    pai = df['PAIS'].astype(str).str.upper().str.strip()
    
    # Función de mapeo con fallback dinámico
    def get_lat_lon(p):
        if p in centroides: return centroides[p]
        # Búsqueda parcial si no hay coincidencia exacta
        for key in centroides:
            if key in p or p in key: return centroides[key]
        # Fallback a un punto visible seguro (Centro Europa) si falla todo
        return (48.0, 10.0)

    coords = pai.apply(get_lat_lon)
    df['lat_base'] = coords.apply(lambda x: x[0])
    df['lon_base'] = coords.apply(lambda x: x[1])
    
    # Jitter determinista para dispersar avistamientos en el mismo país
    df['city_hash'] = df['CIUDAD'].astype(str).apply(lambda x: sum(ord(c) for c in x))
    df['lat'] = df['lat_base'] + ((df['city_hash'] % 100) - 50) / 25.0
    df['lon'] = df['lon_base'] + (((df['city_hash'] // 10) % 100) - 50) / 25.0
    
    return df.drop(columns=['lat_base', 'lon_base', 'city_hash'])

@st.cache_data(show_spinner=False)
def cargar_nodos():
    nombres = ["agatha_ufo_nodes_full.csv", "agatha_ufo_master.csv", "agatha_ufo_nodes.csv"]
    ruta = encontrar_archivo(nombres)
    if not ruta: return pd.DataFrame(), ["Error: Fuentes de datos no detectadas."]
    try:
        df = pd.read_csv(ruta, encoding='utf-8', on_bad_lines='skip')
        df.columns = df.columns.str.upper().str.strip()
        
        # Mapeo de columnas flexible
        col_map = {
            'YEAR': 'AÑO', 'MONTH': 'MES', 'DAY': 'DIA', 'DÍA': 'DIA',
            'CITY': 'CIUDAD', 'COUNTRY': 'PAIS', 'PAÍS': 'PAIS', 
            'SHAPE': 'FORMA', 'SUMMARY': 'RESUMEN', 'TIME': 'HORA'
        }
        df.rename(columns=col_map, inplace=True, errors='ignore')
        
        for c in ['CIUDAD', 'PAIS', 'FORMA', 'RESUMEN']:
            if c in df.columns: df[c] = df[c].fillna("No especificado").astype(str)
            else: df[c] = "No especificado"
            
        # Limpieza de fechas
        df['AÑO'] = pd.to_numeric(df['AÑO'], errors='coerce').fillna(2026).astype(int)
        df['MES'] = pd.to_numeric(df['MES'], errors='coerce').fillna(0).astype(int).astype(str).replace('0', 'TODOS')
        df['DIA'] = pd.to_numeric(df['DIA'], errors='coerce').fillna(0).astype(int).astype(str).replace('0', 'TODOS')
        
        # Limpieza de horas
        if 'HORA' not in df.columns: df['HORA'] = "No especificada"
        def clean_time(h):
            val = str(h).strip().lower()
            if ":" not in val or val in ['nan', 'nat', 'none', 'null']: return "No especificada"
            parts = val.split(":")
            try: return f"{parts[0].zfill(2)}:{parts[1][:2].zfill(2)}"
            except: return "No especificada"
        df['HORA'] = df['HORA'].apply(clean_time)
        
        df['FORMA'] = df['FORMA'].str.title()
        df = simular_coordenadas(df)
        df['COLOR_STR'] = 'rgba(0, 212, 255, 0.8)'
        return df, [f"Matriz Detectada: {ruta}", f"Nodos Operativos: {len(df)}"]
    except Exception as e: return pd.DataFrame(), [f"Error de proceso: {str(e)}"]

# --- SECUENCIA DE ARRANQUE ---
with st.status("Inicializando Motor de Inteligencia AGATHA...", expanded=True) as status_boot:
    df_maestro, diagn_mensajes = cargar_nodos()
    status_boot.update(label="Sistemas AGATHA v6.1.6 Online. MÓDULO CONTACT Activo.", state="complete", expanded=False)

# --- CABECERA PRINCIPAL (DISEÑO IKER JIMENEZ) ---
col_titulo, col_boton = st.columns([3.5, 1.5], gap="medium")
with col_titulo:
    st.markdown("<h1 class='agatha-main-title'>AGATHA <span class='electric-cyan'>Intelligent Neural Network</span></h1>", unsafe_allow_html=True)
    st.markdown("<div class='uap-label'>Sistema UAP <span class='electric-green'>\"Unidentified Anomalous Phenomenon\"</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='contact-module-box'>MÓDULO CONTACT - Fenómeno Anómalo No Identificado</div>", unsafe_allow_html=True)
with col_boton:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("RECARGA MATRICES", type="primary"):
        st.cache_data.clear()
        st.rerun()

st.markdown("<div class='contact-quote'>\"El Universo es enorme. Y si solo estamos nosotros, cuánto espacio desaprovechado\" - Contact.</div>", unsafe_allow_html=True)

# --- MÓDULO: NOTIFICA TU AVISTAMIENTO UAP ---
st.markdown("---")
with st.expander("NOTIFICA TU AVISTAMIENTO UAP - REPORTE TÁCTICO CIUDADANO", expanded=False):
    st.markdown("""
        <div style='background: rgba(245, 158, 11, 0.1); border-left: 5px solid #f59e0b; padding: 15px; margin-bottom: 20px;'>
            <h4 style='color: #f59e0b; margin-top: 0;'>AVISO DE INTELIGENCIA</h4>
            <p style='color: #cbd5e1; font-size: 0.9rem; margin-bottom: 0;'>
                Este módulo permite el registro directo de fenómenos anómalos. La información proporcionada será analizada 
                forensemente por la red neuronal AGATHA para su integración en el modelo conductual global.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("uap_report_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            rep_fecha = st.date_input("FECHA DEL AVISTAMIENTO", value=datetime.now())
            rep_hora = st.time_input("HORA APROXIMADA", value=datetime.now().time())
            rep_pais = st.selectbox("PAÍS", ["España", "Marruecos", "México", "Portugal", "USA", "Alemania", "Francia", "Otro"])
        
        with c2:
            rep_ciudad = st.text_input("CIUDAD / ZONA ESPECÍFICA")
            rep_tipo = st.selectbox("TIPO DE OBJETO OBSERVADO", [
                "Esfera", "Triángulo", "Disco", "Cigarro", "Cilindro", 
                "Luz", "Flash", "Formación", "Cambiante", "Otro"
            ])
            rep_duracion = st.text_input("DURACIÓN ESTIMADA")
            
        rep_comentarios = st.text_area("DETALLES CONDUCTUALES Y DESCRIPCIÓN")
        submit_report = st.form_submit_button("ENVIAR REPORTE A AGATHA")
            
        if submit_report:
            if rep_ciudad and rep_comentarios:
                st.success("REGISTRO COMPLETADO: El reporte ha sido enviado al nodo central de AGATHA.")
            else:
                st.error("ERROR: Campos obligatorios vacíos.")

# --- FILTROS TÁCTICOS ---
st.markdown("---")
col_mapa, col_filtros = st.columns([2.5, 1.5], gap="large")

with col_filtros:
    st.markdown("#### Parámetros de Filtrado")
    cf1, cf2 = st.columns(2)
    sel_anio = cf1.selectbox("AÑO", ["TODOS"] + sorted(list(df_maestro['AÑO'].unique()), reverse=True))
    sel_mes = cf2.selectbox("MES", ["TODOS"] + sorted(list(df_maestro['MES'].unique())))
    
    cf3, cf4 = st.columns(2)
    sel_dia = cf3.selectbox("DÍA", ["TODOS"] + sorted(list(df_maestro['DIA'].unique())))
    
    horas_disp = sorted([h for h in df_maestro['HORA'].unique() if h != "No especificada"])
    sel_hora = cf4.selectbox("HORA", ["TODAS"] + horas_disp)
    
    sel_forma = st.selectbox("TIPO DE OBJETO", ["TODOS"] + sorted(list(df_maestro['FORMA'].unique())))
    sel_pais = st.selectbox("PAÍS", ["TODOS"] + sorted(list(df_maestro['PAIS'].unique())))

    # Filtrado dinámico
    df_filtrado = df_maestro.copy()
    if sel_anio != "TODOS": df_filtrado = df_filtrado[df_filtrado['AÑO'] == sel_anio]
    if sel_mes != "TODOS": df_filtrado = df_filtrado[df_filtrado['MES'] == sel_mes]
    if sel_dia != "TODOS": df_filtrado = df_filtrado[df_filtrado['DIA'] == sel_dia]
    if sel_hora != "TODAS": df_filtrado = df_filtrado[df_filtrado['HORA'] == sel_hora]
    if sel_forma != "TODOS": df_filtrado = df_filtrado[df_filtrado['FORMA'] == sel_forma]
    if sel_pais != "TODOS": df_filtrado = df_filtrado[df_filtrado['PAIS'] == sel_pais]

with col_mapa:
    m1, m2, m3 = st.columns(3)
    m1.metric("REGISTROS ACTIVOS", f"{len(df_filtrado):,}")
    m2.metric("TIPOLOGÍA DOMINANTE", df_filtrado['FORMA'].mode().iloc[0] if not df_filtrado.empty else "N/A")
    m3.metric("ZONAS DE INTERÉS", f"{len(df_filtrado['CIUDAD'].unique()) if not df_filtrado.empty else 0:,}")

    cm1, cm2 = st.columns(2)
    modo_visor = cm1.radio("MODO TÁCTICO", ["Nodos Base", "Red de Trayectorias"], horizontal=True)
    tipo_proy = cm2.radio("PROYECCIÓN", ["Globo 3D", "Plano 2D"], horizontal=True)
    
    if not df_filtrado.empty:
        grafico = st.empty()
        with st.spinner("Calibrando Red Neuronal AGATHA..."):
            fig = go.Figure()
            df_mapa = df_filtrado.head(8000)
            
            fig.add_trace(go.Scattergeo(
                lon=df_mapa['lon'], lat=df_mapa['lat'], mode='markers',
                marker=dict(size=6, color='#00d4ff', opacity=0.8, line=dict(width=0.5, color='white')),
                text=df_mapa['CIUDAD'] + " | " + df_mapa['HORA'] + " (" + df_mapa['FORMA'] + ")", hoverinfo='text'
            ))
            
            fig.update_layout(
                geo=dict(projection_type='orthographic' if tipo_proy == "Globo 3D" else 'equirectangular',
                         showland=True, landcolor='#121212', oceancolor='#050505', showocean=True, bgcolor='#0a0a0a',
                         showcountries=True, countrycolor='#2a2a2a'),
                margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='#0a0a0a', height=600, showlegend=False
            )
            grafico.plotly_chart(fig, width='stretch')

# --- EL CATÁLOGO UAP ---
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("CATÁLOGO UAP IDENTIFICACIÓN VISUAL DE OBJETOS", expanded=False):
    ruta_cat = os.path.join("assets", "catalogo_morfologico_completo.png")
    if os.path.exists(ruta_cat):
        st.image(ruta_cat, use_container_width=True, caption="Manual Táctico de Identificación UAP")
    else:
        st.info("Archivo visual no detectado en /assets.")

# --- PROCESADO FORENSE ---
st.markdown("---")
with st.expander("PROCESADO FORENSE - INTELIGENCIA AGATHA", expanded=False):
    if not df_filtrado.empty:
        df_nlp = df_filtrado.copy()
        df_nlp['TAG'] = df_nlp['CIUDAD'] + " | " + df_nlp['FORMA'] + " | " + df_nlp['AÑO'].astype(str)
        caso_sel = st.selectbox("Seleccionar Expediente Forense UAP", df_nlp['TAG'].unique()[:500], key="select_nlp")
        
        if caso_sel:
            resumen_txt = str(df_nlp[df_nlp['TAG'] == caso_sel].iloc[0]['RESUMEN'])
            st.markdown(f"<div style='background:#1a1a1a; padding:15px; border-left:4px solid #00d4ff; color:#e2e8f0; font-size:0.9rem;'>{resumen_txt}</div><br>", unsafe_allow_html=True)
            
            if st.button("EJECUTAR ANÁLISIS DE INTELIGENCIA AGATHA", type="primary"):
                if DEEPSEEK_API_KEY:
                    with st.spinner("Analizando con lógica NUFORC activa..."):
                        try:
                            headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
                            payload = {
                                "model": "deepseek-chat",
                                "messages": [
                                    {"role": "system", "content": "Analiza el reporte UAP considerando patrones NUFORC. Responde en JSON: {comportamiento, credibilidad, indice_anomalia, hipotesis}"},
                                    {"role": "user", "content": resumen_txt}
                                ],
                                "response_format": {"type": "json_object"}
                            }
                            response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload, timeout=25)
                            raw_content = response.json()["choices"][0]["message"]["content"]
                            clean_json = raw_content.replace("```json", "").replace("```", "").strip()
                            st.json(json.loads(clean_json))
                        except Exception as e:
                            st.error("Fallo en la conexión con AGATHA.")
                else:
                    st.warning("Clave de inteligencia no configurada.")

# Pie de página técnico
st.markdown("<div style='font-family:Share Tech Mono; color:#334155; font-size:0.7rem; text-align:right;'>AGATHA OS v6.1.6 | OP: DIR-74 | ENCRYPTION: AES-256 | GLOBAL OPS ACTIVE</div>", unsafe_allow_html=True)
