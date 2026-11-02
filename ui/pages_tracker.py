"""Compliance tracker page."""
import streamlit as st
import pandas as pd
from datetime import date
from storage.database import ComplianceDatabase
from core.compliance_data import get_default_requirements, get_status_config
from core.compliance_tracker import ComplianceTracker
from ui.components import (
    render_progress_chart,
    render_category_chart,
    render_timeline_chart,
    render_progress_card
)
from utils.helpers import show_success_message, show_error_message, show_warning_message


def render_tracker_page():
    """Render the compliance tracking page."""
    st.title("📊 Seguimiento de Cumplimiento")
    
    st.markdown("""
    Gestiona y monitorea el progreso de implementación de los requisitos de ISO/IEC 42001:2023.
    """)
    
    db = ComplianceDatabase()
    
    # Initialize data if empty
    if db.get_count() == 0:
        st.warning("⚠️ No hay requisitos en la base de datos")
        
        if st.button("🚀 Inicializar con Catálogo Predeterminado", type="primary"):
            with st.spinner("Cargando requisitos..."):
                default_reqs = get_default_requirements()
                inserted = db.bulk_insert_requirements(default_reqs)
                show_success_message(f"Se cargaron {inserted} requisitos exitosamente")
                st.rerun()
        return
    
    # Load current data
    df = db.get_all_requirements()
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Lista de Requisitos",
        "📈 Dashboard",
        "📊 Análisis",
        "⚙️ Gestión"
    ])
    
    # TAB 1: Requirements List
    with tab1:
        render_requirements_list(db, df)
    
    # TAB 2: Dashboard
    with tab2:
        render_dashboard(df)
    
    # TAB 3: Analysis
    with tab3:
        render_analysis(df)
    
    # TAB 4: Management
    with tab4:
        render_management(db, df)


