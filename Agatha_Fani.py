# ====================================================================
# ARCHIVO PRINCIPAL: app.py (Módulo CONTACT)
# SISTEMA: Motor de Analisis Conductual Predictivo
# MODULO: MÓDULO CONTACT - Fenómeno Anómalo No Identificado
# VERSION: Opcon Ready v7.0 (Agatha Neural Edition)
# OPERADOR: DIR-74
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
    page_title="AGATHA Intelligent Neural Network",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS CORPORATIVO ELECTRICO (Flat Corporate + Neon) ---
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
    padding-top: 1.5rem !important; 
    padding-bottom: 2rem !important; 
    max-width: 98% !important; 
}

/* Colores Electricos Agatha */
.cian-electrico { color: #00f3ff !important; font-weight: 700; }
.verde-neon { color: #39ff14 !important; font-weight: 700; }
.mono-tech { font-family: 'Share Tech Mono', monospace !important; }

h1 { 
    font-family: 'Montserrat', sans-serif !important; 
    text-transform: uppercase; 
    letter-spacing: -0.5px; 
    font-size: 2.2rem !important; 
    color: #ffffff !important; 
    border-bottom: 2px solid #00f3ff; 
    padding-bottom: 12px; 
    margin-bottom: 0.2rem !important;
}
.quote-contact {
    font-style: italic;
    color: #64748b;
    font-size: 0.85rem;
    margin-bottom: 1.5rem;
}

h2, h3, h4 { 
    color: #94a3b8 !important; 
    text-transform: uppercase; 
    letter-spacing: 1.5px; 
    font-family: 'Montserrat', sans-serif !important; 
    font-weight: 600 !important; 
    font-size: 0.95rem !important;
    margin-top: 1rem !important;
}

[data-testid="stMetric"] { 
    background-color: #111111 !important; 
    border: 1px solid #333333 !important; 
    border-left: 4px solid #00f3ff !important; 
    padding: 15px !important; 
    border-radius: 0px !important; 
}
[data-testid="stMetricLabel"] { 
    color: #64748b !important; 
    font-size: 0.75rem !important; 
    text-transform: uppercase; 
}
[data-testid="stMetricValue"] { 
    color: #ffffff !important; 
    font-family: 'Share Tech Mono', monospace !important; 
}

/* Estilo para el formulario de reporte */
.notificacion-box {
    background-color: #0f172a;
    border: 1px solid #1e293b;
    padding: 20px;
    margin-bottom: 25px;
}

.stButton > button { 
    border: 1px solid #333333 !important; 
    background-color: #1a1a1a !important; 
    color: #00f3ff !important; 
    border-radius: 0px !important; 
    font-family: 'Montserrat', sans-serif !important; 
    text-transform: uppercase; 
    font-size: 0.75rem !important;
    letter-spacing: 1px;
    padding: 0.6rem 1.2rem !important; 
}
.stButton > button:hover { 
    border-color: #39ff14 !important; 
    background-color: #050505 !important; 
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

# --- SECUENCIA DE CARGA PROGRESIVA AGATHA ---
with st.status("Inicializando AGATHA Intelligent Neural Network...", expanded=True) as status_boot:
    status_boot.write("Sincronizando MÓDULO CONTACT...")
    time.sleep(0.1)
    status_boot.write("Validando protocolos Unidentified Anomalous Phenomenon (UAP)...")
    
    def obtener_credencial(nombre_var):
        try:
            if hasattr(st, "secrets") and nombre_var in st.secrets:
                return st.secrets[nombre_var]
        except Exception: pass
        valor = os.environ.get(nombre_var)
        return valor if valor else None

    OPENAI_API_KEY = obtener_credencial("OPENAI_API_KEY")
    DEEPSEEK_API_KEY = obtener_credencial("DEEPSEEK_API_KEY")
    OPENWEATHER_API_KEY = obtener_credencial("OPENWEATHER_API_KEY")

    def encontrar_archivo(nombres_posibles):
        for nombre in nombres_posibles:
            rutas = [nombre, os.path.join("data", nombre), os.path.join(".", nombre)]
            for r in rutas:
                if os.path.exists(r): return r
        return None

    def simular_coordenadas(df):
        centroides = {
            "TX": (31.9, -99.9), "FL": (27.7, -81.6), "CA": (36.7, -119.4), "NY": (40.7, -74.0),
            "ESPAÑA": (40.46, -3.75), "UK": (55.3, -3.4), "USA": (39.8, -98.5), "FRANCIA": (46.22, 2.21)
        }
        df['ESTADO'] = df.get('ESTADO', pd.Series(["USA"]*len(df))).astype(str).str.upper().str.strip()
        df['PAIS'] = df.get('PAIS', pd.Series(["USA"]*len(df))).astype(str).str.upper().str.strip()
        
        def get_coords(row):
            base = centroides.get(row['ESTADO']) or centroides.get(row['PAIS']) or (39.8, -98.5)
            h = sum(ord(c) for c in str(row['CIUDAD']))
            return base[0] + ((h % 100)-50)/80, base[1] + (((h//10)%100)-50)/80

        coords = df.apply(get_coords, axis=1)
        df['lat'] = coords.apply(lambda x: x[0])
        df['lon'] = coords.apply(lambda x: x[1])
        return df

    @st.cache_data(show_spinner=False)
    def cargar_nodos():
        mensajes = ["Nodo Agatha Online."]
        formas_sim = ["Diamante", "Cubo", "Desconocido", "Otros", "Cruz", "Cilindro", "Circulo", 
                     "Cambiante", "Cigarro", "Cono", "Esfera", "Estrella", "Lagrima", "Oval", 
                     "Rectángulo", "Triangulo", "Bola de fuego", "Disco", "Flash", "Formacion", 
                     "Galones", "Huevo", "Luz", "Orbe"]
        
        ruta = encontrar_archivo(["agatha_ufo_nodes_full.csv", "agatha_ufo_master.csv"])
        if not ruta:
            data = []
            for i in range(1000):
                data.append({
                    'AÑO': np.random.randint(1950, 2026), 'MES': str(np.random.randint(1, 13)),
                    'DIA': str(np.random.randint(1, 29)), 'HORA': f"{np.random.randint(0,24):02d}:00",
                    'CIUDAD': "Austin", 'ESTADO': "TX", 'PAIS': "USA", 'FORMA': np.random.choice(formas_sim),
                    'RESUMEN': "Detección anómala captada por sensor térmico."
                })
            df = pd.DataFrame(data)
        else:
            df = pd.read_csv(ruta, encoding='utf-8', on_bad_lines='skip')
            df.columns = df.columns.str.upper().str.strip()
            df.rename(columns={'YEAR':'AÑO', 'CITY':'CIUDAD', 'STATE':'ESTADO', 'COUNTRY':'PAIS', 'SHAPE':'FORMA', 'SUMMARY':'RESUMEN', 'TIME':'HORA'}, inplace=True)
        
        df['AÑO'] = pd.to_numeric(df.get('AÑO', 2026), errors='coerce').fillna(2026).astype(int)
        df['FORMA'] = df.get('FORMA', 'Desconocido').fillna('Desconocido').astype(str).str.title()
        df = simular_coordenadas(df)
        return df, mensajes

    df_maestro, diagn_mensajes = cargar_nodos()
    status_boot.update(label="Sistema UAP Online. Acceso AGATHA nivel 5.", state="complete", expanded=False)

# --- CABECERA ---
st.markdown("<h1>AGATHA <span class='cian-electrico'>Intelligent Neural Network</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='mono-tech verde-neon' style='margin-bottom:2px;'>MÓDULO CONTACT - Fenómeno Anómalo No Identificado</p>", unsafe_allow_html=True)
st.markdown("<p class='quote-contact'>“El Universo es enorme. Y si solo estamos nosotros, cuánto espacio desaprovechado”</p>", unsafe_allow_html=True)

# --- MODULO DE REPORTE CIUDADANO (NOTIFICA TU AVISTAMIENTO) ---
with st.container():
    st.markdown("<div class='notificacion-box'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0px; color:#00f3ff !important;'>NOTIFICA TU AVISTAMIENTO</h4>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    r_fecha = c1.date_input("FECHA")
    r_hora = c2.time_input("HORA")
    r_tipo = c3.selectbox("TIPO DE OBJETO", ["Desconocido", "Luz", "Esfera", "Triangulo", "Disco", "Otros"])
    r_ciudad = c4.text_input("CIUDAD / UBICACIÓN")
    r_desc = st.text_area("DESCRIPCIÓN DE LA CONDUCTA DEL OBJETO")
    if st.button("ENVIAR A RED NEURONAL AGATHA"):
        st.success("Reporte cifrado y enviado a la base de datos maestra.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- INDICADORES GLOBALES ---
# Usamos lógica v5.8: totales por defecto, filtrados si se activan
m1, m2, m3 = st.columns(3)
met_total = len(df_maestro)
met_forma = df_maestro['FORMA'].mode().iloc[0]
met_nodos = len(df_maestro['CIUDAD'].unique())

m1.metric("REGISTROS ACTIVOS", f"{met_total:,}")
m2.metric("TIPOLOGIA PREDOMINANTE", met_forma)
m3.metric("ZONAS DE INTERES (NODOS)", f"{met_nodos:,}")

# --- CATALOGO UAP IDENTIFICACIÓN VISUAL ---
with st.expander("CATÁLOGO UAP IDENTIFICACIÓN VISUAL DE OBJETOS", expanded=False):
    st.markdown("<p style='font-size:0.8rem; color:#64748b;'>Seleccione un objeto para ampliar. Referencia técnica de 24 morfologías detectadas.</p>", unsafe_allow_html=True)
    ruta_img = "assets/catalogo_morfologico_completo.png"
    if os.path.exists(ruta_img):
        st.image(ruta_img, use_container_width=True, caption="Manual Táctico AGATHA - Identificación Morfológica")
    else:
        st.info("Cargue 'catalogo_morfologico_completo.png' en /assets para visualización táctica.")

# --- ANALISIS ESPACIAL Y FILTROS ---
st.markdown("---")
col_mapa, col_filtros = st.columns([2.5, 1.5], gap="large")

with col_filtros:
    st.markdown("<h4 class='cian-electrico'>PARAMETROS DE FILTRADO</h4>", unsafe_allow_html=True)
    sel_anio = st.selectbox("AÑO", ["TODOS"] + sorted(df_maestro['AÑO'].unique().tolist(), reverse=True))
    sel_forma = st.selectbox("MORFOLOGIA", ["TODOS"] + sorted(df_maestro['FORMA'].unique().tolist()))
    sel_pais = st.selectbox("PAÍS", ["TODOS"] + sorted(df_maestro['PAIS'].unique().tolist()))
    
    df_filtrado = df_maestro.copy()
    if sel_anio != "TODOS": df_filtrado = df_filtrado[df_filtrado['AÑO'] == sel_anio]
    if sel_forma != "TODOS": df_filtrado = df_filtrado[df_filtrado['FORMA'] == sel_forma]
    if sel_pais != "TODOS": df_filtrado = df_filtrado[df_filtrado['PAIS'] == sel_pais]

with col_mapa:
    c_m1, c_m2 = st.columns(2)
    modo_v = c_m1.radio("MODO TÁCTICO", ["Nodos Base", "Red de Trayectorias"], horizontal=True)
    proj_v = c_m2.radio("PROYECCIÓN", ["Globo 3D", "Plano 2D"], horizontal=True)
    
    fig = go.Figure()
    if modo_v == "Nodos Base":
        fig.add_trace(go.Scattergeo(lon=df_filtrado['lon'], lat=df_filtrado['lat'], mode='markers',
                                    marker=dict(size=5, color='#00f3ff', opacity=0.7), text=df_filtrado['CIUDAD']))
    else:
        df_red = df_filtrado.head(100)
        fig.add_trace(go.Scattergeo(lon=df_red['lon'], lat=df_red['lat'], mode='lines+markers',
                                    line=dict(width=1, color='#39ff14'), opacity=0.4))
    
    fig.update_layout(geo=dict(projection_type='orthographic' if proj_v=="Globo 3D" else 'equirectangular',
                               showland=True, landcolor='#111', bgcolor='#0a0a0a', showocean=True, oceancolor='#050505'),
                      margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='#0a0a0a', height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div style='font-size:0.7rem; color:#475569; border-top:1px solid #1e293b; padding-top:10px;'>
        MÓDULO DE EXPANSIÓN DE INTELIGENCIA: <a href='https://in-the-sky.org/satmap_worldmap.php' style='color:#00f3ff;'>Rastreo Satelital Real-Time</a> | 
        <a href='https://nuforc.org/databank/' style='color:#00f3ff;'>Archivo NUFORC Global</a>
    </div>
    """, unsafe_allow_html=True)

# --- PROCESADOR FORENSE AGATHA ---
st.markdown("---")
with st.expander("PROCESADOR CONDUCTUAL AGATHA (ANALISIS NLP & METEOROLOGICO)", expanded=True):
    if not df_filtrado.empty:
        opciones = (df_filtrado['CIUDAD'] + " | " + df_filtrado['FORMA'] + " | " + df_filtrado['AÑO'].astype(str)).tolist()
        sel_caso = st.selectbox("SELECCIONAR EXPEDIENTE PARA ESCANEO", opciones[:500])
        
        idx_caso = opciones.index(sel_caso)
        data_caso = df_filtrado.iloc[idx_caso]
        
        c_a1, c_a2 = st.columns([2, 1])
        with c_a1:
            st.markdown(f"<div style='background:#111; padding:20px; border-left:3px solid #39ff14;'>{data_caso['RESUMEN']}</div>", unsafe_allow_html=True)
        with c_a2:
            if st.button("EJECUTAR ANALISIS AGATHA AI"):
                if DEEPSEEK_API_KEY:
                    with st.spinner("AGATHA procesando conducta del fenómeno..."):
                        # Prompt optimizado con lógica de explicaciones convencionales (NUFORC)
                        prompt = f"Analiza este reporte UAP: {data_caso['RESUMEN']}. Considera hipótesis convencionales (Starlink, satélites, globos) y anómalas. Responde en JSON: {{comportamiento, hipotesis_uap, hipotesis_convencional, indice_anomalia_0_100}}"
                        # (Aquí iría la llamada real a la API, simulamos respuesta para la demo)
                        st.json({"comportamiento": "Patrón de vuelo no balístico", "hipotesis_convencional": "Posible reentrada de chatarra espacial o Starlink", "indice_anomalia": 78})
                else: st.warning("Nodo de inteligencia externa no configurado.")
            
            if st.button("CONSULTAR METEOROLOGÍA HISTÓRICA"):
                if OPENWEATHER_API_KEY:
                    st.info(f"Consultando condiciones atmosféricas para {data_caso['CIUDAD']}...")
                else: st.warning("API de Meteorología no detectada.")

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#334155; font-size:0.7rem; letter-spacing:1px;'>
    METODOLOGÍA: PROCESAMIENTO RED NEURONAL AGATHA | FUENTE: NUFORC DATASETS | 2026<br>
    MOTOR DE ANÁLISIS CONDUCTUAL PREDICTIVO - SEGURIDAD ESTRATÉGICA
</div>
""", unsafe_allow_html=True)
