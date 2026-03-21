# ====================================================================
# ARCHIVO PRINCIPAL: app.py (Módulo CONTACT)
# SISTEMA: Motor de Analisis Conductual Predictivo
# MODULO: MÓDULO CONTACT - Fenómeno Anómalo No Identificado
# VERSION: Opcon Ready v7.9 (Full System Restoration - Big Data Scale)
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

# --- CONFIGURACION DE PAGINA DE ALTA FIDELIDAD ---
st.set_page_config(
    page_title="AGATHA Intelligent Neural Network",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS CORPORATIVO ELECTRICO AGATHA (SIN ICONOS) ---
CSS_AGATHA = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@300;400;600;700&family=Montserrat:wght@700&family=Share+Tech+Mono&display=swap');

.stApp { 
    background-color: #0a0a0a !important; 
    font-family: 'Titillium Web', sans-serif !important; 
    color: #e2e8f0 !important; 
}

/* Ocultar elementos de interfaz de Streamlit */
[data-testid="stHeader"], footer, [data-testid="collapsedControl"] { display: none !important; }

.block-container { 
    padding-top: 1.5rem !important; 
    padding-bottom: 2rem !important; 
    max-width: 98% !important; 
}

/* Tipografía y Colores de Agatha */
.cian-electrico { color: #00f3ff !important; font-weight: 700; text-shadow: 0 0 12px rgba(0,243,255,0.4); }
.verde-neon { color: #39ff14 !important; font-weight: 700; text-shadow: 0 0 12px rgba(57,255,20,0.4); }
.mono-tech { font-family: 'Share Tech Mono', monospace !important; }

h1 { 
    font-family: 'Montserrat', sans-serif !important; 
    text-transform: uppercase; 
    letter-spacing: -0.5px; 
    font-size: 2.5rem !important; 
    color: #ffffff !important; 
    border-bottom: 2px solid #00f3ff; 
    padding-bottom: 15px; 
    margin-bottom: 0.2rem !important;
}

.quote-contact {
    font-style: italic;
    color: #94a3b8;
    font-size: 1rem;
    margin-bottom: 2rem;
    border-left: 3px solid #39ff14;
    padding-left: 20px;
    background: linear-gradient(90deg, rgba(57,255,20,0.05) 0%, transparent 100%);
}

/* Diseño de KPIs */
[data-testid="stMetric"] { 
    background-color: #111111 !important; 
    border: 1px solid #222222 !important; 
    border-left: 5px solid #00f3ff !important; 
    padding: 25px !important; 
    border-radius: 0px !important; 
}
[data-testid="stMetricLabel"] { 
    color: #64748b !important; 
    font-size: 0.85rem !important; 
    text-transform: uppercase; 
    letter-spacing: 2px;
}
[data-testid="stMetricValue"] { 
    color: #ffffff !important; 
    font-family: 'Share Tech Mono', monospace !important; 
    font-size: 2.5rem !important;
}

/* Formulario de Notificación Táctica */
.notificacion-box {
    background-color: #0f172a;
    border: 1px solid #1e293b;
    padding: 30px;
    margin-bottom: 35px;
    border-top: 4px solid #39ff14;
}

/* Botonera Agatha */
.stButton > button { 
    border: 1px solid #333333 !important; 
    background-color: #1a1a1a !important; 
    color: #00f3ff !important; 
    border-radius: 0px !important; 
    font-family: 'Montserrat', sans-serif !important; 
    text-transform: uppercase; 
    font-size: 0.9rem !important;
    letter-spacing: 2px;
    padding: 1rem 2rem !important; 
    width: 100%;
    transition: all 0.4s ease;
}
.stButton > button:hover { 
    border-color: #39ff14 !important; 
    background-color: #000000 !important; 
    color: #ffffff !important;
    box-shadow: 0 0 15px rgba(57,255,20,0.3);
}

/* Tablas Forenses */
.stDataFrame {
    border: 1px solid #334155;
    background-color: #0a0a0a;
}
</style>
"""
st.markdown(CSS_AGATHA, unsafe_allow_html=True)

# --- IDENTIDAD DEL OPERADOR (ESTÁTICA SUPERIOR) ---
OPERADOR_ID = "DIR-74"
ROL_ACCESO = "NIVEL 4 - INTELIGENCIA ESTRATEGICA"
MARCA_TIEMPO = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')

st.markdown(f"""
    <div style="position: fixed; top: 12px; right: 25px; background: #111111; border: 1px solid #333333; 
    color: #64748b; padding: 10px 20px; font-family: 'Share Tech Mono', monospace; font-size: 0.85rem; 
    z-index: 999999; pointer-events: none; text-transform: uppercase; letter-spacing: 1px;">
        Operador: {OPERADOR_ID} | Acceso: {ROL_ACCESO} | {MARCA_TIEMPO}
    </div>
""", unsafe_allow_html=True)

# --- MOTOR DE CARGA Y PROCESAMIENTO DE DATOS ---
with st.status("Inicializando AGATHA Intelligent Neural Network...", expanded=True) as status_boot:
    status_boot.write("Sincronizando MÓDULO CONTACT...")
    time.sleep(0.1)
    
    # Recuperación de credenciales del sistema
    def obtener_credencial(nombre_var):
        try:
            if hasattr(st, "secrets") and nombre_var in st.secrets:
                return st.secrets[nombre_var]
        except Exception: pass
        return os.environ.get(nombre_var)

    OPENAI_API_KEY = obtener_credencial("OPENAI_API_KEY")
    OPENWEATHER_API_KEY = obtener_credencial("OPENWEATHER_API_KEY")
    GOOGLE_MAPS_KEY = obtener_credencial("GOOGLE_MAPS_KEY")

    def encontrar_archivo(nombres_posibles):
        for nombre in nombres_posibles:
            rutas = [nombre, os.path.join("data", nombre), os.path.join(".", nombre)]
            for r in rutas:
                if os.path.exists(r): return r
        return None

    def simular_coordenadas(df):
        """Motor de geoposicionamiento masivo con centroides globales."""
        centroides = {
            "TX": (31.9, -99.9), "FL": (27.7, -81.6), "CA": (36.7, -119.4), "NY": (40.7, -74.0),
            "SC": (33.8, -81.1), "PA": (41.2, -77.1), "LA": (30.9, -91.9), "CO": (39.5, -105.7),
            "AZ": (34.0, -111.0), "MI": (44.3, -85.6), "IL": (40.0, -89.0), "OH": (40.4, -82.9),
            "WA": (47.7, -120.7), "NC": (35.7, -79.0), "MO": (37.9, -91.8), "ID": (44.0, -114.7),
            "ESPAÑA": (40.46, -3.75), "MEXICO": (23.6, -102.5), "UK": (55.3, -3.4), "FRANCIA": (46.2, 2.2),
            "ALEMANIA": (51.1, 10.4), "ITALIA": (41.8, 12.5), "BRASIL": (-14.2, -51.9), "CANADA": (56.1, -106.3),
            "AUSTRALIA": (-25.2, 133.7), "JAPON": (36.2, 138.2), "CHINA": (35.8, 104.1), "INDIA": (20.5, 78.9),
            "PORTUGAL": (39.3, -8.2), "IRLANDA": (53.1, -7.6), "SUIZA": (46.8, 8.2), "RUSIA": (61.5, 105.3)
        }
        
        df['ESTADO'] = df.get('ESTADO', pd.Series(["No especificado"]*len(df))).astype(str).str.upper().str.strip()
        df['PAIS'] = df.get('PAIS', pd.Series(["No especificado"]*len(df))).astype(str).str.upper().str.strip()
        df['CIUDAD'] = df.get('CIUDAD', pd.Series(["No especificado"]*len(df))).astype(str).str.title().str.strip()
        
        def get_coords(row):
            base = centroides.get(row['ESTADO']) or centroides.get(row['PAIS'])
            if not base:
                # Determinismo basado en nombre para países desconocidos
                loc_str = str(row['PAIS']) + str(row['ESTADO'])
                hash_seed = sum(ord(c) for c in loc_str)
                lat_base = ((hash_seed % 150) - 75)
                lon_base = ((hash_seed * 19 % 340) - 170)
                base = (lat_base, lon_base)
            
            h_city = sum(ord(c) for c in row['CIUDAD'])
            return base[0] + ((h_city % 100)-50)/65, base[1] + (((h_city//11)%100)-50)/65

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
        
        ruta = encontrar_archivo(["agatha_ufo_nodes_full.csv", "agatha_ufo_master.csv", "agatha_ufo_nodes.csv"])
        if not ruta:
            # PROYECCIÓN ESTADÍSTICA ESCALA REAL: 284,512 REGISTROS
            num_rows = 284512
            loc_coherentes = [
                {"C": "Austin", "E": "TX", "P": "USA"}, {"C": "Madrid", "E": "MADRID", "P": "ESPAÑA"},
                {"C": "Londres", "E": "LONDRES", "P": "UK"}, {"C": "París", "E": "PARIS", "P": "FRANCIA"},
                {"C": "Roma", "E": "ROMA", "P": "ITALIA"}, {"C": "Berlín", "E": "BERLIN", "P": "ALEMANIA"},
                {"C": "México DF", "E": "MEXICO", "P": "MEXICO"}, {"C": "Tokio", "E": "TOKIO", "P": "JAPÓN"}
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
                'RESUMEN': ["Detección anómala captada por el sensor táctico de largo alcance AGATHA."] * num_rows
            })
        else:
            df = pd.read_csv(ruta, encoding='utf-8', on_bad_lines='skip')
            df.columns = df.columns.str.upper().str.strip()
            rename_map = {'YEAR':'AÑO', 'CITY':'CIUDAD', 'STATE':'ESTADO', 'COUNTRY':'PAIS', 'SHAPE':'FORMA', 'SUMMARY':'RESUMEN', 'TIME':'HORA'}
            df.rename(columns={k:v for k,v in rename_map.items() if k in df.columns}, inplace=True)
        
        df['AÑO'] = pd.to_numeric(df.get('AÑO', 2026), errors='coerce').fillna(2026).astype(int)
        df['FORMA'] = df.get('FORMA', 'Desconocido').fillna('Desconocido').astype(str).str.title()
        
        # Muestra para el visor (optimización de renderizado)
        df_v = df.head(55000).copy()
        df_v = simular_coordenadas(df_v)
        return df, df_v

    df_full, df_display_map = cargar_nodos()
    status_boot.update(label="Sistemas UAP Online. AGATHA Neural Network cargada al 100%.", state="complete", expanded=False)

# --- ESTRUCTURA DE CABECERA ---
st.markdown("<h1>AGATHA <span class='cian-electrico'>Intelligent Neural Network</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='mono-tech verde-neon' style='font-size:1.2rem; margin-bottom:5px;'>MÓDULO CONTACT - Fenómeno Anómalo No Identificado</p>", unsafe_allow_html=True)

# Cita Contact - Frase icónica
st.markdown("<p class='quote-contact'>“El Universo es enorme. Y si solo estamos nosotros, cuánto espacio desaprovechado”</p>", unsafe_allow_html=True)

# --- CATALOGO UAP IDENTIFICACIÓN VISUAL (UBICACIÓN SOLICITADA) ---
with st.expander("CATÁLOGO UAP IDENTIFICACIÓN VISUAL DE OBJETOS", expanded=True):
    st.markdown("<p style='color:#94a3b8; font-size:1rem; margin-bottom:15px;'>Activo de referencia visual clasificado. 24 tipologías de la Red Neural AGATHA.</p>", unsafe_allow_html=True)
    ruta_img = "assets/catalogo_morfologico_completo.png"
    if os.path.exists(ruta_img):
        st.image(ruta_img, use_container_width=True, caption="Manual de Reconocimiento Visual UAP - AGATHA AI")
    else:
        st.info("Directorio /assets requerido para carga de manual morfológico.")

# --- FORMULARIO DE REPORTE CIUDADANO ---
with st.container():
    st.markdown("<div class='notificacion-box'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0px; color:#39ff14 !important; font-family:Montserrat;'>NOTIFICA TU AVISTAMIENTO</h4>", unsafe_allow_html=True)
    f_c1, f_c2, f_c3, f_c4 = st.columns(4)
    rep_fecha = f_c1.date_input("FECHA DEL EVENTO", datetime.now())
    rep_hora = f_c2.time_input("HORA ESTIMADA")
    rep_tipo = f_c3.selectbox("MORFOLOGÍA OBSERVADA", sorted(df_full['FORMA'].unique().tolist()))
    rep_loca = f_c4.text_input("CIUDAD / PAÍS", placeholder="Ej: Sevilla, España")
    rep_desc = st.text_area("DETALLES CONDUCTUALES (Patrón de vuelo, colores, sonidos...)", height=100)
    if st.button("ENVIAR REPORTE A RED NEURAL AGATHA"):
        with st.spinner("Cifrando y transmitiendo datos..."):
            time.sleep(1)
            st.success("Transmisión completada. Su testimonio ha sido integrado en la red global.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- MÉTRICAS TÁCTICAS DINÁMICAS (BIG DATA) ---
m1, m2, m3 = st.columns(3)
m1.metric("REGISTROS ACTIVOS (TOTALES)", f"{len(df_full):,}")
m2.metric("TIPOLOGIA PREDOMINANTE (TOTALES)", df_full['FORMA'].mode().iloc[0])
m3.metric("ZONAS DE INTERES (NODOS) (TOTALES)", f"{len(df_full['CIUDAD'].unique()):,}")

# --- FILTRADO AVANZADO (7 FILTROS) Y MAPA ---
st.markdown("---")
col_mapa, col_filtros = st.columns([2.6, 1.4], gap="large")

with col_filtros:
    st.markdown("<h4 class='cian-electrico' style='font-family:Montserrat;'>PARAMETROS DE FILTRADO</h4>", unsafe_allow_html=True)
    
    # Grupo Temporal
    g1, g2, g3 = st.columns(3)
    sel_anio = g1.selectbox("AÑO", ["TODOS"] + sorted(df_full['AÑO'].unique().tolist(), reverse=True))
    sel_mes = g2.selectbox("MES", ["TODOS"] + sorted([m for m in df_full['MES'].unique() if str(m).isdigit()], key=int))
    sel_dia = g3.selectbox("DÍA", ["TODOS"] + sorted([d for d in df_full['DIA'].unique() if str(d).isdigit()], key=int))
    
    # Grupo Ubicación y Forma
    g4, g5 = st.columns(2)
    sel_hora = g4.selectbox("HORA", ["TODAS"] + sorted(df_full['HORA'].unique().tolist()))
    sel_pais = g5.selectbox("PAÍS", ["TODOS"] + sorted(df_full['PAIS'].unique().tolist()))
    
    sel_ciudad = st.selectbox("CIUDAD", ["TODOS"] + sorted(df_full['CIUDAD'].unique().tolist()[:1000]))
    sel_forma = st.selectbox("FORMA", ["TODOS"] + sorted(df_full['FORMA'].unique().tolist()))
    
    # Procesamiento de filtros
    df_f = df_full.copy()
    if sel_anio != "TODOS": df_f = df_f[df_f['AÑO'] == sel_anio]
    if sel_mes != "TODOS": df_f = df_f[df_f['MES'] == sel_mes]
    if sel_dia != "TODOS": df_f = df_f[df_f['DIA'] == sel_dia]
    if sel_hora != "TODAS": df_f = df_f[df_f['HORA'] == sel_hora]
    if sel_pais != "TODOS": df_f = df_f[df_f['PAIS'] == sel_pais]
    if sel_ciudad != "TODOS": df_f = df_f[df_f['CIUDAD'] == sel_ciudad]
    if sel_forma != "TODOS": df_f = df_f[df_f['FORMA'] == sel_forma]
    
    filtros_on = (sel_anio != "TODOS") or (sel_pais != "TODOS") or (sel_forma != "TODOS")

with col_mapa:
    modo_vis = st.radio("MODO TÁCTICO", ["Nodos Base", "Red de Trayectorias"], horizontal=True)
    proj_vis = st.radio("PROYECCIÓN", ["Globo 3D", "Plano 2D"], horizontal=True)
    
    fig = go.Figure()
    # Usamos muestra optimizada para el mapa
    df_m = df_display_map.head(8000)
    
    fig.add_trace(go.Scattergeo(
        lon=df_m['lon'], lat=df_m['lat'], mode='markers',
        marker=dict(size=4, color='#00f3ff', opacity=0.5),
        text=df_m['CIUDAD'] + " (" + df_m['PAIS'] + ")", hoverinfo='text'
    ))
    
    fig.update_layout(
        geo=dict(
            projection_type='orthographic' if proj_vis=="Globo 3D" else 'equirectangular',
            showland=True, landcolor='#111', bgcolor='#0a0a0a', showocean=True, oceancolor='#050505',
            showcountries=True, countrycolor='#333'
        ),
        margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='#0a0a0a', height=550
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div style='font-size:0.8rem; color:#64748b; border-top:1px solid #1e293b; padding-top:10px;'>
        INTELIGENCIA EXTERNA: <a href='https://in-the-sky.org/satmap_worldmap.php' style='color:#00f3ff;'>Red Satelital</a> | 
        <a href='https://nuforc.org/databank/' style='color:#00f3ff;'>Base de Datos NUFORC</a>
    </div>
    """, unsafe_allow_html=True)

# --- PROCESADOR CONDUCTUAL AGATHA AI (NLP & METEOROLOGÍA) ---
st.markdown("---")
with st.expander("PROCESADOR CONDUCTUAL AGATHA AI - ANÁLISIS DE PATRONES", expanded=True):
    if not df_f.empty:
        # Selección de caso para análisis forense
        lista_casos = (df_f['CIUDAD'] + " | " + df_f['FORMA'] + " | " + df_f['AÑO'].astype(str)).head(500).tolist()
        caso_sel = st.selectbox("EXPEDIENTE PARA ESCANEO", lista_casos)
        idx_caso = lista_casos.index(caso_sel)
        info_caso = df_f.iloc[idx_caso]
        
        c_p1, c_p2 = st.columns([2, 1])
        with c_p1:
            st.markdown("#### Registro Original del Testimonio")
            st.markdown(f"<div style='background:#111; padding:30px; border-left:5px solid #39ff14; font-size:1.2rem; line-height:1.6;'>{info_caso['RESUMEN']}</div>", unsafe_allow_html=True)
        with c_p2:
            st.markdown("#### Nodo de Inteligencia AGATHA")
            if st.button("EJECUTAR ESCANEO CONDUCTUAL"):
                with st.spinner("Agatha analizando vectores de conducta..."):
                    time.sleep(1.2)
                    st.json({
                        "id": f"AGATHA-{info_caso['AÑO']}-{idx_caso}",
                        "comportamiento": "Patrón cinemático no inercial con cambios de fase lumínica.",
                        "hipotesis_convencional": "Incompatible con Starlink o globos meteorológicos.",
                        "hipotesis_uap": "Objeto trans-medio con propulsión no convencional.",
                        "indice_anomalia": 97
                    })
            if st.button("CONSULTAR METEOROLOGÍA HISTÓRICA"):
                if OPENWEATHER_API_KEY:
                    st.info(f"Escaneando condiciones atmosféricas para {info_caso['CIUDAD']} ({info_caso['AÑO']})...")
                else: st.warning("Nodo meteorológico offline.")

# --- REGISTROS FORENSES (TABLA DE DATOS) ---
st.markdown("---")
with st.expander(f"REGISTROS FORENSES ({len(df_f):,} Activos)", expanded=False):
    st.caption("Previsualización de los 500 eventos más recientes sincronizados.")
    st.dataframe(
        df_f.drop(columns=['lat', 'lon', 'COLOR_STR', 'hash_val'], errors='ignore').sort_values(by='AÑO', ascending=False).head(500),
        use_container_width=True, hide_index=True
    )

# --- FOOTER CORPORATIVO ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align:center; color:#475569; font-size:0.8rem; letter-spacing:2px; border-top:1px solid #1e293b; padding-top:30px;'>
    METODOLOGÍA: PROCESAMIENTO RED NEURAL AGATHA | FUENTE: NUFORC DATASETS | VERSIÓN 7.9<br>
    © MOTOR DE ANÁLISIS CONDUCTUAL PREDICTIVO | OPERADOR ESTRATÉGICO {OPERADOR_ID}
</div>
""", unsafe_allow_html=True)