def render_requirements_list(db: ComplianceDatabase, df: pd.DataFrame):
    """Render the requirements list with editing capabilities."""
    st.subheader("📋 Tabla de Requisitos")
    
    # Filters
    with st.expander("🔍 Filtros", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_status = st.multiselect(
                "Estado",
                options=['No iniciado', 'En progreso', 'Cumplido', 'No aplica'],
                default=[]
            )
        
        with col2:
            categories = df['category'].unique().tolist() if 'category' in df.columns else []
            filter_category = st.multiselect(
                "Categoría",
                options=categories,
                default=[]
            )
        
        with col3:
            filter_clause = st.text_input("Cláusula", placeholder="Ej: 6.1")
    
    # Apply filters
    filtered_df = df.copy()
    if filter_status:
        filtered_df = filtered_df[filtered_df['estado'].isin(filter_status)]
    if filter_category:
        filtered_df = filtered_df[filtered_df['category'].isin(filter_category)]
    if filter_clause:
        filtered_df = filtered_df[filtered_df['clause'].str.contains(filter_clause, case=False, na=False)]
    
    st.info(f"Mostrando {len(filtered_df)} de {len(df)} requisitos")
    
    # Editable data editor
    if not filtered_df.empty:
        status_config = get_status_config()
        
        # Configure column settings
        column_config = {
            'id': st.column_config.NumberColumn('ID', disabled=True, width='small'),
            'clause': st.column_config.TextColumn('Cláusula', width='small', disabled=True),
            'requirement': st.column_config.TextColumn('Requisito', width='medium', disabled=True),
            'description': st.column_config.TextColumn('Descripción', width='large'),
            'category': st.column_config.TextColumn('Categoría', width='small'),
            'estado': st.column_config.SelectboxColumn(
                'Estado',
                options=['No iniciado', 'En progreso', 'Cumplido', 'No aplica'],
                required=True,
                width='medium'
            ),
            'responsable': st.column_config.TextColumn('Responsable', width='medium'),
            'fecha_objetivo': st.column_config.DateColumn('Fecha Objetivo', format='DD/MM/YYYY', width='medium'),
            'evidencia': st.column_config.TextColumn('Evidencia', width='large'),
            'notas': st.column_config.TextColumn('Notas', width='large'),
        }
        
        # Display editable table
        edited_df = st.data_editor(
            filtered_df,
            column_config=column_config,
            hide_index=True,
            width="stretch",
            num_rows="fixed",
            disabled=['id', 'clause', 'requirement', 'created_at', 'updated_at']
        )
        
        # Save changes button
        if st.button("💾 Guardar Cambios", type="primary"):
            with st.spinner("Guardando..."):
                try:
                    # Update each modified row
                    for idx in edited_df.index:
                        req_id = edited_df.loc[idx, 'id']
                        updates = {}
                        
                        # Compare and collect changes
                        for col in ['description', 'category', 'estado', 'responsable', 'fecha_objetivo', 'evidencia', 'notas']:
                            if col in edited_df.columns:
                                old_val = df.loc[df['id'] == req_id, col].values[0] if len(df.loc[df['id'] == req_id]) > 0 else None
                                new_val = edited_df.loc[idx, col]
                                
                                # Handle NaN/None comparison
                                if pd.isna(old_val) and pd.isna(new_val):
                                    continue
                                if old_val != new_val:
                                    updates[col] = new_val
                        
                        # Save if there are changes
                        if updates:
                            db.update_requirement(req_id, updates)
                    
                    show_success_message("Cambios guardados exitosamente")
                    st.rerun()
                    
                except Exception as e:
                    show_error_message(f"Error al guardar: {str(e)}")


def render_dashboard(df: pd.DataFrame):
    """Render dashboard with metrics and charts."""
    st.subheader("📈 Dashboard de Progreso")
    
    # Overall progress
    stats = ComplianceTracker.calculate_progress(df)
    render_progress_card(stats)
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        render_progress_chart(stats)
    
    with col2:
        # By category
        st.markdown("### Por Categoría")
        category_stats = ComplianceTracker.get_by_category(df)
        for category, cat_stats in category_stats.items():
            st.metric(
                label=category,
                value=f"{cat_stats['completed']}/{cat_stats['total']}",
                delta=f"{cat_stats['completion_rate']}%"
            )
    
    st.divider()
    
    # Category chart
    render_category_chart(df)


def render_analysis(df: pd.DataFrame):
    """Render analysis views."""
    st.subheader("📊 Análisis Detallado")
    
    # Timeline
    st.markdown("### 📅 Cronograma")
    render_timeline_chart(df)
    
    st.divider()
    
    # Overdue and upcoming
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚠️ Requisitos Vencidos")
        overdue = ComplianceTracker.get_overdue_requirements(df)
        if not overdue.empty:
            st.dataframe(
                overdue[['clause', 'requirement', 'estado', 'fecha_objetivo', 'responsable']],
                hide_index=True,
                width="stretch"
            )
        else:
            st.success("✅ No hay requisitos vencidos")
    
    with col2:
        st.markdown("### 📅 Próximos 30 Días")
        upcoming = ComplianceTracker.get_upcoming_requirements(df, days=30)
        if not upcoming.empty:
            st.dataframe(
                upcoming[['clause', 'requirement', 'estado', 'fecha_objetivo', 'responsable']],
                hide_index=True,
                width="stretch"
            )
        else:
            st.info("No hay requisitos próximos en los siguientes 30 días")


def render_management(db: ComplianceDatabase, df: pd.DataFrame):
    """Render management/admin functions."""
    st.subheader("⚙️ Gestión de Datos")
    
    st.warning("⚠️ Las siguientes acciones son sensibles. Usa con precaución.")
    
    # Export options
    st.markdown("### 📤 Exportar Datos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Exportar a Excel", width="stretch"):
            export_path = f"compliance_export_{date.today().isoformat()}.xlsx"
            if ComplianceTracker.export_to_excel(df, export_path):
                with open(export_path, 'rb') as f:
                    st.download_button(
                        label="⬇️ Descargar Excel",
                        data=f,
                        file_name=export_path,
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
    
    with col2:
        if st.button("📄 Exportar a CSV", width="stretch"):
            export_path = f"compliance_export_{date.today().isoformat()}.csv"
            if ComplianceTracker.export_to_csv(df, export_path):
                with open(export_path, 'rb') as f:
                    st.download_button(
                        label="⬇️ Descargar CSV",
                        data=f,
                        file_name=export_path,
                        mime='text/csv'
                    )
    
    st.divider()
    
    # Reset database
    st.markdown("### 🔄 Reiniciar Base de Datos")
    
    with st.expander("⚠️ Zona de Peligro", expanded=False):
        st.error("Esta acción eliminará TODOS los datos de cumplimiento.")
        
        confirm = st.checkbox("Entiendo que esto eliminará todos los datos")
        
        if confirm:
            if st.button("🗑️ ELIMINAR TODOS LOS DATOS", type="primary"):
                db.clear_all_requirements()
                show_warning_message("Base de datos limpiada. Recarga la página.")
                st.rerun()
