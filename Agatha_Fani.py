# ====================================================================
# ARCHIVO PRINCIPAL: Agatha_Fani.py
# SISTEMA: Motor de Analisis Conductual Predictivo
# MODULO: Inteligencia FANI / UAP (Integracion API Real)
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
    import os
    import time
    from datetime import datetime
    from sklearn.ensemble import IsolationForest
    from openai import OpenAI
except ImportError as e:
    st.error(f"ALERTA DE SISTEMA: Falta instalar la dependencia -> {e}")
    st.stop()

# --- CSS CORPORATIVO MATE Y MOTOR DE TABLAS TACTICAS ---
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

/* Contenedor de Tabla con Scroll */
.contenedor-tabla { width: 100%; max-height: 500px; overflow-y: auto; border: 1px solid #334155; background-color: #0f1115; margin-bottom: 20px; }
.rejilla-tactica { width: 100%; border-collapse: collapse; font-family: 'Titillium Web', sans-serif; font-size: 0.85rem; color: #e2e8f0; }
.rejilla-tactica thead th { position: sticky; top: 0; background-color: #1e293b; color: #38bdf8; text-align: left; padding: 12px 15px; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 1px; border-bottom: 2px solid #334155; z-index: 10; }
.rejilla-tactica tbody td { padding: 10px 15px; border-bottom: 1px solid #1e293b; }
.rejilla-tactica tbody tr:hover { background-color: #1e293b; }
.valor-num { font-family: 'Share Tech Mono', monospace; color: #ffffff; }

.stButton > button { border: 1px solid #475569 !important; background-color: #1e293b !important; color: #f8fafc !important; border-radius: 2px !important; font-family: 'Montserrat', sans-serif !important; font-weight: 600 !important; text-transform: uppercase; padding: 0.5rem 1rem !important; box-shadow: none !important;}
.stButton > button:hover { border-color: #3b82f6 !important; color: #ffffff !important; background-color: #2563eb !important; }
button[data-baseweb="tab"] { background-color: transparent !important; color: #64748b !important; font-family: 'Montserrat', sans-serif !important; font-weight: 600 !important; font-size: 0.9rem !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: #ffffff !important; border-bottom: 3px solid #3b82f6 !important; background-color: transparent !important;}
</style>
"""
st.markdown(CSS_MATE, unsafe_allow_html=True)

# --- IDENTIDAD DEL OPERADOR ---
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

# --- GESTION DE SECRETOS Y APIS ---
mapbox_token = st.secrets.get("MAPBOX_API_KEY", None)
openai_token = st.secrets.get("OPENAI_API_KEY", None)

# --- MOTORES DE INGESTA DE DATOS DESDE CARPETA DATA/ ---
def limpiar_cabeceras(df):
    df.columns = [str(c).strip().replace('_', ' ').title() for c in df.columns]
    return df

@st.cache_data(show_spinner=False)
def cargar_nodos():
    ruta_nodos = os.path.join("data", "agatha_ufo_nodes_full.csv")
    if os.path.exists(ruta_nodos):
        df = pd.read_csv(ruta_nodos, sep=None, engine='python', encoding_errors='ignore')
        df = limpiar_cabeceras(df)
        
        if 'Latitud' not in df.columns: df['Latitud'] = np.random.uniform(30.0, 48.0, len(df))
        if 'Longitud' not in df.columns: df['Longitud'] = np.random.uniform(-125.0, -70.0, len(df))
        
        def asignar_color(forma):
            forma = str(forma).lower()
            if "tri" in forma: return [225, 29, 72, 200]
            elif "orb" in forma or "esfera" in forma or "cambiante" in forma: return [234, 179, 8, 200]
            elif "cigar" in forma or "cilindro" in forma: return [34, 197, 94, 200]
            elif "octa" in forma: return [56, 189, 248, 200]
            else: return [148, 163, 184, 150]
        
        df['Color Rgb'] = df.get('Shape', df.iloc[:,0]).apply(asignar_color)
        
        def es_tier_1(texto):
            keywords = ['piloto', 'radar', 'militar', 'base', 'blackhawk', 'fuerza aerea', 'controlador']
            return "Si" if any(k in str(texto).lower() for k in keywords) else "No"

        def es_fisica_imposible(texto):
            keywords = ['90 degree', 'instantaneo', 'silencio', 'silent', 'mach', 'teletransportacion', 'desaparece']
            return "Si" if any(k in str(texto).lower() for k in keywords) else "No"

        if 'Summary' in df.columns:
            df['Credibilidad Tier 1'] = df['Summary'].apply(es_tier_1)
            df['Fisica Anomala'] = df['Summary'].apply(es_fisica_imposible)
            
        return df
    else:
        return pd.DataFrame({"Estado": ["Archivo agatha_ufo_nodes_full.csv no detectado en carpeta data/"]})

@st.cache_data(show_spinner=False)
def cargar_relaciones(df_nodos):
    ruta_relaciones = os.path.join("data", "agatha_ufo_relationships_sample.csv")
    if os.path.exists(ruta_relaciones) and len(df_nodos) > 1 and "Latitud" in df_nodos.columns:
        df_rel = pd.read_csv(ruta_relaciones, sep=None, engine='python', encoding_errors='ignore')
        df_rel = limpiar_cabeceras(df_rel)
        
        edges = []
        for _, row in df_rel.head(300).iterrows(): 
            idx_origen = int(row.get('Source Id', 0)) % len(df_nodos)
            idx_destino = int(row.get('Target Id', 1)) % len(df_nodos)
            
            nodo_a = df_nodos.iloc[idx_origen]
            nodo_b = df_nodos.iloc[idx_destino]
            
            edges.append({
                'Origen Lon': nodo_a['Longitud'],
                'Origen Lat': nodo_a['Latitud'],
                'Destino Lon': nodo_b['Longitud'],
                'Destino Lat': nodo_b['Latitud'],
                'Color': nodo_a.get('Color Rgb', [148, 163, 184, 150])
            })
        return pd.DataFrame(edges)
    return pd.DataFrame()

df_maestro = cargar_nodos()
df_grafos = cargar_relaciones(df_maestro)

# --- FUNCION RENDERIZADO TABLA TACTICA (CERO GUIONES BAJOS) ---
def render_tabla_tactica(df):
    html = '<div class="contenedor-tabla"><table class="rejilla-tactica"><thead><tr>'
    for col in df.columns:
        if col not in ['Color Rgb', 'Latitud', 'Longitud']: 
            html += f'<th>{col}</th>'
    html += '</tr></thead><tbody>'
    for _, row in df.iterrows():
        html += '<tr>'
        for col in df.columns:
            if col not in ['Color Rgb', 'Latitud', 'Longitud']:
                val = row[col]
                clase = 'valor-num' if isinstance(val, (int, float, np.integer, np.floating)) else ''
                html += f'<td class="{clase}">{val}</td>'
        html += '</tr>'
    html += '</tbody></table></div>'
    st.markdown(html, unsafe_allow_html=True)

# --- TERMINAL DE OPERACIONES (SIDEBAR) ---
st.sidebar.markdown("### Centro de Comando AGATHA")
filtro_region = st.sidebar.selectbox("Filtro Geopolitico:", ["Global", "Marruecos y España", "Norteamerica"])

formas_disp = df_maestro.get('Shape', pd.Series(['Desconocido'])).unique()
filtro_forma = st.sidebar.multiselect("Clasificacion de Nave:", formas_disp, default=formas_disp[:4])

solo_tier1 = st.sidebar.toggle("Filtro Estricto: Testigos Tier 1 (Militar/Radar)")
mostrar_lineas = st.sidebar.toggle("Habilitar Grafos de Trayectoria", value=True)
mostrar_calor = st.sidebar.toggle("Habilitar Conglomeracion (Heatmap)")

# --- APLICACION DE FILTROS ---
if 'Shape' in df_maestro.columns:
    df_filtrado = df_maestro[df_maestro['Shape'].isin(filtro_forma)].copy()
else:
    df_filtrado = df_maestro.copy()

if solo_tier1 and 'Credibilidad Tier 1' in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado['Credibilidad Tier 1'] == "Si"]

# --- ENCABEZADO ---
st.markdown("<h1>Motor de Analisis Conductual Predictivo</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-top:-15px; color:#94a3b8;'>Modulo de Inteligencia FANI (Red Multimodal)</h3>", unsafe_allow_html=True)
st.markdown("---")

# --- METRICAS ESTRATEGICAS ---
total_casos = len(df_filtrado)
casos_tier1 = len(df_filtrado[df_filtrado.get('Credibilidad Tier 1', '') == 'Si']) if 'Credibilidad Tier 1' in df_filtrado.columns else 0
casos_fisica = len(df_filtrado[df_filtrado.get('Fisica Anomala', '') == 'Si']) if 'Fisica Anomala' in df_filtrado.columns else 0

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Volumen de Detecciones", f"{total_casos:,}")
col_m2.metric("Contactos Confirmados (Tier 1)", f"{casos_tier1:,}", "Validacion Militar", delta_color="off")
col_m3.metric("Eventos de Fisica Anomala", f"{casos_fisica:,}", "Alta Prioridad", delta_color="inverse")
col_m4.metric("Nodos de Grafo Activos", f"{len(df_grafos) if mostrar_lineas else 0:,}")

# --- ARQUITECTURA DE PESTAÑAS ---
tab_visor, tab_datos, tab_analisis = st.tabs(["Visor Geoespacial Multimodal", "Registros de Inteligencia", "Analisis NLP y Fenomenologia"])

with tab_visor:
    st.markdown("#### Proyeccion de Nodos y Rutas de Vigilancia")
    
    # Centrado dinamico
    cam_lat = df_filtrado['Latitud'].mean() if not df_filtrado.empty and 'Latitud' in df_filtrado.columns else 39.8
    cam_lon = df_filtrado['Longitud'].mean() if not df_filtrado.empty and 'Longitud' in df_filtrado.columns else -98.5
    view_state = pdk.ViewState(latitude=cam_lat, longitude=cam_lon, zoom=3.5, pitch=45, bearing=0)
    
    capas = []
    
    if not df_filtrado.empty and 'Latitud' in df_filtrado.columns:
        capas.append(pdk.Layer(
            "ScatterplotLayer",
            data=df_filtrado,
            get_position=["Longitud", "Latitud"],
            get_radius=30000,
            get_fill_color="Color Rgb",
            pickable=True,
            auto_highlight=True
        ))

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

    if mostrar_calor and not df_filtrado.empty and 'Latitud' in df_filtrado.columns:
        capas.append(pdk.Layer(
            "HeatmapLayer",
            data=df_filtrado,
            get_position=["Longitud", "Latitud"],
            opacity=0.6,
            get_weight=1
        ))

    # Seleccion de mapa inteligente basado en existencia de API KEY
    estilo_mapa_3d = "mapbox://styles/mapbox/dark-v11" if mapbox_token else "carto-darkmatter"
    diccionario_api = {"mapbox": mapbox_token} if mapbox_token else None

    st.pydeck_chart(pdk.Deck(
        api_keys=diccionario_api,
        map_style=estilo_mapa_3d, 
        initial_view_state=view_state, 
        layers=capas
    ))

with tab_datos:
    st.markdown("#### Extraccion Forense de Archivos NUFORC / AARO")
    if not df_filtrado.empty:
        df_display = df_filtrado.head(100).copy()
        render_tabla_tactica(df_display)
    else:
        st.warning("No hay registros que coincidan con los parametros seleccionados o falta el archivo CSV en la carpeta data/.")

with tab_analisis:
    col_a1, col_a2 = st.columns([1, 1])
    
    with col_a1:
        st.markdown("#### Inteligencia Artificial: Escaner NLP")
        texto_input = st.text_area("Pegar texto descriptivo o transcripcion de radar:", height=150, value="Un objeto triangular enorme, del tamaño de un campo de futbol, se mantuvo estatico sobre Camp Grayling en silencio absoluto. Despues desaparecio del radar militar.")
        
        if st.button("Ejecutar Escaner Cognitivo", type="primary", width="stretch"):
            if texto_input:
                with st.spinner("Conectando con Motor GPT y procesando matriz semantica..."):
                    if openai_token:
                        try:
                            cliente_ai = OpenAI(api_key=openai_token)
                            prompt_sistema = """
                            Actua como analista de inteligencia militar. Extrae del siguiente reporte tres variables:
                            1. MODUS OPERANDI (Forma, comportamiento o tipo de vuelo)
                            2. NIVEL DE AMENAZA (Critico, Elevado, Estandar)
                            3. DIRECTIVA (Accion recomendada)
                            Devuelve solo los datos, separados por barras verticales (|). No uses saltos de linea ni comillas.
                            """
                            respuesta = cliente_ai.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {"role": "system", "content": prompt_sistema},
                                    {"role": "user", "content": texto_input}
                                ],
                                temperature=0.1
                            )
                            datos = respuesta.choices[0].message.content.split("|")
                            mo = datos[0].strip() if len(datos) > 0 else "No Concluyente"
                            amenaza = datos[1].strip() if len(datos) > 1 else "Estandar"
                            directiva = datos[2].strip() if len(datos) > 2 else "Contencion"
                        except Exception as e:
                            st.error(f"Fallo en la conexion IA: {e}")
                            mo, amenaza, directiva = "Fallo de API", "Desconocido", "Verificar Conexion"
                    else:
                        # Fallback automatico a simulacion si no hay key
                        time.sleep(1.5)
                        mo = "Triangulo / Vuelo Estatico / Supresion Sonica"
                        amenaza = "CRITICO"
                        directiva = "Despliegue Interceptores Aereos"

                    color_am = "#f43f5e" if "Critic" in amenaza or "Elevad" in amenaza else "#3b82f6"

                    st.markdown(f"""
                    <div style="background-color: #1e293b; border: 1px solid #334155; border-left: 4px solid #10b981; padding: 15px; border-radius: 4px; font-family: 'Titillium Web', sans-serif;">
                        <p style="margin: 8px 0; color: #e2e8f0; font-size: 1rem;"><b>TIPOLOGIA Y COMPORTAMIENTO:</b> <span style="color: #38bdf8; font-family: 'Share Tech Mono', monospace; font-size: 1.05rem;">{mo}</span></p>
                        <p style="margin: 8px 0; color: #e2e8f0; font-size: 1rem;"><b>NIVEL AMENAZA CALCULADO:</b> <span style="color: {color_am}; font-family: 'Share Tech Mono', monospace; font-size: 1.05rem; font-weight: bold;">{amenaza}</span></p>
                        <p style="margin: 8px 0; color: #e2e8f0; font-size: 1rem;"><b>DIRECTIVA OPERATIVA:</b> <span style="color: #38bdf8; font-family: 'Share Tech Mono', monospace; font-size: 1.05rem;">{directiva}</span></p>
                    </div>
                    """, unsafe_allow_html=True)

    with col_a2:
        st.markdown("#### Matriz de Similitud Fenomenologica")
        if not df_filtrado.empty and 'Shape' in df_filtrado.columns:
            conteo_formas = df_filtrado['Shape'].value_counts().reset_index()
            conteo_formas.columns = ['Forma Estructural', 'Volumen de Incidentes']
            
            fig_formas = px.bar(conteo_formas, x='Volumen de Incidentes', y='Forma Estructural', orientation='h', template="plotly_dark")
            fig_formas.update_traces(marker_color='#3b82f6')
            fig_formas.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            
            fig_formas.add_annotation(text=f"AGATHA INTEL - {OPERADOR_ID}", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(size=12, color="rgba(255, 255, 255, 0.1)"), textangle=-10)
            st.plotly_chart(fig_formas, use_container_width=True)[data-testid="stHeader"], footer { display: none !important; }
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
