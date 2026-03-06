# ====================================================================
# ARCHIVO PRINCIPAL: Agatha_Fani.py
# SISTEMA: Motor de Analisis Conductual Predictivo
# MODULO: Inteligencia FANI / UAP (Grafos Multimodales)
# ====================================================================

import streamlit as st

# --- CONFIGURACION DE PAGINA ---
st.set_page_config(
    page_title="AGATHA - Inteligencia Predictiva FANI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DIAGNOSTICO DE LIBRERIAS ---
try:
    import pandas as pd
    import numpy as np
    import pydeck as pdk
    import plotly.express as px
    import plotly.graph_objects as go
    import os
    import time
    import re
    from datetime import datetime
except ImportError as e:
    st.error(f"ALERTA DE SISTEMA: Falta instalar la dependencia -> {e}")
    st.stop()

# --- CSS CORPORATIVO MATE (FLAT DESIGN SOC) ---
CSS_MATE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@300;400;600;700&family=Montserrat:wght@700&family=Share+Tech+Mono&display=swap');

.stApp { background-color: #0f1115 !important; font-family: 'Titillium Web', sans-serif !important; color: #e2e8f0 !important; }
[data-testid="stHeader"], footer { display: none !important; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 1rem !important; max-width: 95% !important; }

h1 { font-family: 'Montserrat', sans-serif !important; text-transform: uppercase; letter-spacing: -0.5px; font-size: 2.2rem !important; color: #ffffff !important; border-bottom: 1px solid #334155; padding-bottom: 10px; text-shadow: none !important;}
h2, h3, h4, h5 { color: #94a3b8 !important; text-transform: uppercase; letter-spacing: 1px; font-family: 'Montserrat', sans-serif !important; font-weight: 600 !important; }

[data-testid="stMetric"] { background-color: #1e293b !important; border: 1px solid #334155 !important; border-left: 4px solid #3b82f6 !important; padding: 15px !important; border-radius: 4px !important; box-shadow: none !important;}
[data-testid="stMetricLabel"] { color: #94a3b8 !important; font-size: 0.85rem !important; font-weight: 600 !important; text-transform: uppercase; }
[data-testid="stMetricValue"] { color: #ffffff !important; font-family: 'Share Tech Mono', monospace !important; font-size: 2.2rem !important; text-shadow: none !important;}

/* Motor de Tablas Tacticas */
.tabla-tactica { width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 0.85rem; border: 1px solid #334155; background-color: #0f1115; }
.tabla-tactica th { background-color: #1e293b; color: #38bdf8; text-align: left; padding: 12px; font-family: 'Montserrat', sans-serif; text-transform: uppercase; border-bottom: 2px solid #475569; letter-spacing: 1px;}
.tabla-tactica td { padding: 10px; color: #e2e8f0; border-bottom: 1px solid #1e293b; font-family: 'Titillium Web', sans-serif; }
.tabla-tactica tr:hover { background-color: #1e293b; }

.stButton > button { border: 1px solid #475569 !important; background-color: #1e293b !important; color: #f8fafc !important; border-radius: 2px !important; font-family: 'Montserrat', sans-serif !important; font-weight: 600 !important; text-transform: uppercase; padding: 0.5rem 1rem !important; box-shadow: none !important;}
.stButton > button:hover { border-color: #3b82f6 !important; color: #ffffff !important; background-color: #2563eb !important; }
button[data-baseweb="tab"] { background-color: transparent !important; color: #64748b !important; font-family: 'Montserrat', sans-serif !important; font-weight: 600 !important; font-size: 0.9rem !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: #ffffff !important; border-bottom: 3px solid #3b82f6 !important; background-color: transparent !important;}
</style>
"""
st.markdown(CSS_MATE, unsafe_allow_html=True)

# --- IDENTIDAD DEL OPERADOR (ADAPTACION MARRUECOS / ESPAÑA) ---
OPERADOR_ID = "Y. ALAOUI (ID DIR-74)"
ROL_ACCESO = "NIVEL 4 - INTELIGENCIA ESTRATEGICA"
MARCA_TIEMPO = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')

st.markdown(f"""
    <div style="position: fixed; top: 15px; right: 20px; background: #1e293b; border: 1px solid #475569; color: #cbd5e1; padding: 6px 15px; font-family: 'Share Tech Mono', monospace; font-size: 0.85rem; z-index: 999999; pointer-events: none; border-radius: 2px;">
        OPERADOR: {OPERADOR_ID} | PERMISO: {ROL_ACCESO}
    </div>
    <div style="position: fixed; bottom: 50px; right: 30px; color: rgba(255, 255, 255, 0.04); font-family: 'Share Tech Mono', monospace; font-size: 1.5rem; z-index: 999999; pointer-events: none; transform: rotate(-10deg); user-select: none;">
        AGATHA INTEL - TRAZA FORENSE: {MARCA_TIEMPO}
    </div>
""", unsafe_allow_html=True)

# --- MOTORES DE INGESTA Y PROCESAMIENTO DE DATOS ---
@st.cache_data(show_spinner=False)
def cargar_nodos():
    ruta_nodos = "agatha_ufo_nodes_full.csv"
    if os.path.exists(ruta_nodos):
        df = pd.read_csv(ruta_nodos, sep=None, engine='python', encoding_errors='ignore')
    else:
        # Simulacion de respaldo si el CSV no esta en la misma carpeta
        df = pd.DataFrame({
            "City": ["Rabat", "Casablanca", "Madrid", "Valencia", "Nevada", "Texas", "Oregon"],
            "State": ["RBA", "CAS", "MAD", "VAL", "NV", "TX", "OR"],
            "Country": ["Marruecos", "Marruecos", "España", "España", "EEUU", "EEUU", "EEUU"],
            "Shape": ["Triangulo", "Cigarro", "Orbe", "Triangulo", "Orbe", "Octaedro", "Cambiante"],
            "Year": [2024, 2025, 2023, 2026, 2025, 2024, 2025],
            "Summary": [
                "Objeto triangular detectado por radar militar, silencio absoluto.",
                "Cilindro plateado acelera instantaneamente a Mach 3.",
                "Orbe luminoso cruzando el cielo, avistado por piloto civil.",
                "Tres triangulos negros sobre central nuclear.",
                "Esfera brillante realiza giros de 90 grados.",
                "Octaedro enorme estatico, interfiere con dispositivos electromagnetico.",
                "Objeto cambiante perseguido por helicoptero Blackhawk."
            ]
        })

    # Normalizacion de cabeceras (Cero Guiones Bajos)
    df.columns = [str(c).strip().replace('_', ' ').title() for c in df.columns]
    
    # Motor de Coordenadas (Mock Inteligente basado en Pais para renderizado 3D)
    np.random.seed(42)
    latitudes = []
    longitudes = []
    for pais in df.get('Country', ['EEUU'] * len(df)):
        pais = str(pais).upper()
        if "MARRUECOS" in pais or "MOROCCO" in pais:
            latitudes.append(np.random.uniform(28.0, 35.0))
            longitudes.append(np.random.uniform(-11.0, -1.0))
        elif "ESPAÑA" in pais or "SPAIN" in pais:
            latitudes.append(np.random.uniform(36.0, 43.0))
            longitudes.append(np.random.uniform(-9.0, 3.0))
        else: # Mayoritariamente EEUU
            latitudes.append(np.random.uniform(30.0, 48.0))
            longitudes.append(np.random.uniform(-125.0, -70.0))
            
    df['Latitud'] = latitudes
    df['Longitud'] = longitudes

    # Asignacion de Codigo de Color por Forma
    def asignar_color(forma):
        forma = str(forma).lower()
        if "tri" in forma: return [225, 29, 72, 200]      # Rojo Tactico
        elif "orb" in forma or "esfera" in forma or "cambiante" in forma: return [234, 179, 8, 200] # Amarillo
        elif "cigar" in forma or "cilindro" in forma: return [34, 197, 94, 200] # Verde
        elif "octa" in forma: return [56, 189, 248, 200]  # Azul Cyan
        else: return [148, 163, 184, 150]                 # Gris Estandar
    
    df['Color RGB'] = df['Shape'].apply(asignar_color)

    # Analisis NLP Forense: Extraccion de Tier 1 y Fisica Imposible
    def es_tier_1(texto):
        texto = str(texto).lower()
        keywords = ['piloto', 'radar', 'militar', 'base', 'blackhawk', 'fuerza aerea', 'controlador']
        return "Si" if any(k in texto for k in keywords) else "No"

    def es_fisica_imposible(texto):
        texto = str(texto).lower()
        keywords = ['90 degree', 'instantaneo', 'silencio', 'silent', 'mach', 'teletransportacion', 'desaparece']
        return "Si" if any(k in texto for k in keywords) else "No"

    df['Credibilidad Tier 1'] = df.get('Summary', '').apply(es_tier_1)
    df['Fisica Anomala'] = df.get('Summary', '').apply(es_fisica_imposible)
    
    # ID unicos para grafos
    df['ID Nodo'] = range(len(df))
    return df

@st.cache_data(show_spinner=False)
def generar_grafos_adyacencia(df):
    # Simulamos el procesamiento del archivo agatha_ufo_relationships_sample.csv
    # creando lineas de trayectoria entre nodos del mismo tipo de objeto
    edges = []
    # Seleccionamos una muestra para no sobrecargar el renderizado en pantalla
    df_sample = df.head(200) 
    for i, row_a in df_sample.iterrows():
        for j, row_b in df_sample.iterrows():
            if i >= j: continue
            if row_a['Shape'] == row_b['Shape'] and str(row_a['Shape']).lower() != 'unknown':
                # Conectar nodos si pertenecen a EEUU o Marruecos/España internamente
                if row_a['Country'] == row_b['Country']:
                    # Solo un 5% de probabilidad para mantener el grafo legible
                    if np.random.random() > 0.95:
                        edges.append({
                            'Origen Lon': row_a['Longitud'],
                            'Origen Lat': row_a['Latitud'],
                            'Destino Lon': row_b['Longitud'],
                            'Destino Lat': row_b['Latitud'],
                            'Color': row_a['Color RGB'],
                            'Contexto': 'Trayectoria Estructural'
                        })
    return pd.DataFrame(edges)

df_maestro = cargar_nodos()
df_grafos = generar_grafos_adyacencia(df_maestro)

def render_tabla_tactica(df):
    html = '<div style="max-height: 400px; overflow-y: auto;"><table class="tabla-tactica"><thead><tr>'
    for col in df.columns:
        if col not in ['Color RGB', 'ID Nodo', 'Latitud', 'Longitud']: # Ocultar columnas tecnicas
            html += f'<th>{col}</th>'
    html += '</tr></thead><tbody>'
    for _, row in df.iterrows():
        html += '<tr>'
        for col in df.columns:
            if col not in ['Color RGB', 'ID Nodo', 'Latitud', 'Longitud']:
                val = row[col]
                html += f'<td>{val}</td>'
        html += '</tr>'
    html += '</tbody></table></div>'
    st.markdown(html, unsafe_allow_html=True)

# --- TERMINAL DE OPERACIONES (SIDEBAR) ---
st.sidebar.markdown("### Centro de Comando AGATHA")

filtro_region = st.sidebar.selectbox("Filtro Geopolitico:", ["Global", "Marruecos y España", "EEUU (North America)"])
filtro_forma = st.sidebar.multiselect("Clasificacion de Nave:", df_maestro['Shape'].unique(), default=df_maestro['Shape'].unique()[:4])
solo_tier1 = st.sidebar.toggle("Filtro Estricto: Testigos Tier 1 (Militar/Radar)")
mostrar_lineas = st.sidebar.toggle("Habilitar Grafos de Trayectoria", value=True)
mostrar_calor = st.sidebar.toggle("Habilitar Conglomeracion (Heatmap)")

# --- APLICACION DE FILTROS ---
df_filtrado = df_maestro[df_maestro['Shape'].isin(filtro_forma)].copy()

if filtro_region == "Marruecos y España":
    df_filtrado = df_filtrado[df_filtrado['Country'].str.contains('Marruecos|España|Morocco|Spain', case=False, na=False)]
elif filtro_region == "EEUU (North America)":
    df_filtrado = df_filtrado[df_filtrado['Country'].str.contains('EEUU|USA|United States', case=False, na=False)]

if solo_tier1:
    df_filtrado = df_filtrado[df_filtrado['Credibilidad Tier 1'] == "Si"]

# --- ENCABEZADO ---
st.markdown("<h1>Motor de Analisis Conductual Predictivo</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-top:-15px; color:#94a3b8;'>Modulo de Inteligencia FANI (Red Multimodal)</h3>", unsafe_allow_html=True)
st.markdown("---")

# --- METRICAS ESTRATEGICAS ---
total_casos = len(df_filtrado)
casos_tier1 = len(df_filtrado[df_filtrado['Credibilidad Tier 1'] == 'Si'])
casos_fisica = len(df_filtrado[df_filtrado['Fisica Anomala'] == 'Si'])

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Volumen de Detecciones", f"{total_casos:,}")
col_m2.metric("Contactos Confirmados (Tier 1)", f"{casos_tier1:,}", "Validacion Militar", delta_color="off")
col_m3.metric("Eventos de Fisica Anomala", f"{casos_fisica:,}", "Alta Prioridad", delta_color="inverse")
col_m4.metric("Nodos de Grafo Activos", f"{len(df_grafos) if mostrar_lineas else 0:,}")

# --- ARQUITECTURA DE PESTAÑAS ---
tab_visor, tab_datos, tab_analisis = st.tabs(["Visor Geoespacial Multimodal", "Registros de Inteligencia", "Analisis NLP y Fenomenologia"])

with tab_visor:
    st.markdown("#### Proyeccion de Nodos y Rutas de Vigilancia")
    
    # Centrar la camara segun la region seleccionada
    if filtro_region == "Marruecos y España":
        cam_lat, cam_lon, zoom_level = 34.0, -4.0, 4.5
    else:
        cam_lat, cam_lon, zoom_level = 39.8, -98.5, 3.5

    view_state = pdk.ViewState(latitude=cam_lat, longitude=cam_lon, zoom=zoom_level, pitch=45, bearing=0)
    
    capas = []
    
    # Capa 1: Nodos de Evento (Puntos)
    if not df_filtrado.empty:
        capas.append(pdk.Layer(
            "ScatterplotLayer",
            data=df_filtrado,
            get_position=["Longitud", "Latitud"],
            get_radius=30000,
            get_fill_color="Color RGB",
            pickable=True,
            auto_highlight=True
        ))

    # Capa 2: Grafo Multimodal (Arcos de Relacion)
    if mostrar_lineas and not df_grafos.empty:
        capas.append(pdk.Layer(
            "ArcLayer",
            data=df_grafos,
            get_source_position=["Origen Lon", "Origen Lat"],
            get_target_position=["Destino Lon", "Destino Lat"],
            get_source_color="Color",
            get_target_color="Color",
            get_width=3,
            pickable=True
        ))

    # Capa 3: Conglomeracion (Heatmap)
    if mostrar_calor and not df_filtrado.empty:
        capas.append(pdk.Layer(
            "HeatmapLayer",
            data=df_filtrado,
            get_position=["Longitud", "Latitud"],
            opacity=0.6,
            get_weight=1
        ))

    st.pydeck_chart(pdk.Deck(
        map_style="carto-darkmatter",
        initial_view_state=view_state,
        layers=capas,
        tooltip={"text": "Clasificacion: {Shape}\nTier 1: {Credibilidad Tier 1}\nFisica Anomala: {Fisica Anomala}"}
    ))

with tab_datos:
    st.markdown("#### Extraccion Forense de Archivos NUFORC / AARO")
    if not df_filtrado.empty:
        columnas_mostrar = ["City", "State", "Country", "Shape", "Year", "Credibilidad Tier 1", "Fisica Anomala", "Summary"]
        df_display = df_filtrado[columnas_mostrar].head(100) # Limitamos a 100 para no saturar el DOM HTML
        render_tabla_tactica(df_display)
    else:
        st.warning("No hay registros que coincidan con los parametros balisticos seleccionados.")

with tab_analisis:
    col_a1, col_a2 = st.columns([1, 1])
    
    with col_a1:
        st.markdown("#### Procesamiento de Lenguaje Natural (Narrativa)")
        st.markdown("<p style='color: #94a3b8; font-size:0.9rem;'>Analisis semantico de atestados para extraccion de parametros estructurales y operativos.</p>", unsafe_allow_html=True)
        
        texto_input = st.text_area("Pegar texto descriptivo o transcripcion de radar:", height=150, value="Un objeto triangular enorme, del tamaño de un campo de futbol, se mantuvo estatico sobre Camp Grayling en silencio absoluto. Luego desaparecio.")
        
        if st.button("Ejecutar Escaner Cognitivo", type="primary", width="stretch"):
            with st.spinner("Procesando matriz semantica..."):
                time.sleep(1)
                
                txt_lower = texto_input.lower()
                forma_detectada = "Triangulo" if "triangul" in txt_lower else "Orbe" if "esfera" in txt_lower else "No Concluyente"
                instalacion = "Camp Grayling" if "grayling" in txt_lower else "Base Aerea" if "base" in txt_lower else "No detectada"
                fisica = "Vuelo Estatico / Supresion Sonica" if "estatico" in txt_lower and "silencio" in txt_lower else "Aceleracion Anomala"
                
                # Interfaz de extraccion sin guiones bajos ni JSON
                st.markdown(f"""
                <div style="background-color: #1e293b; border: 1px solid #334155; border-left: 4px solid #10b981; padding: 15px; border-radius: 4px; font-family: 'Titillium Web', sans-serif;">
                    <p style="margin: 8px 0; color: #e2e8f0; font-size: 1rem;"><b>TIPOLOGIA ESTRUCTURAL:</b> <span style="color: #38bdf8; font-family: 'Share Tech Mono', monospace; font-size: 1.05rem;">{forma_detectada}</span></p>
                    <p style="margin: 8px 0; color: #e2e8f0; font-size: 1rem;"><b>PROXIMIDAD CRITICA:</b> <span style="color: #38bdf8; font-family: 'Share Tech Mono', monospace; font-size: 1.05rem;">{instalacion}</span></p>
                    <p style="margin: 8px 0; color: #e2e8f0; font-size: 1rem;"><b>PATRON COMPORTAMENTAL:</b> <span style="color: #f43f5e; font-family: 'Share Tech Mono', monospace; font-size: 1.05rem; font-weight: bold;">{fisica}</span></p>
                </div>
                """, unsafe_allow_html=True)

    with col_a2:
        st.markdown("#### Matriz de Similitud Fenomenologica")
        st.markdown("<p style='color: #94a3b8; font-size:0.9rem;'>Correlacion historica de incidentes segun tipologia estructural reportada.</p>", unsafe_allow_html=True)
        
        # Grafico de barras purificado
        if not df_filtrado.empty:
            conteo_formas = df_filtrado['Shape'].value_counts().reset_index()
            conteo_formas.columns = ['Forma Estructural', 'Volumen de Incidentes']
            
            fig_formas = px.bar(conteo_formas, x='Volumen de Incidentes', y='Forma Estructural', orientation='h', template="plotly_dark")
            fig_formas.update_traces(marker_color='#3b82f6')
            fig_formas.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            
            # Etiqueta forense en el grafico
            fig_formas.add_annotation(text=f"AGATHA INTEL - {OPERADOR_ID}", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(size=12, color="rgba(255, 255, 255, 0.1)"), textangle=-10)
            
            st.plotly_chart(fig_formas, use_container_width=True)
