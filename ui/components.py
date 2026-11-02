"""Reusable UI components."""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import date
from utils.helpers import get_status_emoji, get_status_color


def render_progress_card(stats: dict) -> None:
    """Render progress statistics card.
    
    Args:
        stats: Dictionary with progress statistics
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total Requisitos",
            value=stats['total']
        )
    
    with col2:
        st.metric(
            label="🟢 Cumplidos",
            value=stats['completed'],
            delta=f"{stats['completion_rate']}%"
        )
    
    with col3:
        st.metric(
            label="🟡 En Progreso",
            value=stats['in_progress']
        )
    
    with col4:
        st.metric(
            label="⚪ No Iniciados",
            value=stats['not_started']
        )


def render_progress_chart(stats: dict) -> None:
    """Render progress pie chart.
    
    Args:
        stats: Dictionary with progress statistics
    """
    labels = ['Cumplidos', 'En progreso', 'No iniciados', 'No aplica']
    values = [
        stats['completed'],
        stats['in_progress'],
        stats['not_started'],
        stats['not_applicable']
    ]
    colors = ['#4CAF50', '#FDD835', '#E0E0E0', '#9E9E9E']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hole=0.4,
        textinfo='label+percent',
        textposition='outside'
    )])
    
    fig.update_layout(
        title="Distribución de Estados",
        showlegend=True,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_category_chart(df: pd.DataFrame) -> None:
    """Render progress by category bar chart.
    
    Args:
        df: DataFrame with compliance data
    """
    if df.empty or 'category' not in df.columns:
        st.info("No hay datos para mostrar")
        return
    
    # Count by category and status
    category_status = df.groupby(['category', 'estado']).size().reset_index(name='count')
    
    fig = px.bar(
        category_status,
        x='category',
        y='count',
        color='estado',
        title='Progreso por Categoría',
        labels={'category': 'Categoría', 'count': 'Cantidad', 'estado': 'Estado'},
        color_discrete_map={
            'Cumplido': '#4CAF50',
            'En progreso': '#FDD835',
            'No iniciado': '#E0E0E0',
            'No aplica': '#9E9E9E'
        },
        barmode='stack',
        height=400
    )
    
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)


def render_timeline_chart(df: pd.DataFrame) -> None:
    """Render timeline Gantt chart for requirements with dates.
    
    Args:
        df: DataFrame with compliance data
    """
    if df.empty or 'fecha_objetivo' not in df.columns:
        st.info("No hay fechas objetivo definidas")
        return
    
    # Filter rows with dates
    timeline_df = df[df['fecha_objetivo'].notna()].copy()
    
    if timeline_df.empty:
        st.info("No hay requisitos con fechas objetivo definidas")
        return
    
    # Prepare data for Gantt chart
    timeline_df['Start'] = pd.to_datetime('today')
    timeline_df['Finish'] = pd.to_datetime(timeline_df['fecha_objetivo'])
    timeline_df['Task'] = timeline_df['clause'] + ': ' + timeline_df['requirement'].str[:40]
    
    fig = px.timeline(
        timeline_df,
        x_start='Start',
        x_end='Finish',
        y='Task',
        color='estado',
        title='Cronograma de Implementación',
        color_discrete_map={
            'Cumplido': '#4CAF50',
            'En progreso': '#FDD835',
            'No iniciado': '#E0E0E0',
            'No aplica': '#9E9E9E'
        },
        height=max(400, len(timeline_df) * 30)
    )
    
    fig.update_yaxes(categoryorder='total ascending')
    st.plotly_chart(fig, use_container_width=True)


def render_status_badge(status: str) -> None:
    """Render a status badge.
    
    Args:
        status: Status value
    """
    emoji = get_status_emoji(status)
    color = get_status_color(status)
    
    st.markdown(
        f'<span style="background-color: {color}; padding: 5px 10px; '
        f'border-radius: 5px; color: #000;">{emoji} {status}</span>',
        unsafe_allow_html=True
    )


def render_requirement_detail(requirement: dict) -> None:
    """Render detailed view of a requirement.
    
    Args:
        requirement: Dictionary with requirement data
    """
    st.subheader(f"📋 {requirement['clause']}: {requirement['requirement']}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("**Descripción:**")
        st.write(requirement.get('description', 'Sin descripción'))
        
        if requirement.get('notas'):
            st.write("**Notas:**")
            st.info(requirement['notas'])
        
        if requirement.get('evidencia'):
            st.write("**Evidencia:**")
            st.success(requirement['evidencia'])
    
    with col2:
        st.write("**Estado:**")
        render_status_badge(requirement.get('estado', 'No iniciado'))
        
        st.write("**Categoría:**")
        st.write(requirement.get('category', 'N/A'))
        
        if requirement.get('responsable'):
            st.write("**Responsable:**")
            st.write(requirement['responsable'])
        
        if requirement.get('fecha_objetivo'):
            st.write("**Fecha Objetivo:**")
            st.write(requirement['fecha_objetivo'])


def render_quick_stats(df: pd.DataFrame) -> None:
    """Render quick statistics summary.
    
    Args:
        df: DataFrame with compliance data
    """
    if df.empty:
        st.info("No hay datos disponibles")
        return
    
    from core.compliance_tracker import ComplianceTracker
    
    stats = ComplianceTracker.calculate_progress(df)
    overdue = ComplianceTracker.get_overdue_requirements(df)
    upcoming = ComplianceTracker.get_upcoming_requirements(df, days=30)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="📈 Tasa de Cumplimiento",
            value=f"{stats['effective_completion_rate']}%"
        )
    
    with col2:
        st.metric(
            label="⏰ Vencidos",
            value=len(overdue),
            delta="Atención requerida" if len(overdue) > 0 else "Al día",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="📅 Próximos 30 días",
            value=len(upcoming)
        )


def render_source_citation(source: dict) -> None:
    """Render a source citation from RAG results.
    
    Args:
        source: Dictionary with source information
    """
    with st.expander(f"📄 {source['citation']}", expanded=False):
        st.write(source['text'])
        if source.get('score'):
            st.caption(f"Relevancia: {source['score']:.2f}")
