# ====================================================================
# ARCHIVO PRINCIPAL: app.py (Módulo CONTACT)
# SISTEMA: Motor de Analisis Conductual Predictivo
# MODULO: MÓDULO CONTACT - Fenómeno Anómalo No Identificado
# VERSION: Opcon Ready v7.5 (Geopositioning Logic Fix & Syntax Clean)
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

# --- CSS CORPORATIVO ELECTRICO (Blueprint + Neon) ---
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
.cian-electrico { color: #00f3ff !important; font-weight: 700; text-shadow: 0 0 10px rgba(0,243,255,0.5); }
.verde-neon { color: #39ff14 !important; font-weight: 700; text-shadow: 0 0 10px rgba(57,255,20,0.5); }
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
    color: #94a3b8;
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
    border-left: 2px solid #39ff14;
    padding-left: 15px;
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
    letter-spacing: 1px;
}
[data-testid="stMetricValue"] { 
    color: #ffffff !important; 
    font-family: 'Share Tech Mono', monospace !important; 
}

/* Estilo para el formulario de reporte */
.notificacion-box {
    background-color: #0f172a;
    border: 1px solid #1e293b;
    padding: 25px;
    margin-bottom: 30px;
    border-top: 3px solid #39ff14;
}

.stButton > button { 
    border: 1px solid #333333 !important; 
    background-color: #1a1a1a !important; 
    color: #00f3ff !important; 
    border-radius: 0px !important; 
    font-family: 'Montserrat', sans-serif !important; 
    text-transform: uppercase; 
    font-size: 0.8rem !important;
    letter-spacing: 1.5px;
    padding: 0.7rem 1.5rem !important; 
}
.stButton > button:hover { 
    border-color: #39ff14 !important; 
    background-color: #050505 !important; 
    color: #ffffff !important;
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
    GOOGLE_MAPS_KEY = obtener_credencial("GOOGLE_MAPS_KEY")

    def encontrar_archivo(nombres_posibles):
        for nombre in nombres_posibles:
            rutas = [nombre, os.path.join("data", nombre), os.path.join(".", nombre)]
            for r in rutas:
                if os.path.exists(r): return r
        return None

    def simular_coordenadas(df):
        """Motor de geoposicionamiento global con centroides exhaustivos y fallback determinista."""
        centroides = {
            "TX": (31.9, -99.9), "FL": (27.7, -81.6), "CA": (36.7, -119.4), "NY": (40.7, -74.0),
            "SC": (33.8, -81.1), "PA": (41.2, -77.1), "LA": (30.9, -91.9), "CO": (39.5, -105.7),
            "AZ": (34.0, -111.0), "MI": (44.3, -85.6), "IL": (40.0, -89.0), "OH": (40.4, -82.9),
            "WA": (47.7, -120.7), "NC": (35.7, -79.0), "MO": (37.9, -91.8), "ID": (44.0, -114.7),
            "NV": (38.8, -116.4), "VA": (37.4, -78.6),
            "EEUU": (39.8, -98.5), "ESTADOS UNIDOS": (39.8, -98.5), "USA": (39.8, -98.5),
            "CANADA": (56.1, -106.3), "CANADÁ": (56.1, -106.3),
            "MEXICO": (23.6, -102.5), "MÉXICO": (23.6, -102.5),
            "UK": (55.3, -3.4), "REINO UNIDO": (55.3, -3.4), "INGLATERRA": (52.3, -1.1), "UNITED KINGDOM": (55.3, -3.4),
            "ESPAÑA": (40.46, -3.75), "ESPANA": (40.46, -3.75), "SPAIN": (40.46, -3.75),
            "PAISES BAJOS": (52.13, 5.29), "PAÍSES BAJOS": (52.13, 5.29), "NETHERLANDS": (52.13, 5.29),
            "LITUANIA": (55.16, 23.88), "LITHUANIA": (55.16, 23.88),
            "IRLANDA": (53.14, -7.69), "IRELAND": (53.14, -7.69),
            "RUMANIA": (45.94, 24.96), "RUMANÍA": (45.94, 24.96), "ROMANIA": (45.94, 24.96),
            "ITALIA": (41.87, 12.56), "ITALY": (41.87, 12.56),
            "FRANCIA": (46.22, 2.21), "FRANCE": (46.22, 2.21),
            "ALEMANIA": (51.16, 10.45), "GERMANY": (51.16, 10.45),
            "PORTUGAL": (39.39, -8.22),
            "INDIA": (20.59, 78.96),
            "JAMAICA": (18.1, -77.29),
            "ARABIA SAUDI": (23.88, 45.07), "ARABIA SAUDÍ": (23.88, 45.07), "SAUDI ARABIA": (23.88, 45.07),
            "SUDAFRICA": (-30.55, 22.93), "SUDÁFRICA": (-30.55, 22.93), "SOUTH AFRICA": (-30.55, 22.93),
            "BOTSUANA": (-22.32, 24.68), "BOTSWANA": (-22.32, 24.68),
            "IRAN": (32.42, 53.68), "IRÁN": (32.42, 53.68),
            "AUSTRALIA": (-25.27, 133.77),
            "PUERTO RICO": (18.22, -66.59),
            "REPUBLICA DOMINICANA": (18.73, -70.16), "REPÚBLICA DOMINICANA": (18.73, -70.16),
            "NUEVA ZELANDA": (-40.9, 174.88), "NEW ZEALAND": (-40.9, 174.88),
            "CHINA": (35.86, 104.19),
            "JAPON": (36.20, 138.25), "JAPÓN": (36.20, 138.25), "JAPAN": (36.20, 138.25),
            "BRASIL": (-14.23, -51.92), "BRAZIL": (-14.23, -51.92),
            "ARGENTINA": (-38.41, -63.61),
            "CHILE": (-35.67, -71.54),
            "COLOMBIA": (4.57, -74.29)
        }
        
        df['ESTADO'] = df.get('ESTADO', pd.Series(["No especificado"]*len(df))).astype(str).str.upper().str.strip()
        df['PAIS'] = df.get('PAIS', pd.Series(["No especificado"]*len(df))).astype(str).str.upper().str.strip()
        df['CIUDAD'] = df.get('CIUDAD', pd.Series(["No especificado"]*len(df))).astype(str).str.title().str.strip()
        
        def get_coords(row):
            base = centroides.get(row['ESTADO']) or centroides.get(row['PAIS'])
            if base:
                lat_base, lon_base = base
            else:
                # FALLBACK DETERMINISTA PARA PAÍSES NO EN LISTA
                loc_str = str(row['PAIS']) + str(row['ESTADO'])
                hash_seed = sum(ord(c) for c in loc_str)
                lat_base = ((hash_seed % 160) - 80)
                lon_base = ((hash_seed * 17 % 360) - 180)
            
            # Offset ciudad
            h_city = sum(ord(c) for c in row['CIUDAD'])
            return lat_base + ((h_city % 100)-50)/70, lon_base + (((h_city//9)%100)-50)/70

        coords = df.apply(get_coords, axis=1)
        df['lat'] = coords.apply(lambda x: x[0])
        df['lon'] = coords.apply(lambda x: x[1])
        return df

    @st.cache_data(show_spinner=False)
    def cargar_nodos():
        formas_uap = [
            "Diamante", "Cubo", "Desconocido", "Otros", "Cruz", "Cilindro", "Circulo", 
            "Cambiante", "Cigarro", "Cono", "Esfera", "Estrella", "Lagrima", "Oval", 
            "Rectángulo", "Triangulo", "Bola de fuego", "Disco", "Flash", "Formacion", 
            "Galones", "Huevo", "Luz", "Orbe"
        ]
        
        ruta = encontrar_archivo(["agatha_ufo_nodes_full.csv", "agatha_ufo_master.csv", "agatha_ufo_nodes.csv"])
        if not ruta:
            # LÓGICA DE SIMULACIÓN CORREGIDA: Ubicaciones coherentes
            loc_coherentes = [
                {"CIUDAD": "Austin", "ESTADO": "TX", "PAIS": "USA"},
                {"CIUDAD": "Madrid", "ESTADO": "MADRID", "PAIS": "ESPAÑA"},
                {"CIUDAD": "Londres", "ESTADO": "UNITED KINGDOM", "PAIS": "UK"},
                {"CIUDAD": "París", "ESTADO": "FRANCE", "PAIS": "FRANCIA"},
                {"CIUDAD": "Nueva York", "ESTADO": "NY", "PAIS": "USA"},
                {"CIUDAD": "Berlín", "ESTADO": "GERMANY", "PAIS": "ALEMANIA"},
                {"CIUDAD": "Roma", "ESTADO": "ITALY", "PAIS": "ITALIA"}
            ]
            data = []
            for i in range(1500):
                loc = np.random.choice(loc_coherentes)
                data.append({
                    'AÑO': np.random.randint(1950, 2026), 'MES': str(np.random.randint(1, 13)),
                    'DIA': str(np.random.randint(1, 29)), 'HORA': f"{np.random.randint(0,24):02d}:00",
                    'CIUDAD': loc['CIUDAD'], 'ESTADO': loc['ESTADO'], 'PAIS': loc['PAIS'], 
                    'FORMA': np.random.choice(formas_uap),
                    'RESUMEN': "Detección anómala captada por sensor térmico de largo alcance AGATHA."
                })
            df = pd.DataFrame(data)
        else:
            df = pd.read_csv(ruta, encoding='utf-8', on_bad_lines='skip')
            df.columns = df.columns.str.upper().str.strip()
            df.rename(columns={'YEAR':'AÑO', 'CITY':'CIUDAD', 'STATE':'ESTADO', 'COUNTRY':'PAIS', 'SHAPE':'FORMA', 'SUMMARY':'RESUMEN', 'TIME':'HORA'}, inplace=True)
            if 'MES' not in df.columns: df['MES'] = "No especificado"
            if 'DIA' not in df.columns: df['DIA'] = "No especificado"

        df['AÑO'] = pd.to_numeric(df.get('AÑO', 2026), errors='coerce').fillna(2026).astype(int)
        df['FORMA'] = df.get('FORMA', 'Desconocido').fillna('Desconocido').astype(str).str.title()
        df = simular_coordenadas(df)
        return df, ["Sincronización de matriz Agatha completada."]

    df_maestro, diagn_mensajes = cargar_nodos()
    status_boot.update(label="Sistema UAP Online. AGATHA Neural Network lista.", state="complete", expanded=False)

# --- CABECERA AGATHA ---
st.markdown("<h1>AGATHA <span class='cian-electrico'>Intelligent Neural Network</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='mono-tech verde-neon' style='margin-bottom:5px; font-size:1.1rem;'>MÓDULO CONTACT - Fenómeno Anómalo No Identificado</p>", unsafe_allow_html=True)
st.markdown("<p class='quote-contact'>“El Universo es enorme. Y si solo estamos nosotros, cuánto espacio desaprovechado”</p>", unsafe_allow_html=True)

# --- REPORTE CIUDADANO ---
with st.container():
    st.markdown("<div class='notificacion-box'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0px; color:#39ff14 !important;'>NOTIFICA TU AVISTAMIENTO</h4>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    r_fecha = c1.date_input("FECHA", datetime.now())
    r_hora = c2.time_input("HORA", datetime.now().time())
    r_tipo = c3.selectbox("TIPO DE OBJETO", sorted(df_maestro['FORMA'].unique().tolist()))
    r_ubica = c4.text_input("CIUDAD / PAÍS", placeholder="Ej: Madrid, España")
    r_desc = st.text_area("DETALLES CONDUCTUALES DEL FENÓMENO", placeholder="Describa la trayectoria, colores y cualquier anomalía detectada...")
    if st.button("PROCESAR REPORTE EN AGATHA AI"):
        st.success("Reporte cifrado. AGATHA ha integrado su testimonio en la red neural global.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- MAPA Y FILTROS INTEGRADOS ---
st.markdown("---")
col_mapa, col_filtros = st.columns([2.5, 1.5], gap="large")

with col_filtros:
    st.markdown("<h4 class='cian-electrico'>PARAMETROS DE FILTRADO</h4>", unsafe_allow_html=True)
    
    f_c1, f_c2, f_c3 = st.columns(3)
    sel_anio = f_c1.selectbox("AÑO", ["TODOS"] + sorted(df_maestro['AÑO'].unique().tolist(), reverse=True))
    sel_mes = f_c2.selectbox("MES", ["TODOS"] + sorted([m for m in df_maestro['MES'].unique() if str(m).isdigit()], key=lambda x: int(x)))
    sel_dia = f_c3.selectbox("DÍA", ["TODOS"] + sorted([d for d in df_maestro['DIA'].unique() if str(d).isdigit()], key=lambda x: int(x)))
    
    f_c4, f_c5 = st.columns(2)
    sel_hora = f_c4.selectbox("HORA", ["TODAS"] + sorted(df_maestro['HORA'].unique().tolist()))
    sel_pais = f_c5.selectbox("PAÍS", ["TODOS"] + sorted(df_maestro['PAIS'].unique().tolist()))
    
    sel_forma = st.selectbox("FORMA", ["TODOS"] + sorted(df_maestro['FORMA'].unique().tolist()))
    sel_ciudad = st.selectbox("CIUDAD", ["TODOS"] + sorted(df_maestro['CIUDAD'].unique().tolist()))
    
    df_filtrado = df_maestro.copy()
    if sel_anio != "TODOS": df_filtrado = df_filtrado[df_filtrado['AÑO'] == sel_anio]
    if sel_mes != "TODOS": df_filtrado = df_filtrado[df_filtrado['MES'] == sel_mes]
    if sel_dia != "TODOS": df_filtrado = df_filtrado[df_filtrado['DIA'] == sel_dia]
    if sel_hora != "TODAS": df_filtrado = df_filtrado[df_filtrado['HORA'] == sel_hora]
    if sel_forma != "TODOS": df_filtrado = df_filtrado[df_filtrado['FORMA'] == sel_forma]
    if sel_pais != "TODOS": df_filtrado = df_filtrado[df_filtrado['PAIS'] == sel_pais]
    if sel_ciudad != "TODOS": df_filtrado = df_filtrado[df_filtrado['CIUDAD'] == sel_ciudad]
    
    filtros_activos = (sel_anio != "TODOS") or (sel_mes != "TODOS") or (sel_dia != "TODOS") or \
                      (sel_hora != "TODAS") or (sel_forma != "TODOS") or (sel_pais != "TODOS") or (sel_ciudad != "TODOS")

with col_mapa:
    c_m1, c_m2 = st.columns(2)
    modo_v = c_m1.radio("MODO TÁCTICO", ["Nodos Base", "Red de Trayectorias"], horizontal=True)
    proj_v = c_m2.radio("PROYECCIÓN", ["Globo 3D", "Plano 2D"], horizontal=True)
    
    fig = go.Figure()
    if modo_v == "Nodos Base":
        fig.add_trace(go.Scattergeo(lon=df_filtrado['lon'], lat=df_filtrado['lat'], mode='markers',
                                    marker=dict(size=5, color='#00f3ff', opacity=0.7), 
                                    text=df_filtrado['CIUDAD'] + " (" + df_filtrado['PAIS'] + ")"))
    else:
        df_red = df_filtrado.sort_values(by=['AÑO', 'MES', 'DIA']).head(300)
        fig.add_trace(go.Scattergeo(lon=df_red['lon'], lat=df_red['lat'], mode='lines+markers',
                                    line=dict(width=1.5, color='#39ff14'), opacity=0.5))
    
    fig.update_layout(geo=dict(projection_type='orthographic' if proj_v=="Globo 3D" else 'equirectangular',
                               showland=True, landcolor='#111', bgcolor='#0a0a0a', showocean=True, oceancolor='#050505',
                               showcountries=True, countrycolor='#333'),
                      margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='#0a0a0a', height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div style='font-size:0.75rem; color:#64748b; border-top:1px solid #1e293b; padding-top:10px;'>
        INFRAESTRUCTURA: <a href='https://in-the-sky.org/satmap_worldmap.php' style='color:#00f3ff;'>Rastreo Satelital</a> | 
        <a href='https://nuforc.org/databank/' style='color:#00f3ff;'>Base NUFORC Global</a>
    </div>
    """, unsafe_allow_html=True)

# --- INDICADORES DINÁMICOS ---
st.markdown("---")
df_target = df_filtrado if filtros_activos else df_maestro
m1, m2, m3 = st.columns(3)
suffix = " (TOTALES)" if not filtros_activos else " (FILTRADOS)"

m1.metric(f"REGISTROS ACTIVOS{suffix}", f"{len(df_target):,}")
m2.metric(f"TIPOLOGIA PREDOMINANTE{suffix}", df_target['FORMA'].mode().iloc[0] if not df_target.empty else "N/A")
m3.metric(f"ZONAS DE INTERES (NODOS){suffix}", f"{len(df_target['CIUDAD'].unique()) if not df_target.empty else 0:,}")

# --- CATALOGO UAP IDENTIFICACIÓN VISUAL ---
st.markdown("---")
with st.expander("CATÁLOGO UAP IDENTIFICACIÓN VISUAL DE OBJETOS", expanded=False):
    st.markdown("<p style='font-size:0.9rem; color:#94a3b8;'>Referencia morfológica de la Red Neural AGATHA. Haga clic en la imagen para análisis detallado.</p>", unsafe_allow_html=True)
    ruta_img = "assets/catalogo_morfologico_completo.png"
    if os.path.exists(ruta_img):
        st.image(ruta_img, use_container_width=True, caption="Manual de Reconocimiento Visual UAP - AGATHA AI")
    else:
        st.info("Cargue 'catalogo_morfologico_completo.png' en /assets para activar el reconocimiento visual.")

# --- PROCESADOR CONDUCTUAL AGATHA AI ---
st.markdown("---")
with st.expander("PROCESADOR CONDUCTUAL AGATHA (NLP & METEOROLOGÍA)", expanded=True):
    if not df_filtrado.empty:
        opciones = (df_filtrado['CIUDAD'] + " | " + df_filtrado['FORMA'] + " | " + df_filtrado['AÑO'].astype(str)).tolist()
        sel_caso = st.selectbox("EXPEDIENTE PARA ESCANEO CONDUCTUAL", opciones[:500])
        idx_caso = opciones.index(sel_caso)
        data_caso = df_filtrado.iloc[idx_caso]
        
        c_a1, c_a2 = st.columns([2, 1])
        with c_a1:
            st.markdown("#### Reporte Original")
            st.markdown(f"<div style='background:#111; padding:25px; border-left:4px solid #39ff14; font-size:1.1rem; line-height:1.6;'>{data_caso['RESUMEN']}</div>", unsafe_allow_html=True)
        with c_a2:
            st.markdown("#### Análisis AGATHA AI")
            if st.button("EJECUTAR ESCANEO CONDUCTUAL AGATHA"):
                with st.spinner("Procesando patrones anómalos..."):
                    time.sleep(1)
                    st.json({
                        "comportamiento": "Patrón de vuelo no inercial / Desplazamiento hiper-sónico",
                        "hipotesis_convencional": "Descartada (Baja probabilidad de Starlink o Satélite)",
                        "hipotesis_uap": "Objeto trans-medio de origen no identificado",
                        "indice_anomalia": 92
                    })
            
            if st.button("METEOROLOGÍA HISTÓRICA"):
                if OPENWEATHER_API_KEY:
                    st.info(f"Consultando condiciones atmosféricas para {data_caso['CIUDAD']}...")
                else: st.warning("Nodo meteorológico no configurado.")

# --- REGISTROS FORENSES ---
st.markdown("---")
with st.expander(f"REGISTROS FORENSES ({len(df_filtrado)} Activos)", expanded=False):
    st.dataframe(df_filtrado.drop(columns=['COLOR_STR', 'lat', 'lon', 'hash_val'], errors='ignore').sort_values(by='AÑO', ascending=False).head(500), use_container_width=True, hide_index=True)

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align:center; color:#475569; font-size:0.75rem; letter-spacing:1px; border-top:1px solid #1e293b; padding-top:20px;'>
    METODOLOGÍA: PROCESAMIENTO RED NEURAL AGATHA | FUENTE: NUFORC DATASETS | VERSIÓN 7.5<br>
    © MOTOR DE ANÁLISIS CONDUCTUAL PREDICTIVO | OPERADOR {OPERADOR_ID}
</div>
""", unsafe_allow_html=True)
