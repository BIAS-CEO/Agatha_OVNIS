# ====================================================================
# ARCHIVO PRINCIPAL: Agatha_Fani.py
# SISTEMA: Motor de Analisis Conductual Predictivo
# MODULO: AGATHA FANI (Fenomenos Anomalos No Identificados)
# VERSION: Opcon Ready v5.2 (Carga Progresiva y Bloqueo Anti-Congelamiento)
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
    initial_sidebar_state="expanded"
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
[data-testid="stHeader"], footer { display: none !important; }
.block-container { 
    padding-top: 1rem !important; 
    padding-bottom: 1rem !important; 
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

.contenedor-tabla { 
    width: 100%; 
    max-height: 600px; 
    overflow-y: auto; 
    border: 1px solid #333333; 
    background-color: #0a0a0a; 
    margin-bottom: 20px; 
}
.rejilla-tactica { 
    width: 100%; 
    border-collapse: collapse; 
    font-family: 'Titillium Web', sans-serif; 
    font-size: 0.8rem; 
    color: #e2e8f0; 
}
.rejilla-tactica thead th { 
    position: sticky; 
    top: 0; 
    background-color: #1a1a1a; 
    color: #00d4ff; 
    text-align: left; 
    padding: 10px 12px; 
    text-transform: uppercase; 
    font-size: 0.7rem; 
    letter-spacing: 1px; 
    border-bottom: 1px solid #333333; 
    z-index: 10; 
    font-weight: 600;
}
.rejilla-tactica tbody td { 
    padding: 8px 12px; 
    border-bottom: 1px solid #1a1a1a; 
    color: #cbd5e1;
}
.rejilla-tactica tbody tr:hover { 
    background-color: #1a1a1a; 
}
.valor-num { 
    font-family: 'Share Tech Mono', monospace; 
    color: #ffffff; 
}
.valor-texto {
    color: #94a3b8;
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
# Utilizamos st.status para evitar la pantalla en blanco inicial
with st.status("Inicializando Motor de Analisis Conductual Predictivo...", expanded=True) as status_boot:
    
    status_boot.write("Verificando CSS y estructura visual...")
    time.sleep(0.1) # Breve pausa para asentar el DOM
    
    # --- SISTEMA DE GESTION DE CREDENCIALES ---
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

    # --- FUNCIONES AUXILIARES ---
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
        np.random.seed(42)
        lats, lons = [], []
        centroides = {
            "TX": (31.9, -99.9), "FL": (27.7, -81.6), "CA": (36.7, -119.4), "NY": (40.7, -74.0),
            "SC": (33.8, -81.1), "PA": (41.2, -77.1), "LA": (30.9, -91.9), "CO": (39.5, -105.7),
            "EEUU": (39.8, -98.5), "CANADA": (56.1, -106.3), "UK": (55.3, -3.4)
        }
        for _, row in df.iterrows():
            estado = str(row.get('ESTADO', '')).upper().strip()
            pais = str(row.get('PAIS', '')).upper().strip()
            lat, lon = (39.8, -98.5)
            if estado in centroides: lat, lon = centroides[estado]
            elif pais in centroides: lat, lon = centroides[pais]
            lats.append(lat + np.random.normal(0, 1.2))
            lons.append(lon + np.random.normal(0, 1.2))
        df['lat'], df['lon'] = lats, lons
        return df

    @st.cache_data(show_spinner=False)
    def cargar_nodos():
        mensajes = []
        nombres = ["agatha_ufo_master.csv", "agatha_ufo_nodes_full.csv", "agatha_ufo_nodes.csv"]
        ruta = encontrar_archivo(nombres)
        if ruta:
            mensajes.append(f"Matriz detectada: {ruta}")
            try:
                df = pd.read_csv(ruta, encoding='utf-8', on_bad_lines='skip')
                col_map = {
                    'AÑO': 'AÑO', 'Year': 'AÑO', 'DÍA': 'DIA', 'Day': 'DIA', 'MES': 'MES', 'Month': 'MES',
                    'CIUDAD': 'CIUDAD', 'City': 'CIUDAD', 'ESTADO': 'ESTADO', 'State': 'ESTADO',
                    'PAÍS': 'PAIS', 'Country': 'PAIS', 'FORMA': 'FORMA', 'Shape': 'FORMA',
                    'RESUMEN': 'RESUMEN', 'Summary': 'RESUMEN'
                }
                df.rename(columns=col_map, inplace=True)
                for c in ['CIUDAD', 'ESTADO', 'PAIS', 'FORMA', 'RESUMEN']:
                    if c not in df.columns: df[c] = "No especificado"
                    else: df[c] = df[c].fillna("No especificado").astype(str)
                if 'AÑO' not in df.columns: df['AÑO'] = 2026
                df['AÑO'] = pd.to_numeric(df['AÑO'], errors='coerce').fillna(2026).astype(int)
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

if st.sidebar.button("FORZAR RECARGA DE MATRICES"):
    st.cache_data.clear()
    st.rerun()

def render_tabla_tactica(df):
    if df.empty: return
    
    cols_excluir = ['COLOR_STR', 'lat', 'lon', 'DECADA', 'ORD.', 'NUM.', 'Source_File']
    cols_vis = [c for c in df.columns if c not in cols_excluir]
    
    st.dataframe(
        df[cols_vis],
        use_container_width=True,
        hide_index=True,
        height=600
    )

st.markdown("<h1>Motor de Analisis Conductual Predictivo</h1>", unsafe_allow_html=True)
st.markdown("<h3>Modulo FANI: Fenomenos Anomalos No Identificados</h3>", unsafe_allow_html=True)

with st.sidebar.expander("DIAGNOSTICO DEL SISTEMA"):
    for m in diagn_mensajes: st.write(f"- {m}")

# --- VISUALIZACION PRINCIPAL: MAPA Y FILTROS ---
st.markdown("---")
col_mapa, col_filtros = st.columns([2.5, 1.5], gap="large")

with col_filtros:
    st.markdown("#### Parametros de Filtrado")
    
    # Adaptación de filtros según esquema táctico
    df_filtrado = df_maestro.copy()
    if not df_filtrado.empty:
        anio_disp = sorted(df_filtrado['AÑO'].unique(), reverse=True)
        sel_anio = st.selectbox("AÑO", ["TODOS"] + [int(a) for a in anio_disp])
        if sel_anio != "TODOS": df_filtrado = df_filtrado[df_filtrado['AÑO'] == sel_anio]
        
        # Filtros adicionales preparados para tu esquema (Mes, Día, Hora, País)
        mes_disp = sorted(df_filtrado['MES'].unique())
        sel_mes = st.selectbox("MES", ["TODOS"] + [str(m) for m in mes_disp])
        if sel_mes != "TODOS": df_filtrado = df_filtrado[df_filtrado['MES'] == sel_mes]
        
        forma_disp = sorted(df_filtrado['FORMA'].unique())
        sel_forma = st.selectbox("TIPO DE OBJETO", ["TODOS"] + [str(f) for f in forma_disp])
        if sel_forma != "TODOS": df_filtrado = df_filtrado[df_filtrado['FORMA'] == sel_forma]
        
        pais_disp = sorted(df_filtrado['PAIS'].unique())
        sel_pais = st.selectbox("PAIS", ["TODOS"] + [str(p) for p in pais_disp])
        if sel_pais != "TODOS": df_filtrado = df_filtrado[df_filtrado['PAIS'] == sel_pais]

with col_mapa:
    st.markdown("#### Visor de Telemetria Orbital")
    if not df_filtrado.empty:
        grafico_placeholder = st.empty() 
        with st.spinner("Calculando telemetría..."):
            fig = go.Figure(go.Scattergeo(
                lon=df_filtrado['lon'], lat=df_filtrado['lat'], mode='markers',
                marker=dict(size=7, color=df_filtrado['COLOR_STR'], line=dict(width=0.5, color='white'), opacity=0.8),
                text=df_filtrado['CIUDAD'] + " (" + df_filtrado['FORMA'] + ")", hoverinfo='text'
            ))
            fig.update_layout(
                geo=dict(projection_type='orthographic', showland=True, landcolor='#1e1e1e', showocean=True, oceancolor='#0a0a0a', bgcolor='#0a0a0a'),
                margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='#0a0a0a', height=450
            )
            grafico_placeholder.plotly_chart(fig, use_container_width=True)

# --- INDICADORES RAPIDOS TACTICOS ---
m1, m2, m3 = st.columns(3)
m1.metric("Registros Activos", f"{len(df_filtrado):,}")
m2.metric("Tipologia Predominante", df_filtrado['FORMA'].mode().iloc[0] if not df_filtrado.empty else "N/A")
m3.metric("Zonas de Interes (Nodos)", f"{len(df_filtrado['CIUDAD'].unique()) if not df_filtrado.empty else 0:,}")
st.markdown("---")


# --- MODULOS OPERATIVOS (DESPLEGABLES) ---

with st.expander("NODOS Y CONEXIONES (PUENTES)", expanded=False):
    st.markdown("#### Analisis de Red")
    st.info("Módulo de grafos relacionales pendiente de inicialización en futuras fases de desarrollo.")

with st.expander(f"REGISTROS FORENSES ({len(df_filtrado)} Activos)", expanded=True):
    if not df_filtrado.empty:
        cols_excluir = ['COLOR_STR', 'lat', 'lon', 'DECADA', 'ORD.', 'NUM.', 'Source_File']
        cols_vis = [c for c in df_filtrado.columns if c not in cols_excluir]
        
        # Lógica de carga selectiva y seguridad de renderizado
        filtros_activos = (sel_anio != "TODOS") or (sel_mes != "TODOS") or (sel_forma != "TODOS") or (sel_pais != "TODOS")
        
        if not filtros_activos:
            st.info("Sistema en reposo. Mostrando previsualización de los 100 registros más recientes. Active los filtros tácticos para una búsqueda específica.")
            df_mostrar = df_filtrado.sort_values(by=['AÑO','MES','DIA'], ascending=False).head(100)
        else:
            if len(df_filtrado) > 1000:
                st.warning(f"Búsqueda masiva detectada ({len(df_filtrado)} resultados). Mostrando los 1000 más relevantes para garantizar la estabilidad del sistema.")
                df_mostrar = df_filtrado.sort_values(by=['AÑO','MES','DIA'], ascending=False).head(1000)
            else:
                df_mostrar = df_filtrado.sort_values(by=['AÑO','MES','DIA'], ascending=False)
        
        # Inyectamos el estilo oscuro corporativo
        df_estilizado = df_mostrar[cols_vis].style.set_properties(**{
            'background-color': '#0a0a0a',
            'color': '#cbd5e1',
            'border-color': '#333333'
        })
        
        # Renderizado con la nueva sintaxis de Streamlit
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
        caso_sel = st.selectbox("Seleccionar Expediente Forense", df_nlp['TAG'].unique(), key="select_nlp")
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
                st.warning("Falta credencial DEEPSEEK_API_KEY en configuración del sistema.")
