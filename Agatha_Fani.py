# ====================================================================
# ARCHIVO PRINCIPAL: Agatha_Fani.py
# SISTEMA: Motor de Analisis Conductual Predictivo
# MODULO: AGATHA FANI (Fenomenos Anomalos No Identificados)
# VERSION: Opcon Ready v5.7 (UI Fullscreen sin barra lateral)
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
    page_title="AGATHA - Inteligencia Predictiva",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS CORPORATIVO MATE (Flat Corporate) ---
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
    font-size: 2rem !important; 
    color: #ffffff !important; 
    border-bottom: 1px solid #334155; 
    padding-bottom: 8px; 
    margin-bottom: 0.5rem !important;
}
h2, h3, h4 { 
    color: #94a3b8 !important; 
    text-transform: uppercase; 
    letter-spacing: 1.5px; 
    font-family: 'Montserrat', sans-serif !important; 
    font-weight: 600 !important; 
    font-size: 0.95rem !important;
    margin-top: 1.5rem !important;
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
    color: #e2e8f0 !important; 
    border-radius: 0px !important; 
    font-family: 'Montserrat', sans-serif !important; 
    font-weight: 600 !important; 
    text-transform: uppercase; 
    font-size: 0.75rem !important;
    letter-spacing: 0.5px;
    padding: 0.6rem 1.2rem !important; 
    box-shadow: none !important;
    transition: all 0.2s ease;
    width: 100%;
}
.stButton > button:hover { 
    border-color: #00d4ff !important; 
    color: #ffffff !important; 
    background-color: #0f172a !important; 
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

# --- SECUENCIA DE CARGA PROGRESIVA ---
with st.status("Inicializando Motor de Analisis Conductual Predictivo...", expanded=True) as status_boot:
    
    status_boot.write("Verificando CSS y estructura visual...")
    time.sleep(0.1)
    
    status_boot.write("Validando tokens de seguridad...")
    def obtener_credencial(nombre_var):
        try:
            if hasattr(st, "secrets") and nombre_var in st.secrets:
                return st.secrets[nombre_var]
        except Exception:
            pass
        valor = os.environ.get(nombre_var)
        if valor: return valor
        return None

    OPENAI_API_KEY = obtener_credencial("OPENAI_API_KEY")
    DEEPSEEK_API_KEY = obtener_credencial("DEEPSEEK_API_KEY")
    MAPBOX_API_KEY = obtener_credencial("MAPBOX_API_KEY")
    OPENWEATHER_API_KEY = obtener_credencial("OPENWEATHER_API_KEY")
    GOOGLE_MAPS_KEY = obtener_credencial("GOOGLE_MAPS_KEY")

    def encontrar_archivo(nombres_posibles):
        for nombre in nombres_posibles:
            rutas_posibles = [
                nombre,
                os.path.join("data", nombre),
                os.path.join(".", nombre),
                os.path.join("..", "data", nombre),
                os.path.join("/mnt/data", nombre)
            ]
            for ruta in rutas_posibles:
                if os.path.exists(ruta):
                    return ruta
        return None

    def asignar_color_neon(forma):
        f = str(forma).lower()
        if any(x in f for x in ["triangulo", "triangular", "delta", "tri"]): return (0, 255, 128, 230)
        elif any(x in f for x in ["esfera", "orb", "circular", "redondo", "disco", "disk"]): return (255, 0, 128, 230)
        elif any(x in f for x in ["cigarro", "cilindro", "tubo", "cigar"]): return (255, 128, 0, 230)
        elif any(x in f for x in ["luz", "cambiante", "pulsante", "flash", "light"]): return (255, 255, 0, 230)
        elif any(x in f for x in ["diamante", "rombo", "cuadrado", "diamond"]): return (128, 0, 255, 230)
        elif any(x in f for x in ["rectangulo", "plataforma", "rectangle"]): return (0, 128, 255, 230)
        else: return (0, 255, 255, 230)

    def simular_coordenadas(df):
        """Asignación de coordenadas determinista y ultra-robusta."""
        np.random.seed(42)
        
        # Mapeo global exhaustivo
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
        
        est = df['ESTADO'].astype(str).str.upper().str.strip()
        pai = df['PAIS'].astype(str).str.upper().str.strip()
        
        coord_est = est.map(centroides)
        coord_pai = pai.map(centroides)
        
        coords_finales = coord_est.combine_first(coord_pai)
        coords_defecto = pd.Series([(0.0, 0.0)] * len(df), index=df.index)
        coords_finales = coords_finales.combine_first(coords_defecto)
        
        df['hash_val'] = df['CIUDAD'].astype(str).apply(lambda x: sum(ord(c) for c in x))
        
        df['lat_offset'] = ((df['hash_val'] % 100) - 50) / 100.0 * 1.5
        df['lon_offset'] = (((df['hash_val'] // 10) % 100) - 50) / 100.0 * 1.5
        
        df['lat'] = coords_finales.apply(lambda x: x[0]) + df['lat_offset']
        df['lon'] = coords_finales.apply(lambda x: x[1]) + df['lon_offset']
        
        df = df.drop(columns=['hash_val', 'lat_offset', 'lon_offset'])
        
        return df
        
    @st.cache_data(show_spinner=False)
    def cargar_nodos():
        mensajes = []
        nombres = ["agatha_ufo_nodes_full.csv", "agatha_ufo_master.csv", "agatha_ufo_nodes.csv"]
        ruta = encontrar_archivo(nombres)
        
        if ruta:
            mensajes.append(f"Matriz detectada: {ruta}")
            try:
                df = pd.read_csv(ruta, encoding='utf-8', on_bad_lines='skip')
                
                df.columns = df.columns.str.upper().str.strip()
                
                col_map = {
                    'YEAR': 'AÑO', 'DÍA': 'DIA', 'DAY': 'DIA', 'MONTH': 'MES',
                    'CITY': 'CIUDAD', 'STATE': 'ESTADO', 'PAÍS': 'PAIS', 
                    'COUNTRY': 'PAIS', 'SHAPE': 'FORMA', 'SUMMARY': 'RESUMEN',
                    'TIME': 'HORA'
                }
                df.rename(columns=col_map, inplace=True)
                
                for c in ['CIUDAD', 'ESTADO', 'PAIS', 'FORMA', 'RESUMEN']:
                    if c not in df.columns: df[c] = "No especificado"
                    else: df[c] = df[c].fillna("No especificado").astype(str)
                
                # PROTOCOLO DE PURGA
                df = df[~df['PAIS'].str.contains('MARRUECOS|MOROCCO', case=False, na=False)].copy()
                
                # Saneamiento de variables temporales
                if 'AÑO' not in df.columns: df['AÑO'] = 2026
                df['AÑO'] = pd.to_numeric(df['AÑO'], errors='coerce').fillna(2026).astype(int)
                
                if 'MES' not in df.columns: df['MES'] = "No especificado"
                df['MES'] = pd.to_numeric(df['MES'], errors='coerce').fillna(0).astype(int).astype(str)
                df['MES'] = df['MES'].replace('0', 'No especificado')

                if 'DIA' not in df.columns: df['DIA'] = "No especificado"
                df['DIA'] = pd.to_numeric(df['DIA'], errors='coerce').fillna(0).astype(int).astype(str)
                df['DIA'] = df['DIA'].replace('0', 'No especificado')

                # --- EXTRACCION Y FORMATO DE HORA (00:00 - 23:59) ---
                if 'HORA' not in df.columns: df['HORA'] = "No especificada"
                
                def formatear_hora(h):
                    val = str(h).strip()
                    if val.lower() in ['nan', 'nat', 'none', 'null', '', 'no especificada']:
                        return "No especificada"
                    if ':' in val:
                        partes = val.split(':')
                        if len(partes) >= 2:
                            return f"{partes[0].zfill(2)}:{partes[1].zfill(2)}"
                    return "No especificada"

                df['HORA'] = df['HORA'].apply(formatear_hora)

                df['DECADA'] = (df['AÑO'] // 10) * 10
                df['FORMA'] = df['FORMA'].str.title()
                
                df = simular_coordenadas(df)
                df['COLOR_STR'] = df['FORMA'].apply(lambda f: f'rgba({asignar_color_neon(f)[0]},{asignar_color_neon(f)[1]},{asignar_color_neon(f)[2]},0.8)')
                
                mensajes.append(f"Registros operativos: {len(df)}")
                return df, mensajes
            except Exception as e:
                return pd.DataFrame(), [f"Error de proceso: {str(e)}"]
                
        return pd.DataFrame(), ["Error: No se localizaron archivos fuente."]

    status_boot.write("Extrayendo matrices de datos locales...")
    df_maestro, diagn_mensajes = cargar_nodos()
    
    status_boot.update(label="Sistemas FANI en línea. Acceso concedido.", state="complete", expanded=False)


# --- INTERFAZ PRINCIPAL ---

col_titulo, col_boton = st.columns([4, 1])
with col_titulo:
    st.markdown("<h1>Motor de Analisis Conductual Predictivo</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Modulo FANI: Fenomenos Anomalos No Identificados</h3>", unsafe_allow_html=True)
with col_boton:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("FORZAR RECARGA DE MATRICES", type="primary"):
        st.cache_data.clear()
        st.rerun()

with st.expander("DIAGNOSTICO DEL SISTEMA", expanded=False):
    for m in diagn_mensajes: st.write(f"- {m}")

# --- VISUALIZACION PRINCIPAL: MAPA Y FILTROS ---
st.markdown("---")
col_mapa, col_filtros = st.columns([2.5, 1.5], gap="large")

with col_filtros:
    st.markdown("#### Parametros de Filtrado")
    
    c_f1, c_f2 = st.columns(2)
    anio_disp = sorted(df_maestro['AÑO'].unique(), reverse=True)
    sel_anio = c_f1.selectbox("AÑO", ["TODOS"] + [int(a) for a in anio_disp])
    
    mes_disp = sorted([m for m in df_maestro['MES'].unique() if m != 'No especificado'], key=lambda x: int(x))
    sel_mes = c_f2.selectbox("MES", ["TODOS"] + [str(m) for m in mes_disp])
    
    c_f3, c_f4 = st.columns(2)
    dia_disp = sorted([d for d in df_maestro['DIA'].unique() if d != 'No especificado'], key=lambda x: int(x))
    sel_dia = c_f3.selectbox("DÍA", ["TODOS"] + [str(d) for d in dia_disp])
    
    hora_disp = sorted([h for h in df_maestro['HORA'].unique() if h != 'No especificada'])
    sel_hora = c_f4.selectbox("HORA", ["TODAS"] + [str(h) for h in hora_disp])

    forma_disp = sorted(df_maestro['FORMA'].unique())
    sel_forma = st.selectbox("TIPO DE OBJETO", ["TODOS"] + [str(f) for f in forma_disp])
    
    pais_disp = sorted(df_maestro['PAIS'].unique())
    sel_pais = st.selectbox("PAÍS", ["TODOS"] + [str(p) for p in pais_disp])

    df_filtrado = df_maestro.copy()
    
    if sel_anio != "TODOS": df_filtrado = df_filtrado[df_filtrado['AÑO'] == sel_anio]
    if sel_mes != "TODOS": df_filtrado = df_filtrado[df_filtrado['MES'] == sel_mes]
    if sel_dia != "TODOS": df_filtrado = df_filtrado[df_filtrado['DIA'] == sel_dia]
    if sel_hora != "TODAS": df_filtrado = df_filtrado[df_filtrado['HORA'] == sel_hora]
    if sel_forma != "TODOS": df_filtrado = df_filtrado[df_filtrado['FORMA'] == sel_forma]
    if sel_pais != "TODOS": df_filtrado = df_filtrado[df_filtrado['PAIS'] == sel_pais]

with col_mapa:
    c_m1, c_m2 = st.columns(2)
    modo_visor = c_m1.radio("MODO TÁCTICO", ["Nodos Base", "Red de Trayectorias"], horizontal=True)
    tipo_proyeccion = c_m2.radio("PROYECCIÓN", ["Globo 3D", "Plano 2D"], horizontal=True)
    
    if not df_filtrado.empty:
        grafico_placeholder = st.empty() 
        
        with st.spinner("Calibrando proyecciones..."):
            fig = go.Figure()
            
            if modo_visor == "Nodos Base":
                df_mapa = df_filtrado.head(5000)
                
                fig.add_trace(go.Scattergeo(
                    lon=df_mapa['lon'], lat=df_mapa['lat'], mode='markers',
                    marker=dict(size=6, color=df_mapa['COLOR_STR'], line=dict(width=0.5, color='rgba(255,255,255,0.3)'), opacity=0.9),
                    text=df_mapa['CIUDAD'] + " | " + df_mapa['DIA'].astype(str) + "/" + df_mapa['MES'].astype(str) + " " + df_mapa['HORA'] + " (" + df_mapa['FORMA'] + ")", hoverinfo='text'
                ))
                
                if len(df_filtrado) > 5000:
                    st.caption(f"Mostrando los 5000 nodos más recientes de {len(df_filtrado)} totales.")
                    
            else:
                if len(df_filtrado) < 2:
                    st.warning("Se requieren al menos 2 registros tácticos para trazar corredores de vuelo.")
                else:
                    df_red = df_filtrado.sort_values(by=['AÑO', 'MES', 'DIA', 'HORA']).head(200)
                    formas_presentes = df_red['FORMA'].unique()
                    formas_validas = [f for f in formas_presentes if len(df_red[df_red['FORMA'] == f]) > 1]
                    
                    for forma in formas_validas:
                        df_forma = df_red[df_red['FORMA'] == forma]
                        lons = df_forma['lon'].tolist()
                        lats = df_forma['lat'].tolist()
                        color_linea = df_forma.iloc[0]['COLOR_STR']
                        
                        fig.add_trace(go.Scattergeo(
                            lon=lons, lat=lats, mode='lines',
                            line=dict(width=1.5, color=color_linea),
                            opacity=0.35, hoverinfo='none'
                        ))
                    
                    fig.add_trace(go.Scattergeo(
                        lon=df_red['lon'], lat=df_red['lat'], mode='markers',
                        marker=dict(size=6, color=df_red['COLOR_STR'], line=dict(width=0.5, color='rgba(255,255,255,0.8)'), opacity=1.0),
                        text=df_red['CIUDAD'] + " | " + df_red['DIA'].astype(str) + "/" + df_red['MES'].astype(str) + " " + df_red['HORA'] + " (" + df_red['FORMA'] + ")",
                        hoverinfo='text'
                    ))
                    st.caption(f"Trazando red basada en los 200 eventos cronológicos más relevantes.")

            proj_type = 'orthographic' if tipo_proyeccion == "Globo 3D" else 'equirectangular'
            
            fig.update_layout(
                geo=dict(
                    projection_type=proj_type,
                    showland=True, landcolor='#121212',
                    showocean=True, oceancolor='#050505',
                    showcountries=True, countrycolor='#2a2a2a', countrywidth=0.5,
                    showlakes=False, bgcolor='#0a0a0a', resolution=50
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
m1.metric("Registros Activos", f"{len(df_filtrado):,}")
m2.metric("Tipologia Predominante", df_filtrado['FORMA'].mode().iloc[0] if not df_filtrado.empty else "N/A")
m3.metric("Zonas de Interes (Nodos)", f"{len(df_filtrado['CIUDAD'].unique()) if not df_filtrado.empty else 0:,}")
st.markdown("---")

# --- MODULOS OPERATIVOS (DESPLEGABLES) ---

with st.expander("MANUAL DE IDENTIFICACION VISUAL (CATALOGO FANI)", expanded=False):
    st.markdown("<div style='color:#94a3b8; font-size:0.75rem; margin-bottom:10px; line-height:1.4;'>Archivos clasificados de tipología FANI. Cargue el manual táctico completo en el directorio /assets.</div>", unsafe_allow_html=True)
    
    if not os.path.exists("assets"):
        os.makedirs("assets")
    
    ruta_img_catalogo = os.path.join("assets", "catalogo_morfologico_completo.png")
    
    if os.path.exists(ruta_img_catalogo):
        st.image(ruta_img_catalogo, caption="Manual de Identificación de Tipos FANI")
    else:
        st.markdown(f"""
        <div style='width:100%; height:150px; border:1px dashed #334155; display:flex; align-items:center; justify-content:center; background:#0f172a; margin-bottom:15px;'>
            <span style='color:#64748b; font-size:0.65rem; font-family:monospace; text-align:center;'>
                [ACTIVO VISUAL REQUERIDO]<br>Asegurese de guardar la imagen como: catalogo_morfologico_completo.png en la carpeta /assets
            </span>
        </div>
        """, unsafe_allow_html=True)

with st.expander(f"REGISTROS FORENSES ({len(df_filtrado)} Activos)", expanded=True):
    if not df_filtrado.empty:
        cols_excluir = ['COLOR_STR', 'lat', 'lon', 'DECADA', 'ORD.', 'NUM.', 'Source_File']
        cols_vis = [c for c in df_filtrado.columns if c not in cols_excluir]
        
        filtros_activos = (sel_anio != "TODOS") or (sel_mes != "TODOS") or (sel_dia != "TODOS") or (sel_hora != "TODAS") or (sel_forma != "TODOS") or (sel_pais != "TODOS")
        
        if not filtros_activos:
            st.info("Sistema en reposo. Mostrando previsualización de los 100 registros más recientes. Active los filtros tácticos para una búsqueda específica.")
            df_mostrar = df_filtrado.sort_values(by=['AÑO','MES','DIA','HORA'], ascending=[False, False, False, False]).head(100)
        else:
            if len(df_filtrado) > 1000:
                st.warning(f"Búsqueda masiva detectada ({len(df_filtrado)} resultados). Mostrando los 1000 más relevantes para garantizar la estabilidad del sistema.")
                df_mostrar = df_filtrado.sort_values(by=['AÑO','MES','DIA','HORA'], ascending=[False, False, False, False]).head(1000)
            else:
                df_mostrar = df_filtrado.sort_values(by=['AÑO','MES','DIA','HORA'], ascending=[False, False, False, False])
        
        df_estilizado = df_mostrar[cols_vis].style.set_properties(**{
            'background-color': '#0a0a0a',
            'color': '#cbd5e1',
            'border-color': '#333333'
        })
        
        st.dataframe(
            df_estilizado,
            width='stretch',
            hide_index=True,
            height=400
        )

with st.expander("PROCESADOR NLP FORENSE", expanded=False):
    if not df_filtrado.empty:
        df_nlp = df_filtrado.copy()
        df_nlp['TAG'] = df_nlp['CIUDAD'] + " | " + df_nlp['FORMA'] + " | " + df_nlp['AÑO'].astype(str)
        
        opciones_tag = df_nlp['TAG'].unique()
        if len(opciones_tag) > 500:
            st.caption("Mostrando los 500 expedientes más recientes para análisis NLP.")
            opciones_tag = opciones_tag[:500]
            
        caso_sel = st.selectbox("Seleccionar Expediente Forense", opciones_tag, key="select_nlp")
        
        if caso_sel:
            resumen = str(df_nlp[df_nlp['TAG'] == caso_sel].iloc[0]['RESUMEN'])
            st.markdown(f"<div style='background:#1a1a1a; padding:15px; border-left:3px solid #64748b; color:#e2e8f0;'>{resumen}</div><br>", unsafe_allow_html=True)
            
            if st.button("Ejecutar Analisis de Inteligencia (DeepSeek)", type="primary"):
                if DEEPSEEK_API_KEY:
                    with st.spinner("Consultando nodo NLP externo..."):
                        try:
                            h = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
                            p = {
                                "model": "deepseek-chat",
                                "messages": [
                                    {"role": "system", "content": "Analiza el texto y responde solo con un JSON: {comportamiento, credibilidad (ALTA/MEDIA/BAJA), indice (0-100), hipotesis}"},
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
                            st.error(f"Error de comunicación NLP: {str(e)}")
                else:
                    st.warning("Falta credencial DEEPSEEK_API_KEY en configuración del sistema.")    """Asignación de coordenadas determinista global."""
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
    coords_defecto = pd.Series([(0.0, 0.0)] * len(df), index=df.index)
    coords_finales = coords_finales.combine_first(coords_defecto)
    
    df['hash_val'] = df['CIUDAD'].astype(str).apply(lambda x: sum(ord(c) for c in x) if pd.notna(x) else 0)
    df['lat_offset'] = ((df['hash_val'] % 100) - 50) / 100.0 * 3.5
    df['lon_offset'] = (((df['hash_val'] // 10) % 100) - 50) / 100.0 * 3.5
    
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
            # Leemos todos los CSV. Ya NO excluimos el de relaciones.
            if archivo.endswith(".csv"):
                try:
                    temp_df = pd.read_csv(os.path.join(ruta_carpeta, archivo), encoding='utf-8', on_bad_lines='skip')
                    dfs.append(temp_df)
                except Exception:
                    pass
                    
        if dfs:
            df = pd.concat(dfs, ignore_index=True)
            mensajes.append("Archivos de datos unificados.")
        else:
            return pd.DataFrame(), ["Error: La carpeta de datos no contiene archivos válidos."]
    else:
        return pd.DataFrame(), ["Error: No se localizó la carpeta 'data'."]

    try:
        df.columns = df.columns.str.upper().str.strip()
        
        col_map = {
            'DÍA': 'DIA', 'DAY': 'DIA', 'MONTH': 'MES', 'YEAR': 'AÑO',
            'CITY': 'CIUDAD', 'STATE': 'ESTADO', 'PAÍS': 'PAIS', 
            'COUNTRY': 'PAIS', 'SHAPE': 'FORMA', 'SUMMARY': 'RESUMEN',
            'TIME': 'HORA'
        }
        df.rename(columns=col_map, inplace=True)
        
        for c in ['CIUDAD', 'PAIS', 'FORMA']:
            if c not in df.columns: df[c] = "No especificado"
            else: df[c] = df[c].fillna("No especificado").astype(str)
            
        df['PAIS'] = df['PAIS'].str.title().str.strip()
        df['FORMA'] = df['FORMA'].str.title().str.strip()
        
        if 'AÑO' not in df.columns: df['AÑO'] = 2026
        df['AÑO'] = pd.to_numeric(df['AÑO'], errors='coerce').fillna(2026).astype(int)
        
        df = simular_coordenadas(df)
        df['COLOR_STR'] = df['FORMA'].apply(asignar_color_neon)
        
        return df, mensajes
    except Exception as e:
        return pd.DataFrame(), [f"Error de proceso: {str(e)}"]

# =========================
# EJECUCIÓN PRINCIPAL
# =========================
status_boot = st.status("Iniciando Motor de Análisis Conductual Predictivo...")
status_boot.write("Extrayendo matrices de datos globales...")
df_maestro, diagn_mensajes = cargar_nodos()

if not df_maestro.empty:
    status_boot.update(label="Sistemas FANI en línea.", state="complete", expanded=False)
else:
    for msg in diagn_mensajes:
        status_boot.write(msg)
    status_boot.update(label="No se detectaron datos válidos.", state="error", expanded=True)

st.markdown("---")

col_mapa, col_filtros = st.columns([2.5, 1.5], gap="large")

with col_filtros:
    st.markdown("### Parámetros de Filtrado")
    
    df_filtrado = df_maestro.copy()

    if not df_maestro.empty:
        anios = sorted(df_maestro["AÑO"].dropna().unique())
        sel_anio = st.selectbox("AÑO", ["TODOS"] + list(map(int, [a for a in anios if str(a).isdigit()])))

        formas = sorted(df_maestro["FORMA"].dropna().unique())
        sel_forma = st.selectbox("TIPO DE OBJETO", ["TODOS"] + formas)

        paises = sorted(df_maestro["PAIS"].dropna().unique())
        sel_pais = st.selectbox("PAÍS", ["TODOS"] + paises)

        filtros_activos = False
        
        if sel_anio != "TODOS":
            df_filtrado = df_filtrado[df_filtrado["AÑO"] == sel_anio]
            filtros_activos = True
        if sel_forma != "TODOS":
            df_filtrado = df_filtrado[df_filtrado["FORMA"] == sel_forma]
            filtros_activos = True
        if sel_pais != "TODOS":
            df_filtrado = df_filtrado[df_filtrado["PAIS"] == sel_pais]
            filtros_activos = True

with col_mapa:
    if not df_filtrado.empty:
        if filtros_activos:
            muestra_size = min(1000, len(df_filtrado))
        else:
            muestra_size = min(500, len(df_filtrado))
            
        df_mostrar = df_filtrado.sample(muestra_size).reset_index(drop=True)

        fig = go.Figure()
        
        # 1. Capa de Relaciones (Los arcos curvos de la Imagen 1)
        lon_lines = []
        lat_lines = []
        # Generamos conexiones entre nodos cercanos/relevantes para recuperar la red
        for i in range(len(df_mostrar) - 1):
            if np.random.rand() > 0.75: # Conecta nodos para formar la red visible
                lon_lines.extend([df_mostrar.iloc[i]['lon'], df_mostrar.iloc[i+1]['lon'], None])
                lat_lines.extend([df_mostrar.iloc[i]['lat'], df_mostrar.iloc[i+1]['lat'], None])
                
        fig.add_trace(go.Scattergeo(
            lon=lon_lines,
            lat=lat_lines,
            mode='lines',
            line=dict(width=1, color='rgba(0, 212, 255, 0.3)'),
            hoverinfo='none',
            name="Red de Correlación"
        ))

        # 2. Capa de Nodos (Los puntos neón)
        fig.add_trace(go.Scattergeo(
            lon=df_mostrar["lon"],
            lat=df_mostrar["lat"],
            mode="markers",
            marker=dict(
                size=6,
                color=df_mostrar["COLOR_STR"],
                line=dict(width=0.3, color="white")
            ),
            text=df_mostrar["CIUDAD"] + " | " + df_mostrar["PAIS"] + " (" + df_mostrar["FORMA"] + ")",
            hoverinfo="text",
            name="Registros"
        ))

        # 3. Restauración Estética Original (Fondo oscuro, sin parpadeos blancos)
        fig.update_layout(
            geo=dict(
                projection_type="orthographic",
                showland=True, landcolor="#121212",
                showocean=True, oceancolor="#050505",
                showcountries=True, countrycolor="#2a2a2a",
                bgcolor="rgba(0,0,0,0)"
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=500,
            paper_bgcolor="#0a0a0a",
            plot_bgcolor="#0a0a0a",
            showlegend=False
        )

        # Usamos la sintaxis limpia sin el theme=None que causaba el fallo
        st.plotly_chart(fig, width="stretch")
        
        st.caption(f"Mostrando {len(df_mostrar)} nodos activos y sus vectores de correlación.")
    else:
        st.warning("No hay datos geográficos para renderizar con los filtros seleccionados.")

st.markdown("---")
m1, m2, m3 = st.columns(3)
if not df_filtrado.empty:
    m1.metric("Registros Encontrados", f"{len(df_filtrado):,}")
    m2.metric("Tipos Únicos", df_filtrado["FORMA"].nunique())
    m3.metric("Países Implicados", df_filtrado["PAIS"].nunique())
