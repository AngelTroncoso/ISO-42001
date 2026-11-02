"""Search/RAG page for querying the ISO standard."""
import streamlit as st
from ui.components import render_source_citation
from utils.helpers import show_warning_message, show_error_message


QUESTION_KEY = "search_question"
HISTORY_KEY = "query_history"

EXAMPLE_QUESTIONS = [
    "¿Cuáles son los requisitos de la cláusula 4?",
    "¿Qué dice la norma sobre evaluación de riesgos de IA?",
    "¿Cómo se debe implementar la supervisión humana?",
    "¿Qué controles hay para mitigar el sesgo en IA?",
    "¿Cuáles son los requisitos de documentación?",
    "¿Qué dice sobre gestión de datos para IA?",
    "¿Cómo hacer una evaluación de impacto de IA?",
    "¿Qué requisitos hay para auditoría interna?",
]


def _set_question(text: str) -> None:
    """Store the question in session state before the page is redrawn.

    Args:
        text: Question text to place in the input field.
    """
    st.session_state[QUESTION_KEY] = text


def _init_state() -> None:
    """Initialize session state keys used by the search page."""
    if QUESTION_KEY not in st.session_state:
        st.session_state[QUESTION_KEY] = ""
    if HISTORY_KEY not in st.session_state:
        st.session_state[HISTORY_KEY] = []


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

    _init_state()

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

    # Query suggestions: on_click stores the text before the input is drawn
    st.subheader("💡 Preguntas Sugeridas")

    col1, col2 = st.columns(2)
    for i, question in enumerate(EXAMPLE_QUESTIONS):
        target = col1 if i < len(EXAMPLE_QUESTIONS) // 2 else col2
        target.button(
            f"📌 {question}",
            key=f"suggestion_{i}",
            on_click=_set_question,
            args=(question,),
            width="stretch",
        )

    st.divider()

    # Query input: bound to session state, so suggestions and Limpiar update it
    st.subheader("❓ Tu Pregunta")

    st.text_area(
        "Escribe tu pregunta sobre la norma:",
        key=QUESTION_KEY,
        height=100,
        placeholder="Ejemplo: ¿Qué requisitos establece la cláusula 6 sobre gestión de riesgos?",
    )

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        search_button = st.button("🔍 Buscar", type="primary", width="stretch")

    with col2:
        st.button(
            "🗑️ Limpiar",
            on_click=_set_question,
            args=("",),
            width="stretch",
        )

    if search_button:
        query = st.session_state[QUESTION_KEY].strip()

        if not query:
            show_error_message("Por favor escribe una pregunta")
        else:
            with st.spinner("Buscando en el documento..."):
                result = rag_engine.query(
                    question=query,
                    top_k=top_k,
                    similarity_threshold=similarity_threshold
                )

            if result['error']:
                show_error_message(f"Error: {result['error']}")
            else:
                # Save query to history (no duplicates in a row)
                history = st.session_state[HISTORY_KEY]
                if not history or history[-1] != query:
                    history.append(query)

                st.divider()
                st.subheader("💬 Respuesta")
                st.markdown(result['answer'])

                if result['sources']:
                    st.divider()
                    st.subheader("📚 Fuentes y Referencias")
                    st.caption(f"Se encontraron {len(result['sources'])} fragmentos relevantes:")

                    for source in result['sources']:
                        render_source_citation(source)
                else:
                    st.info(
                        "No se encontraron fuentes específicas en la norma cargada. "
                        "La información puede no estar en el documento."
                    )

    # Query history
    st.divider()

    with st.expander("📜 Historial de Búsquedas", expanded=False):
        history = st.session_state[HISTORY_KEY]

        if history:
            for i, hist_query in enumerate(reversed(history[-10:])):
                st.write(f"{i + 1}. {hist_query}")
        else:
            st.info("No hay búsquedas previas")

        if st.button("🗑️ Borrar historial"):
            st.session_state[HISTORY_KEY] = []
            st.rerun()