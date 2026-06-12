# ============================================================
# Importación de herramientas que necesitará la app
# ============================================================

from pathlib import Path
import base64

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================
# Rutas del proyecto
# ============================================================

APP_PATH = Path(__file__).resolve()
PROJECT_ROOT = APP_PATH.parents[1]

DATA_PATH = PROJECT_ROOT / "data" / "final"
MODEL_PATH = PROJECT_ROOT / "models"
ASSETS_PATH = PROJECT_ROOT / "assets"

APP_ICON = ASSETS_PATH / "app_page_icon.png"
HEADER_ICON = ASSETS_PATH / "header_icon.png"

RANKING_FILE = DATA_PATH / "hr_process_automation_ranking_clean.csv"
MODEL_FILE = MODEL_PATH / "automation_priority_model.pkl"


# ============================================================
# Configuración general de la app
# ============================================================

st.set_page_config(
    page_title="HR Process Automation Scanner",
    page_icon=str(APP_ICON),
    layout="wide"
)

def load_custom_css():
    st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 1500px;
        }

        section[data-testid="stSidebar"] {
            background-color: #F8FAFC;
            border-right: 1px solid #E5E7EB;
        }

        .main-title {
            font-size: 2.4rem;
            font-weight: 800;
            color: #111827;
            margin-bottom: 0.3rem;
        }

        .main-subtitle {
            font-size: 1.02rem;
            color: #4B5563;
            margin-bottom: 1.2rem;
        }

        .section-title {
            font-size: 1.8rem;
            font-weight: 700;
            color: #111827;
            margin-top: 0.5rem;
            margin-bottom: 1rem;
        }

        .kpi-card {
            background: white;
            border: 1px solid #E5E7EB;
            border-radius: 18px;
            padding: 18px 20px;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
            min-height: 120px;
        }

        .kpi-label {
            font-size: 0.95rem;
            color: #6B7280;
            margin-bottom: 0.5rem;
        }

        .kpi-value {
            font-size: 2.1rem;
            font-weight: 800;
            color: #111827;
            line-height: 1.1;
        }

        .mini-note {
            font-size: 0.85rem;
            color: #9CA3AF;
            margin-top: 0.4rem;
        }

        div[data-baseweb="tab-list"] {
            gap: 1.5rem;
            border-bottom: 1px solid #E5E7EB;
            margin-bottom: 1.2rem;
        }

        button[data-baseweb="tab"] {
            font-size: 0.95rem;
            font-weight: 600;
            color: #4B5563;
            padding-bottom: 0.6rem;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: #DC2626 !important;
            border-bottom: 3px solid #DC2626 !important;
        }

        .chart-card {
            background: white;
            border: 1px solid #E5E7EB;
            border-radius: 18px;
            padding: 18px;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
            margin-bottom: 1rem;
        }
            .method-card {
            background: white;
            border: 1px solid #E5E7EB;
            border-radius: 18px;
            padding: 22px 24px;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
            margin-bottom: 1rem;
            min-height: 180px;
        }

        .method-title {
            font-size: 1.15rem;
            font-weight: 800;
            color: #111827;
            margin-bottom: 0.6rem;
        }

        .method-text {
            font-size: 0.95rem;
            color: #4B5563;
            line-height: 1.55;
        }

        .badge {
            display: inline-block;
            background-color: #EEF2FF;
            color: #3730A3;
            border-radius: 999px;
            padding: 6px 12px;
            font-size: 0.85rem;
            font-weight: 700;
            margin-right: 0.4rem;
            margin-bottom: 0.4rem;
        }

        .warning-card {
            background: #FFFBEB;
            border: 1px solid #FDE68A;
            border-radius: 18px;
            padding: 20px 22px;
            color: #78350F;
            margin-top: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
load_custom_css()


# ============================================================
# Funciones de carga
# ============================================================

@st.cache_data
def load_data():
    data = pd.read_csv(RANKING_FILE)
    return data


@st.cache_resource
def load_model():
    model = joblib.load(MODEL_FILE)
    return model


df = load_data()
model = load_model()

# ============================================================
# Título principal
# ============================================================

import base64

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


header_icon_base64 = image_to_base64(HEADER_ICON)

st.markdown(f"""
<div style="
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 0.9rem;
">
    <img src="data:image/png;base64,{header_icon_base64}" style="
        width: 48px;
        height: 48px;
        object-fit: contain;
        flex-shrink: 0;
    ">
    <div>
        <div class="main-title">HR Process Automation Scanner</div>
        <div class="main-subtitle">
            Herramienta analítica para identificar, priorizar y recomendar oportunidades de automatización en procesos de HR Operations.
        </div>
        <div class="main-subtitle">
            La aplicación combina análisis operativo, reglas de negocio y Machine Learning para clasificar unidades operativas según su prioridad de automatización.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# Sidebar — filtros
# ============================================================

st.sidebar.markdown("## Filtros")
st.sidebar.markdown(
    "Ajusta la vista para explorar oportunidades específicas de automatización."
)

# Botón para resetear filtros
reset_filters = st.sidebar.button("Restablecer filtros")

if reset_filters:
    selected_processes = sorted(df["hr_process_name"].dropna().unique())
    selected_systems = sorted(df["hr_system_name"].dropna().unique())
    selected_regions = sorted(df["region"].dropna().unique())
    selected_channels = sorted(df["hr_contact_channel"].dropna().unique())
    selected_priorities = sorted(df["automation_priority"].dropna().unique())
else:
    selected_processes = sorted(df["hr_process_name"].dropna().unique())
    selected_systems = sorted(df["hr_system_name"].dropna().unique())
    selected_regions = sorted(df["region"].dropna().unique())
    selected_channels = sorted(df["hr_contact_channel"].dropna().unique())
    selected_priorities = sorted(df["automation_priority"].dropna().unique())


with st.sidebar.expander("Proceso HR", expanded=False):
    process_filter = st.multiselect(
        "Selecciona procesos",
        options=sorted(df["hr_process_name"].dropna().unique()),
        default=selected_processes,
        label_visibility="collapsed"
    )

with st.sidebar.expander("Sistema HR", expanded=False):
    system_filter = st.multiselect(
        "Selecciona sistemas",
        options=sorted(df["hr_system_name"].dropna().unique()),
        default=selected_systems,
        label_visibility="collapsed"
    )

with st.sidebar.expander("Región", expanded=False):
    region_filter = st.multiselect(
        "Selecciona regiones",
        options=sorted(df["region"].dropna().unique()),
        default=selected_regions,
        label_visibility="collapsed"
    )

with st.sidebar.expander("Canal interno HR", expanded=False):
    channel_filter = st.multiselect(
        "Selecciona canales",
        options=sorted(df["hr_contact_channel"].dropna().unique()),
        default=selected_channels,
        label_visibility="collapsed"
    )

with st.sidebar.expander("Prioridad de automatización", expanded=True):
    priority_filter = st.multiselect(
        "Selecciona prioridades",
        options=sorted(df["automation_priority"].dropna().unique()),
        default=selected_priorities,
        label_visibility="collapsed"
    )


filtered_df = df[
    (df["hr_process_name"].isin(process_filter)) &
    (df["hr_system_name"].isin(system_filter)) &
    (df["region"].isin(region_filter)) &
    (df["hr_contact_channel"].isin(channel_filter)) &
    (df["automation_priority"].isin(priority_filter))
].copy()


st.sidebar.divider()

st.sidebar.metric(
    "Unidades filtradas",
    f"{len(filtered_df):,.0f}"
)

st.sidebar.metric(
    "Casos filtrados",
    f"{int(filtered_df['total_cases'].sum()):,.0f}"
)


# ============================================================
# Tabs principales
# ============================================================

tab_overview, tab_ranking, tab_simulator, tab_about = st.tabs(
    [
        "Resumen ejecutivo",
        "Ranking de automatización",
        "Simulador predictivo",
        "Metodología"
    ]
)


# ============================================================
# TAB 1 — Resumen ejecutivo
# ============================================================

with tab_overview:
    total_units = len(filtered_df)
    total_cases = int(filtered_df["total_cases"].sum())
    avg_score = round(filtered_df["automation_score"].mean(), 2)
    total_saved_hours = round(filtered_df["estimated_operational_hours_saved"].sum(), 0)

    st.markdown(
        '<div class="section-title">Resumen ejecutivo</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Unidades operativas</div>
            <div class="kpi-value">{total_units:,.0f}</div>
            <div class="mini-note">Combinaciones analizadas</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Casos analizados</div>
            <div class="kpi-value">{total_cases:,.0f}</div>
            <div class="mini-note">Volumen total procesado</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Score promedio</div>
            <div class="kpi-value">{avg_score:,.2f}</div>
            <div class="mini-note">Potencial medio de automatización</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Horas ahorrables</div>
            <div class="kpi-value">{total_saved_hours:,.0f}</div>
            <div class="mini-note">Ahorro operativo estimado</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ========================================================
    # Distribución de prioridad
    # ========================================================

    col_left, col_right = st.columns([1, 1.35])

    with col_left:
        st.markdown(
            '<div class="section-title">Distribución de prioridad</div>',
            unsafe_allow_html=True
        )

        priority_summary = (
            filtered_df["automation_priority"]
            .value_counts()
            .reset_index()
        )

        priority_summary.columns = ["automation_priority", "total_units"]

        priority_order = ["Alta", "Media", "Baja"]

        priority_summary["automation_priority"] = pd.Categorical(
            priority_summary["automation_priority"],
            categories=priority_order,
            ordered=True
        )

        priority_summary = priority_summary.sort_values("automation_priority")

        priority_colors = {
            "Alta": "#DC2626",
            "Media": "#F59E0B",
            "Baja": "#10B981"
        }

        priority_fig = px.pie(
            priority_summary,
            names="automation_priority",
            values="total_units",
            color="automation_priority",
            color_discrete_map=priority_colors,
            hole=0.68
        )

        priority_fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(line=dict(color="white", width=3))
        )

        priority_fig.add_annotation(
            text=f"<b>{total_units:,.0f}</b><br>unidades",
            x=0.5,
            y=0.5,
            font=dict(size=20, color="#111827"),
            showarrow=False
        )

        priority_fig.update_layout(
            showlegend=False,
            height=390,
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="white",
            plot_bgcolor="white"
        )

        st.plotly_chart(priority_fig, use_container_width=True)

    with col_right:
        st.markdown(
            '<div class="section-title">Top 10 procesos por ahorro estimado</div>',
            unsafe_allow_html=True
        )

        process_summary = (
            filtered_df
            .groupby("hr_process_name", as_index=False)
            .agg(
                total_estimated_hours_saved=("estimated_operational_hours_saved", "sum")
            )
            .sort_values("total_estimated_hours_saved", ascending=False)
            .head(10)
        )

        process_summary = process_summary.sort_values(
            "total_estimated_hours_saved",
            ascending=True
        )

        process_fig = px.bar(
            process_summary,
            x="total_estimated_hours_saved",
            y="hr_process_name",
            orientation="h",
            text="total_estimated_hours_saved"
        )

        process_fig.update_traces(
            marker_color="#2563EB",
            texttemplate="%{text:,.0f}",
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Horas: %{x:,.0f}<extra></extra>"
        )

        process_fig.update_layout(
            height=390,
            margin=dict(t=10, b=20, l=10, r=80),
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis_title="Horas operativas estimadas ahorrables",
            yaxis_title="",
            xaxis=dict(showgrid=True, gridcolor="#E5E7EB", zeroline=False),
            yaxis=dict(showgrid=False),
            showlegend=False
        )

        st.plotly_chart(process_fig, use_container_width=True)

    st.divider()

    # ========================================================
    # Principales oportunidades
    # ========================================================

    st.markdown(
        '<div class="section-title">Principales oportunidades detectadas</div>',
        unsafe_allow_html=True
    )

    overview_columns = [
        "ranking",
        "hr_process_name",
        "hr_system_name",
        "region",
        "hr_contact_channel",
        "total_cases",
        "automation_score",
        "automation_priority",
        "recommended_solution",
        "estimated_operational_hours_saved"
    ]

    st.dataframe(
        filtered_df[overview_columns]
        .sort_values("ranking")
        .head(10),
        use_container_width=True,
        hide_index=True
    )

    
# ============================================================
# TAB 2 — Ranking
# ============================================================

with tab_ranking:
    st.markdown(
        '<div class="section-title">Ranking de oportunidades de automatización</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        Esta sección permite explorar las unidades operativas con mayor oportunidad de automatización.
        Cada fila representa una combinación específica de proceso HR, sistema HR, región y canal interno.
        """
    )

    ranking_filtered = filtered_df.sort_values("ranking").copy()

    high_priority_units = int(
        (ranking_filtered["automation_priority"] == "Alta").sum()
    )

    top_score = round(ranking_filtered["automation_score"].max(), 2)

    top_savings = round(
        ranking_filtered["estimated_operational_hours_saved"].max(),
        0
    )

    avg_cases = round(
        ranking_filtered["total_cases"].mean(),
        0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Prioridad alta</div>
            <div class="kpi-value">{high_priority_units:,.0f}</div>
            <div class="mini-note">Unidades críticas filtradas</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Score máximo</div>
            <div class="kpi-value">{top_score:,.2f}</div>
            <div class="mini-note">Mayor oportunidad detectada</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Mayor ahorro unitario</div>
            <div class="kpi-value">{top_savings:,.0f}</div>
            <div class="mini-note">Horas estimadas en una unidad</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Casos promedio</div>
            <div class="kpi-value">{avg_cases:,.0f}</div>
            <div class="mini-note">Promedio por unidad operativa</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ========================================================
    # Top 10 oportunidades visuales
    # ========================================================

    st.markdown(
        '<div class="section-title">Top 10 oportunidades por score</div>',
        unsafe_allow_html=True
    )

    top_10_ranking = (
        ranking_filtered
        .head(10)
        .sort_values("automation_score", ascending=True)
    )

    top_10_ranking["opportunity_label"] = (
        top_10_ranking["ranking"].astype(str)
        + ". "
        + top_10_ranking["hr_process_name"]
        + " | "
        + top_10_ranking["region"]
    )

    ranking_fig = px.bar(
        top_10_ranking,
        x="automation_score",
        y="opportunity_label",
        orientation="h",
        text="automation_score",
        hover_data={
            "hr_system_name": True,
            "hr_contact_channel": True,
            "total_cases": True,
            "automation_priority": True,
            "recommended_solution": True,
            "estimated_operational_hours_saved": ":,.0f",
            "opportunity_label": False
        }
    )

    ranking_fig.update_traces(
        marker_color="#2563EB",
        texttemplate="%{text:.2f}",
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Score: %{x:.2f}<br>"
            "<extra></extra>"
        )
    )

    ranking_fig.update_layout(
        height=480,
        margin=dict(t=10, b=30, l=10, r=90),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis_title="Automation Opportunity Score",
        yaxis_title="",
        xaxis=dict(showgrid=True, gridcolor="#E5E7EB", zeroline=False),
        yaxis=dict(showgrid=False),
        showlegend=False
    )

    st.plotly_chart(ranking_fig, use_container_width=True)

    st.divider()

    # ========================================================
    # Tabla ejecutiva
    # ========================================================

    st.markdown(
        '<div class="section-title">Matriz de priorización</div>',
        unsafe_allow_html=True
    )

    selected_columns = [
        "ranking",
        "hr_process_name",
        "hr_system_name",
        "region",
        "hr_contact_channel",
        "total_cases",
        "automation_score",
        "automation_priority",
        "recommended_solution",
        "estimated_operational_hours_saved"
    ]

    ranking_table = ranking_filtered[selected_columns].copy()

    st.dataframe(
        ranking_table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ranking": st.column_config.NumberColumn(
                "Ranking",
                help="Posición de la unidad operativa en el ranking final",
                format="%d"
            ),
            "hr_process_name": st.column_config.TextColumn(
                "Proceso HR"
            ),
            "hr_system_name": st.column_config.TextColumn(
                "Sistema HR"
            ),
            "region": st.column_config.TextColumn(
                "Región"
            ),
            "hr_contact_channel": st.column_config.TextColumn(
                "Canal interno"
            ),
            "total_cases": st.column_config.NumberColumn(
                "Casos",
                format="%d"
            ),
            "automation_score": st.column_config.NumberColumn(
                "Score",
                format="%.2f"
            ),
            "automation_priority": st.column_config.TextColumn(
                "Prioridad"
            ),
            "recommended_solution": st.column_config.TextColumn(
                "Solución recomendada"
            ),
            "estimated_operational_hours_saved": st.column_config.NumberColumn(
                "Horas ahorrables",
                format="%.0f"
            )
        }
    )

    csv = ranking_table.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Descargar ranking filtrado",
        data=csv,
        file_name="filtered_automation_ranking.csv",
        mime="text/csv"
    )
    
