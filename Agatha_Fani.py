# ====================================================================
# ARCHIVO PRINCIPAL: app.py (Módulo Agatha Fani)
# SISTEMA: Motor de Analisis Conductual Predictivo
# MODULO: AGATHA FANI (Fenomenos Anomalos No Identificados)
# VERSION: Opcon Ready v5.7.1 (Corrección de KeyError AÑO)
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
        
        # Saneamiento previo
        df['ESTADO'] = df.get('ESTADO', pd.Series(["No especificado"]*len(df))).astype(str).str.upper().str.strip()
        df['PAIS'] = df.get('PAIS', pd.Series(["No especificado"]*len(df))).astype(str).str.upper().str.strip()
        
        coord_est = df['ESTADO'].map(centroides)
        coord_pai = df['PAIS'].map(centroides)
        
        coords_finales = coord_est.combine_first(coord_pai)
        coords_defecto = pd.Series([(0.0, 0.0)] * len(df), index=df.index)
        coords_finales = coords_finales.combine_first(coords_defecto)
        
        df['hash_val'] = df.get('CIUDAD', pd.Series([""]*len(df))).astype(str).apply(lambda x: sum(ord(c) for c in x))
        
        df['lat_offset'] = ((df['hash_val'] % 100) - 50) / 100.0 * 1.5
        df['lon_offset'] = (((df['hash_val'] // 10) % 100) - 50) / 100.0 * 1.5
        
        df['lat'] = coords_finales.apply(lambda x: x[0]) + df['lat_offset']
        df['lon'] = coords_finales.apply(lambda x: x[1]) + df['lon_offset']
        
        df = df.drop(columns=['hash_val', 'lat_offset', 'lon_offset'], errors='ignore')
        return df
        
    @st.cache_data(show_spinner=False)
    def cargar_nodos():
        mensajes = []
        nombres = ["agatha_ufo_nodes_full.csv", "agatha_ufo_master.csv", "agatha_ufo_nodes.csv"]
        ruta = encontrar_archivo(nombres)
        
        if not ruta:
            mensajes.append("Aviso: No se detectaron archivos fuente. Generando matriz simulada.")
            formas_sim = ["Diamante", "Cubo", "Desconocido", "Otros", "Cruz", "Cilindro", "Circulo", 
                         "Cambiante", "Cigarro", "Cono", "Esfera", "Estrella", "Lagrima", "Oval", 
                         "Rectángulo", "Triangulo", "Bola de fuego", "Disco", "Flash", "Formacion", 
                         "Galones", "Huevo", "Luz", "Orbe"]
            data = []
            for i in range(1000):
                data.append({
                    'AÑO': np.random.randint(1950, 2026),
                    'MES': str(np.random.randint(1, 13)),
                    'DIA': str(np.random.randint(1, 29)),
                    'HORA': f"{np.random.randint(0,24):02d}:{np.random.randint(0,60):02d}",
                    'CIUDAD': np.random.choice(["Austin", "Madrid", "Londres", "New York", "Paris"]),
                    'ESTADO': np.random.choice(["TX", "MADRID", "LONDRES", "NY", "PARIS"]),
                    'PAIS': np.random.choice(["USA", "ESPAÑA", "UK", "USA", "FRANCIA"]),
                    'FORMA': np.random.choice(formas_sim),
                    'RESUMEN': "Detección anómala registrada en el sector táctico."
                })
            df = pd.DataFrame(data)
        else:
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
            except Exception as e:
                mensajes.append(f"Error crítico de lectura: {str(e)}")
                return pd.DataFrame(), mensajes

        # ASEGURAR COLUMNAS CRÍTICAS
        for c in ['CIUDAD', 'ESTADO', 'PAIS', 'FORMA', 'RESUMEN']:
            if c not in df.columns: df[c] = "No especificado"
            else: df[c] = df[c].fillna("No especificado").astype(str)
        
        # PROTOCOLO DE PURGA
        if 'PAIS' in df.columns:
            df = df[~df['PAIS'].str.contains('MARRUECOS|MOROCCO', case=False, na=False)].copy()
        
        # VALIDACIÓN DE AÑO (Origen del KeyError)
        if 'AÑO' not in df.columns: 
            df['AÑO'] = 2026
        else:
            df['AÑO'] = pd.to_numeric(df['AÑO'], errors='coerce').fillna(2026).astype(int)
        
        for t in ['MES', 'DIA']:
            if t not in df.columns: df[t] = "No especificado"
            df[t] = pd.to_numeric(df[t], errors='coerce').fillna(0).astype(int).astype(str)
            df[t] = df[t].replace('0', 'No especificado')

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
        df['COLOR_STR'] = df['FORMA'].apply(lambda f: f'rgba({asignar_color_neon(f)[0]},{asignar_color_neon(f)[1]},{asignar_color_neon(f)[2]},0.8)')
        
        mensajes.append(f"Registros operativos: {len(df)}")
        return df, mensajes

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

st.markdown("---")
col_mapa, col_filtros = st.columns([2.5, 1.5], gap="large")

with col_filtros:
    st.markdown("#### Parametros de Filtrado")
    
    # PROTECCIÓN CONTRA DATAFRAME VACÍO O SIN COLUMNAS
    if not df_maestro.empty and 'AÑO' in df_maestro.columns:
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
    else:
        st.error("Matriz de datos no compatible. Verifique archivos fuente.")
        df_filtrado = pd.DataFrame()

with col_mapa:
    c_m1, c_m2 = st.columns(2)
    modo_visor = c_m1.radio("MODO TÁCTICO", ["Nodos Base", "Red de Trayectorias"], horizontal=True)
    tipo_proyeccion = c_m2.radio("PROYECCIÓN", ["Globo 3D", "Plano 2D"], horizontal=True)
    
    if not df_filtrado.empty:
        grafico_placeholder = st.empty() 
        fig = go.Figure()
        
        if modo_visor == "Nodos Base":
            df_mapa = df_filtrado.head(5000)
            fig.add_trace(go.Scattergeo(
                lon=df_mapa['lon'], lat=df_mapa['lat'], mode='markers',
                marker=dict(size=6, color=df_mapa['COLOR_STR'], line=dict(width=0.5, color='rgba(255,255,255,0.3)'), opacity=0.9),
                text=df_mapa['CIUDAD'] + " | " + df_mapa['FORMA'], hoverinfo='text'
            ))
        else:
            df_red = df_filtrado.sort_values(by=['AÑO', 'MES', 'DIA', 'HORA']).head(200)
            formas_validas = [f for f in df_red['FORMA'].unique() if len(df_red[df_red['FORMA'] == f]) > 1]
            for forma in formas_validas:
                df_forma = df_red[df_red['FORMA'] == forma]
                fig.add_trace(go.Scattergeo(
                    lon=df_forma['lon'], lat=df_forma['lat'], mode='lines+markers',
                    line=dict(width=1.5, color=df_forma.iloc[0]['COLOR_STR']),
                    marker=dict(size=4), opacity=0.5, name=forma
                ))

        proj_type = 'orthographic' if tipo_proyeccion == "Globo 3D" else 'equirectangular'
        fig.update_layout(
            geo=dict(projection_type=proj_type, showland=True, landcolor='#121212', 
                    showocean=True, oceancolor='#050505', bgcolor='#0a0a0a'),
            margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='#0a0a0a', height=450, showlegend=False
        )
        grafico_placeholder.plotly_chart(fig, use_container_width=True)

# --- INDICADORES ---
m1, m2, m3 = st.columns(3)
m1.metric("Registros Activos", f"{len(df_filtrado):,}")
m2.metric("Tipologia Predominante", df_filtrado['FORMA'].mode().iloc[0] if not df_filtrado.empty else "N/A")
m3.metric("Zonas de Interes (Nodos)", f"{len(df_filtrado['CIUDAD'].unique()) if not df_filtrado.empty else 0:,}")

# --- REGISTROS FORENSES ---
with st.expander(f"REGISTROS FORENSES ({len(df_filtrado)} Activos)", expanded=True):
    if not df_filtrado.empty:
        df_mostrar = df_filtrado.sort_values(by=['AÑO','MES','DIA','HORA'], ascending=False).head(100)
        st.dataframe(df_mostrar.drop(columns=['COLOR_STR', 'lat', 'lon', 'hash_val'], errors='ignore'), use_container_width=True, hide_index=True)

# --- PROCESADOR NLP FORENSE ---
with st.expander("PROCESADOR NLP FORENSE", expanded=False):
    if not df_filtrado.empty:
        opciones_tag = (df_filtrado['CIUDAD'] + " | " + df_filtrado['FORMA']).unique()[:500]
        caso_sel = st.selectbox("Seleccionar Expediente Forense", opciones_tag)
        if st.button("Ejecutar Analisis de Inteligencia (DeepSeek)", type="primary"):
            if DEEPSEEK_API_KEY:
                with st.spinner("Consultando nodo NLP externo..."):
                    try:
                        resumen = df_filtrado.iloc[0]['RESUMEN']
                        h = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
                        p = {"model": "deepseek-chat", "messages": [{"role": "user", "content": f"Analiza: {resumen}"}]}
                        r = requests.post("https://api.deepseek.com/v1/chat/completions", headers=h, json=p, timeout=25)
                        st.json(r.json())
                    except Exception as e: st.error(f"Error: {str(e)}")
            else: st.warning("Falta credencial DEEPSEEK_API_KEY.")

st.divider()
st.markdown("**Nota de Confidencialidad:** Informe generado por Motor de Análisis Conductual Predictivo. Nivel de acceso 5 requerido para exportación.")
