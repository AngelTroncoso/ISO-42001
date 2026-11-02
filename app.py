"""Main Streamlit application for ISO 42001 compliance tracking."""
import streamlit as st
import logging
from pathlib import Path

# Import configuration
from config import load_config, validate_config

# Import UI pages
from ui.pages_home import render_home_page
from ui.pages_library import render_library_page
from ui.pages_search import render_search_page
from ui.pages_tracker import render_tracker_page
from ui.pages_advisor import render_advisor_page

# Import utilities
from utils.helpers import setup_logging, ensure_directory


# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


# Page configuration
st.set_page_config(
    page_title="ISO 42001 Compliance Tracker",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': """
        # ISO/IEC 42001:2023 Compliance Tracker
        
        Sistema de gestión y seguimiento para la implementación del estándar 
        ISO/IEC 42001:2023 - Sistema de Gestión de Inteligencia Artificial.
        
        **Características:**
        - 📚 Consulta de la norma con RAG
        - 📊 Seguimiento de cumplimiento
        - 💬 Asesor virtual experto
        - 📈 Dashboard y análisis
        
        ---
        Desarrollado con Streamlit, LlamaIndex y Mistral AI
        """
    }
)


def init_app():
    """Initialize application state and configuration."""
    # Load configuration
    config = load_config()
    
    # Validate configuration
    is_valid, error_msg = validate_config(config)
    if not is_valid:
        st.error(f"❌ Error de configuración: {error_msg}")
        st.info("""
        **Configura tu API key de Mistral AI:**
        
        1. Crea un archivo `.env` en la raíz del proyecto con:
           ```
           MISTRAL_API_KEY=tu_clave_aqui
           ```
        
        2. O crea `.streamlit/secrets.toml` con:
           ```
           MISTRAL_API_KEY = "tu_clave_aqui"
           ```
        
        Obtén tu API key en: https://console.mistral.ai/
        """)
        st.stop()
    
    # Store config in session state
    if 'config' not in st.session_state:
        st.session_state.config = config
    
    # Ensure data directory exists
    data_dir = Path(config['DATA_DIR'])
    ensure_directory(data_dir)
    
    # Initialize RAG engine and load persisted index if available
    if 'rag_engine' not in st.session_state:
        from core.rag_engine import RAGEngine
        index_dir = data_dir / 'index'
        
        if index_dir.exists() and (index_dir / 'docstore.json').exists():
            try:
                rag_engine = RAGEngine(
                    api_key=config['MISTRAL_API_KEY'],
                    llm_model=config['MISTRAL_LLM_MODEL'],
                    embed_model=config['MISTRAL_EMBED_MODEL'],
                    chunk_size=config['CHUNK_SIZE'],
                    chunk_overlap=config['CHUNK_OVERLAP']
                )
                if rag_engine.load_index(index_dir):
                    st.session_state.rag_engine = rag_engine
                    logger.info("Loaded persisted index from disk")
            except Exception as e:
                logger.warning(f"Could not load persisted index: {e}")
    
    # Initialize page state
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    
    logger.info("Application initialized successfully")


def render_sidebar():
    """Render the sidebar navigation."""
    with st.sidebar:
        st.title("🤖 ISO 42001")
        st.caption("Sistema de Gestión de IA")
        
        st.divider()
        
        # Navigation
        st.subheader("📍 Navegación")
        
        pages = {
            'home': {'label': '🏠 Inicio', 'icon': '🏠'},
            'library': {'label': '📚 Biblioteca', 'icon': '📚'},
            'search': {'label': '🔍 Consultar Norma', 'icon': '🔍'},
            'tracker': {'label': '📊 Seguimiento', 'icon': '📊'},
            'advisor': {'label': '💬 Asesor IA', 'icon': '💬'},
        }
        
        for page_key, page_info in pages.items():
            if st.button(
                page_info['label'],
                key=f"nav_{page_key}",
                width="stretch",
                type="primary" if st.session_state.page == page_key else "secondary"
            ):
                st.session_state.page = page_key
                st.rerun()
        
        st.divider()
        
        # System info
        with st.expander("ℹ️ Información del Sistema"):
            config = st.session_state.get('config', {})
            st.write(f"**Modelo LLM:** {config.get('MISTRAL_LLM_MODEL', 'N/A')}")
            st.write(f"**Modelo Embeddings:** {config.get('MISTRAL_EMBED_MODEL', 'N/A')}")
            st.write(f"**Chunk Size:** {config.get('CHUNK_SIZE', 'N/A')}")
            st.write(f"**Chunk Overlap:** {config.get('CHUNK_OVERLAP', 'N/A')}")
        
        st.divider()
        
        # Help
        with st.expander("❓ Ayuda Rápida"):
            st.markdown("""
            ### Primeros Pasos:
            
            1. **📚 Biblioteca**: Sube el PDF de ISO 42001
            2. **📊 Seguimiento**: Inicializa el catálogo de requisitos
            3. **🔍 Consultar**: Pregunta sobre la norma
            4. **💬 Asesor**: Obtén guía de implementación
            
            ### Soporte:
            
            - Documentación completa en README.md
            - Verifica configuración en Settings
            - Revisa logs si hay errores
            """)
        
        st.divider()
        
        # Footer
        st.caption("v1.0.0 | ISO/IEC 42001:2023")
        st.caption("© 2024 - Uso educativo y profesional")


def main():
    """Main application entry point."""
    # Initialize app
    init_app()
    
    # Render sidebar
    render_sidebar()
    
    # Render current page
    current_page = st.session_state.page
    
    try:
        if current_page == 'home':
            render_home_page()
        elif current_page == 'library':
            render_library_page()
        elif current_page == 'search':
            render_search_page()
        elif current_page == 'tracker':
            render_tracker_page()
        elif current_page == 'advisor':
            render_advisor_page()
        else:
            st.error(f"Página desconocida: {current_page}")
            
    except Exception as e:
        logger.error(f"Error rendering page {current_page}: {e}", exc_info=True)
        st.error(f"❌ Error al cargar la página: {str(e)}")
        st.info("Por favor, revisa los logs o recarga la aplicación.")


if __name__ == "__main__":
    main()