# ============================================================
# Función de recomendación para simulador
# ============================================================

def recommend_solution_from_inputs(
    automation_priority,
    avg_complexity_score,
    sla_breach_rate,
    hr_contact_channel
):
    if automation_priority == "Alta":
        if avg_complexity_score >= 6.5 and sla_breach_rate >= 0.5:
            return "IA asistida con revisión humana"
        elif hr_contact_channel in ["Email", "Employee Self-Service Portal"] and avg_complexity_score < 6:
            return "Workflow automation"
        elif hr_contact_channel in ["HR Chat / Virtual Assistant", "Internal Collaboration Tool"] and avg_complexity_score < 6:
            return "Chatbot o asistente virtual"
        elif sla_breach_rate >= 0.5:
            return "Automatización parcial con alertas SLA"
        else:
            return "Automatización prioritaria"

    if automation_priority == "Media":
        if avg_complexity_score >= 6:
            return "Rediseño del proceso antes de automatizar"
        elif sla_breach_rate >= 0.5:
            return "Automatización parcial con alertas SLA"
        else:
            return "Automatización parcial"

    if avg_complexity_score >= 7:
        return "Mantener revisión humana"

    return "Baja prioridad de automatización"


def estimate_operational_hours_saved(
    total_cases,
    avg_resolution_time_hours,
    automation_priority
):
    manual_work_rate_mapping = {
        "Alta": 0.18,
        "Media": 0.12,
        "Baja": 0.08
    }

    savings_rate_mapping = {
        "Alta": 0.35,
        "Media": 0.20,
        "Baja": 0.05
    }

    manual_work_rate = manual_work_rate_mapping.get(automation_priority, 0.08)
    savings_rate = savings_rate_mapping.get(automation_priority, 0.05)

    estimated_manual_handling_time = avg_resolution_time_hours * manual_work_rate

    estimated_hours_saved = (
        total_cases *
        estimated_manual_handling_time *
        savings_rate
    )

    return round(estimated_hours_saved, 2)


