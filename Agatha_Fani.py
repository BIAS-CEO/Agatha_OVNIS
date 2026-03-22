# ====================================================================
# ARCHIVO PRINCIPAL: Agatha_Fani.py
# SISTEMA: AGATHA Intelligent Neural Network
# MODULO: MODULO CONTACT (Fenomeno Anomalo No Identificado)
# VERSION: Opcon Ready v10.9 (Map Engine Force & Purge Button)
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

# --- CSS CORPORATIVO MATE (Flat Corporate + Colores Electricos) ---
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

h1 { 
    font-family: 'Montserrat', sans-serif !important; 
    text-transform: uppercase; 
    letter-spacing: -0.5px; 
    font-size: 2.5rem !important; 
    color: #00d4ff !important; 
    text-shadow: 0 0 15px rgba(0, 212, 255, 0.4);
    border-bottom: 1px solid #334155; 
    padding-bottom: 8px; 
    margin-bottom: 0.2rem !important;
}
h2, h3, h4 { 
    color: #e2e8f0 !important; 
    text-transform: uppercase; 
    letter-spacing: 1.5px; 
    font-family: 'Montserrat', sans-serif !important; 
    font-weight: 600 !important; 
    font-size: 1.1rem !important;
    margin-top: 0.5rem !important;
}

.cita-contact {
    font-family: 'Titillium Web', sans-serif;
    font-style: italic;
    color: #a855f7;
    font-size: 1.1rem;
    letter-spacing: 0.5px;
    margin-bottom: 1.5rem;
    text-shadow: 0 0 10px rgba(168, 85, 247, 0.3);
}

