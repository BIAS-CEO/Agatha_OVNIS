# ====================================================================
# ARCHIVO PRINCIPAL: Agatha_Fani.py
# SISTEMA: AGATHA Intelligent Neural Network
# MODULO: MODULO CONTACT (Fenomeno Anomalo No Identificado)
# VERSION: Opcon Ready v10.10 (Malla Deep Black & Tactical Maps)
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
from PIL import Image

# --- CONFIGURACION DE PAGINA ---
st.set_page_config(
    page_title="AGATHA - Intelligent Neural Network",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS TACTICO MILITAR (Opcon Ready) ---
CSS_TACTICO = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@300;400;600;700&family=Montserrat:wght@700&family=Share+Tech+Mono&display=swap');

/* Malla Global - Deep Black */
.stApp { 
    background-color: #000000 !important; 
    font-family: 'Titillium Web', sans-serif !important; 
    color: #e2e8f0 !important; 
}

/* Ocultar Headers y Footers */
[data-testid="stHeader"], footer, [data-testid="collapsedControl"] { display: none !important; }

/* Contenedor Principal con mas aire */
.block-container { 
    padding-top: 2rem !important; 
    padding-bottom: 2rem !important; 
    max-width: 96% !important; 
}

/* Cabeceros - Montserrat */
h1 { 
    font-family: 'Montserrat', sans-serif !important; 
    text-transform: uppercase; 
    letter-spacing: -0.5px; 
    font-size: 2.2rem !important; 
    color: #00d4ff !important; 
    text-shadow: 0 0 15px rgba(0, 212, 255, 0.4);
    border-bottom: 2px solid #1e293b; 
    padding-bottom: 8px; 
    margin-bottom: 0.2rem !important;
}
h2, h3, h4 { 
    color: #cbd5e1 !important; 
    text-transform: uppercase; 
    letter-spacing: 2px; 
    font-family: 'Montserrat', sans-serif !important; 
    font-weight: 600 !important; 
    font-size: 1rem !important;
    margin-top: 0.5rem !important;
}

/* Cita Operativa */
.cita-contact {
    font-family: 'Titillium Web', sans-serif;
    font-style: italic;
    color: #a855f7;
    font-size: 1.05rem;
    letter-spacing: 0.5px;
    margin-bottom: 1.5rem;
    text-shadow: 0 0 10px rgba(168, 85, 247, 0.3);
}

/* Metric Tactica (Reducida y Oscurecida) */
[data-testid="stMetric"] { 
    background-color: #0d1117 !important; 
    border: 1px solid #1e293b !important; 
    border-left: 4px solid #00d4ff !important; 
    padding: 10px !important; 
    border-radius: 4px !important; 
    height: 100%;
}
[data-testid="stMetricLabel"] { 
    color: #64748b !important; 
    font-size: 0.65rem !important; 
    font-weight: 700 !important; 
    text-transform: uppercase; 
    letter-spacing: 1px;
}
[data-testid="stMetricValue"] { 
    color: #ffffff !important; 
    font-family: 'Share Tech Mono', monospace !important; 
    font-size: 1.6rem !important;
    font-weight: 400 !important;
}

/* ELIMINAR HUECO ENTRE IMAGEN Y BOTON EN LAS COLUMNAS */
div[data-testid="column"] > div > div[data-testid="stVerticalBlock"] { gap: 0rem !important; }
div[data-testid="stImage"] { margin-bottom: 0px !important; }
div[data-testid="stImage"] img { border-bottom-left-radius: 0px !important; border-bottom-right-radius: 0px !important; }
div[data-testid="stButton"] { margin-top: 0px !important; }

/* Botones Principales (Estilo Plano) */
div[data-testid="stButton"] button {
    width: 100% !important; 
    height: auto !important;
    padding: 8px 4px !important;
    border: 1px solid #1e293b !important; 
    border-top: none !important; 
    background-color: #0d1117 !important; 
    border-radius: 0px !important; 
    transition: all 0.2s ease;
    display: block !important;
}
div[data-testid="stButton"] button p {
    font-family: 'Montserrat', sans-serif !important; 
    font-weight: 600 !important; 
    text-transform: uppercase; 
    color: #00d4ff !important; 
    font-size: 0.65rem !important;
    white-space: normal !important; 
    word-wrap: break-word !important; 
    overflow: visible !important; 
    text-overflow: clip !important; 
    line-height: 1.2 !important; 
    margin: 0 !important; 
    text-align: center !important;
}
div[data-testid="stButton"] button:hover { border-color: #00d4ff !important; background-color: #00d4ff !important; border-top: 1px solid #00d4ff !important;}
div[data-testid="stButton"] button:hover p { color: #000000 !important; }

/* Boton de Portada (Brillante) */
.boton-entrada div[data-testid="stButton"] button {
    border-top: 2px solid #00d4ff !important;
    border-color: #00d4ff !important;
    box-shadow: 0 0 25px rgba(0, 212, 255, 0.4) !important;
}
.boton-entrada div[data-testid="stButton"] button p { font-size: 1.1rem !important; padding: 0.5rem !important;}

/* Boton Purgar (Rojo Tactico) */
.boton-purgar div[data-testid="stButton"] button { border-color: #ff3333 !important; border-top: 1px solid #ff3333 !important;}
.boton-purgar div[data-testid="stButton"] button p { color: #ff3333 !important; }
.boton-purgar div[data-testid="stButton"] button:hover { background-color: #ff3333 !important; }
.boton-purgar div[data-testid="stButton"] button:hover p { color: #000000 !important; }

/* Boton Simular (Verde Tactico) */
.boton-simular div[data-testid="stButton"] button { border-color: #00ff88 !important; border-top: 1px solid #00ff88 !important; box-shadow: 0 0 20px rgba(0, 255, 136, 0.3) !important;}
.boton-simular div[data-testid="stButton"] button p { color: #00ff88 !important; font-size: 0.9rem !important;}
.boton-simular div[data-testid="stButton"] button:hover { background-color: #00ff88 !important; }
.boton-simular div[data-testid="stButton"] button:hover p { color: #000000 !important; }

/* --- REFACTORIZACION DE RADIO BUTTONS TACTICOS --- */
div[data-testid="stRadio"] { 
    background-color: #0d1117; 
    border: 1px solid #1e293b; 
    padding: 10px; 
    border-radius: 4px;
}
div[data-testid="stRadio"] label[data-testid="stWidgetLabel"] { 
    color: #64748b !important; 
    font-weight: 700; 
    text-transform: uppercase; 
    font-size: 0.7rem; 
    margin-bottom: 8px;
}
/* Convertir radios en array de botones horizontales */
div.row-widget.stRadio > div {
    flex-direction: row;
    gap: 4px;
}
div.row-widget.stRadio > div > div {
    background-color: #161b22; 
    border: 1px solid #1e293b; 
    padding: 6px 12px; 
    border-radius: 20px;
    cursor: pointer;
}
div.row-widget.stRadio > div > div:has(input[checked]) {
    border-color: #00d4ff;
    background-color: rgba(0, 212, 255, 0.1);
}
div.row-widget.stRadio > div > div label p { 
    color: #e2e8f0; 
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
}
div.row-widget.stRadio > div > div:has(input[checked]) label p { 
    color: #00d4ff; 
    font-weight: 700;
}
/* Ocultar los circulos nativos */
div.row-widget.stRadio div[data-testid="stMarkdownContainer"] { margin-left: 0; }
div.row-widget.stRadio input { display: none; }

/* --- TABLA FORENSE --- */
div[data-testid="stDataFrame"] { background-color: #000000; }
div[data-testid="stDataFrame"] table { color: #cbd5e1; background-color: #000000; }
div[data-testid="stDataFrame"] th {
    text-transform: uppercase;
    color: #00d4ff;
    font-family: 'Montserrat', sans-serif;
    font-size: 0.75rem;
    background-color: #0d1117 !important;
}
div[data-testid="stDataFrame"] td { font-family: 'Share Tech Mono', monospace; }
div[data-testid="stDataFrame"] tr:hover td { background-color: rgba(0, 212, 255, 0.1) !important; }
</style>
"""
st.markdown(CSS_TACTICO, unsafe_allow_html=True)

# --- INICIALIZACION DE ESTADOS ---
if "pantalla_actual" not in st.session_state: st.session_state["pantalla_actual"] = "portada"
if "simulaciones_activas" not in st.session_state: st.session_state["simulaciones_activas"] = []
if "reportes_ciudadanos" not in st.session_state: st.session_state["reportes_ciudadanos"] = []

# --- FUNCIONES NUCLEO GLOBAL ---
def normalizar_miniatura(ruta_imagen, tamaño=(300, 300)):
    try:
        img = Image.open(ruta_imagen).convert("RGBA")
        img.thumbnail(tamaño, Image.Resampling.LANCZOS)
        fondo = Image.new('RGBA', tamaño, (10, 10, 10, 0)) 
        desplazamiento = (int((tamaño[0] - img.width) / 2), int((tamaño[1] - img.height) / 2))
        fondo.paste(img, desplazamiento)
        return fondo
    except Exception: return None

@st.dialog("VISOR TACTICO UAP", width="large")
def abrir_visor_completo(nombre_forma_archivo):
    ruta_completa = os.path.join("assets", f"{nombre_forma_archivo}_completo.png")
    if os.path.exists(ruta_completa): st.image(ruta_completa, use_container_width=True)
    else: st.error(f"[ERROR ARCHIVO] Falta el archivo de detalle: {ruta_completa}")

def obtener_credencial(nombre_var):
    try:
        if hasattr(st, "secrets") and nombre_var in st.secrets: return st.secrets[nombre_var]
    except Exception: pass
    valor = os.environ.get(nombre_var)
    if valor: return valor
    return None

DEEPSEEK_API_KEY = obtener_credencial("DEEPSEEK_API_KEY")

def asignar_color_neon(forma):
    f = str(forma).lower()
    if any(x in f for x in ["triangulo", "triangular", "delta", "tri"]): return 'rgba(0, 255, 128, 0.9)'
    elif any(x in f for x in ["esfera", "orb", "circular", "redondo", "disco", "disk"]): return 'rgba(255, 0, 128, 0.9)'
    elif any(x in f for x in ["cigarro", "cilindro", "tubo", "cigar"]): return 'rgba(255, 128, 0, 0.9)'
    elif any(x in f for x in ["luz", "cambiante", "pulsante", "flash", "light"]): return 'rgba(255, 255, 0, 0.9)'
    elif any(x in f for x in ["diamante", "rombo", "cuadrado", "diamond"]): return 'rgba(128, 0, 255, 0.9)'
    elif any(x in f for x in ["rectangulo", "plataforma", "rectangle"]): return 'rgba(0, 128, 255, 0.9)'
    else: return 'rgba(0, 212, 255, 0.9)'

def simular_coordenadas(df):
    np.random.seed(42)
    centroides = {
        "TX": (31.9, -99.9), "FL": (27.7, -81.6), "CA": (36.7, -119.4), "NY": (40.7, -74.0),
        "EEUU": (39.8, -98.5), "CANADA": (56.1, -106.3), "MEXICO": (23.6, -102.5),
        "ESPAÑA": (40.46, -3.75), "FRANCIA": (46.22, 2.21), "ALEMANIA": (51.16, 10.45)
    }
    
    pai = df['PAIS'].astype(str).str.upper().str.strip()
    coords_pai = pai.map(centroides)
    
    def coords_seguras(row_hash): return (((row_hash % 130) - 60), ((row_hash % 240) - 120))
    df['hash_val'] = df['CIUDAD'].astype(str).apply(lambda x: sum(ord(c) for c in x) if pd.notna(x) else 0)
    coordenadas_respaldo = df['hash_val'].apply(coords_seguras)
    coords_finales = coords_pai.combine_first(pd.Series([(c[0], c[1]) for c in coordenadas_respaldo], index=df.index))
    
    df['lat'] = coords_finales.apply(lambda x: x[0]) + (((df['hash_val'] % 100) - 50) / 100.0 * 1.5)
    df['lon'] = coords_finales.apply(lambda x: x[1]) + ((((df['hash_val'] // 10) % 100) - 50) / 100.0 * 1.5)
    
    df = df.drop(columns=['hash_val'])
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce').fillna(0.0)
    df['lon'] = pd.to_numeric(df['lon'], errors='coerce').fillna(0.0)
    
    return df
    
@st.cache_data(show_spinner=False)
def cargar_nodos():
    ruta_carpeta = "data"
    dfs = []
    
    # Columnas base de supervivencia
    columnas_seguras = ['AÑO', 'MES', 'DIA', 'HORA', 'CIUDAD', 'PAIS', 'FORMA', 'lat', 'lon', 'COLOR_STR']
    
    if os.path.exists(ruta_carpeta):
        for archivo in os.listdir(ruta_carpeta):
            if archivo.endswith(".csv") and "avistamientos_testimonios" not in archivo.lower() and "relationships" not in archivo.lower():
                try:
                    temp_df = pd.read_csv(os.path.join(ruta_carpeta, archivo), sep=None, engine='python', encoding='utf-8-sig', on_bad_lines='skip')
                    dfs.append(temp_df)
                except Exception: pass
                
    if dfs: 
        df = pd.concat(dfs, ignore_index=True)
    else: 
        return pd.DataFrame(columns=columnas_seguras), ["[ERROR] Datos no encontrados. Motor en reposo."]

    try:
        df.columns = df.columns.str.upper().str.strip()
        col_map = {'YEAR': 'AÑO', 'CITY': 'CIUDAD', 'COUNTRY': 'PAIS', 'PAÍS': 'PAIS', 'SHAPE': 'FORMA', 'TIME': 'HORA'}
        df.rename(columns=col_map, inplace=True)
        df = df.loc[:, ~df.columns.duplicated()]
        
        # Supervivencia: Si el CSV no tiene la columna, se crea vacía para que no explote
        for c in ['CIUDAD', 'PAIS', 'FORMA']: 
            if c not in df.columns: df[c] = "No especificado"
            df[c] = df[c].fillna("No especificado").astype(str).str.title().str.strip()
            
        df['AÑO'] = pd.to_numeric(df.get('AÑO', 2026), errors='coerce').fillna(2026).astype(int)
        df['DIA'] = pd.to_numeric(df.get('DIA', 0), errors='coerce').fillna(0).astype(int).astype(str).replace('0', 'No especificado')
        df['MES'] = pd.to_numeric(df.get('MES', 0), errors='coerce').fillna(0).astype(int).astype(str).replace('0', 'No especificado')
        
        def formatear_hora(h):
            val = str(h).strip()
            if val.lower() in ['nan', 'nat', 'none', 'null', '', 'no especificada']: return "No especificada"
            if ':' in val:
                partes = val.split(':')
                if len(partes) >= 2: return f"{partes[0].zfill(2)}:{partes[1].zfill(2)}"
            return "No especificada"

        df['HORA'] = df.get('HORA', pd.Series(["No especificada"]*len(df))).apply(formatear_hora)
        df = simular_coordenadas(df)
        df['COLOR_STR'] = df['FORMA'].apply(asignar_color_neon)
        
        return df, ["[INFO] Sincronización de nodos completa."]
    except Exception as e: 
        return pd.DataFrame(columns=columnas_seguras), [f"[ERROR] Proceso interrumpido: {str(e)}"]
        
@st.cache_data(show_spinner=False)
def cargar_archivo_relaciones():
    rutas_posibles = ["agatha_ufo_relationships.csv", os.path.join("data", "agatha_ufo_relationships.csv")]
    for r in rutas_posibles:
        if os.path.exists(r):
            try: return pd.read_csv(r, sep=None, engine='python', encoding='utf-8-sig', on_bad_lines='skip')
            except Exception: pass
    return pd.DataFrame()

# ====================================================================
# PANTALLA 1: PORTADA / PANTALLA DE ARRANQUE
# ====================================================================
if st.session_state["pantalla_actual"] == "portada":
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_vacia1, col_centro, col_vacia2 = st.columns([1, 4, 1])
    
    with col_centro:
        ruta_panel_maestro = os.path.join("assets", "dashboard_maestro_global.png")
        if os.path.exists(ruta_panel_maestro):
            st.image(ruta_panel_maestro, use_container_width=True)
            
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='boton-entrada'>", unsafe_allow_html=True)
        if st.button("ACCEDER A AGATHA INTELLIGENT NEURAL NETWORK", type="primary", use_container_width=True):
            st.session_state["pantalla_actual"] = "principal"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ====================================================================
# PANTALLA 2: INTERFAZ PRINCIPAL TACTICA
# ====================================================================
elif st.session_state["pantalla_actual"] == "principal":
    
    with st.status("Estableciendo conexión segura con AGATHA...", expanded=False) as status_arranque:
        df_maestro, mensajes_diagnostico = cargar_nodos()
        status_arranque.update(label="Sistema UAP 'Opcon Ready' en línea.", state="complete")

    IDENTIFICACION_OPERADOR = "DIR-74"
    NIVEL_ACCESO = "NIVEL 4 - INTELIGENCIA ESTRATEGICA"
    MARCA_TIEMPORAL = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    st.markdown(f"""
        <div style="position: fixed; top: 12px; right: 20px; background: #0d1117; border: 1px solid #1e293b; 
        color: #64748b; padding: 6px 15px; font-family: 'Share Tech Mono', monospace; font-size: 0.7rem; 
        z-index: 999999; pointer-events: none; text-transform: uppercase; letter-spacing: 0.5px;">
            Operador: {IDENTIFICACION_OPERADOR} | Acceso: {NIVEL_ACCESO} | {MARCA_TIEMPORAL}
        </div>
    """, unsafe_allow_html=True)

    columna_titulo, columna_desconexion = st.columns([4, 1])
    with columna_titulo:
        st.markdown("<h1>AGATHA Intelligent Neural Network</h1>", unsafe_allow_html=True)
        st.markdown("<h3>MODULO CONTACT - Fenómeno Anómalo No Identificado</h3>", unsafe_allow_html=True)
        st.markdown("<div class='cita-contact'>«El Universo es enorme. Y si solo estamos nosotros, cuanto espacio desaprovechado»</div>", unsafe_allow_html=True)
    with columna_desconexion:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("DESCONECTAR", type="primary"):
            st.session_state["pantalla_actual"] = "portada"
            st.rerun()

    # --- CATALOGO UAP ---
    with st.expander("CATALOGO UAP - IDENTIFICACION VISUAL", expanded=False):
        st.markdown("<div style='color:#00d4ff; font-size:0.8rem; margin-bottom:15px; line-height:1.4;'>INFORMACION TACTICA: Selecciona la forma para abrir el analisis visual de reconocimiento.</div>", unsafe_allow_html=True)
        lista_archivos_morfologicos = [
            "bola_de_fuego", "cambiante", "cigarro", "cilindro", "circulo", "cono",
            "cruz", "cubo", "desconocido", "diamante", "disco", "esfera",
            "estrella", "flash", "formacion", "galones", "huevo", "lagrima",
            "luz", "orbe", "otros", "oval", "rectangulo", "triangulo"
        ]
        for i in range(0, 24, 6):
            columnas_cuadricula = st.columns(6, gap="small")
            for j in range(6):
                indice = i + j
                if indice < len(lista_archivos_morfologicos):
                    forma_archivo = lista_archivos_morfologicos[indice]
                    with columnas_cuadricula[j]:
                        ruta_miniatura = os.path.join("assets", f"{forma_archivo}.png")
                        if os.path.exists(ruta_miniatura):
                            imagen_procesada = normalizar_miniatura(ruta_miniatura)
                            if imagen_procesada:
                                st.image(imagen_procesada, use_container_width=True)
                                if st.button(f"{forma_archivo.replace('_',' ').upper()}", key=f"btn_{forma_archivo}", use_container_width=True):
                                    abrir_visor_completo(forma_archivo)
            st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True) 

    # --- PANEL TACTICO SUPERIOR ---
    st.markdown("---")
    columna_metrica1, columna_metrica2, columna_controles = st.columns([1, 1, 3])
    
    total_activos = len(df_maestro) if not df_maestro.empty else 0
    df_formas_validas = df_maestro[~df_maestro['FORMA'].str.upper().isin(['DESCONOCIDO', 'NO ESPECIFICADO'])] if not df_maestro.empty else pd.DataFrame()
    forma_dominante = df_formas_validas['FORMA'].mode().iloc[0] if not df_formas_validas.empty else "ND"

    columna_metrica1.metric("REGISTROS ACTIVOS", f"{total_activos:,}".replace(",", "."))
    columna_metrica2.metric("TIPOLOGIA PREDOMINANTE", forma_dominante.upper())
    
    with columna_controles:
        col_c1, col_c2 = st.columns([2, 1])
        modo_operacion = col_c1.radio("MODO TACTICO", ["Nodos Base", "Red de Trayectorias", "IA Predictiva"], horizontal=True)
        tipo_camara = col_c2.radio("PROYECCION", ["Globo 3D", "Plano 2D"], horizontal=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- VISUALIZACION PRINCIPAL (MAPA TACTICO REDISEÑADO) ---
    columna_mapa, columna_filtros = st.columns([3, 1], gap="medium")

    datos_filtrados = df_maestro.copy()
    filtros_aplicados = False
    
    datos_mapa_tactico = df_maestro[ (df_maestro['PAIS'].str.upper() != 'NO ESPECIFICADO') ].copy()

    with columna_filtros:
        st.markdown("#### Parámetros de Filtrado")
        
        c_f1, c_f2 = st.columns(2)
        años_disponibles = sorted(df_maestro['AÑO'].unique(), reverse=True)
        seleccion_año = c_f1.selectbox("AÑO", ["TODOS"] + [int(a) for a in años_disponibles])
        formas_disponibles = sorted(df_maestro['FORMA'].unique())
        seleccion_forma = c_f2.selectbox("TIPO", ["TODOS"] + [str(f) for f in formas_disponibles])
        
        paises_disponibles = sorted(df_maestro['PAIS'].unique())
        seleccion_pais = st.selectbox("PAIS", ["TODOS"] + [str(p) for p in paises_disponibles])

        if seleccion_año != "TODOS": 
            datos_filtrados = datos_filtrados[datos_filtrados['AÑO'] == seleccion_año]
            filtros_aplicados = True
        if seleccion_forma != "TODOS": 
            datos_filtrados = datos_filtrados[datos_filtrados['FORMA'] == seleccion_forma]
            filtros_aplicados = True
        if seleccion_pais != "TODOS": 
            datos_filtrados = datos_filtrados[datos_filtrados['PAIS'] == seleccion_pais]
            filtros_aplicados = True
            
        datos_mapa_tactico = datos_filtrados[ (datos_filtrados['PAIS'].str.upper() != 'NO ESPECIFICADO') ].copy()

        st.markdown("---")
        st.markdown(f"<p style='color: #00d4ff; font-weight: 700; font-family:Share Tech Mono;'>NODOS FILTRADOS: {len(datos_filtrados)}</p>", unsafe_allow_html=True)
        
        # SIMULACION
        st.markdown("<br>", unsafe_allow_html=True)
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("<div class='boton-simular'>", unsafe_allow_html=True)
            if st.button("SIMULAR APARICION"):
                lat_s = np.random.uniform(25, 55); lon_s = np.random.uniform(-125, 30)
                st.session_state["simulaciones_activas"].append({'lat': lat_s, 'lon': lon_s, 'txt': f"[SIMULACRO] CONTACTO | {datetime.now().strftime('%H:%M')} UTC"})
            st.markdown("</div>", unsafe_allow_html=True)
        with col_s2:
            st.markdown("<div class='boton-purgar'>", unsafe_allow_html=True)
            if st.button("PURGAR RASTROS"): st.session_state["simulaciones_activas"] = []
            st.markdown("</div>", unsafe_allow_html=True)

    with columna_mapa:
        espacio_grafico = st.empty()
        with st.spinner("Calibrando proyección táctica..."):
            mapa_visual = go.Figure()
            
            def generar_tooltip(df):
                return (
                    "<b>Ciudad:</b> " + df['CIUDAD'] + "<br>" +
                    "<b>País:</b> " + df['PAIS'] + "<br>" +
                    "<b>Forma:</b> " + df['FORMA'] + "<br>" +
                    "<b>Fecha:</b> " + df['DIA'].astype(str) + "/" + df['MES'].astype(str) + "/" + df['AÑO'].astype(str) + "<br>" +
                    "<b>Hora:</b> " + df['HORA']
                )
            
            if modo_operacion == "Nodos Base":
                if not datos_mapa_tactico.empty:
                    df_render = datos_mapa_tactico.head(1000) if filtros_aplicados else datos_mapa_tactico.sample(min(800, len(datos_mapa_tactico)))
                    mapa_visual.add_trace(go.Scattergeo(
                        lon=df_render['lon'], lat=df_render['lat'], mode='markers',
                        marker=dict(size=12, color=df_render['COLOR_STR'], line=dict(width=1.5, color='rgba(255,255,255,0.8)'), opacity=0.9),
                        text=generar_tooltip(df_render), hoverinfo='text'
                    ))
                
            elif modo_operacion == "Red de Trayectorias":
                if not datos_mapa_tactico.empty:
                    df_malla = datos_mapa_tactico.sort_values(by=['AÑO', 'MES', 'DIA']).head(300)
                    for forma in df_malla['FORMA'].unique():
                        df_f = df_malla[df_malla['FORMA'] == forma]
                        if len(df_f) > 1:
                            mapa_visual.add_trace(go.Scattergeo(
                                lon=df_f['lon'].tolist(), lat=df_f['lat'].tolist(), mode='lines',
                                line=dict(width=1.5, color=df_f.iloc[0]['COLOR_STR']), opacity=0.3, hoverinfo='none'
                            ))
                    
                    mapa_visual.add_trace(go.Scattergeo(
                        lon=df_malla['lon'], lat=df_malla['lat'], mode='markers',
                        marker=dict(size=12, color=df_malla['COLOR_STR'], line=dict(width=1.5, color='rgba(255,255,255,0.8)')),
                        text=generar_tooltip(df_malla), hoverinfo='text'
                    ))
                
            elif modo_operacion == "IA Predictiva":
                if not datos_mapa_tactico.empty:
                    zonas_probabilidad = datos_mapa_tactico.groupby(['CIUDAD', 'lat', 'lon']).size().reset_index(name='conteo')
                    zonas_probabilidad = zonas_probabilidad.sort_values(by='conteo', ascending=False).head(15)
                    
                    mapa_visual.add_trace(go.Scattergeo(
                        lon=datos_mapa_tactico['lon'], lat=datos_mapa_tactico['lat'], mode='markers',
                        marker=dict(size=5, color='rgba(60,60,60,0.3)'), hoverinfo='none'
                    ))
                    
                    mapa_visual.add_trace(go.Scattergeo(
                        lon=zonas_probabilidad['lon'], lat=zonas_probabilidad['lat'], mode='markers',
                        marker=dict(size=zonas_probabilidad['conteo']*2.5 + 15, color='rgba(255, 0, 50, 0.4)', line=dict(width=2, color='rgba(255,0,0,0.8)')),
                        text="<b>[ZONA CALIENTE]</b><br>" + zonas_probabilidad['CIUDAD'] + "<br>Eventos: " + zonas_probabilidad['conteo'].astype(str), hoverinfo='text'
                    ))

            if st.session_state["simulaciones_activas"]:
                lon_s = [s['lon'] for s in st.session_state["simulaciones_activas"]]
                lat_s = [s['lat'] for s in st.session_state["simulaciones_activas"]]
                txt_s = [s['txt'] for s in st.session_state["simulaciones_activas"]]
                
                mapa_visual.add_trace(go.Scattergeo(
                    lon=lon_s, lat=lat_s, mode='markers',
                    marker=dict(size=16, color='rgba(0, 255, 136, 1)', symbol='cross', line=dict(width=2, color='rgba(255,255,255,1)')),
                    text=txt_s, hoverinfo='text'
                ))
                mapa_visual.add_trace(go.Scattergeo(
                    lon=lon_s, lat=lat_s, mode='markers',
                    marker=dict(size=40, color='rgba(0, 255, 136, 0.15)', line=dict(width=2, color='rgba(0, 255, 136, 0.6)')), hoverinfo='none'
                ))

            proyeccion = 'orthographic' if tipo_camara == "Globo 3D" else 'equirectangular'
            
            mapa_visual.update_layout(
                geo=dict(
                    projection_type=proyeccion,
                    showland=True, landcolor='#0d1117', 
                    showocean=True, oceancolor='#000000', 
                    showcountries=True, countrycolor='#1e293b', countrywidth=0.8,
                    showcoastlines=True, coastlinecolor='#1e293b', coastlinewidth=0.8,
                    bgcolor='rgba(0,0,0,0)', resolution=50
                ),
                margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', 
                height=550, showlegend=False
            )
            
            espacio_grafico.plotly_chart(mapa_visual, width='stretch', use_container_width=True)
            
    # --- INDICADORES INFERIORES TACTICOS (FILTRADOS) ---
    columna_filtro1, columna_filtro2, columna_filtro3 = st.columns(3)
    total_filtrados = len(datos_filtrados)
    df_formas_filt = datos_filtrados[~datos_filtrados['FORMA'].str.upper().isin(['DESCONOCIDO', 'NO ESPECIFICADO'])] if not datos_filtrados.empty else pd.DataFrame()
    forma_dominante_filt = df_formas_filt['FORMA'].mode().iloc[0] if not df_formas_filt.empty else "ND"
    paises_afectados = len(datos_filtrados['PAIS'].unique()) if not datos_filtrados.empty else 0

    columna_filtro1.metric("NODOS EN PANTALLA", f"{total_filtrados:,}".replace(",", "."))
    columna_filtro2.metric("TIPOLOGIA (FILTRO)", forma_dominante_filt.upper())
    columna_filtro3.metric("PAISES AFECTADOS", f"{paises_afectados:,}".replace(",", "."))
    st.markdown("---")

    # --- MODULOS OPERATIVOS ---
    with st.expander(f"REGISTROS FORENSES UAP ({len(datos_filtrados)} Nodos Detectados)", expanded=True):
        if not datos_filtrados.empty:
            columnas_tabla = ['DIA', 'MES', 'AÑO', 'HORA', 'CIUDAD', 'PAIS', 'FORMA']
            columnas_ok = [c for c in columnas_tabla if c in datos_filtrados.columns]
            
            df_tabla = datos_filtrados.sort_values(by=['AÑO','MES','DIA'], ascending=False)
            if not filtros_aplicados:
                st.info("[SISTEMA] Modo reposo. Mostrando previsualización de 100 registros recientes.")
                df_tabla = df_tabla.head(100)
            elif len(df_tabla) > 1000:
                st.warning(f"[ALERTA] Búsqueda masiva ({len(df_tabla)} resultados). Limitando visualización a 1000.")
                df_tabla = df_tabla.head(1000)
            
            st.dataframe(df_tabla[columnas_ok], use_container_width=True, hide_index=True, height=400)

    # --- PROCESADOR NLP AGATHA ---
    if DEEPSEEK_API_KEY:
        with st.expander("PROCESADOR DE TESTIMONIOS INTELIGENTE (NLP AGATHA)", expanded=False):
            ruta_testimonios = os.path.join("data", "avistamientos_testimonios.csv")
            if os.path.exists(ruta_testimonios):
                try:
                    df_nlp = pd.read_csv(ruta_testimonios, sep=None, engine='python', encoding='utf-8-sig', on_bad_lines='skip')
                    df_nlp.columns = df_nlp.columns.str.strip()
                    df_nlp['TAG'] = df_nlp['ID de Caso'].astype(str) + " | " + df_nlp['Ubicación'].astype(str)
                    
                    st.caption(f"Cargados {len(df_nlp)} testimonios detallados.")
                    caso_sel = st.selectbox("Seleccionar Expediente Testifical", df_nlp['TAG'].unique())
                    
                    if caso_sel:
                        fila = df_nlp[df_nlp['TAG'] == caso_sel].iloc[0]
                        texto_analisis = f"TESTIMONIO: {fila.get('Descripción del Fenómeno', '')}\n\nCONCLUSIÓN PREVIA: {fila.get('Conclusión del Investigador', 'N/A')}"
                        st.markdown(f"<div style='background:#0d1117; padding:15px; border-left:3px solid #a855f7; color:#cbd5e1; white-space: pre-wrap; font-size:0.9rem;'>{texto_analisis}</div>", unsafe_allow_html=True)
                        
                        if st.button("EJECUTAR ANALISIS DE INTELIGENCIA", type="primary"):
                            with st.spinner("AGATHA procesando análisis conductual..."):
                                try:
                                    cabeceras = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
                                    parametros = {
                                        "model": "deepseek-chat",
                                        "messages": [
                                            {"role": "system", "content": "Analiza el texto de este avistamiento UAP y responde estrictamente con un JSON con esta estructura exacta: {\"comportamiento\": \"...\", \"credibilidad\": \"ALTA/MEDIA/BAJA\", \"indice_anomalia\": \"0-100\", \"explicacion_probable\": \"ej. Satelites, Starlink, Globo, Cohete, Fenomeno Meteorologico, o Desconocido\"}"},
                                            {"role": "user", "content": texto_analisis}
                                        ],
                                        "response_format": {"type": "json_object"}
                                    }
                                    respuesta = requests.post("https://api.deepseek.com/v1/chat/completions", headers=cabeceras, json=parametros, timeout=25)
                                    contenido_respuesta = respuesta.json()["choices"][0]["message"]["content"]
                                    
                                    if contenido_respuesta.startswith("```"):
                                        contenido_respuesta = contenido_respuesta.split("```")[1]
                                        if contenido_respuesta.startswith("json"): contenido_respuesta = contenido_respuesta[4:]
                                    
                                    datos_ia = json.loads(contenido_respuesta.strip())
                                    
                                    st.markdown("<h4 style='color:#00d4ff; margin-top:15px;'>REPORTE DE INTELIGENCIA AGATHA</h4>", unsafe_allow_html=True)
                                    c1, c2, c3 = st.columns(3)
                                    c1.metric("INDICE ANOMALIA", f"{datos_ia.get('indice_anomalia', '0')}%")
                                    c2.metric("CONDUCTA", str(datos_ia.get('credibilidad', 'N/A')).upper())
                                    c3.metric("CONCLUSION", str(datos_ia.get('explicacion_probable', 'N/A')).upper())
                                    st.markdown(f"<div style='background:#0f172a; padding:15px; border:1px solid #1e293b; color:#cbd5e1; font-family: monospace;'>{datos_ia.get('comportamiento', 'Sin datos conductuales')}</div>", unsafe_allow_html=True)
                                except Exception as e: st.error(f"[ERROR] API: {str(e)}")
                except Exception as e: st.error(f"Error cargando testimonios: {str(e)}")
