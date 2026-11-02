"""Advisor chatbot page."""
import streamlit as st
from core.agent import ISO42001Agent
from config import load_config
from utils.helpers import show_warning_message, show_error_message


def render_advisor_page():
    """Render the AI advisor chatbot page."""
    st.title("💬 Asesor de Implementación ISO 42001")
    
    st.markdown("""
    Consulta con un experto virtual en ISO/IEC 42001 que te guiará paso a paso en la implementación
    del Sistema de Gestión de Inteligencia Artificial.
    """)
    
    config = load_config()
    
    # Initialize agent if not exists
    if 'agent' not in st.session_state:
        try:
            agent = ISO42001Agent(
                api_key=config['MISTRAL_API_KEY'],
                model=config['MISTRAL_LLM_MODEL']
            )
            st.session_state.agent = agent
            st.success("✅ Asesor inicializado y listo")
        except Exception as e:
            show_error_message(f"Error al inicializar el asesor: {str(e)}")
            return
    
    agent = st.session_state.agent
    
    # Initialize chat history if not exists
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    st.divider()
    
    # Quick action buttons
    st.subheader("🚀 Sugerencias Rápidas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📍 ¿Por dónde empiezo?", width="stretch"):
            response = agent.get_quick_response('start')
            st.session_state.chat_history.append({
                'role': 'user',
                'content': '¿Por dónde empiezo con la implementación?'
            })
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response
            })
            st.rerun()
        
        if st.button("📋 ¿Qué documentos necesito?", width="stretch"):
            response = agent.get_quick_response('documents')
            st.session_state.chat_history.append({
                'role': 'user',
                'content': '¿Qué documentos necesito para ISO 42001?'
            })
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response
            })
            st.rerun()
    
    with col2:
        if st.button("⚠️ Ayúdame con análisis de riesgos", width="stretch"):
            response = agent.get_quick_response('risk_analysis')
            st.session_state.chat_history.append({
                'role': 'user',
                'content': 'Ayúdame con el análisis de riesgos de IA'
            })
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response
            })
            st.rerun()
        
        if st.button("✅ Prepárame para auditoría", width="stretch"):
            response = agent.get_quick_response('audit')
            st.session_state.chat_history.append({
                'role': 'user',
                'content': '¿Cómo prepararme para la auditoría de certificación?'
            })
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response
            })
            st.rerun()
    
    st.divider()
    
    # Chat interface
    st.subheader("💬 Conversación")
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        if not st.session_state.chat_history:
            st.info("""
            👋 ¡Hola! Soy tu asesor experto en ISO/IEC 42001:2023.
            
            Puedo ayudarte con:
            - Interpretación de requisitos del estándar
            - Guía paso a paso para la implementación
            - Recomendaciones de documentación y controles
            - Preparación para auditorías
            - Resolución de dudas específicas
            
            ¿En qué puedo ayudarte hoy?
            """)
        
        for message in st.session_state.chat_history:
            with st.chat_message(message['role']):
                st.markdown(message['content'])
    
    # Chat input
    user_input = st.chat_input("Escribe tu pregunta o consulta aquí...")
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input
        })
        
        # Get agent response
        with st.spinner("Pensando..."):
            response = agent.chat(user_input, include_history=True)
        
        # Add assistant response to history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': response
        })
        
        # Rerun to display new messages
        st.rerun()
    
    st.divider()
    
    # Chat management
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Limpiar conversación", width="stretch"):
            st.session_state.chat_history = []
            agent.reset_conversation()
            st.rerun()
    
    with col2:
        msg_count = agent.get_conversation_length()
        st.metric("Mensajes en contexto", msg_count)
    
    with col3:
        if st.session_state.chat_history:
            # Export conversation
            export_text = "\n\n".join([
                f"{'Usuario' if msg['role'] == 'user' else 'Asesor'}: {msg['content']}"
                for msg in st.session_state.chat_history
            ])
            st.download_button(
                label="📥 Exportar chat",
                data=export_text,
                file_name="conversacion_iso42001.txt",
                mime="text/plain",
                width="stretch"
            )
    
    # Tips
    with st.expander("💡 Consejos para usar el Asesor"):
        st.markdown("""
        ### Cómo obtener mejores respuestas:
        
        1. **Sé específico**: En lugar de "cuéntame sobre la norma", pregunta "¿cuáles son los pasos para hacer una evaluación de impacto de IA?"
        
        2. **Proporciona contexto**: Menciona el tamaño de tu organización, sector, o sistemas de IA que usas
        
        3. **Pregunta por ejemplos**: "Dame un ejemplo de política de IA" o "¿Cómo documentar un control de sesgo?"
        
        4. **Divide preguntas complejas**: Mejor varias preguntas simples que una muy compleja
        
        5. **Usa las sugerencias rápidas**: Los botones de arriba activan respuestas estructuradas para temas comunes
        
        ### El asesor puede ayudarte con:
        
        - ✅ Interpretación de requisitos y controles
        - ✅ Pasos de implementación prácticos
        - ✅ Plantillas y ejemplos de documentos
        - ✅ Recomendaciones según tu contexto
        - ✅ Preparación para auditorías
        - ✅ Resolución de problemas específicos
        
        ### El asesor NO puede:
        
        - ❌ Auditar o certificar tu organización
        - ❌ Garantizar cumplimiento legal específico
        - ❌ Reemplazar la revisión por auditores calificados
        - ❌ Acceder a tus sistemas o datos reales
        """)