# ============================================================
# TAB 3 — Simulador predictivo
# ============================================================

with tab_simulator:
    st.markdown(
        '<div class="section-title">Simulador predictivo de automatización</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        Este simulador permite introducir las características de una unidad operativa 
        y predecir su prioridad de automatización usando el modelo de Machine Learning entrenado.
        """
    )

    st.info(
        "Uso recomendado: ajusta los valores operativos de una unidad HR y pulsa el botón para obtener una prioridad, una solución recomendada y una estimación de ahorro."
    )

    st.divider()

    # ========================================================
    # Formulario de entrada
    # ========================================================

    st.markdown(
        '<div class="section-title">Datos de la unidad operativa</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        hr_process_name = st.selectbox(
            "Proceso HR",
            sorted(df["hr_process_name"].dropna().unique())
        )

        hr_system_name = st.selectbox(
            "Sistema HR",
            sorted(df["hr_system_name"].dropna().unique())
        )

        region = st.selectbox(
            "Región",
            sorted(df["region"].dropna().unique())
        )

        hr_contact_channel = st.selectbox(
            "Canal interno HR",
            sorted(df["hr_contact_channel"].dropna().unique())
        )

    with col2:
        total_cases = st.number_input(
            "Total de casos",
            min_value=1,
            max_value=1000,
            value=75
        )

        avg_resolution_time_hours = st.number_input(
            "Tiempo medio de resolución",
            min_value=1.0,
            max_value=300.0,
            value=120.0
        )

        avg_first_response_time_hours = st.number_input(
            "Tiempo medio de primera respuesta",
            min_value=0.1,
            max_value=100.0,
            value=36.0
        )

        avg_previous_cases = st.number_input(
            "Casos previos promedio",
            min_value=0.0,
            max_value=50.0,
            value=10.0
        )

    with col3:
        sla_breach_rate = st.slider(
            "Tasa de incumplimiento SLA",
            min_value=0.0,
            max_value=1.0,
            value=0.50,
            step=0.01
        )

        escalation_rate = st.slider(
            "Tasa de escalación",
            min_value=0.0,
            max_value=1.0,
            value=0.50,
            step=0.01
        )

        avg_complexity_score = st.slider(
            "Complejidad media",
            min_value=1.0,
            max_value=10.0,
            value=5.5,
            step=0.1
        )

        avg_satisfaction_score = st.slider(
            "Satisfacción media",
            min_value=1.0,
            max_value=5.0,
            value=3.0,
            step=0.1
        )

        high_priority_rate = st.slider(
            "Proporción de casos de prioridad alta",
            min_value=0.0,
            max_value=1.0,
            value=0.25,
            step=0.01
        )

        urgent_priority_rate = st.slider(
            "Proporción de casos urgentes",
            min_value=0.0,
            max_value=1.0,
            value=0.25,
            step=0.01
        )

    avg_employee_tenure_months = st.number_input(
        "Antigüedad media del empleado en meses",
        min_value=1.0,
        max_value=120.0,
        value=30.0
    )

    input_data = pd.DataFrame([
        {
            "hr_process_name": hr_process_name,
            "hr_system_name": hr_system_name,
            "hr_contact_channel": hr_contact_channel,
            "region": region,
            "total_cases": total_cases,
            "avg_resolution_time_hours": avg_resolution_time_hours,
            "avg_first_response_time_hours": avg_first_response_time_hours,
            "sla_breach_rate": sla_breach_rate,
            "escalation_rate": escalation_rate,
            "avg_complexity_score": avg_complexity_score,
            "avg_satisfaction_score": avg_satisfaction_score,
            "avg_previous_cases": avg_previous_cases,
            "avg_employee_tenure_months": avg_employee_tenure_months,
            "high_priority_rate": high_priority_rate,
            "urgent_priority_rate": urgent_priority_rate
        }
    ])

    st.divider()

    # ========================================================
    # Predicción
    # ========================================================

    predict_button = st.button(
        "Predecir prioridad de automatización",
        use_container_width=True
    )

    if predict_button:
        prediction = model.predict(input_data)[0]

        predicted_probability = None

        if hasattr(model, "predict_proba"):
            prediction_probabilities = model.predict_proba(input_data)[0]
            predicted_class_index = list(model.classes_).index(prediction)
            predicted_probability = prediction_probabilities[predicted_class_index]

            probability_df = pd.DataFrame({
                "Prioridad": model.classes_,
                "Probabilidad": prediction_probabilities
            })

            probability_df["Probabilidad"] = (
                probability_df["Probabilidad"] * 100
            ).round(2)

        recommended_solution = recommend_solution_from_inputs(
            automation_priority=prediction,
            avg_complexity_score=avg_complexity_score,
            sla_breach_rate=sla_breach_rate,
            hr_contact_channel=hr_contact_channel
        )

        estimated_hours_saved = estimate_operational_hours_saved(
            total_cases=total_cases,
            avg_resolution_time_hours=avg_resolution_time_hours,
            automation_priority=prediction
        )

        if prediction == "Alta":
            priority_color = "#DC2626"
            decision_message = "Prioridad alta: conviene evaluar esta unidad como candidata fuerte para automatización."
        elif prediction == "Media":
            priority_color = "#F59E0B"
            decision_message = "Prioridad media: conviene analizar viabilidad, impacto y dependencias antes de automatizar."
        else:
            priority_color = "#10B981"
            decision_message = "Prioridad baja: no parece ser una candidata inmediata para automatización."

        st.markdown(
            '<div class="section-title">Resultado de la simulación</div>',
            unsafe_allow_html=True
        )

        result_col1, result_col2, result_col3 = st.columns(3)

        with result_col1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Prioridad predicha</div>
                <div class="kpi-value" style="color:{priority_color};">{prediction}</div>
                <div class="mini-note">Clasificación del modelo</div>
            </div>
            """, unsafe_allow_html=True)

        with result_col2:
            confidence_value = (
                f"{predicted_probability * 100:.1f}%"
                if predicted_probability is not None
                else "No disponible"
            )

            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Confianza del modelo</div>
                <div class="kpi-value">{confidence_value}</div>
                <div class="mini-note">Probabilidad de la clase predicha</div>
            </div>
            """, unsafe_allow_html=True)

        with result_col3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Horas ahorrables</div>
                <div class="kpi-value">{estimated_hours_saved:,.0f}</div>
                <div class="mini-note">Estimación operativa conservadora</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Recomendación tecnológica</div>
            <div class="kpi-value" style="font-size:1.6rem;">{recommended_solution}</div>
            <div class="mini-note">{decision_message}</div>
        </div>
        """, unsafe_allow_html=True)

        if predicted_probability is not None:
            st.markdown(
                '<div class="section-title">Probabilidad por clase</div>',
                unsafe_allow_html=True
            )

            probability_fig = px.bar(
                probability_df.sort_values("Probabilidad", ascending=True),
                x="Probabilidad",
                y="Prioridad",
                orientation="h",
                text="Probabilidad",
                color="Prioridad",
                color_discrete_map={
                    "Alta": "#DC2626",
                    "Media": "#F59E0B",
                    "Baja": "#10B981"
                }
            )

            probability_fig.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>Probabilidad: %{x:.1f}%<extra></extra>"
            )

            probability_fig.update_layout(
                height=300,
                margin=dict(t=10, b=20, l=10, r=80),
                paper_bgcolor="white",
                plot_bgcolor="white",
                xaxis_title="Probabilidad estimada",
                yaxis_title="",
                xaxis=dict(showgrid=True, gridcolor="#E5E7EB", zeroline=False),
                yaxis=dict(showgrid=False),
                showlegend=False
            )

            st.plotly_chart(probability_fig, use_container_width=True)

        with st.expander("Ver datos usados para la predicción"):
            st.dataframe(input_data, use_container_width=True, hide_index=True)
        