[data-testid="stMetric"] { 
    background-color: #1a1a1a !important; 
    border: 1px solid #333333 !important; 
    border-left: 3px solid #00d4ff !important; 
    padding: 12px !important; 
    border-radius: 0px !important; 
    box-shadow: none !important;
    height: 100%;
}
[data-testid="stMetricLabel"] { 
    color: #64748b !important; 
    font-size: 0.70rem !important; 
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

/* ELIMINAR HUECO ENTRE IMAGEN Y BOTON EN LAS COLUMNAS */
div[data-testid="column"] > div > div[data-testid="stVerticalBlock"] {
    gap: 0rem !important;
}

div[data-testid="stImage"] {
    margin-bottom: 0px !important; 
    width: 100% !important;
}
div[data-testid="stImage"] img {
    width: 100% !important;
    border-bottom-left-radius: 0px !important;
    border-bottom-right-radius: 0px !important;
}

div[data-testid="stButton"] {
    width: 100% !important;
    margin-top: 0px !important;
}

div[data-testid="stButton"] button {
    width: 100% !important; 
    height: auto !important;
    min-height: 40px !important;
    margin: 0 !important;
    padding: 8px 4px !important;
    border: 1px solid #333333 !important; 
    border-top: none !important; 
    background-color: #1a1a1a !important; 
    border-radius: 0px !important; 
    box-shadow: none !important;
    transition: all 0.3s ease;
    display: block !important;
}

div[data-testid="stButton"] button p {
    font-family: 'Montserrat', sans-serif !important; 
    font-weight: 600 !important; 
    text-transform: uppercase; 
    color: #00d4ff !important; 
    font-size: 0.65rem !important;
    letter-spacing: 0.5px !important;
    white-space: normal !important;
    word-wrap: break-word !important;
    overflow: visible !important;
    text-overflow: clip !important;
    line-height: 1.2 !important;
    margin: 0 !important;
    text-align: center !important;
}

div[data-testid="stButton"] button:hover { 
    border-color: #00d4ff !important; 
    border-top: 1px solid #00d4ff !important;
    background-color: #00d4ff !important; 
}
div[data-testid="stButton"] button:hover p {
    color: #0a0a0a !important; 
}

/* Boton de Pantalla de Arranque y Simulacion */
.boton-entrada div[data-testid="stButton"] button {
    border-top: 1px solid #00d4ff !important;
    border-color: #00d4ff !important;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.4) !important;
}
.boton-entrada div[data-testid="stButton"] button p {
    font-size: 1.2rem !important;
    padding: 0.5rem !important;
}

/* Boton Simular */
.boton-simular div[data-testid="stButton"] button {
    border-color: #00ff88 !important;
    border-top: 1px solid #00ff88 !important;
    box-shadow: 0 0 20px rgba(0, 255, 136, 0.3) !important;
}
.boton-simular div[data-testid="stButton"] button p {
    font-size: 0.8rem !important;
    color: #00ff88 !important;
}
.boton-simular div[data-testid="stButton"] button:hover {
    background-color: #00ff88 !important;
}

/* Boton Purgar */
.boton-purgar div[data-testid="stButton"] button {
    border-color: #ff3333 !important;
    border-top: 1px solid #ff3333 !important;
    box-shadow: 0 0 20px rgba(255, 51, 51, 0.3) !important;
}
.boton-purgar div[data-testid="stButton"] button p {
    font-size: 0.8rem !important;
    color: #ff3333 !important;
}
.boton-purgar div[data-testid="stButton"] button:hover {
    background-color: #ff3333 !important;
}

/* Contenedores de radio buttons tacticos */
div.row-widget.stRadio > div {
    flex-direction: column;
    gap: 0px;
}
div.row-widget.stRadio > div > label {
    margin-bottom: 5px;
}
</style>
"""
st.markdown(CSS_MATE, unsafe_allow_html=True)

# --- INICIALIZACION DE ESTADOS ---
if "pantalla_actual" not in st.session_state:
    st.session_state["pantalla_actual"] = "portada"

if "reportes_ciudadanos" not in st.session_state:
    st.session_state["reportes_ciudadanos"] = []
    
if "simulaciones_activas" not in st.session_state:
    st.session_state["simulaciones_activas"] = []

# --- FUNCIONES NUCLEO GLOBALES ---

def normalizar_miniatura(ruta_imagen, tamaño=(300, 300)):
    try:
        img = Image.open(ruta_imagen).convert("RGBA")
        img.thumbnail(tamaño, Image.Resampling.LANCZOS)
        fondo = Image.new('RGBA', tamaño, (10, 10, 10, 0)) 
        desplazamiento = (int((tamaño[0] - img.width) / 2), int((tamaño[1] - img.height) / 2))
        fondo.paste(img, desplazamiento)
        return fondo
    except Exception:
        return None

@st.dialog("VISOR TACTICO UAP", width="large")
def abrir_visor_completo(nombre_forma_archivo):
    ruta_completa = os.path.join("assets", f"{nombre_forma_archivo}_completo.png")
    if os.path.exists(ruta_completa):
        try:
            st.image(ruta_completa, use_container_width=True)
        except Exception:
            st.error("[ERROR SISTEMA] El archivo de imagen detallada esta corrupto o no es valido.")
    else:
        st.error(f"[ERROR ARCHIVO] Falta el archivo de detalle: {ruta_completa}")

def obtener_credencial(nombre_var):
    try:
        if hasattr(st, "secrets") and nombre_var in st.secrets:
            return st.secrets[nombre_var]
    except Exception:
        pass
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
        "EEUU": (39.8, -98.5), "ESTADOS UNIDOS": (39.8, -98.5), "USA": (39.8, -98.5),
        "CANADA": (56.1, -106.3), "CANADÁ": (56.1, -106.3),
        "MEXICO": (23.6, -102.5), "MÉXICO": (23.6, -102.5),
        "UK": (55.3, -3.4), "REINO UNIDO": (55.3, -3.4), "INGLATERRA": (52.3, -1.1),
        "ESPAÑA": (40.46, -3.75), "ESPANA": (40.46, -3.75), "SPAIN": (40.46, -3.75),
        "FRANCIA": (46.22, 2.21), "ALEMANIA": (51.16, 10.45), "ITALIA": (41.87, 12.56),
        "INDIA": (20.59, 78.96), "CHINA": (35.86, 104.19), "JAPON": (36.20, 138.25), "JAPÓN": (36.20, 138.25),
        "AUSTRALIA": (-25.27, 133.77), "BRASIL": (-14.23, -51.92), "ARGENTINA": (-38.41, -63.61)
    }
    
    est = df.get('ESTADO', pd.Series(index=df.index)).astype(str).str.upper().str.strip()
    pai = df['PAIS'].astype(str).str.upper().str.strip()
    
    coord_est = est.map(centroides)
    coord_pai = pai.map(centroides)
    
    coords_finales = coord_est.combine_first(coord_pai)
    
    def coords_seguras(row_hash):
        return (((row_hash % 130) - 60), ((row_hash % 240) - 120))
        
    df['hash_val'] = df['CIUDAD'].astype(str).apply(lambda x: sum(ord(c) for c in x) if pd.notna(x) else 0)
    coordenadas_respaldo = df['hash_val'].apply(coords_seguras)
    
    coords_finales = coords_finales.combine_first(pd.Series([(c[0], c[1]) for c in coordenadas_respaldo], index=df.index))
    
    df['lat_offset'] = ((df['hash_val'] % 100) - 50) / 100.0 * 1.5
    df['lon_offset'] = (((df['hash_val'] // 10) % 100) - 50) / 100.0 * 1.5
    
    df['lat'] = coords_finales.apply(lambda x: x[0]) + df['lat_offset']
    df['lon'] = coords_finales.apply(lambda x: x[1]) + df['lon_offset']
    
    df = df.drop(columns=['hash_val', 'lat_offset', 'lon_offset'])
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce').fillna(0.0)
    df['lon'] = pd.to_numeric(df['lon'], errors='coerce').fillna(0.0)
    
    return df
    
@st.cache_data(show_spinner=False)
def cargar_nodos():
    mensajes = []
    ruta_carpeta = "data"
    dfs = []
    
    if os.path.exists(ruta_carpeta):
        for archivo in os.listdir(ruta_carpeta):
            if archivo.endswith(".csv") and "avistamientos_testimonios" not in archivo.lower() and "relationships" not in archivo.lower():
                try:
                    temp_df = pd.read_csv(os.path.join(ruta_carpeta, archivo), sep=None, engine='python', encoding='utf-8-sig', on_bad_lines='skip')
                    dfs.append(temp_df)
                except Exception:
                    pass
    if dfs:
        df = pd.concat(dfs, ignore_index=True)
        mensajes.append("Archivos de datos locales unificados y decodificados correctamente.")
    else:
        return pd.DataFrame(), ["[ERROR] La carpeta de datos no contiene archivos validos."]

    try:
        df.columns = df.columns.str.upper().str.strip()
        col_map = {'YEAR': 'AÑO', 'DÍA': 'DIA', 'DAY': 'DIA', 'MONTH': 'MES', 'CITY': 'CIUDAD', 'STATE': 'ESTADO', 'PAÍS': 'PAIS', 'COUNTRY': 'PAIS', 'SHAPE': 'FORMA', 'SUMMARY': 'RESUMEN', 'TIME': 'HORA'}
        df.rename(columns=col_map, inplace=True)
        df = df.loc[:, ~df.columns.duplicated()]
        
        for c in ['CIUDAD', 'PAIS', 'FORMA']:
            if c not in df.columns: df[c] = "No especificado"
            else: df[c] = df[c].fillna("No especificado").astype(str)
            
        df['PAIS'] = df['PAIS'].str.title().str.strip()
        df['FORMA'] = df['FORMA'].str.title().str.strip()
        
        if 'AÑO' not in df.columns: df['AÑO'] = 2026
        df['AÑO'] = pd.to_numeric(df['AÑO'], errors='coerce').fillna(2026).astype(int)
        if 'MES' not in df.columns: df['MES'] = "No especificado"
        df['MES'] = pd.to_numeric(df['MES'], errors='coerce').fillna(0).astype(int).astype(str).replace('0', 'No especificado')
        if 'DIA' not in df.columns: df['DIA'] = "No especificado"
        df['DIA'] = pd.to_numeric(df['DIA'], errors='coerce').fillna(0).astype(int).astype(str).replace('0', 'No especificado')
        if 'HORA' not in df.columns: df['HORA'] = "No especificada"
        
        def formatear_hora(h):
            val = str(h).strip()
            if val.lower() in ['nan', 'nat', 'none', 'null', '', 'no especificada']: return "No especificada"
            if ':' in val:
                partes = val.split(':')
                if len(partes) >= 2: return f"{partes[0].zfill(2)}:{partes[1].zfill(2)}"
            return "No especificada"

        df['HORA'] = df['HORA'].apply(formatear_hora)
        df['FORMA'] = df['FORMA'].str.title()
        df = simular_coordenadas(df)
        df['COLOR_STR'] = df['FORMA'].apply(asignar_color_neon)
        
        return df, mensajes
    except Exception as e:
        return pd.DataFrame(), [f"[ERROR] Proceso interrumpido: {str(e)}"]

@st.cache_data(show_spinner=False)
def cargar_archivo_relaciones():
    rutas_posibles = ["agatha_ufo_relationships.csv", os.path.join("data", "agatha_ufo_relationships.csv")]
    for r in rutas_posibles:
        if os.path.exists(r):
            try:
                df_rel = pd.read_csv(r, sep=None, engine='python', encoding='utf-8-sig', on_bad_lines='skip')
                return df_rel
            except Exception:
                pass
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
            try:
                st.image(ruta_panel_maestro, use_container_width=True)
            except Exception:
                st.error("[ERROR SISTEMA] La imagen 'dashboard_maestro_global.png' esta corrupta.")
        else:
            st.warning("[AVISO] No se encontro la imagen en assets/dashboard_maestro_global.png")
            
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
    
    with st.status("Estableciendo conexion segura con AGATHA...", expanded=False) as status_arranque:
        df_maestro, mensajes_diagnostico = cargar_nodos()
        status_arranque.update(label="Sistema UAP 'Unidentified Anomalous Phenomenon' en linea.", state="complete", expanded=False)

    IDENTIFICACION_OPERADOR = "DIR-74"
    NIVEL_ACCESO = "NIVEL 4 - INTELIGENCIA ESTRATEGICA"
    MARCA_TIEMPORAL = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    st.markdown(f"""
        <div style="position: fixed; top: 12px; right: 20px; background: #1a1a1a; border: 1px solid #333333; 
        color: #64748b; padding: 6px 15px; font-family: 'Share Tech Mono', monospace; font-size: 0.75rem; 
        z-index: 999999; pointer-events: none; text-transform: uppercase; letter-spacing: 0.5px;">
            Operador: {IDENTIFICACION_OPERADOR} | Acceso: {NIVEL_ACCESO} | {MARCA_TIEMPORAL}
        </div>
    """, unsafe_allow_html=True)

    columna_titulo, columna_desconexion = st.columns([4, 1])
    with columna_titulo:
        st.markdown("<h1>AGATHA Intelligent Neural Network</h1>", unsafe_allow_html=True)
        st.markdown("<h3>MODULO CONTACT - Fenomeno Anomalo No Identificado</h3>", unsafe_allow_html=True)
        st.markdown("<div class='cita-contact'>«El Universo es enorme. Y si solo estamos nosotros, cuanto espacio desaprovechado»</div>", unsafe_allow_html=True)
    with columna_desconexion:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("DESCONECTAR", type="primary"):
            st.session_state["pantalla_actual"] = "portada"
            st.rerun()

    # --- CATALOGO UAP ---
    with st.expander("CATALOGO UAP IDENTIFICACION VISUAL DE OBJETOS", expanded=False):
        st.markdown("<div style='color:#00d4ff; font-size:0.85rem; margin-bottom:15px; line-height:1.4;'>INFORMACION TACTICA: Selecciona la forma para abrir el analisis visual de reconocimiento.</div>", unsafe_allow_html=True)
        
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
                    forma_nombre_interfaz = forma_archivo.replace("_", " ").title()
                    
                    with columnas_cuadricula[j]:
                        ruta_miniatura = os.path.join("assets", f"{forma_archivo}.png")
                        
                        if os.path.exists(ruta_miniatura):
                            imagen_procesada = normalizar_miniatura(ruta_miniatura)
                            if imagen_procesada:
                                st.image(imagen_procesada, use_container_width=True)
                                if st.button(f"{forma_nombre_interfaz.upper()}", key=f"btn_{forma_archivo}", use_container_width=True):
                                    abrir_visor_completo(forma_archivo)
                            else:
                                st.markdown("<div style='width:100%; aspect-ratio:1/1; border:1px dashed #334155; display:flex; align-items:center; justify-content:center; background:#0f172a;'><span style='color:#64748b; font-size:0.6rem;'>Error de pixeles</span></div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div style='width:100%; aspect-ratio:1/1; border:1px dashed #334155; display:flex; align-items:center; justify-content:center; background:#0f172a;'><span style='color:#64748b; font-size:0.6rem;'>Falta:<br>{forma_archivo}.png</span></div>", unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True) 

    # --- NOTIFICAR AVISTAMIENTO ---
    with st.expander("NOTIFICA TU AVISTAMIENTO (Red UAP Espana / Global)", expanded=False):
        st.markdown("<p style='color: #00d4ff; font-size: 0.9rem;'>Ayuda a alimentar la base de datos de AGATHA. Tu reporte sera procesado y cruzado con otros eventos anomalos.</p>", unsafe_allow_html=True)
        
        with st.form("formulario_avistamiento", clear_on_submit=True):
            col_formulario1, col_formulario2 = st.columns(2)
            dato_fecha = col_formulario1.date_input("Fecha del contacto")
            dato_hora = col_formulario2.time_input("Hora aproximada")
            
            col_formulario3, col_formulario4 = st.columns(2)
            dato_forma = col_formulario3.selectbox("Forma del objeto", ["Luz / Flash", "Esfera / Orbe", "Triangulo / Delta", "Cigarro / Cilindro", "Cambiante", "Desconocido", "Otros"])
            dato_ciudad = col_formulario4.text_input("Ciudad y Pais")
            
            dato_descripcion = st.text_area("Descripcion detallada del comportamiento")
            
            boton_envio = st.form_submit_button("ENVIAR A LA RED NEURAL AGATHA")
            
            if boton_envio:
                if dato_ciudad and dato_descripcion:
                    st.session_state["reportes_ciudadanos"].append({
                        "FECHA": str(dato_fecha), "HORA": str(dato_hora), "FORMA": dato_forma,
                        "UBICACION": dato_ciudad, "DESCRIPCION": dato_descripcion
                    })
                    st.success("[EXITO] Avistamiento registrado correctamente. AGATHA analizara el patron de correlacion.")
                else:
                    st.error("[ERROR] Por favor, completa al menos la ubicacion y la descripcion.")

        if len(st.session_state["reportes_ciudadanos"]) > 0:
            st.markdown(f"<p style='color: #94a3b8; font-size: 0.8rem; margin-top: 10px;'>Reportes en la sesion actual: {len(st.session_state['reportes_ciudadanos'])}</p>", unsafe_allow_html=True)

    # --- PANEL TACTICO SUPERIOR ---
    st.markdown("---")
    
    columna_metrica1, columna_metrica2, columna_metrica3, columna_controles = st.columns([1, 1, 1, 1.5])
    
    total_registros_activos = len(df_maestro) if not df_maestro.empty else 0
    formas_validas_para_metrica = df_maestro[~df_maestro['FORMA'].str.upper().isin(['DESCONOCIDO', 'OTROS', 'NO ESPECIFICADO', 'UNKNOWN', 'OTHER', 'N/A', ''])] if not df_maestro.empty else pd.DataFrame()
    forma_dominante = formas_validas_para_metrica['FORMA'].mode().iloc[0] if not formas_validas_para_metrica.empty else "NO DETECTADO"
    total_zonas = len(df_maestro['CIUDAD'].unique()) if not df_maestro.empty else 0

    with columna_metrica1:
        st.metric("REGISTROS ACTIVOS (TOTALES)", f"{total_registros_activos:,}".replace(",", "."))
    with columna_metrica2:
        st.metric("TIPOLOGIA PREDOMINANTE (GLOBAL)", forma_dominante.upper())
    with columna_metrica3:
        st.metric("ZONAS DE INTERES (NODOS GLOBAL)", f"{total_zonas:,}".replace(",", "."))
    with columna_controles:
        st.markdown("<div style='background-color: #1a1a1a; padding: 12px; border: 1px solid #333; height: 100%;'>", unsafe_allow_html=True)
        col_radio1, col_radio2 = st.columns(2)
        modo_operacion = col_radio1.radio("MODO TACTICO", ["Nodos Base", "Red de Trayectorias", "IA Predictiva"])
        tipo_camara = col_radio2.radio("PROYECCION", ["Globo 3D", "Plano 2D"])
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- VISUALIZACION PRINCIPAL Y MOTORES ---
    columna_mapa, columna_filtros = st.columns([2.5, 1.5], gap="large")

    datos_filtrados = df_maestro.copy()
    filtros_aplicados = False
    
    nodos_origen_lon, nodos_origen_lat = [], []
    nodos_destino_lon, nodos_destino_lat = [], []
    
    datos_mapa_limpio = df_maestro[
        (df_maestro['PAIS'].str.upper() != 'NO ESPECIFICADO') & 
        (df_maestro['CIUDAD'].str.upper() != 'NO ESPECIFICADO')
    ]

    with columna_filtros:
        if modo_operacion == "Nodos Base":
            st.markdown("#### Parametros de Filtrado UAP")
            
            c_f1, c_f2 = st.columns(2)
            años_disponibles = sorted(df_maestro['AÑO'].unique(), reverse=True) if not df_maestro.empty else []
            seleccion_año = c_f1.selectbox("AÑO", ["TODOS"] + [int(a) for a in años_disponibles])
            
            meses_disponibles = sorted([m for m in df_maestro['MES'].unique() if m != 'No especificado'], key=lambda x: int(x)) if not df_maestro.empty else []
            seleccion_mes = c_f2.selectbox("MES", ["TODOS"] + [str(m) for m in meses_disponibles])
            
            c_f3, c_f4 = st.columns(2)
            dias_disponibles = sorted([d for d in df_maestro['DIA'].unique() if d != 'No especificado'], key=lambda x: int(x)) if not df_maestro.empty else []
            seleccion_dia = c_f3.selectbox("DIA", ["TODOS"] + [str(d) for d in dias_disponibles])
            
            horas_disponibles = sorted([h for h in df_maestro['HORA'].unique() if h != 'No especificada']) if not df_maestro.empty else []
            seleccion_hora = c_f4.selectbox("HORA", ["TODAS"] + [str(h) for h in horas_disponibles])

            formas_disponibles = sorted(df_maestro['FORMA'].unique()) if not df_maestro.empty else []
            seleccion_forma = st.selectbox("TIPO DE OBJETO", ["TODOS"] + [str(f) for f in formas_disponibles])
            
            paises_disponibles = sorted(df_maestro['PAIS'].unique()) if not df_maestro.empty else []
            seleccion_pais = st.selectbox("PAIS", ["TODOS"] + [str(p) for p in paises_disponibles])

            if seleccion_año != "TODOS": 
                datos_filtrados = datos_filtrados[datos_filtrados['AÑO'] == seleccion_año]
                filtros_aplicados = True
            if seleccion_mes != "TODOS": 
                datos_filtrados = datos_filtrados[datos_filtrados['MES'] == seleccion_mes]
                filtros_aplicados = True
            if seleccion_dia != "TODOS": 
                datos_filtrados = datos_filtrados[datos_filtrados['DIA'] == seleccion_dia]
                filtros_aplicados = True
            if seleccion_hora != "TODAS": 
                datos_filtrados = datos_filtrados[datos_filtrados['HORA'] == seleccion_hora]
                filtros_aplicados = True
            if seleccion_forma != "TODOS": 
                datos_filtrados = datos_filtrados[datos_filtrados['FORMA'] == seleccion_forma]
                filtros_aplicados = True
            if seleccion_pais != "TODOS": 
                datos_filtrados = datos_filtrados[datos_filtrados['PAIS'] == seleccion_pais]
                filtros_aplicados = True
                
            datos_mapa_limpio = datos_filtrados[
                (datos_filtrados['PAIS'].str.upper() != 'NO ESPECIFICADO') & 
                (datos_filtrados['CIUDAD'].str.upper() != 'NO ESPECIFICADO')
            ]

            st.markdown("---")
            st.markdown(f"<p style='color: #00d4ff; font-weight: 600;'>RESULTADOS DEL FILTRO: {len(datos_filtrados)} registros</p>", unsafe_allow_html=True)
            
        elif modo_operacion == "Red de Trayectorias":
            st.markdown("#### Analisis de Correlaciones UAP")
            st.markdown("<p style='color:#94a3b8; font-size:0.85rem;'>Este modulo analiza vectores de relacion tactica. Al seleccionar TODAS, el sistema agrupa los puentes por morfologia cronologica.</p>", unsafe_allow_html=True)
            
            df_relaciones = cargar_archivo_relaciones()
            
            if not df_relaciones.empty and 'Relationship_Type' in df_relaciones.columns:
                traduccion_relaciones = {
                    "Shared Strategic Context (Military/Aviation)": "Contexto Estrategico Compartido (Militar/Aviacion)",
                    "Similar Physical Anomalies": "Anomalias Fisicas Similares"
                }
                
                df_relaciones['TIPO_RELACION_ES'] = df_relaciones['Relationship_Type'].map(lambda x: traduccion_relaciones.get(x, str(x)))
                tipos_de_conexion = sorted(df_relaciones['TIPO_RELACION_ES'].unique())
                
                conexion_seleccionada = st.selectbox("VER RELACIONES", ["TODAS"] + tipos_de_conexion)
                
                if conexion_seleccionada != "TODAS":
                    df_relaciones_filtrado = df_relaciones[df_relaciones['TIPO_RELACION_ES'] == conexion_seleccionada]
                    ciudades_origen = df_relaciones_filtrado['Source_City'].dropna().astype(str).str.title().str.strip()
                    ciudades_destino = df_relaciones_filtrado['Target_City'].dropna().astype(str).str.title().str.strip()
                    todas_ciudades_implicadas = pd.concat([ciudades_origen, ciudades_destino]).unique()
                    
                    df_maestro_limpio = df_maestro.copy()
                    df_maestro_limpio['CIUDAD_LIMPIA'] = df_maestro_limpio['CIUDAD'].astype(str).str.title().str.strip()
                    datos_filtrados = df_maestro_limpio[df_maestro_limpio['CIUDAD_LIMPIA'].isin(todas_ciudades_implicadas)].copy()
                    filtros_aplicados = True
                else:
                    datos_filtrados = df_maestro.copy()
                    filtros_aplicados = False
                
                datos_mapa_limpio = datos_filtrados[
                    (datos_filtrados['PAIS'].str.upper() != 'NO ESPECIFICADO') & 
                    (datos_filtrados['CIUDAD'].str.upper() != 'NO ESPECIFICADO')
                ]
                
                st.markdown("---")
                st.markdown(f"<p style='color: #00d4ff; font-weight: 600;'>NODOS CONECTADOS: {len(datos_filtrados)} registros</p>", unsafe_allow_html=True)
            else:
                st.warning("[AVISO] No se encontraron archivos de relacion de parametros o columnas validas.")
                
        elif modo_operacion == "IA Predictiva":
            st.markdown("#### Analisis Predictivo Estocastico")
            st.markdown("<p style='color:#ff0033; font-size:0.85rem; font-weight:bold;'>[ALERTA] Calculando densidad de eventos y zonas de alta probabilidad para las proximas 72 horas.</p>", unsafe_allow_html=True)
            st.markdown("<p style='color:#94a3b8; font-size:0.85rem;'>AGATHA utiliza el historico de nodos para trazar mapas de calor probabilistico.</p>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown(f"<p style='color: #ff0033; font-weight: 600;'>ZONAS CALIENTES IDENTIFICADAS EN EL MAPA</p>", unsafe_allow_html=True)

        # BOTONES DE SIMULACION EN TODOS LOS MODOS
        st.markdown("<br>", unsafe_allow_html=True)
        col_simulacion_1, col_simulacion_2 = st.columns(2)
        with col_simulacion_1:
            st.markdown("<div class='boton-simular'>", unsafe_allow_html=True)
            if st.button("SIMULAR APARICION", use_container_width=True):
                lat_simulada = np.random.uniform(25, 55)
                lon_simulada = np.random.uniform(-125, 30)
                st.session_state["simulaciones_activas"].append({
                    'lat': lat_simulada, 
                    'lon': lon_simulada, 
                    'texto': f"<b>[SIMULACRO] CONTACTO DETECTADO</b><br>Hora: {datetime.now().strftime('%H:%M:%S')} UTC"
                })
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_simulacion_2:
            st.markdown("<div class='boton-purgar'>", unsafe_allow_html=True)
            if st.button("PURGAR RASTROS", use_container_width=True):
                st.session_state["simulaciones_activas"] = []
            st.markdown("</div>", unsafe_allow_html=True)
            
        if len(st.session_state["simulaciones_activas"]) > 0:
            st.markdown(f"<p style='color:#00ff88; font-size:0.75rem; text-align:center; margin-top:5px;'>Simulacros activos en pantalla: {len(st.session_state['simulaciones_activas'])}</p>", unsafe_allow_html=True)

    with columna_mapa:
        espacio_grafico = st.empty() 
        
        with st.spinner("Calibrando proyecciones tacticas..."):
            mapa_visual = go.Figure()
            
            texto_hover_nodos = (
                "<b>Ciudad:</b> " + datos_mapa_limpio['CIUDAD'] + "<br>" +
                "<b>País:</b> " + datos_mapa_limpio['PAIS'] + "<br>" +
                "<b>Forma:</b> " + datos_mapa_limpio['FORMA'] + "<br>" +
                "<b>Fecha:</b> " + datos_mapa_limpio['DIA'].astype(str) + "/" + datos_mapa_limpio['MES'].astype(str) + "/" + datos_mapa_limpio['AÑO'].astype(str) + "<br>" +
                "<b>Hora:</b> " + datos_mapa_limpio['HORA']
            )
            
            if modo_operacion == "Nodos Base":
                if not datos_mapa_limpio.empty:
                    datos_renderizados = datos_mapa_limpio.head(1000) if filtros_aplicados else datos_mapa_limpio.sample(min(500, len(datos_mapa_limpio)))
                    
                    texto_hover_renderizados = (
                        "<b>Ciudad:</b> " + datos_renderizados['CIUDAD'] + "<br>" +
                        "<b>País:</b> " + datos_renderizados['PAIS'] + "<br>" +
                        "<b>Forma:</b> " + datos_renderizados['FORMA'] + "<br>" +
                        "<b>Fecha:</b> " + datos_renderizados['DIA'].astype(str) + "/" + datos_renderizados['MES'].astype(str) + "/" + datos_renderizados['AÑO'].astype(str) + "<br>" +
                        "<b>Hora:</b> " + datos_renderizados['HORA']
                    )
                    
                    mapa_visual.add_trace(go.Scattergeo(
                        lon=datos_renderizados['lon'], lat=datos_renderizados['lat'], mode='markers',
                        marker=dict(size=12, color=datos_renderizados['COLOR_STR'], line=dict(width=1.5, color='rgba(255,255,255,0.8)'), opacity=0.9),
                        text=texto_hover_renderizados, hoverinfo='text'
                    ))
                
            elif modo_operacion == "Red de Trayectorias":
                if not datos_mapa_limpio.empty:
                    df_red_cronologica = datos_mapa_limpio.sort_values(by=['AÑO', 'MES', 'DIA', 'HORA']).head(300)
                    
                    # 1. FORZAR LOS PUENTES ENTRE NODOS
                    try:
                        # Diccionario rapido para emparejar Ciudad -> Coordenadas
                        dict_coords = dict(zip(datos_mapa_limpio['CIUDAD'].astype(str).str.upper().str.strip(), zip(datos_mapa_limpio['lon'], datos_mapa_limpio['lat'])))
                        
                        if 'conexion_seleccionada' in locals() and conexion_seleccionada != "TODAS" and 'df_relaciones_filtrado' in locals():
                            for _, row in df_relaciones_filtrado.iterrows():
                                c_origen = str(row.get('Source_City', '')).upper().strip()
                                c_destino = str(row.get('Target_City', '')).upper().strip()
                                
                                if c_origen in dict_coords and c_destino in dict_coords:
                                    mapa_visual.add_trace(go.Scattergeo(
                                        lon=[dict_coords[c_origen][0], dict_coords[c_destino][0]],
                                        lat=[dict_coords[c_origen][1], dict_coords[c_destino][1]],
                                        mode='lines',
                                        line=dict(width=2.5, color='rgba(0, 212, 255, 0.9)'),
                                        opacity=0.9,
                                        hoverinfo='none'
                                    ))
                        elif 'df_relaciones' in locals() and not df_relaciones.empty:
                            for _, row in df_relaciones.iterrows():
                                c_origen = str(row.get('Source_City', '')).upper().strip()
                                c_destino = str(row.get('Target_City', '')).upper().strip()
                                
                                if c_origen in dict_coords and c_destino in dict_coords:
                                    mapa_visual.add_trace(go.Scattergeo(
                                        lon=[dict_coords[c_origen][0], dict_coords[c_destino][0]],
                                        lat=[dict_coords[c_origen][1], dict_coords[c_destino][1]],
                                        mode='lines',
                                        line=dict(width=1.5, color='rgba(255, 51, 51, 0.5)'),
                                        opacity=0.6,
                                        hoverinfo='none'
                                    ))
                        else:
                            # Fallback por defecto: Traza cronologica por forma
                            formas_malla = df_red_cronologica['FORMA'].unique()
                            for forma in formas_malla:
                                df_f = df_red_cronologica[df_red_cronologica['FORMA'] == forma]
                                if len(df_f) > 1:
                                    mapa_visual.add_trace(go.Scattergeo(
                                        lon=df_f['lon'].tolist(), lat=df_f['lat'].tolist(), mode='lines',
                                        line=dict(width=1.5, color=df_f.iloc[0]['COLOR_STR']), opacity=0.35, hoverinfo='none'
                                    ))
                    except Exception as e:
                        pass # Ignorar fallos de cruce para no detener el renderizado del mapa
                    
                    # 2. DIBUJAR LOS NODOS (Superpuestos a las lineas)
                    texto_hover_red = (
                        "<b>Ciudad:</b> " + df_red_cronologica['CIUDAD'] + "<br>" +
                        "<b>País:</b> " + df_red_cronologica['PAIS'] + "<br>" +
                        "<b>Forma:</b> " + df_red_cronologica['FORMA'] + "<br>" +
                        "<b>Fecha:</b> " + df_red_cronologica['DIA'].astype(str) + "/" + df_red_cronologica['MES'].astype(str) + "/" + df_red_cronologica['AÑO'].astype(str) + "<br>" +
                        "<b>Hora:</b> " + df_red_cronologica['HORA']
                    )
                    
                    mapa_visual.add_trace(go.Scattergeo(
                        lon=df_red_cronologica['lon'], lat=df_red_cronologica['lat'], mode='markers',
                        marker=dict(size=12, color=df_red_cronologica['COLOR_STR'], line=dict(width=1.5, color='rgba(255,255,255,0.8)'), opacity=1.0),
                        text=texto_hover_red, hoverinfo='text'
                    )
                
            elif modo_operacion == "IA Predictiva":
                if not datos_mapa_limpio.empty:
                    zonas_probabilidad = datos_mapa_limpio.groupby(['CIUDAD', 'PAIS', 'lat', 'lon']).size().reset_index(name='conteo')
                    zonas_probabilidad = zonas_probabilidad.sort_values(by='conteo', ascending=False).head(10)
                    
                    mapa_visual.add_trace(go.Scattergeo(
                        lon=datos_mapa_limpio['lon'], lat=datos_mapa_limpio['lat'], mode='markers',
                        marker=dict(size=6, color='rgba(100,100,100,0.5)', line=dict(width=0.5, color='rgba(255,255,255,0.2)')), hoverinfo='none'
                    ))
                    
                    mapa_visual.add_trace(go.Scattergeo(
                        lon=zonas_probabilidad['lon'], lat=zonas_probabilidad['lat'], mode='markers',
                        marker=dict(size=zonas_probabilidad['conteo']*2 + 15, color='rgba(255, 0, 50, 0.4)', line=dict(width=2, color='rgba(255,0,0,0.8)')),
                        text="<b>[PROBABILIDAD ALTA]</b><br>Ciudad: " + zonas_probabilidad['CIUDAD'] + "<br>Histórico: " + zonas_probabilidad['conteo'].astype(str) + " eventos", hoverinfo='text'
                    ))

            # Renderizar siempre las Simulaciones Activas independientemente del modo
            if len(st.session_state["simulaciones_activas"]) > 0:
                lon_sims = [s['lon'] for s in st.session_state["simulaciones_activas"]]
                lat_sims = [s['lat'] for s in st.session_state["simulaciones_activas"]]
                txt_sims = [s['texto'] for s in st.session_state["simulaciones_activas"]]
                
                mapa_visual.add_trace(go.Scattergeo(
                    lon=lon_sims, lat=lat_sims, mode='markers',
                    marker=dict(size=16, color='rgba(0, 255, 136, 1)', symbol='cross', line=dict(width=2, color='rgba(255,255,255,1)')),
                    text=txt_sims, hoverinfo='text'
                ))
                mapa_visual.add_trace(go.Scattergeo(
                    lon=lon_sims, lat=lat_sims, mode='markers',
                    marker=dict(size=40, color='rgba(0, 255, 136, 0.3)', line=dict(width=2, color='rgba(0, 255, 136, 0.8)')),
                    hoverinfo='none'
                ))

            tipo_proyeccion_final = 'orthographic' if tipo_camara == "Globo 3D" else 'equirectangular'
            
            mapa_visual.update_layout(
                geo=dict(
                    projection_type=tipo_proyeccion_final,
                    showland=True, landcolor='#121212',
                    showocean=True, oceancolor='#050505',
                    showcountries=True, countrycolor='#2a2a2a', countrywidth=0.5,
                    showlakes=False, bgcolor='rgba(0,0,0,0)', resolution=50
                ),
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor='#0a0a0a', 
                height=450,
                showlegend=False
            )
            
            espacio_grafico.plotly_chart(mapa_visual, width='stretch')

    # --- INDICADORES RAPIDOS TACTICOS (RESULTADOS FILTRADOS) ---
    columna_filtro1, columna_filtro2, columna_filtro3 = st.columns(3)
    
    total_datos_filtrados = len(datos_filtrados)
    formas_validas_filtro = datos_filtrados[~datos_filtrados['FORMA'].str.upper().isin(['DESCONOCIDO', 'OTROS', 'NO ESPECIFICADO', 'UNKNOWN', 'OTHER', 'N/A', ''])] if not datos_filtrados.empty else pd.DataFrame()
    forma_dominante_filtro = formas_validas_filtro['FORMA'].mode().iloc[0] if not formas_validas_filtro.empty else "NO DETECTADO"
    zonas_afectadas = len(datos_filtrados['CIUDAD'].unique()) if not datos_filtrados.empty else 0

    columna_filtro1.metric("REGISTROS UAP (EN PANTALLA)", f"{total_datos_filtrados:,}".replace(",", "."))
    columna_filtro2.metric("TIPOLOGIA PREDOMINANTE (EN PANTALLA)", forma_dominante_filtro.upper())
    columna_filtro3.metric("ZONAS AFECTADAS (EN PANTALLA)", f"{zonas_afectadas:,}".replace(",", "."))
    st.markdown("---")

    # --- MODULOS OPERATIVOS (DESPLEGABLES) ---

    with st.expander(f"REGISTROS FORENSES ({len(datos_filtrados)} Activos detectados)", expanded=True):
        if not datos_filtrados.empty:
            columnas_requeridas = ['DIA', 'MES', 'AÑO', 'HORA', 'CIUDAD', 'PAIS', 'FORMA']
            columnas_existentes = [c for c in columnas_requeridas if c in datos_filtrados.columns]
            
            if not filtros_aplicados:
                st.info("[SISTEMA] Sistema en reposo. Mostrando previsualizacion de los 100 registros mas recientes.")
                datos_a_mostrar = datos_filtrados.sort_values(by=['AÑO','MES','DIA','HORA'], ascending=[False, False, False, False]).head(100)
            else:
                if len(datos_filtrados) > 1000:
                    st.warning(f"[ALERTA] Busqueda masiva detectada ({len(datos_filtrados)} resultados). Mostrando los 1000 mas relevantes para garantizar la estabilidad del sistema.")
                    datos_a_mostrar = datos_filtrados.sort_values(by=['AÑO','MES','DIA','HORA'], ascending=[False, False, False, False]).head(1000)
                else:
                    datos_a_mostrar = datos_filtrados.sort_values(by=['AÑO','MES','DIA','HORA'], ascending=[False, False, False, False])
            
            datos_a_mostrar = datos_a_mostrar[columnas_existentes].copy()
            renombres_ui = {'DIA': 'DÍA', 'PAIS': 'PAÍS'}
            datos_a_mostrar.rename(columns=renombres_ui, inplace=True)
            
            try:
                datos_estilizados = datos_a_mostrar.style.set_properties(**{
                    'background-color': '#0a0a0a',
                    'color': '#cbd5e1',
                    'border-color': '#333333'
                })
                st.dataframe(datos_estilizados, width='stretch', hide_index=True, height=400)
            except Exception:
                st.dataframe(datos_a_mostrar, width='stretch', hide_index=True, height=400)

    # --- PROCESADOR NLP FORENSE DE AGATHA ---
    with st.expander("PROCESADOR NLP FORENSE", expanded=False):
        
        ruta_archivo_testimonios_1 = os.path.join("data", "avistamientos_testimonios.csv")
        ruta_archivo_testimonios_2 = "avistamientos_testimonios.csv"
        datos_procesamiento_nlp = pd.DataFrame()
        
        if os.path.exists(ruta_archivo_testimonios_1):
            datos_procesamiento_nlp = pd.read_csv(ruta_archivo_testimonios_1, sep=None, engine='python', encoding='utf-8-sig', on_bad_lines='skip')
        elif os.path.exists(ruta_archivo_testimonios_2):
            datos_procesamiento_nlp = pd.read_csv(ruta_archivo_testimonios_2, sep=None, engine='python', encoding='utf-8-sig', on_bad_lines='skip')
            
        if not datos_procesamiento_nlp.empty:
            datos_procesamiento_nlp.columns = datos_procesamiento_nlp.columns.str.strip()
            
            def generar_etiqueta(fila):
                identificador = str(fila.get('ID de Caso', 'N/A'))
                lugar = str(fila.get('Ubicación', 'N/A'))
                fecha_avistamiento = str(fila.get('Fecha/Hora', 'N/A'))
                return f"{identificador} | {lugar} | {fecha_avistamiento}"
            
            datos_procesamiento_nlp['ETIQUETA'] = datos_procesamiento_nlp.apply(generar_etiqueta, axis=1)
            opciones_disponibles = datos_procesamiento_nlp['ETIQUETA'].unique()
            
            st.caption(f"Cargados {len(datos_procesamiento_nlp)} expedientes testificales detallados.")
            expediente_elegido = st.selectbox("Seleccionar Expediente Testifical UAP", opciones_disponibles, key="select_nlp")
            
            if expediente_elegido:
                fila_elegida = datos_procesamiento_nlp[datos_procesamiento_nlp['ETIQUETA'] == expediente_elegido].iloc[0]
                texto_descripcion = str(fila_elegida.get('Descripción del Fenómeno', 'Sin descripcion detallada.'))
                texto_conclusion = str(fila_elegida.get('Conclusión del Investigador', ''))
                
                texto_final_analisis = f"DESCRIPCION DEL TESTIGO: {texto_descripcion}"
                if texto_conclusion and texto_conclusion.lower() != 'nan':
                    texto_final_analisis += f"\n\nCONCLUSION PREVIA: {texto_conclusion}"
                
                st.markdown(f"<div style='background:#1a1a1a; padding:15px; border-left:3px solid #a855f7; color:#e2e8f0; white-space: pre-wrap;'>{texto_final_analisis}</div><br>", unsafe_allow_html=True)
                
                if st.button("Ejecutar Analisis de Inteligencia AGATHA", type="primary"):
                    if DEEPSEEK_API_KEY:
                        with st.spinner("AGATHA procesando analisis conductual..."):
                            try:
                                cabeceras = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
                                parametros = {
                                    "model": "deepseek-chat",
                                    "messages": [
                                        {"role": "system", "content": "Analiza el texto de este avistamiento UAP y responde estrictamente con un JSON con esta estructura exacta: {\"comportamiento\": \"...\", \"credibilidad\": \"ALTA/MEDIA/BAJA\", \"indice_anomalia\": \"0-100\", \"explicacion_probable\": \"ej. Satelites, Starlink, Globo, Cohete, Fenomeno Meteorologico, o Desconocido\"}"},
                                        {"role": "user", "content": texto_final_analisis}
                                    ],
                                    "response_format": {"type": "json_object"}
                                }
                                respuesta = requests.post("https://api.deepseek.com/v1/chat/completions", headers=cabeceras, json=parametros, timeout=25)
                                contenido_respuesta = respuesta.json()["choices"][0]["message"]["content"]
                                
                                if contenido_respuesta.startswith("```"):
                                    contenido_respuesta = contenido_respuesta.split("```")[1]
                                    if contenido_respuesta.startswith("json"): contenido_respuesta = contenido_respuesta[4:]
                                
                                datos_extraidos_nlp = json.loads(contenido_respuesta.strip())
                                
                                st.markdown("<h4 style='color:#00d4ff; margin-top:20px; border-bottom:1px solid #333; padding-bottom:5px;'>REPORTE TACTICO DE INTELIGENCIA</h4>", unsafe_allow_html=True)
                                
                                col_analisis1, col_analisis2, col_analisis3 = st.columns(3)
                                col_analisis1.metric("INDICE DE ANOMALIA", f"{datos_extraidos_nlp.get('indice_anomalia', '0')}%")
                                col_analisis2.metric("CREDIBILIDAD DEL REPORTE", str(datos_extraidos_nlp.get('credibilidad', 'N/A')).upper())
                                col_analisis3.metric("EXPLICACION PROBABLE", str(datos_extraidos_nlp.get('explicacion_probable', 'N/A')).upper())
                                
                                st.markdown("<br><span style='color:#94a3b8; font-weight:600; letter-spacing:1px;'>ANALISIS CINEMATICO Y CONDUCTUAL:</span>", unsafe_allow_html=True)
                                st.markdown(f"<div style='background:#0f172a; padding:15px; border:1px solid #1e293b; color:#cbd5e1; font-family: monospace;'>{datos_extraidos_nlp.get('comportamiento', 'Sin datos conductuales extraidos.')}</div>", unsafe_allow_html=True)

                            except Exception as e:
                                st.error(f"[ERROR SISTEMA] Fallo interno en los circuitos de AGATHA: {str(e)}")
                    else:
                        st.warning("[AVISO] Falta credencial de procesamiento neuronal en la configuracion del sistema.")
        else:
            st.warning("[AVISO] No se encontro el archivo 'avistamientos_testimonios.csv'. Por favor, suba el archivo al directorio raiz o a la carpeta 'data' para activar el analisis forense.")
