# ====================================================================
# ARCHIVO PRINCIPAL: Agatha_Fani.py
# SISTEMA: AGATHA Intelligent Neural Network
# MODULO: MODULO CONTACT (Fenomeno Anomalo No Identificado)
# VERSION: Opcon Ready v9.1 (Ajustes de UI sin iconos)
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
    page_title="AGATHA - Intelligent Neural Network",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS CORPORATIVO MATE (Flat Corporate + Colores Eléctricos) ---
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
}
[data-testid="stMetricLabel"] { 
    color: #64748b !important; 
    font-size: 0.75rem !important; 
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

.stButton > button { 
    border: 1px solid #333333 !important; 
    background-color: #1a1a1a !important; 
    color: #00d4ff !important; 
    border-radius: 0px !important; 
    font-family: 'Montserrat', sans-serif !important; 
    font-weight: 600 !important; 
    text-transform: uppercase; 
    font-size: 0.85rem !important;
    letter-spacing: 1px;
    padding: 0.8rem 1.5rem !important; 
    box-shadow: 0 0 10px rgba(0, 212, 255, 0.2) !important;
    transition: all 0.3s ease;
    width: 100%;
}
.stButton > button:hover { 
    border-color: #00d4ff !important; 
    color: #0a0a0a !important; 
    background-color: #00d4ff !important; 
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.6) !important;
}

