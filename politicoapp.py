import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Spain Political Intelligence 2026",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal y subtítulo de la aplicación
st.title("📊 Spain Political Intelligence 2026")
st.subheader("Análisis de tendencias políticas, económicas y sociales (Mayo – Noviembre 2026)")
st.markdown("---")

with st.sidebar:
    st.header("ℹ️ Sobre el Proyecto")
    st.write(
        "Este panel analiza la evolución de la opinión pública en España, "
        "cruzando encuestas sociológicas con indicadores económicos reales."
    )
    
    st.subheader("🏛️ Fuentes de Datos")
    st.markdown("""
    - **CIS:** Barómetro de septiembre 2026.
    - **More in Common:** Pulso electoral (noviembre 2026, n=2.315).
    - **INE:** Índice de Precios de Vivienda (Q2 2026).
    - **Ministerio del Interior:** Balance migratorio (Ene-Oct 2026).
    """)
    
    st.warning(
        "⚠️ Nota metodológica: Los datos intermedios de la serie temporal son "
        "estimaciones extraídas de gráficos; los datos de noviembre son exactos."
    )


# Datos 1: Evolución de problemas sociales (Fuente: More in Common)
data_evolucion = {
    "Mes": ["Mayo", "Julio", "Septiembre", "Octubre", "Noviembre"],
    "Vivienda": [42.8, 40.5, 38.2, 44.0, 50.2],
    "Inmigración": [28.2, 29.4, 46.4, 38.0, 43.6],
    "Inflación": [33.0, 27.3, 26.3, 29.6, 31.7],
    "Corrupción": [31.2, 38.0, 35.0, 31.2, 30.7],
    "Sanidad": [25.2, 25.1, 21.3, 24.5, 25.3]
}
df_evolucion = pd.DataFrame(data_evolucion)

# Datos 2: Barómetro CIS Septiembre 2026 (Principales problemas)
data_cis = {
    "Problema": [
        "Vivienda", "Crisis económica", "Inmigración", "Gobierno y políticos",
        "Problemas políticos en general", "Calidad del empleo", "Paro", "Sanidad"
    ],
    "Porcentaje": [37.5, 21.6, 19.7, 18.8, 13.9, 13.7, 11.5, 11.1]
}
df_cis = pd.DataFrame(data_cis)

# Datos 3: Prioridades según orientación ideológica (Noviembre 2026)
data_ideologia = {
    "Problema": ["Vivienda", "Sanidad", "Inflación", "Inmigración", "Corrupción"],
    "Izquierda": [62.9, 32.1, 29.2, 25.9, None],
    "Centro": [47.4, 26.0, 30.3, 48.6, 32.2],
    "Derecha": [41.0, None, 33.0, 61.0, 44.3]
}
df_ideologia = pd.DataFrame(data_ideologia)

# Datos 4: Índice de Precios de Vivienda (Fuente: INE - Variación anual %)
data_vivienda = {
    "Trimestre": [
        "2024 Q3", "2024 Q4", "2025 Q1", "2025 Q2",
        "2025 Q3", "2025 Q4", "2026 Q1", "2026 Q2"
    ],
    "General": [8.1, 11.3, 12.2, 12.7, 12.8, 12.9, 12.9, 12.2],
    "Vivienda Nueva": [9.8, 12.3, 12.2, 12.1, 9.7, 11.2, 9.1, 7.4],
    "Segunda Mano": [7.9, 11.1, 12.3, 12.8, 13.4, 13.1, 13.5, 12.9]
}
df_vivienda = pd.DataFrame(data_vivienda)

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Opinión Pública", 
    "🧭 Polarización Ideológica", 
    "🏠 Economía y Migración", 
    "🧠 Conclusiones y Estrategia"
])

with tab1:
    st.header("1. Evolución de las Preocupaciones Ciudadanas (More in Common)")
    st.write("Porcentaje de encuestados que mencionan cada tema entre los tres principales problemas del país.")
    
    # Selector interactivo para filtrar las líneas del gráfico
    problemas_seleccionados = st.multiselect(
        "Selecciona los problemas que deseas visualizar en el gráfico:",
        options=["Vivienda", "Inmigración", "Inflación", "Corrupción", "Sanidad"],
        default=["Vivienda", "Inmigración", "Corrupción"]
    )
    
    if problemas_seleccionados:
        # Gráfico de líneas interactivo con Plotly
        fig_evolucion = px.line(
            df_evolucion,
            x="Mes",
            y=problemas_seleccionados,
            markers=True,
            title="Dinámica del descontento social (Mayo - Noviembre 2026)",
            labels={"value": "Porcentaje (%)", "Mes": "Periodo", "variable": "Problema"}
        )
        fig_evolucion.update_layout(hovermode="x unified")
        st.plotly_chart(fig_evolucion, width="stretch")
    else:
        st.warning("Por favor, selecciona al menos un problema para mostrar el gráfico.")

    st.markdown("---")
    
    # Dos columnas: Tabla de evolución y Gráfico del CIS
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tabla de datos: More in Common (%)")
        st.dataframe(df_evolucion, width="stretch")
        
    with col2:
        st.subheader("Referencia: Barómetro CIS (Septiembre 2026)")
        fig_cis = px.bar(
            df_cis.sort_values(by="Porcentaje", ascending=True),
            x="Porcentaje",
            y="Problema",
            orientation="h",
            title="Principales problemas según el CIS (%)",
            color="Porcentaje",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_cis, width="stretch")

