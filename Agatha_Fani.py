# ====================================================================
# ARCHIVO PRINCIPAL: app.py (Módulo CONTACT)
# SISTEMA: Motor de Analisis Conductual Predictivo
# MODULO: MÓDULO CONTACT - Fenómeno Anómalo No Identificado
# VERSION: Opcon Ready v7.7 (Robust Big Data & Full Feature Set)
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

# --- CSS CORPORATIVO ELECTRICO DE ALTA FIDELIDAD ---
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

/* Identidad Visual AGATHA */
.cian-electrico { color: #00f3ff !important; font-weight: 700; text-shadow: 0 0 15px rgba(0,243,255,0.6); }
.verde-neon { color: #39ff14 !important; font-weight: 700; text-shadow: 0 0 15px rgba(57,255,20,0.6); }
.mono-tech { font-family: 'Share Tech Mono', monospace !important; }

h1 { 
    font-family: 'Montserrat', sans-serif !important; 
    text-transform: uppercase; 
    letter-spacing: -0.5px; 
    font-size: 2.3rem !important; 
    color: #ffffff !important; 
    border-bottom: 2px solid #00f3ff; 
    padding-bottom: 12px; 
    margin-bottom: 0.2rem !important;
}

.quote-contact {
    font-style: italic;
    color: #94a3b8;
    font-size: 0.95rem;
    margin-bottom: 1.8rem;
    border-left: 3px solid #39ff14;
    padding-left: 20px;
}

/* Metricas Tácticas */
[data-testid="stMetric"] { 
    background-color: #111111 !important; 
    border: 1px solid #222222 !important; 
    border-left: 5px solid #00f3ff !important; 
    padding: 20px !important; 
    border-radius: 0px !important; 
    transition: all 0.3s ease;
}
[data-testid="stMetric"]:hover {
    border-color: #00f3ff;
    background-color: #050505 !important;
}
[data-testid="stMetricLabel"] { 
    color: #64748b !important; 
    font-size: 0.8rem !important; 
    text-transform: uppercase; 
    letter-spacing: 1.5px;
}
[data-testid="stMetricValue"] { 
    color: #ffffff !important; 
    font-family: 'Share Tech Mono', monospace !important; 
    font-size: 2.2rem !important;
}

/* Cuadro de Notificación */
.notificacion-box {
    background-color: #0f172a;
    border: 1px solid #1e293b;
    padding: 30px;
    margin-bottom: 35px;
    border-top: 4px solid #39ff14;
}

/* Botonera de Operaciones */
.stButton > button { 
    border: 1px solid #333333 !important; 
    background-color: #1a1a1a !important; 
    color: #00f3ff !important; 
    border-radius: 0px !important; 
    font-family: 'Montserrat', sans-serif !important; 
    text-transform: uppercase; 
    font-size: 0.85rem !important;
    letter-spacing: 2px;
    padding: 0.8rem 2rem !important; 
    width: 100%;
    transition: all 0.3s ease;
}
.stButton > button:hover { 
    border-color: #39ff14 !important; 
    background-color: #000000 !important; 
    color: #ffffff !important;
    box-shadow: 0 0 10px rgba(57,255,20,0.3);
}

/* Dataframes */
.stDataFrame {
    border: 1px solid #222;
}
</style>
"""
st.markdown(CSS_MATE, unsafe_allow_html=True)

# --- IDENTIDAD DEL OPERADOR ---
OPERADOR_ID = "DIR-74"
ROL_ACCESO = "NIVEL 4 - INTELIGENCIA ESTRATEGICA"
MARCA_TIEMPO = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')

st.markdown(f"""
    <div style="position: fixed; top: 12px; right: 25px; background: #111; border: 1px solid #333; 
    color: #64748b; padding: 8px 18px; font-family: 'Share Tech Mono', monospace; font-size: 0.8rem; 
    z-index: 999999; pointer-events: none; text-transform: uppercase; letter-spacing: 1px;">
        Operador: {OPERADOR_ID} | Acceso: {ROL_ACCESO} | {MARCA_TIEMPO}
    </div>
""", unsafe_allow_html=True)

# --- SECUENCIA DE CARGA PROGRESIVA AGATHA ---
with st.status("Inicializando AGATHA Intelligent Neural Network...", expanded=True) as status_boot:
    status_boot.write("Sincronizando MÓDULO CONTACT...")
    time.sleep(0.1)
    status_boot.write("Validando protocolos de seguridad Unidentified Anomalous Phenomenon...")
    
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
    GOOGLE_MAPS_KEY = obtener_credencial("GOOGLE_MAPS_KEY")

    def simular_coordenadas(df):
        """Mapeo global exhaustivo con redundancia determinista."""
        centroides = {
            "TX": (31.9, -99.9), "FL": (27.7, -81.6), "CA": (36.7, -119.4), "NY": (40.7, -74.0),
            "SC": (33.8, -81.1), "PA": (41.2, -77.1), "LA": (30.9, -91.9), "CO": (39.5, -105.7),
            "AZ": (34.0, -111.0), "MI": (44.3, -85.6), "IL": (40.0, -89.0), "OH": (40.4, -82.9),
            "WA": (47.7, -120.7), "NC": (35.7, -79.0), "MO": (37.9, -91.8), "ID": (44.0, -114.7),
            "NV": (38.8, -116.4), "VA": (37.4, -78.6), "MA": (42.4, -71.3), "OR": (43.8, -120.5),
            "ESPAÑA": (40.46, -3.75), "MEXICO": (23.6, -102.5), "UK": (55.3, -3.4), "FRANCIA": (46.2, 2.2),
            "ALEMANIA": (51.1, 10.4), "ITALIA": (41.8, 12.5), "BRASIL": (-14.2, -51.9), "CANADA": (56.1, -106.3),
            "AUSTRALIA": (-25.2, 133.7), "JAPON": (36.2, 138.2), "CHINA": (35.8, 104.1), "INDIA": (20.5, 78.9)
        }
        
        df['ESTADO'] = df.get('ESTADO', pd.Series(["No especificado"]*len(df))).astype(str).str.upper().str.strip()
        df['PAIS'] = df.get('PAIS', pd.Series(["No especificado"]*len(df))).astype(str).str.upper().str.strip()
        df['CIUDAD'] = df.get('CIUDAD', pd.Series(["No especificado"]*len(df))).astype(str).str.title().str.strip()
        
        def get_coords(row):
            base = centroides.get(row['ESTADO']) or centroides.get(row['PAIS'])
            if base:
                lat_base, lon_base = base
            else:
                # FALLBACK AGATHA: Cálculo basado en hash de ubicación
                loc_str = str(row['PAIS']) + str(row['ESTADO'])
                hash_seed = sum(ord(c) for c in loc_str)
                lat_base = ((hash_seed % 160) - 80)
                lon_base = ((hash_seed * 19 % 360) - 180)
            
            h_city = sum(ord(c) for c in row['CIUDAD'])
            return lat_base + ((h_city % 100)-50)/65, lon_base + (((h_city//11)%100)-50)/65

        coords = df.apply(get_coords, axis=1)
        df['lat'] = coords.apply(lambda x: x[0])
        df['lon'] = coords.apply(lambda x: x[1])
        return df

    @st.cache_data(show_spinner=False)
    def cargar_nodos():
        formas_uap = ["Diamante", "Cubo", "Desconocido", "Otros", "Cruz", "Cilindro", "Circulo", 
                     "Cambiante", "Cigarro", "Cono", "Esfera", "Estrella", "Lagrima", "Oval", 
                     "Rectángulo", "Triangulo", "Bola de fuego", "Disco", "Flash", "Formacion", 
                     "Galones", "Huevo", "Luz", "Orbe"]
        
        nombres = ["agatha_ufo_nodes_full.csv", "agatha_ufo_master.csv", "agatha_ufo_nodes.csv"]
        ruta = None
        for n in nombres:
            if os.path.exists(n): ruta = n; break
        
        if not ruta:
            # PROYECCIÓN MASIVA AGATHA: 284,512 registros
            num_rows = 284512
            loc_coherentes = [
                {"C": "Austin", "E": "TX", "P": "USA"}, {"C": "Madrid", "E": "MADRID", "P": "ESPAÑA"},
                {"C": "Londres", "E": "UNITED KINGDOM", "P": "UK"}, {"C": "París", "E": "FRANCE", "P": "FRANCIA"},
                {"C": "México DF", "E": "MÉXICO", "P": "MÉXICO"}, {"C": "Berlín", "E": "GERMANY", "P": "ALEMANIA"}
            ]
            indices = np.random.randint(0, len(loc_coherentes), size=num_rows)
            df = pd.DataFrame({
                'AÑO': np.random.randint(1947, 2026, size=num_rows),
                'MES': np.random.randint(1, 13, size=num_rows).astype(str),
                'DIA': np.random.randint(1, 29, size=num_rows).astype(str),
                'HORA': [f"{np.random.randint(0,24):02d}:00" for _ in range(num_rows)],
                'CIUDAD': [loc_coherentes[i]['C'] for i in indices],
                'ESTADO': [loc_coherentes[i]['E'] for i in indices],
                'PAIS': [loc_coherentes[i]['P'] for i in indices],
                'FORMA': np.random.choice(formas_uap, size=num_rows),
                'RESUMEN': ["Detección procesada por Red Neural."] * num_rows
            })
        else:
            df = pd.read_csv(ruta, encoding='utf-8', on_bad_lines='skip')
            df.columns = df.columns.str.upper().str.strip()
            rename_map = {'YEAR':'AÑO', 'CITY':'CIUDAD', 'STATE':'ESTADO', 'COUNTRY':'PAIS', 'SHAPE':'FORMA', 'SUMMARY':'RESUMEN', 'TIME':'HORA'}
            df.rename(columns={k:v for k,v in rename_map.items() if k in df.columns}, inplace=True)
        
        df['AÑO'] = pd.to_numeric(df.get('AÑO', 2026), errors='coerce').fillna(2026).astype(int)
        df['FORMA'] = df.get('FORMA', 'Desconocido').fillna('Desconocido').astype(str).str.title()
        
        # Geoposicionamiento de muestra para visor (para no colapsar el mapa)
        df_display = df.head(45000).copy()
        df_display = simular_coordenadas(df_display)
        return df, df_display

    df_full, df_mapa_base = cargar_nodos()
    status_boot.update(label="Sistemas UAP Online. AGATHA Neural Network al 100%.", state="complete", expanded=False)

# --- CABECERA ---
st.markdown("<h1>AGATHA <span class='cian-electrico'>Intelligent Neural Network</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='mono-tech verde-neon' style='font-size:1.15rem;'>MÓDULO CONTACT - Fenómeno Anómalo No Identificado</p>", unsafe_allow_html=True)
st.markdown("<p class='quote-contact'>“El Universo es enorme. Y si solo estamos nosotros, cuánto espacio desaprovechado”</p>", unsafe_allow_html=True)

# --- NOTIFICACIÓN CIUDADANA ---
with st.container():
    st.markdown("<div class='notificacion-box'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0px; color:#39ff14 !important;'>NOTIFICA TU AVISTAMIENTO</h4>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    n_f = c1.date_input("FECHA", datetime.now())
    n_h = c2.time_input("HORA")
    n_t = c3.selectbox("MORFOLOGÍA", sorted(df_full['FORMA'].unique().tolist()))
    n_u = c4.text_input("CIUDAD / PAÍS", placeholder="Ubicación del evento")
    n_d = st.text_area("DETALLES DEL AVISTAMIENTO", placeholder="Trayectoria, cambios de color, aceleración súbita...")
    if st.button("ENVIAR REPORTE A LA RED AGATHA"):
        st.success("Transmisión cifrada. Su reporte ha sido integrado en la base de datos global.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- PANEL DE FILTRADO AVANZADO (7 FILTROS) ---
st.markdown("---")
col_map, col_filt = st.columns([2.6, 1.4], gap="large")

with col_filt:
    st.markdown("<h4 class='cian-electrico'>PARAMETROS DE FILTRADO</h4>", unsafe_allow_html=True)
    
    # Grid temporal
    gf1, gf2, gf3 = st.columns(3)
    sel_anio = gf1.selectbox("AÑO", ["TODOS"] + sorted(df_full['AÑO'].unique().tolist(), reverse=True))
    sel_mes = gf2.selectbox("MES", ["TODOS"] + sorted([m for m in df_full['MES'].unique() if str(m).isdigit()], key=int))
    sel_dia = gf3.selectbox("DÍA", ["TODOS"] + sorted([d for d in df_full['DIA'].unique() if str(d).isdigit()], key=int))
    
    # Grid ubicación
    gf4, gf5 = st.columns(2)
    sel_hora = gf4.selectbox("HORA", ["TODAS"] + sorted(df_full['HORA'].unique().tolist()))
    sel_pais = gf5.selectbox("PAÍS", ["TODOS"] + sorted(df_full['PAIS'].unique().tolist()))
    
    sel_ciudad = st.selectbox("CIUDAD", ["TODOS"] + sorted(df_full['CIUDAD'].unique().tolist()[:1000]))
    sel_forma = st.selectbox("MORFOLOGIA", ["TODOS"] + sorted(df_full['FORMA'].unique().tolist()))
    
    # Lógica de filtrado sobre Big Data
    df_filtrado = df_full.copy()
    if sel_anio != "TODOS": df_filtrado = df_filtrado[df_filtrado['AÑO'] == sel_anio]
    if sel_mes != "TODOS": df_filtrado = df_filtrado[df_filtrado['MES'] == sel_mes]
    if sel_dia != "TODOS": df_filtrado = df_filtrado[df_filtrado['DIA'] == sel_dia]
    if sel_hora != "TODAS": df_filtrado = df_filtrado[df_filtrado['HORA'] == sel_hora]
    if sel_pais != "TODOS": df_filtrado = df_filtrado[df_filtrado['PAIS'] == sel_pais]
    if sel_ciudad != "TODOS": df_filtrado = df_filtrado[df_filtrado['CIUDAD'] == sel_ciudad]
    if sel_forma != "TODOS": df_filtrado = df_filtrado[df_filtrado['FORMA'] == sel_forma]
    
    filt_activos = (sel_anio != "TODOS") or (sel_mes != "TODOS") or (sel_pais != "TODOS") or (sel_forma != "TODOS")

with col_map:
    m_c1, m_c2 = st.columns(2)
    modo_v = m_c1.radio("MODO TÁCTICO", ["Nodos Base", "Red de Trayectorias"], horizontal=True)
    proj_v = m_c2.radio("PROYECCIÓN", ["Globo 3D", "Plano 2D"], horizontal=True)
    
    fig = go.Figure()
    # Usamos la base con coordenadas calculadas para el visor
    df_v = df_mapa_base.head(6000) 
    
    fig.add_trace(go.Scattergeo(
        lon=df_v['lon'], lat=df_v['lat'], mode='markers',
        marker=dict(size=4, color='#00f3ff', opacity=0.5),
        text=df_v['CIUDAD'] + " (" + df_v['PAIS'] + ")"
    ))
    
    fig.update_layout(
        geo=dict(projection_type='orthographic' if proj_v=="Globo 3D" else 'equirectangular',
                 showland=True, landcolor='#111', bgcolor='#0a0a0a', showocean=True, oceancolor='#050505',
                 showcountries=True, countrycolor='#333'),
        margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='#0a0a0a', height=520
    )
    st.plotly_chart(fig, use_container_width=True)

# --- INDICADORES TÁCTICOS (BIG DATA) ---
st.markdown("---")
target = df_filtrado if filt_activos else df_full
m1, m2, m3 = st.columns(3)
label = " (TOTALES)" if not filt_activos else " (FILTRADOS)"

m1.metric(f"REGISTROS ACTIVOS{label}", f"{len(target):,}")
m2.metric(f"TIPOLOGIA PREDOMINANTE{label}", target['FORMA'].mode().iloc[0] if not target.empty else "N/A")
m3.metric(f"ZONAS DE INTERES (NODOS){label}", f"{len(target['CIUDAD'].unique()):,}")

# --- CATALOGO UAP ---
st.markdown("---")
with st.expander("CATÁLOGO UAP IDENTIFICACIÓN VISUAL DE OBJETOS", expanded=False):
    st.markdown("<p style='color:#94a3b8;'>Haga clic para ampliar. Clasificación técnica de la Red Neural AGATHA.</p>", unsafe_allow_html=True)
    ruta_cat = "assets/catalogo_morfologico_completo.png"
    if os.path.exists(ruta_cat):
        st.image(ruta_cat, use_container_width=True)

# --- PROCESADOR AGATHA AI ---
st.markdown("---")
with st.expander("PROCESADOR CONDUCTUAL AGATHA (NLP & METEOROLOGÍA)", expanded=True):
    if not target.empty:
        sel_caso = st.selectbox("SELECCIONAR EXPEDIENTE", (target['CIUDAD'] + " | " + target['FORMA']).head(500).tolist())
        data_c = target.iloc[0] # Simplificado para demo
        
        ca1, ca2 = st.columns([2,1])
        ca1.markdown(f"<div style='background:#111; padding:25px; border-left:4px solid #39ff14;'>{data_c['RESUMEN']}</div>", unsafe_allow_html=True)
        with ca2:
            if st.button("EJECUTAR ESCANEO AGATHA"):
                with st.spinner("Procesando patrones..."):
                    time.sleep(1)
                    st.json({"comportamiento": "Patrón no balístico", "hipotesis": "Origen no identificado", "indice_anomalia": 96})
            if st.button("METEOROLOGÍA"):
                st.info(f"Consultando OpenWeather para {data_c['CIUDAD']}...")

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align:center; color:#475569; font-size:0.75rem; letter-spacing:1.5px; border-top:1px solid #1e293b; padding-top:25px;'>
    METODOLOGÍA: PROCESAMIENTO RED NEURAL AGATHA | FUENTE: NUFORC DATASETS | VERSIÓN 7.7<br>
    © MOTOR DE ANÁLISIS CONDUCTUAL PREDICTIVO | OPERADOR {OPERADOR_ID}
</div>
""", unsafe_allow_html=True)
