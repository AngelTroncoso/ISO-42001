"""Library page for PDF management."""
import streamlit as st
from pathlib import Path
import time
from core.pdf_loader import validate_pdf, get_pdf_info
from core.rag_engine import RAGEngine
from utils.helpers import (
    show_success_message, show_error_message, show_warning_message,
    format_file_size, ensure_directory
)
from config import load_config


def render_library_page():
    """Render the PDF library management page."""
    st.title("📚 Biblioteca de Documentos")
    
    st.markdown("""
    Sube el PDF de la norma ISO/IEC 42001:2023 para poder consultarlo mediante búsqueda semántica.
    
    ⚠️ **Nota importante**: Este sistema NO incluye el texto de la norma por derechos de autor.
    Debes tener tu propia copia legal del documento.
    """)
    
    config = load_config()
    data_dir = Path(config['DATA_DIR'])
    ensure_directory(data_dir)
    
    st.divider()
    
    # Current status
    st.subheader("📊 Estado Actual")
    
    if 'rag_engine' in st.session_state and st.session_state.rag_engine:
        stats = st.session_state.rag_engine.get_index_stats()
        if stats['is_ready']:
            st.success(f"✅ Documentos cargados: {stats['num_documents']}")
            for doc in stats['documents_loaded']:
                st.write(f"- {doc}")
        else:
            st.warning("⚠️ No hay documentos indexados")
    else:
        st.warning("⚠️ Motor RAG no inicializado. Sube un documento para comenzar.")
    
    st.divider()
    
    # File upload section
    st.subheader("📤 Cargar Documento")
    
    uploaded_file = st.file_uploader(
        "Selecciona el archivo PDF de ISO/IEC 42001:2023",
        type=['pdf'],
        help="El archivo debe ser un PDF con texto extraíble (no escaneado)"
    )
    
    if uploaded_file is not None:
        # Show file info
        file_size = len(uploaded_file.getvalue())
        st.info(f"📄 Archivo: {uploaded_file.name} ({format_file_size(file_size)})")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            load_button = st.button("🚀 Cargar y Procesar", type="primary", width="stretch")
        
        if load_button:
            # Save uploaded file temporarily
            temp_path = data_dir / uploaded_file.name
            
            with st.spinner("Guardando archivo..."):
                with open(temp_path, 'wb') as f:
                    f.write(uploaded_file.getvalue())
            
            # Validate PDF
            with st.spinner("Validando PDF..."):
                is_valid, error_msg = validate_pdf(temp_path)
            
            if not is_valid:
                show_error_message(f"Error de validación: {error_msg}")
                temp_path.unlink()  # Delete invalid file
                return
            
            # Show PDF info
            pdf_info = get_pdf_info(temp_path)
            st.success(f"✅ PDF válido: {pdf_info['num_pages']} páginas")
            
            # Load into RAG engine
            try:
                with st.spinner("Procesando documento y creando índice vectorial... Esto puede tomar unos minutos."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Initialize RAG engine if not exists
                    if 'rag_engine' not in st.session_state:
                        status_text.text("Inicializando motor RAG...")
                        progress_bar.progress(10)
                        
                        rag_engine = RAGEngine(
                            api_key=config['MISTRAL_API_KEY'],
                            llm_model=config['MISTRAL_LLM_MODEL'],
                            embed_model=config['MISTRAL_EMBED_MODEL'],
                            chunk_size=config['CHUNK_SIZE'],
                            chunk_overlap=config['CHUNK_OVERLAP']
                        )
                        st.session_state.rag_engine = rag_engine
                    else:
                        rag_engine = st.session_state.rag_engine
                    
                    # Load PDF and persist automatically
                    status_text.text("Extrayendo texto y detectando cláusulas...")
                    progress_bar.progress(30)
                    
                    index_dir = data_dir / 'index'
                    num_chunks = rag_engine.load_pdf(temp_path, index_dir)
                    
                    progress_bar.progress(100)
                    status_text.empty()
                    progress_bar.empty()
                    
                    show_success_message(
                        f"Documento cargado exitosamente. Se crearon {num_chunks} fragmentos indexados."
                    )
                    
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                    
            except Exception as e:
                show_error_message(f"Error al procesar el documento: {str(e)}")
                # Clean up
                if temp_path.exists():
                    temp_path.unlink()
    
    st.divider()
    
    # Manage existing documents
    st.subheader("📁 Documentos Almacenados")
    
    pdf_files = list(data_dir.glob("*.pdf"))
    
    if pdf_files:
        st.write(f"Se encontraron {len(pdf_files)} archivo(s) PDF:")
        
        for pdf_file in pdf_files:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"📄 {pdf_file.name}")
            
            with col2:
                file_size = pdf_file.stat().st_size
                st.write(format_file_size(file_size))
            
            with col3:
                if st.button("🗑️ Eliminar", key=f"delete_{pdf_file.name}"):
                    pdf_file.unlink()
                    show_success_message(f"Archivo {pdf_file.name} eliminado")
                    # Clear index if this was the loaded document
                    if 'rag_engine' in st.session_state:
                        st.session_state.rag_engine = None
                    st.rerun()
    else:
        st.info("No hay archivos PDF almacenados localmente")
    
    st.divider()
    
    # Information section
    with st.expander("ℹ️ Información sobre Derechos de Autor"):
        st.markdown("""
        ### Aviso Legal
        
        ISO/IEC 42001:2023 es un estándar internacional protegido por derechos de autor.
        
        **Esta aplicación NO incluye ni distribuye el texto de la norma.** Los usuarios deben:
        
        1. Adquirir una copia legal del estándar desde:
           - ISO: https://www.iso.org/standard/81230.html
           - Organismos nacionales de normalización
           - Proveedores autorizados
        
        2. Subir su propia copia en formato PDF
        
        3. El uso del documento debe cumplir con los términos de la licencia adquirida
        
        El procesamiento y análisis se realiza localmente en tu sesión y los datos no se almacenan
        de forma permanente fuera de tu control.
        """)