/* Estilo específico para el botón de entrada gigante */
.boton-entrada > div > div > button {
    font-size: 1.2rem !important;
    padding: 1.2rem !important;
    border-color: #00d4ff !important;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.4) !important;
}
</style>
"""
st.markdown(CSS_MATE, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE ESTADOS (Manejo de Pantallas) ---
if "pantalla_actual" not in st.session_state:
    st.session_state["pantalla_actual"] = "portada"

if "reportes_ciudadanos" not in st.session_state:
    st.session_state["reportes_ciudadanos"] = []

# --- FUNCIONES NÚCLEO GLOBALES ---
@st.dialog("VISOR TÁCTICO UAP", width="large")
def abrir_visor_completo(nombre_forma_archivo):
    ruta_completa = os.path.join("assets", f"{nombre_forma_archivo}_completo.png")
    if os.path.exists(ruta_completa):
        try:
            st.image(ruta_completa, use_container_width=True)
        except Exception:
            st.error("El archivo de imagen detallada está corrupto o no es válido.")
    else:
        st.error(f"Falta el archivo de detalle: {ruta_completa}")

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
    fallback_coords = df['hash_val'].apply(coords_seguras)
    
    coords_finales = coords_finales.combine_first(pd.Series([(c[0], c[1]) for c in fallback_coords], index=df.index))
    
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
            if archivo.endswith(".csv"):
                try:
                    temp_df = pd.read_csv(os.path.join(ruta_carpeta, archivo), sep=None, engine='python', encoding='utf-8-sig', on_bad_lines='skip')
                    dfs.append(temp_df)
                except Exception:
                    pass
    if dfs:
        df = pd.concat(dfs, ignore_index=True)
        mensajes.append("Archivos de datos locales unificados y decodificados correctamente.")
    else:
        return pd.DataFrame(), ["Error: La carpeta de datos no contiene archivos válidos."]

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
        return pd.DataFrame(), [f"Error de proceso: {str(e)}"]

# ====================================================================
# PANTALLA 1: PORTADA / SPLASH SCREEN
# ====================================================================
if st.session_state["pantalla_actual"] == "portada":
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Cargar imagen central
    ruta_dashboard = os.path.join("assets", "dashboard_maestro_global.png")
    col_img1, col_img2, col_img3 = st.columns([1, 6, 1])
    with col_img2:
        if os.path.exists(ruta_dashboard):
            try:
                st.image(ruta_dashboard, use_container_width=True)
            except Exception:
                st.error("La imagen 'dashboard_maestro_global.png' está corrupta y no se puede cargar.")
        else:
            st.warning("No se encontró la imagen en assets/dashboard_maestro_global.png")
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Botón de acceso gigante
    col_btn1, col_btn2, col_btn3 = st.columns([2, 3, 2])
    with col_btn2:
        st.markdown("<div class='boton-entrada'>", unsafe_allow_html=True)
        if st.button("ACCEDER A AGATHA INTELLIGENT NEURAL NETWORK", type="primary"):
            st.session_state["pantalla_actual"] = "principal"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ====================================================================
# PANTALLA 2: INTERFAZ PRINCIPAL TÁCTICA
# ====================================================================
elif st.session_state["pantalla_actual"] == "principal":
    
    # --- SECUENCIA DE CARGA AL ENTRAR ---
    with st.status("Estableciendo conexión segura con AGATHA...", expanded=False) as status_boot:
        df_maestro, diagn_mensajes = cargar_nodos()
        status_boot.update(label="Sistema UAP 'Unidentified Anomalous Phenomenon' en línea.", state="complete", expanded=False)

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

    # --- CABECERA TÁCTICA ---
    col_titulo, col_boton = st.columns([4, 1])
    with col_titulo:
        st.markdown("<h1>AGATHA Intelligent Neural Network</h1>", unsafe_allow_html=True)
        st.markdown("<h3>MÓDULO CONTACT - Fenómeno Anómalo No Identificado</h3>", unsafe_allow_html=True)
        st.markdown("<div class='cita-contact'>«El Universo es enorme. Y si solo estamos nosotros, cuánto espacio desaprovechado»</div>", unsafe_allow_html=True)
    with col_boton:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("DESCONECTAR", type="primary"):
            st.session_state["pantalla_actual"] = "portada"
            st.rerun()

    # --- CATÁLOGO UAP (GRID 6x4 INTERACTIVO CON FIX DE NOMBRES) ---
    with st.expander("CATÁLOGO UAP IDENTIFICACIÓN VISUAL DE OBJETOS", expanded=False):
        st.markdown("<div style='color:#00d4ff; font-size:0.85rem; margin-bottom:15px; line-height:1.4;'>Selecciona 'AMPLIAR FICHA' en cualquier tipología para abrir el análisis táctico de reconocimiento.</div>", unsafe_allow_html=True)
        
        lista_archivos_formas = [
            "bola_de_fuego", "cambiante", "cigarro", "cilindro", "circulo", "cono",
            "cruz", "cubo", "desconocido", "diamante", "disco", "esfera",
            "estrella", "flash", "formacion", "galones", "huevo", "lagrima",
            "luz", "orbe", "otros", "oval", "rectangulo", "triangulo"
        ]
        
        for i in range(0, 24, 6):
            cols = st.columns(6)
            for j in range(6):
                idx = i + j
                if idx < len(lista_archivos_formas):
                    forma_archivo = lista_archivos_formas[idx]
                    forma_nombre_ui = forma_archivo.replace("_", " ").title()
                    
                    with cols[j]:
                        ruta_thumb = os.path.join("assets", f"{forma_archivo}.png")
                        
                        if os.path.exists(ruta_thumb):
                            try:
                                st.image(ruta_thumb, use_container_width=True)
                                if st.button(f"FICHA: {forma_nombre_ui.upper()}", key=f"btn_{forma_archivo}"):
                                    abrir_visor_completo(forma_archivo)
                            except Exception:
                                st.markdown(f"<div style='width:100%; aspect-ratio:1/1; border:1px dashed #334155; display:flex; align-items:center; justify-content:center; background:#0f172a; margin-bottom:10px;'><span style='color:#64748b; font-size:0.6rem; text-align:center;'>Error formato:<br>{forma_archivo}.png</span></div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div style='width:100%; aspect-ratio:1/1; border:1px dashed #334155; display:flex; align-items:center; justify-content:center; background:#0f172a; margin-bottom:10px;'><span style='color:#64748b; font-size:0.6rem; text-align:center;'>Falta:<br>{forma_archivo}.png</span></div>", unsafe_allow_html=True)

    # --- NOTIFICAR AVISTAMIENTO ---
    with st.expander("NOTIFICA TU AVISTAMIENTO (Red UAP España / Global)", expanded=False):
        st.markdown("<p style='color: #00d4ff; font-size: 0.9rem;'>Ayuda a alimentar la base de datos de AGATHA. Tu reporte será procesado y cruzado con otros eventos anómalos.</p>", unsafe_allow_html=True)
        
        with st.form("form_avistamiento", clear_on_submit=True):
            c_f1, c_f2 = st.columns(2)
            f_fecha = c_f1.date_input("Fecha del contacto")
            f_hora = c_f2.time_input("Hora aproximada")
            
            c_f3, c_f4 = st.columns(2)
            f_forma = c_f3.selectbox("Forma del objeto", ["Luz / Flash", "Esfera / Orbe", "Triángulo / Delta", "Cigarro / Cilindro", "Cambiante", "Desconocido", "Otros"])
            f_ciudad = c_f4.text_input("Ciudad y País")
            
            f_desc = st.text_area("Descripción detallada del comportamiento")
            
            submit_btn = st.form_submit_button("ENVIAR A LA RED NEURAL AGATHA")
            
            if submit_btn:
                if f_ciudad and f_desc:
                    st.session_state["reportes_ciudadanos"].append({
                        "FECHA": str(f_fecha), "HORA": str(f_hora), "FORMA": f_forma,
                        "UBICACION": f_ciudad, "DESCRIPCION": f_desc
                    })
                    st.success("Avistamiento registrado correctamente. AGATHA analizará el patrón de correlación.")
                else:
                    st.error("Por favor, completa al menos la ubicación y la descripción para procesar el reporte.")

        if len(st.session_state["reportes_ciudadanos"]) > 0:
            st.markdown(f"<p style='color: #94a3b8; font-size: 0.8rem; margin-top: 10px;'>Reportes en la sesión actual: {len(st.session_state['reportes_ciudadanos'])}</p>", unsafe_allow_html=True)

    # --- VISUALIZACION PRINCIPAL: MAPA Y FILTROS ---
    st.markdown("---")
    col_mapa, col_filtros = st.columns([2.5, 1.5], gap="large")

    with col_filtros:
        st.markdown("#### Parámetros de Filtrado UAP")
        
        c_f1, c_f2 = st.columns(2)
        anio_disp = sorted(df_maestro['AÑO'].unique(), reverse=True) if not df_maestro.empty else []
        sel_anio = c_f1.selectbox("AÑO", ["TODOS"] + [int(a) for a in anio_disp])
        
        mes_disp = sorted([m for m in df_maestro['MES'].unique() if m != 'No especificado'], key=lambda x: int(x)) if not df_maestro.empty else []
        sel_mes = c_f2.selectbox("MES", ["TODOS"] + [str(m) for m in mes_disp])
        
        c_f3, c_f4 = st.columns(2)
        dia_disp = sorted([d for d in df_maestro['DIA'].unique() if d != 'No especificado'], key=lambda x: int(x)) if not df_maestro.empty else []
        sel_dia = c_f3.selectbox("DÍA", ["TODOS"] + [str(d) for d in dia_disp])
        
        hora_disp = sorted([h for h in df_maestro['HORA'].unique() if h != 'No especificada']) if not df_maestro.empty else []
        sel_hora = c_f4.selectbox("HORA", ["TODAS"] + [str(h) for h in hora_disp])

        forma_disp = sorted(df_maestro['FORMA'].unique()) if not df_maestro.empty else []
        sel_forma = st.selectbox("TIPO DE OBJETO", ["TODOS"] + [str(f) for f in forma_disp])
        
        pais_disp = sorted(df_maestro['PAIS'].unique()) if not df_maestro.empty else []
        sel_pais = st.selectbox("PAÍS", ["TODOS"] + [str(p) for p in pais_disp])

        df_filtrado = df_maestro.copy()
        filtros_activos = False
        
        if sel_anio != "TODOS": 
            df_filtrado = df_filtrado[df_filtrado['AÑO'] == sel_anio]
            filtros_activos = True
        if sel_mes != "TODOS": 
            df_filtrado = df_filtrado[df_filtrado['MES'] == sel_mes]
            filtros_activos = True
        if sel_dia != "TODOS": 
            df_filtrado = df_filtrado[df_filtrado['DIA'] == sel_dia]
            filtros_activos = True
        if sel_hora != "TODAS": 
            df_filtrado = df_filtrado[df_filtrado['HORA'] == sel_hora]
            filtros_activos = True
        if sel_forma != "TODOS": 
            df_filtrado = df_filtrado[df_filtrado['FORMA'] == sel_forma]
            filtros_activos = True
        if sel_pais != "TODOS": 
            df_filtrado = df_filtrado[df_filtrado['PAIS'] == sel_pais]
            filtros_activos = True

    with col_mapa:
        c_m1, c_m2 = st.columns(2)
        modo_visor = c_m1.radio("MODO TÁCTICO", ["Nodos Base", "Red de Trayectorias"], horizontal=True)
        tipo_proyeccion = c_m2.radio("PROYECCIÓN", ["Globo 3D", "Plano 2D"], horizontal=True)
        
        if not df_filtrado.empty:
            grafico_placeholder = st.empty() 
            
            with st.spinner("Calibrando proyecciones UAP..."):
                fig = go.Figure()
                
                if modo_visor == "Nodos Base":
                    df_mapa = df_filtrado.head(1000) if filtros_activos else df_filtrado.sample(min(500, len(df_filtrado)))
                    
                    fig.add_trace(go.Scattergeo(
                        lon=df_mapa['lon'], lat=df_mapa['lat'], mode='markers',
                        marker=dict(size=6, color=df_mapa['COLOR_STR'], line=dict(width=0.5, color='rgba(255,255,255,0.3)'), opacity=0.9),
                        text=df_mapa['CIUDAD'] + " | " + df_mapa['DIA'].astype(str) + "/" + df_mapa['MES'].astype(str) + " " + df_mapa['HORA'] + " (" + df_mapa['FORMA'] + ")", hoverinfo='text'
                    ))
                else:
                    if len(df_filtrado) < 2:
                        st.warning("Se requieren al menos 2 registros tácticos para trazar corredores de vuelo.")
                    else:
                        df_red = df_filtrado.sort_values(by=['AÑO', 'MES', 'DIA', 'HORA']).head(200)
                        formas_presentes = df_red['FORMA'].unique()
                        formas_validas = [f for f in formas_presentes if len(df_red[df_red['FORMA'] == f]) > 1]
                        
                        for forma in formas_validas:
                            df_forma = df_red[df_red['FORMA'] == forma]
                            fig.add_trace(go.Scattergeo(
                                lon=df_forma['lon'].tolist(), lat=df_forma['lat'].tolist(), mode='lines',
                                line=dict(width=1.5, color=df_forma.iloc[0]['COLOR_STR']), opacity=0.35, hoverinfo='none'
                            ))
                        
                        fig.add_trace(go.Scattergeo(
                            lon=df_red['lon'], lat=df_red['lat'], mode='markers',
                            marker=dict(size=6, color=df_red['COLOR_STR'], line=dict(width=0.5, color='rgba(255,255,255,0.8)'), opacity=1.0),
                            text=df_red['CIUDAD'] + " | " + df_red['DIA'].astype(str) + "/" + df_red['MES'].astype(str) + " " + df_red['HORA'] + " (" + df_red['FORMA'] + ")",
                            hoverinfo='text'
                        ))

                proj_type = 'orthographic' if tipo_proyeccion == "Globo 3D" else 'equirectangular'
                
                fig.update_layout(
                    geo=dict(
                        projection_type=proj_type,
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
                
                grafico_placeholder.plotly_chart(fig, width='stretch')
                
                if modo_visor == "Red de Trayectorias" and len(df_filtrado) >= 2:
                    if 'formas_validas' in locals() and len(formas_validas) > 0:
                        with st.expander(f"LEYENDA TACTICA: ANALISIS DE CORREDORES ({len(formas_validas)} detectados)", expanded=False):
                            sel_corredor = st.selectbox("Seleccionar vector morfologico para analisis detallado", formas_validas)
                            
                            df_ruta = df_red[df_red['FORMA'] == sel_corredor].sort_values(by=['AÑO', 'MES', 'DIA', 'HORA'])
                            nodo_inicio = df_ruta.iloc[0]
                            nodo_fin = df_ruta.iloc[-1]
                            paises_cruzados = len(df_ruta['PAIS'].unique())
                            
                            st.markdown(f"**ANALISIS DE TRAYECTORIA: TIPO {sel_corredor.upper()}**")
                            st.markdown(f"- **Nodos interconectados:** {len(df_ruta)}")
                            st.markdown(f"- **Origen de la secuencia:** {nodo_inicio['CIUDAD']} ({nodo_inicio['PAIS']}) | Fecha: {nodo_inicio['DIA']}/{nodo_inicio['MES']}/{nodo_inicio['AÑO']} a las {nodo_inicio['HORA']}")
                            st.markdown(f"- **Ultimo contacto:** {nodo_fin['CIUDAD']} ({nodo_fin['PAIS']}) | Fecha: {nodo_fin['DIA']}/{nodo_fin['MES']}/{nodo_fin['AÑO']} a las {nodo_fin['HORA']}")
                            
                            st.info(f"Reporte Conductual: Se ha detectado un desplazamiento a traves de {paises_cruzados} fronteras nacionales. La correlacion temporal sugiere un barrido topografico o una ruta de observacion secuencial.")

    # --- INDICADORES RAPIDOS TACTICOS ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Registros UAP Activos", f"{len(df_filtrado):,}")
    m2.metric("Tipología Predominante", df_filtrado['FORMA'].mode().iloc[0] if not df_filtrado.empty else "N/A")
    m3.metric("Zonas de Interés", f"{len(df_filtrado['CIUDAD'].unique()) if not df_filtrado.empty else 0:,}")
    st.markdown("---")

    # --- MODULOS OPERATIVOS (DESPLEGABLES) ---

    with st.expander(f"REGISTROS FORENSES ({len(df_filtrado)} Activos)", expanded=True):
        if not df_filtrado.empty:
            cols_excluir = ['COLOR_STR', 'lat', 'lon', 'DECADA', 'ORD.', 'NUM.', 'Source_File']
            cols_vis = list(dict.fromkeys([c for c in df_filtrado.columns if c not in cols_excluir]))
            
            if not filtros_activos:
                st.info("Sistema en reposo. Mostrando previsualización de los 100 registros más recientes. Active los filtros tácticos para una búsqueda específica.")
                df_mostrar = df_filtrado.sort_values(by=['AÑO','MES','DIA','HORA'], ascending=[False, False, False, False]).head(100)
            else:
                if len(df_filtrado) > 1000:
                    st.warning(f"Búsqueda masiva detectada ({len(df_filtrado)} resultados). Mostrando los 1000 más relevantes para garantizar la estabilidad del sistema.")
                    df_mostrar = df_filtrado.sort_values(by=['AÑO','MES','DIA','HORA'], ascending=[False, False, False, False]).head(1000)
                else:
                    df_mostrar = df_filtrado.sort_values(by=['AÑO','MES','DIA','HORA'], ascending=[False, False, False, False])
            
            try:
                df_estilizado = df_mostrar[cols_vis].style.set_properties(**{
                    'background-color': '#0a0a0a',
                    'color': '#cbd5e1',
                    'border-color': '#333333'
                })
                st.dataframe(df_estilizado, width='stretch', hide_index=True, height=400)
            except Exception:
                st.dataframe(df_mostrar[cols_vis], width='stretch', hide_index=True, height=400)

    with st.expander("PROCESADOR NLP FORENSE", expanded=False):
        if not df_filtrado.empty and 'RESUMEN' in df_filtrado.columns:
            df_nlp = df_filtrado.copy()
            df_nlp['TAG'] = df_nlp['CIUDAD'] + " | " + df_nlp['FORMA'] + " | " + df_nlp['AÑO'].astype(str)
            
            opciones_tag = df_nlp['TAG'].unique()
            if len(opciones_tag) > 500:
                st.caption("Mostrando los 500 expedientes más recientes para análisis NLP.")
                opciones_tag = opciones_tag[:500]
                
            caso_sel = st.selectbox("Seleccionar Expediente Forense UAP", opciones_tag, key="select_nlp")
            
            if caso_sel:
                resumen = str(df_nlp[df_nlp['TAG'] == caso_sel].iloc[0].get('RESUMEN', 'Sin resumen disponible.'))
                st.markdown(f"<div style='background:#1a1a1a; padding:15px; border-left:3px solid #a855f7; color:#e2e8f0;'>{resumen}</div><br>", unsafe_allow_html=True)
                
                if st.button("Ejecutar Análisis de Inteligencia AGATHA", type="primary"):
                    if DEEPSEEK_API_KEY:
                        with st.spinner("AGATHA procesando análisis conductual..."):
                            try:
                                h = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
                                p = {
                                    "model": "deepseek-chat",
                                    "messages": [
                                        {"role": "system", "content": "Analiza el texto de este avistamiento UAP y responde estrictamente con un JSON con esta estructura: {comportamiento: '...', credibilidad: 'ALTA/MEDIA/BAJA', indice_anomalia: '0-100', explicacion_probable: 'ej. Satélites, Starlink, Globo, Cohete, Fenómeno Meteorológico, o Desconocido'}"},
                                        {"role": "user", "content": resumen}
                                    ],
                                    "response_format": {"type": "json_object"}
                                }
                                r = requests.post("https://api.deepseek.com/v1/chat/completions", headers=h, json=p, timeout=25)
                                content = r.json()["choices"][0]["message"]["content"]
                                
                                if content.startswith("```"):
                                    content = content.split("```")[1]
                                    if content.startswith("json"): content = content[4:]
                                
                                st.json(json.loads(content.strip()))
                            except Exception as e:
                                st.error(f"Error interno en los circuitos de AGATHA: {str(e)}")
                    else:
                        st.warning("Falta credencial de procesamiento neuronal en la configuración del sistema.")