# ============================================================
# TAB 4 — Metodología
# ============================================================

with tab_about:
    st.markdown(
        '<div class="section-title">Metodología del proyecto</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        Esta sección resume cómo se construyó la solución analítica, desde el problema de negocio 
        hasta la aplicación interactiva en Streamlit.
        """
    )

    st.divider()

    # ========================================================
    # Visión general
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="method-card">
            <div class="method-title">1. Problema de negocio</div>
            <div class="method-text">
                Las áreas de HR Operations gestionan grandes volúmenes de solicitudes internas, 
                tickets, incidencias y procesos administrativos. No todos los procesos deben 
                automatizarse primero. El reto consiste en identificar dónde la automatización 
                puede generar mayor impacto operativo, reducir fricción y liberar capacidad del equipo.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="method-card">
            <div class="method-title">2. Enfoque analítico</div>
            <div class="method-text">
                El proyecto convierte datos operativos de tickets en una matriz de priorización. 
                Cada unidad operativa combina proceso HR, sistema HR, región y canal interno. 
                Sobre cada unidad se calculan métricas de volumen, tiempos, SLA, escalaciones, 
                complejidad y recurrencia.
            </div>
        </div>
        """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div class="method-card">
            <div class="method-title">3. Reglas de negocio</div>
            <div class="method-text">
                La priorización no se basa solo en volumen. Se construyó un Automation Opportunity Score 
                combinando señales de impacto, fricción y criticidad. La lógica aplicada fue: más casos, 
                más tiempo de resolución, más SLA incumplido, más escalaciones y mayor complejidad 
                implican mayor oportunidad de automatización.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="method-card">
            <div class="method-title">4. Machine Learning</div>
            <div class="method-text">
                Se entrenó un modelo de clasificación multiclase para predecir la prioridad de automatización: 
                Alta, Media o Baja. El modelo ganador fue Logistic Regression, con un F1 macro aproximado 
                de 0.9685. Su función es aprender y replicar la lógica de priorización definida por negocio.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ========================================================
    # Componentes principales
    # ========================================================

    st.markdown(
        '<div class="section-title">Componentes de la solución</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <span class="badge">HR Operations</span>
    <span class="badge">People Analytics</span>
    <span class="badge">Machine Learning</span>
    <span class="badge">Automation Scoring</span>
    <span class="badge">Streamlit App</span>
    <span class="badge">Decision Support</span>
    """, unsafe_allow_html=True)

    st.markdown("")

    col5, col6, col7 = st.columns(3)

    with col5:
        st.markdown("""
        <div class="method-card">
            <div class="method-title">Input</div>
            <div class="method-text">
                Datos operativos agregados por unidad: proceso HR, sistema, región, canal, volumen, 
                tiempos de resolución, SLA, escalaciones, complejidad, satisfacción y recurrencia.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown("""
        <div class="method-card">
            <div class="method-title">Modelo</div>
            <div class="method-text">
                El modelo clasifica nuevas unidades operativas según su prioridad de automatización. 
                Además, la app muestra la confianza del modelo y la probabilidad estimada por clase.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col7:
        st.markdown("""
        <div class="method-card">
            <div class="method-title">Output</div>
            <div class="method-text">
                Ranking de oportunidades, prioridad de automatización, solución tecnológica recomendada 
                y estimación conservadora de horas operativas potencialmente ahorrables.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ========================================================
    # Uso esperado
    # ========================================================

    st.markdown(
        '<div class="section-title">Uso esperado de la herramienta</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    La app está diseñada para ayudar a equipos de HR Operations, People Analytics y Transformación Digital a:
    
    - identificar oportunidades de automatización;
    - priorizar procesos según impacto operativo;
    - comparar unidades por sistema, región y canal;
    - simular nuevas unidades operativas;
    - estimar ahorro potencial;
    - apoyar decisiones de automatización con datos.
    """)

    st.markdown("""
    <div class="warning-card">
        <b>Nota metodológica:</b> el modelo no debe interpretarse como una predicción causal independiente. 
        Su valor está en automatizar una lógica de priorización basada en reglas de negocio, permitiendo 
        aplicar criterios consistentes a nuevas unidades operativas.
    </div>
    """, unsafe_allow_html=True)



