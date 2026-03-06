# ====================================================================
# ARCHIVO PRINCIPAL: Agatha_Fani.py
# SISTEMA: Motor de Analisis Conductual Predictivo
# MODULO: Inteligencia FANI (Carga Real de CSV y Casos)
# ====================================================================

import streamlit as st

# --- CONFIGURACION DE PAGINA ---
st.set_page_config(
    page_title="AGATHA - Inteligencia Predictiva",
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

# --- CSS CORPORATIVO MATE ---
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
OPERADOR_ID = "DIR-74"
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

# --- GESTION DE SECRETOS ---
mapbox_token = st.secrets.get("MAPBOX_API_KEY", None) if hasattr(st, "secrets") else None
openai_token = st.secrets.get("OPENAI_API_KEY", None) if hasattr(st, "secrets") else None

# --- BUSQUEDA DE ARCHIVOS ---
def encontrar_archivo(nombre):
    if os.path.exists(nombre): return nombre
    if os.path.exists(os.path.join("data", nombre)): return os.path.join("data", nombre)
    return None

# --- MOTORES DE INGESTA DE DATOS ---
@st.cache_data(show_spinner=False)
def cargar_nodos():
    ruta = encontrar_archivo("agatha_ufo_nodes_full.csv")
    if not ruta:
        ruta = encontrar_archivo("agatha_ufo_nodes.csv") # Nombre alternativo
        
    if ruta:
        try:
            df = pd.read_csv(ruta, on_bad_lines='skip', engine='python')
        except Exception:
            df = pd.read_csv(ruta, sep=';', on_bad_lines='skip', engine='python')
            
        # Limpieza de cabeceras (Eliminar guiones bajos)
        df.columns = [str(c).strip().replace('_', ' ').title() for c in df.columns]
        
        # Mapeo forzoso de columnas clave
        mapeo = {"City": "Ciudad", "Country": "Pais", "Shape": "Forma", "Summary": "Resumen", "Year": "Ano"}
        for col_orig, col_dest in mapeo.items():
            if col_orig in df.columns: df.rename(columns={col_orig: col_dest}, inplace=True)
            elif col_orig.title() in df.columns: df.rename(columns={col_orig.title(): col_dest}, inplace=True)

        if 'Resumen' not in df.columns: df['Resumen'] = "Reporte clasificado o no disponible."
        if 'Forma' not in df.columns: df['Forma'] = "Desconocido"
        if 'Pais' not in df.columns: df['Pais'] = "EEUU"
        if 'Ciudad' not in df.columns: df['Ciudad'] = "Zona Operativa"
        if 'Ano' not in df.columns: df['Ano'] = 2024

        df['Forma'] = df['Forma'].fillna("Desconocido").astype(str)
        df['Resumen'] = df['Resumen'].fillna("").astype(str)

        # Inyeccion logica de Coordenadas si no existen
        if 'Latitud' not in df.columns or 'Longitud' not in df.columns:
            lats, lons = [], []
            for _, row in df.iterrows():
                pais = str(row.get('Pais', '')).upper()
                ciudad = str(row.get('Ciudad', ''))
                # Hash simple para que la misma ciudad caiga en el mismo punto siempre
                offset_lat = (hash(ciudad) % 100) / 100.0
                offset_lon = (hash(ciudad[::-1]) % 100) / 100.0
                
                if "MARRUECOS" in pais or "MOROCCO" in pais:
                    lats.append(28.0 + (7.0 * offset_lat))
                    lons.append(-11.0 + (10.0 * offset_lon))
                elif "ESP" in pais or "SPAIN" in pais:
                    lats.append(36.0 + (7.0 * offset_lat))
                    lons.append(-9.0 + (12.0 * offset_lon))
                else: # Default Norteamerica
                    lats.append(30.0 + (18.0 * offset_lat))
                    lons.append(-125.0 + (55.0 * offset_lon))
            df['Latitud'] = lats
            df['Longitud'] = lons

        def asignar_color(forma):
            f = str(forma).lower()
            if "tri" in f: return [225, 29, 72, 200]
            elif "orb" in f or "esfera" in f or "disk" in f: return [234, 179, 8, 200]
            elif "cigar" in f or "cilindro" in f: return [34, 197, 94, 200]
            elif "octa" in f or "pyramid" in f: return [56, 189, 248, 200]
            else: return [148, 163, 184, 150]
        
        df['Color Rgb'] = df['Forma'].apply(asignar_color)
        return df
    else:
        st.error("Archivo agatha_ufo_nodes_full.csv no encontrado en la raiz ni en data/")
        return pd.DataFrame()

@st.cache_data(show_spinner=False)
def cargar_relaciones(df_nodos):
    ruta = encontrar_archivo("agatha_ufo_relationships_sample.csv")
    if not ruta: ruta = encontrar_archivo("agatha_ufo_relationships.csv")
    
    if ruta and not df_nodos.empty:
        try:
            df_rel = pd.read_csv(ruta, on_bad_lines='skip', engine='python')
        except:
            df_rel = pd.read_csv(ruta, sep=';', on_bad_lines='skip', engine='python')
            
        df_rel.columns = [str(c).strip().replace('_', ' ').title() for c in df_rel.columns]
        
        col_src = [c for c in df_rel.columns if "Source" in c]
        col_tgt = [c for c in df_rel.columns if "Target" in c]
        
        edges = []
        if col_src and col_tgt:
            for _, row in df_rel.head(300).iterrows():
                try:
                    idx_orig = int(row[col_src[0]]) % len(df_nodos)
                    idx_dest = int(row[col_tgt[0]]) % len(df_nodos)
                    nodo_a = df_nodos.iloc[idx_orig]
                    nodo_b = df_nodos.iloc[idx_dest]
                    edges.append({
                        'Origen Lon': nodo_a['Longitud'], 'Origen Lat': nodo_a['Latitud'],
                        'Destino Lon': nodo_b['Longitud'], 'Destino Lat': nodo_b['Latitud'],
                        'Color': nodo_a.get('Color Rgb', [148, 163, 184, 150])
                    })
                except: continue
        return pd.DataFrame(edges)
    return pd.DataFrame()

df_maestro = cargar_nodos()
df_grafos = cargar_relaciones(df_maestro)

# --- RENDERIZADO TABLA HTML ---
def render_tabla_tactica(df):
    html = '<div class="contenedor-tabla"><table class="rejilla-tactica"><thead><tr>'
    columnas_validas = [c for c in df.columns if c not in ['Color Rgb', 'Latitud', 'Longitud']]
    for col in columnas_validas: html += f'<th>{col}</th>'
    html += '</tr></thead><tbody>'
    for _, row in df.iterrows():
        html += '<tr>'
        for col in columnas_validas:
            val = row[col]
            clase = 'valor-num' if isinstance(val, (int, float)) else ''
            html += f'<td class="{clase}">{val}</td>'
        html += '</tr>'
    html += '</tbody></table></div>'
    st.markdown(html, unsafe_allow_html=True)

# --- TERMINAL DE OPERACIONES (SIDEBAR) ---
st.sidebar.markdown("### Centro de Comando AGATHA")
filtro_region = st.sidebar.selectbox("Filtro Geopolitico:", ["Global", "Marruecos y España", "Norteamerica"])

if not df_maestro.empty:
    formas_disp = df_maestro['Forma'].unique()
    filtro_forma = st.sidebar.multiselect("Clasificacion de Nave:", formas_disp, default=formas_disp[:4] if len(formas_disp)>4 else formas_disp)
    df_filtrado = df_maestro[df_maestro['Forma'].isin(filtro_forma)].copy()
else:
    df_filtrado = pd.DataFrame()

mostrar_lineas = st.sidebar.toggle("Habilitar Grafos de Trayectoria", value=True)
mostrar_calor = st.sidebar.toggle("Habilitar Conglomeracion (Heatmap)")

# --- ENCABEZADO ---
st.markdown("<h1>Motor de Analisis Conductual Predictivo</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-top:-15px; color:#94a3b8;'>Modulo de Inteligencia FANI (Red Multimodal)</h3>", unsafe_allow_html=True)
st.markdown("---")

# --- METRICAS ESTRATEGICAS ---
total_casos = len(df_filtrado)
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Volumen de Detecciones", f"{total_casos:,}")
col_m2.metric("Nivel de Amenaza Global", "Elevado", "Validacion Radar", delta_color="inverse")
col_m3.metric("Firma Fenomenologica", "Activa")
col_m4.metric("Nodos de Grafo", f"{len(df_grafos) if mostrar_lineas else 0:,}")

# --- ARQUITECTURA DE PESTAÑAS ---
tab_visor, tab_datos, tab_analisis = st.tabs(["Visor Geoespacial Multimodal", "Registros de Inteligencia", "Analisis Forense de Casos (NLP)"])

with tab_visor:
    st.markdown("#### Proyeccion de Nodos y Rutas de Vigilancia")
    
    if not df_filtrado.empty:
        if filtro_region == "Marruecos y España":
            cam_lat, cam_lon, zoom_level = 34.0, -4.0, 4.5
        elif filtro_region == "Norteamerica":
            cam_lat, cam_lon, zoom_level = 39.8, -98.5, 3.5
        else:
            cam_lat, cam_lon, zoom_level = 30.0, -40.0, 2.0
            
        view_state = pdk.ViewState(latitude=cam_lat, longitude=cam_lon, zoom=zoom_level, pitch=45, bearing=0)
        capas = []
        
        capas.append(pdk.Layer(
            "ScatterplotLayer", data=df_filtrado, get_position=["Longitud", "Latitud"],
            get_radius=30000, get_fill_color="Color Rgb", pickable=True, auto_highlight=True
        ))

        if mostrar_lineas and not df_grafos.empty:
            capas.append(pdk.Layer(
                "ArcLayer", data=df_grafos, get_source_position=["Origen Lon", "Origen Lat"],
                get_target_position=["Destino Lon", "Destino Lat"], get_source_color="Color",
                get_target_color="Color", get_width=3, pickable=True
            ))

        if mostrar_calor:
            capas.append(pdk.Layer(
                "HeatmapLayer", data=df_filtrado, get_position=["Longitud", "Latitud"],
                opacity=0.6, get_weight=1
            ))

        estilo_mapa_3d = "mapbox://styles/mapbox/dark-v11" if mapbox_token else "carto-darkmatter"
        dic_api = {"mapbox": mapbox_token} if mapbox_token else None

        st.pydeck_chart(pdk.Deck(api_keys=dic_api, map_style=estilo_mapa_3d, initial_view_state=view_state, layers=capas, tooltip={"text": "Ciudad: {Ciudad}\nForma: {Forma}\nAño: {Ano}"}))
    else:
        st.warning("El mapa requiere la carga correcta de datos.")

with tab_datos:
    st.markdown("#### Archivos de Inteligencia Extraidos")
    if not df_filtrado.empty:
        cols_mostrar = [c for c in df_filtrado.columns if c in ['Ciudad', 'Pais', 'Forma', 'Ano', 'Resumen']]
        df_display = df_filtrado[cols_mostrar].head(100).copy() if cols_mostrar else df_filtrado.head(100).copy()
        render_tabla_tactica(df_display)

with tab_analisis:
    col_a1, col_a2 = st.columns([1, 1])
    
    with col_a1:
        st.markdown("#### Procesador de Atestados Reales (NLP)")
        st.markdown("<p style='color: #94a3b8; font-size:0.9rem;'>Seleccione un caso real de la base de datos para su analisis tactico.</p>", unsafe_allow_html=True)
        
        if not df_filtrado.empty and 'Resumen' in df_filtrado.columns:
            # Crear lista legible para el selector
            df_filtrado['Filtro Visual'] = df_filtrado['Ciudad'].astype(str) + " - " + df_filtrado['Forma'].astype(str) + " (" + df_filtrado['Ano'].astype(str) + ")"
            caso_seleccionado = st.selectbox("Expediente de Inteligencia:", df_filtrado['Filtro Visual'].unique())
            
            # Extraer el resumen real del CSV
            texto_real = df_filtrado[df_filtrado['Filtro Visual'] == caso_seleccionado]['Resumen'].iloc[0]
            
            st.text_area("Cuerpo del Informe:", value=texto_real, height=130, disabled=True)
            
            if st.button("Ejecutar Analisis Forense", type="primary", width="stretch"):
                with st.spinner("Procesando datos estructurales..."):
                    if openai_token:
                        try:
                            cliente_ai = OpenAI(api_key=openai_token)
                            sys_prompt = "Extrae del texto: 1. COMPORTAMIENTO (Breve) 2. NIVEL DE AMENAZA (Critico o Estandar). Separa con barra vertical (|)."
                            resp = cliente_ai.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": texto_real}], temperature=0.1)
                            datos = resp.choices[0].message.content.split("|")
                            comportamiento = datos[0].strip() if len(datos) > 0 else "No Concluyente"
                            amenaza = datos[1].strip() if len(datos) > 1 else "Estandar"
                        except:
                            comportamiento, amenaza = "Fallo de API", "Desconocido"
                    else:
                        time.sleep(1) # Simulacion
                        comportamiento = "Movimiento anomalo detectado"
                        amenaza = "ELEVADO"

                    color_am = "#f43f5e" if "Critic" in amenaza or "Elevad" in amenaza else "#3b82f6"

                    st.markdown(f"""
                    <div style="background-color: #1e293b; border: 1px solid #334155; border-left: 4px solid #10b981; padding: 15px; border-radius: 4px; font-family: 'Titillium Web', sans-serif;">
                        <p style="margin: 8px 0; color: #e2e8f0; font-size: 1rem;"><b>PATRON COMPORTAMENTAL:</b> <span style="color: #38bdf8; font-family: 'Share Tech Mono', monospace; font-size: 1.05rem;">{comportamiento}</span></p>
                        <p style="margin: 8px 0; color: #e2e8f0; font-size: 1rem;"><b>NIVEL AMENAZA:</b> <span style="color: {color_am}; font-family: 'Share Tech Mono', monospace; font-size: 1.05rem; font-weight: bold;">{amenaza}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No hay casos cargados para analizar.")

    with col_a2:
        st.markdown("#### Matriz de Incidencia Estructural")
        if not df_filtrado.empty and 'Forma' in df_filtrado.columns:
            conteo = df_filtrado['Forma'].value_counts().reset_index()
            conteo.columns = ['Forma Estructural', 'Volumen']
            
            fig = px.bar(conteo, x='Volumen', y='Forma Estructural', orientation='h', template="plotly_dark")
            fig.update_traces(marker_color='#3b82f6')
            fig.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            fig.add_annotation(text=f"AGATHA INTEL - {OPERADOR_ID}", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(size=12, color="rgba(255, 255, 255, 0.1)"), textangle=-10)
            st.plotly_chart(fig, use_container_width=True)