with tab2:
    st.header("2. Prioridades Políticas según Ideología")
    st.write(
        "El estudio de More in Common (noviembre 2026) revela una fuerte polarización: "
        "mientras la izquierda prioriza la vivienda, el centro y la derecha sitúan la inmigración en primer lugar."
    )
    
    # Transformar la tabla de formato ancho a largo para graficar barras agrupadas
    df_ideologia_largo = df_ideologia.melt(
        id_vars="Problema",
        var_name="Grupo Político",
        value_name="Porcentaje"
    )
    
    # Definir colores representativos para cada bloque ideológico
    colores_politicos = {
        "Izquierda": "#E63946",  # Rojo
        "Centro": "#F4A261",     # Naranja/Ámbar
        "Derecha": "#1D3557"     # Azul oscuro
    }
    
    fig_ideologia = px.bar(
        df_ideologia_largo,
        x="Problema",
        y="Porcentaje",
        color="Grupo Político",
        barmode="group",
        color_discrete_map=colores_politicos,
        title="Comparativa de preocupaciones por bloque ideológico (%)"
    )
    st.plotly_chart(fig_ideologia, width="stretch")
    
    with st.expander("Ver tabla de datos ideológicos"):
        st.dataframe(df_ideologia, width="stretch")

with tab3:
    st.header("3. Datos Reales: Mercado Inmobiliario y Flujos Migratorios")
    
    # Sección Vivienda (INE)
    st.subheader("📈 Evolución del Precio de la Vivienda (INE)")
    st.write("Variación anual del Índice de Precios de Vivienda (IPV). La vivienda de segunda mano lidera las subidas.")
    
    fig_vivienda = px.line(
        df_vivienda,
        x="Trimestre",
        y=["General", "Vivienda Nueva", "Segunda Mano"],
        markers=True,
        title="Crecimiento interanual del precio de la vivienda en España (%)",
        labels={"value": "Variación Anual (%)", "variable": "Tipología"}
    )
    fig_vivienda.update_layout(hovermode="x unified")
    st.plotly_chart(fig_vivienda, width="stretch")
    
    st.markdown("---")
    
    # Sección Inmigración (Ministerio del Interior)
    st.subheader("🛂 Balance Migratorio: Llegadas Irregulares (Enero - Octubre 2026)")
    st.write("Datos oficiales del Ministerio del Interior (vía marítima y terrestre).")
    
    # Tarjetas de métricas (KPIs)
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric(label="Llegadas Ene-Oct 2025", value="30.263 personas")
    kpi2.metric(label="Llegadas Ene-Oct 2026", value="32.942 personas", delta="+2.679 personas")
    kpi3.metric(label="Variación Interanual", value="+8,9%", delta="Incremento", delta_color="inverse")

with tab4:
    st.header("4. Síntesis Analítica y Procesos Clave")
    
    # Cálculo automático de variaciones entre mayo y noviembre
    ultimo_mes = df_evolucion.iloc[-1]
    primer_mes = df_evolucion.iloc[0]
    
    # Identificar el problema principal actual (excluyendo la columna 'Mes')
    problema_principal = ultimo_mes[1:].idxmax()
    valor_principal = ultimo_mes[problema_principal]
    
    cambio_vivienda = ultimo_mes["Vivienda"] - primer_mes["Vivienda"]
    cambio_inmigracion = ultimo_mes["Inmigración"] - primer_mes["Inmigración"]
    
    # Mostrar tarjetas de resumen calculadas dinámicamente
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Principal Problema (Nov 2026)", problema_principal, f"{valor_principal}%")
    col_m2.metric("Variación Vivienda (May-Nov)", f"{ultimo_mes['Vivienda']}%", f"{cambio_vivienda:+.1f} pts")
    col_m3.metric("Variación Inmigración (May-Nov)", f"{ultimo_mes['Inmigración']}%", f"{cambio_inmigracion:+.1f} pts")
    
    st.markdown("---")
    
    # Conclusiones estructurales del informe
    st.subheader("📌 Cinco procesos estructurales identificados:")
    st.markdown("""
    1. **La vivienda como eje central:** Ha dejado de ser un problema exclusivo de los jóvenes para convertirse en una crisis transversal y de confianza institucional.
    2. **Polarización en torno a la inmigración:** Actúa como el principal divisor entre bloques ideológicos (61,0% en la derecha frente al 25,9% en la izquierda).
    3. **Desgaste por corrupción:** Con un 30,7% de menciones, mantiene una presión constante sobre la estabilidad del sistema político.
    4. **Comunicación política y agenda:** Consultores y estrategas (como Iván Redondo, Miguel Ángel Rodríguez o Aleix Sanmartín) moldean el marco emocional y el debate público.
    5. **Analítica de datos avanzada:** El uso de Python, modelos predictivos y análisis de sentimiento redefine las campañas electorales modernas.
    """)

st.markdown("---")
st.info(
    "📌 **Descargo de responsabilidad:** Esta investigación tiene carácter descriptivo. "
    "Las correlaciones estadísticas o encuestas de opinión no implican necesariamente causalidad directa."
)
st.caption("Spain Political Intelligence Dashboard | Desarrollado con Python, Pandas, Plotly y Streamlit | 2026")

