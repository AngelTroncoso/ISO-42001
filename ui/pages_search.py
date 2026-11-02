"""Search/RAG page for querying the ISO standard."""
import streamlit as st
from ui.components import render_source_citation
from utils.helpers import show_warning_message, show_error_message


def render_search_page():
    """Render the RAG search page."""
    st.title("🔍 Consultar la Norma ISO 42001")
    
    st.markdown("""
    Realiza preguntas sobre la norma ISO/IEC 42001:2023 y obtén respuestas precisas con referencias
    a las cláusulas y páginas específicas.
    """)
    
    # Check if RAG engine is initialized
    if 'rag_engine' not in st.session_state or not st.session_state.rag_engine:
        show_warning_message(
            "Primero debes cargar el documento PDF en la página **📚 Biblioteca**"
        )
        if st.button("Ir a Biblioteca"):
            st.session_state['page'] = 'library'
            st.rerun()
        return
    
    rag_engine = st.session_state.rag_engine
    
    # Check if documents are loaded
    stats = rag_engine.get_index_stats()
    if not stats['is_ready']:
        show_warning_message("No hay documentos cargados. Ve a Biblioteca para subir un PDF.")
        return
    
    st.success(f"✅ Sistema listo. Documentos cargados: {stats['documents_loaded']}")
    
    st.divider()
    
    # Search configuration
    with st.expander("⚙️ Configuración de Búsqueda", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            top_k = st.slider(
                "Número de fragmentos a recuperar",
                min_value=1,
                max_value=10,
                value=5,
                help="Cuántos fragmentos relevantes usar para generar la respuesta"
            )
        with col2:
            similarity_threshold = st.slider(
                "Umbral de similitud",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                step=0.05,
                help="Mínimo nivel de relevancia requerido"
            )
    
    st.divider()
    
    # Query examples/suggestions
    st.subheader("💡 Preguntas Sugeridas")
    
    col1, col2 = st.columns(2)
    
    example_questions = [
        "¿Cuáles son los requisitos de la cláusula 4?",
        "¿Qué dice la norma sobre evaluación de riesgos de IA?",
        "¿Cómo se debe implementar la supervisión humana?",
        "¿Qué controles hay para mitigar el sesgo en IA?",
        "¿Cuáles son los requisitos de documentación?",
        "¿Qué dice sobre gestión de datos para IA?",
        "¿Cómo hacer una evaluación de impacto de IA?",
        "¿Qué requisitos hay para auditoría interna?"
    ]
    
    for i, question in enumerate(example_questions[:4]):
        if col1.button(f"📌 {question}", key=f"q1_{i}", use_container_width=True):
            st.session_state['current_question'] = question
    
    for i, question in enumerate(example_questions[4:]):
        if col2.button(f"📌 {question}", key=f"q2_{i}", use_container_width=True):
            st.session_state['current_question'] = question
    
    st.divider()
    
    # Query input
    st.subheader("❓ Tu Pregunta")
    
    # Pre-fill with selected question if any
    default_query = st.session_state.get('current_question', '')
    if default_query:
        # Clear after using
        del st.session_state['current_question']
    
    query = st.text_area(
        "Escribe tu pregunta sobre la norma:",
        value=default_query,
        height=100,
        placeholder="Ejemplo: ¿Qué requisitos establece la cláusula 6 sobre gestión de riesgos?"
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        search_button = st.button("🔍 Buscar", type="primary", use_container_width=True)
    
    with col2:
        clear_button = st.button("🗑️ Limpiar", use_container_width=True)
    
    if clear_button:
        st.rerun()
    
    if search_button:
        if not query.strip():
            show_error_message("Por favor escribe una pregunta")
            return
        
        with st.spinner("Buscando en el documento..."):
            result = rag_engine.query(
                question=query,
                top_k=top_k,
                similarity_threshold=similarity_threshold
            )
        
        if result['error']:
            show_error_message(f"Error: {result['error']}")
            return
        
        # Display answer
        st.divider()
        st.subheader("💬 Respuesta")
        
        st.markdown(result['answer'])
        
        # Display sources
        if result['sources']:
            st.divider()
            st.subheader("📚 Fuentes y Referencias")
            st.caption(f"Se encontraron {len(result['sources'])} fragmentos relevantes:")
            
            for source in result['sources']:
                render_source_citation(source)
        else:
            st.info("No se encontraron fuentes específicas, pero la respuesta se basó en el conocimiento general del modelo.")
    
    # Query history (optional)
    st.divider()
    
    with st.expander("📜 Historial de Búsquedas", expanded=False):
        if 'query_history' not in st.session_state:
            st.session_state.query_history = []
        
        if st.session_state.query_history:
            for i, hist_query in enumerate(reversed(st.session_state.query_history[-10:])):
                st.write(f"{i+1}. {hist_query}")
        else:
            st.info("No hay búsquedas previas")
        
        if st.button("🗑️ Borrar historial"):
            st.session_state.query_history = []
            st.rerun()
    
    # Save query to history
    if search_button and query.strip():
        if 'query_history' not in st.session_state:
            st.session_state.query_history = []
        st.session_state.query_history.append(query.strip())
