"""Home page."""
import streamlit as st
from storage.database import ComplianceDatabase
from core.compliance_tracker import ComplianceTracker
from ui.components import render_progress_card, render_quick_stats


def render_home_page():
    """Render the home/dashboard page."""
    st.title("🏠 ISO/IEC 42001:2023 - Panel de Control")
    
    st.markdown("""
    ### Bienvenido al Sistema de Gestión de Cumplimiento ISO 42001
    
    Esta aplicación te ayuda a implementar y mantener un Sistema de Gestión de Inteligencia Artificial (AIMS)
    conforme al estándar internacional ISO/IEC 42001:2023.
    """)
    
    # Load current status
    db = ComplianceDatabase()
    df = db.get_all_requirements()
    
    if df.empty:
        st.warning("""
        ⚠️ **No hay requisitos cargados en el sistema.**
        
        Ve a la página **📊 Seguimiento** para inicializar el catálogo de requisitos.
        """)
        return
    
    st.divider()
    
    # Quick stats
    st.subheader("📈 Estado General")
    render_quick_stats(df)
    
    st.divider()
    
    # Progress overview
    st.subheader("📊 Resumen de Progreso")
    stats = ComplianceTracker.calculate_progress(df)
    render_progress_card(stats)
    
    # Show progress bar
    st.progress(
        stats['effective_completion_rate'] / 100,
        text=f"Cumplimiento efectivo: {stats['effective_completion_rate']}%"
    )
    
    st.divider()
    
    # Recent activity / alerts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚠️ Requisitos Vencidos")
        overdue = ComplianceTracker.get_overdue_requirements(df)
        if not overdue.empty:
            for _, req in overdue.head(5).iterrows():
                st.warning(f"**{req['clause']}**: {req['requirement'][:50]}... - Vencido: {req['fecha_objetivo']}")
        else:
            st.success("✅ No hay requisitos vencidos")
    
    with col2:
        st.subheader("📅 Próximos 30 Días")
        upcoming = ComplianceTracker.get_upcoming_requirements(df, days=30)
        if not upcoming.empty:
            for _, req in upcoming.head(5).iterrows():
                st.info(f"**{req['clause']}**: {req['requirement'][:50]}... - Fecha: {req['fecha_objetivo']}")
        else:
            st.info("No hay fechas próximas programadas")
    
    st.divider()
    
    # Quick navigation
    st.subheader("🚀 Accesos Rápidos")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📚 Consultar Norma", use_container_width=True):
            st.session_state['page'] = 'search'
            st.rerun()
    
    with col2:
        if st.button("📊 Ver Seguimiento", use_container_width=True):
            st.session_state['page'] = 'tracker'
            st.rerun()
    
    with col3:
        if st.button("💬 Hablar con Asesor", use_container_width=True):
            st.session_state['page'] = 'advisor'
            st.rerun()
    
    with col4:
        if st.button("📖 Biblioteca", use_container_width=True):
            st.session_state['page'] = 'library'
            st.rerun()
