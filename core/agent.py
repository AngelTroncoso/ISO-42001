"""ISO 42001 advisory agent with conversation management."""
import logging
from typing import Optional
from llama_index.llms.mistralai import MistralAI


logger = logging.getLogger(__name__)


class ISO42001Agent:
    """Advisory agent for ISO 42001 implementation guidance."""
    
    SYSTEM_PROMPT = """Eres un consultor experto en ISO/IEC 42001:2023, el estándar internacional para Sistemas de Gestión de Inteligencia Artificial.

Tu función es guiar a organizaciones paso a paso en la implementación de este estándar. Debes:

1. Proporcionar respuestas claras, prácticas y específicas
2. Desglosar conceptos complejos en pasos accionables
3. Explicar el "por qué" detrás de cada requisito
4. Sugerir documentación, evidencias y controles concretos
5. Adaptar tus recomendaciones al contexto de la organización
6. Ser directo y evitar jerga innecesaria

Estructura tus respuestas de forma organizada:
- Usa listas numeradas para pasos secuenciales
- Usa viñetas para opciones o elementos relacionados
- Destaca puntos clave
- Incluye ejemplos cuando sea útil

Recuerda que hablas con personas que pueden no ser expertas en estándares ISO, así que sé pedagógico y accesible.

IMPORTANTE: Responde SIEMPRE en español neutro."""

    def __init__(self, api_key: str, model: str = "mistral-small-latest"):
        """Initialize the advisory agent.
        
        Args:
            api_key: Mistral API key
            model: LLM model name
        """
        self.api_key = api_key
        self.model = model
        self.llm = MistralAI(api_key=api_key, model=model)
        self.conversation_history = []
        
        logger.info(f"ISO 42001 Agent initialized with {model}")
    
    def chat(self, user_message: str, include_history: bool = True) -> str:
        """Send a message to the agent and get a response.
        
        Args:
            user_message: User's message
            include_history: Whether to include conversation history
            
        Returns:
            Agent's response
        """
        try:
            # Build messages
            messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
            
            # Add conversation history if requested
            if include_history and self.conversation_history:
                messages.extend(self.conversation_history)
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Get response from LLM
            response = self.llm.chat(messages)
            
            # Store in history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": str(response)})
            
            # Keep history manageable (last 10 exchanges)
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return str(response)
            
        except Exception as e:
            logger.error(f"Error in agent chat: {e}")
            return f"Lo siento, ocurrió un error al procesar tu consulta: {str(e)}"
    
    def get_quick_response(self, topic: str) -> str:
        """Get a quick response for common topics.
        
        Args:
            topic: Topic identifier
            
        Returns:
            Response text
        """
        quick_responses = {
            'start': """¡Perfecto! Para comenzar con la implementación de ISO/IEC 42001, te recomiendo estos primeros pasos:

**1. Entender el alcance (Cláusula 4)**
   - Define qué sistemas de IA están dentro del alcance
   - Identifica las partes interesadas clave
   - Documenta el contexto organizacional

**2. Obtener compromiso de la dirección (Cláusula 5)**
   - Presenta el proyecto a la alta dirección
   - Define roles y responsabilidades
   - Asegura recursos necesarios

**3. Evaluación inicial de brechas**
   - Revisa tus procesos actuales vs. requisitos del estándar
   - Identifica qué controles ya tienes
   - Prioriza las áreas críticas

**4. Planificación (Cláusula 6)**
   - Identifica riesgos y oportunidades de los sistemas de IA
   - Define objetivos medibles
   - Crea un plan de implementación por fases

¿Sobre cuál de estos puntos quieres profundizar?""",
            
            'documents': """Para implementar ISO/IEC 42001 necesitas desarrollar estos documentos clave:

**Documentos de Nivel 1 - Estratégicos:**
- Política del Sistema de Gestión de IA
- Manual del AIMS (opcional pero recomendado)
- Objetivos de IA y plan estratégico

**Documentos de Nivel 2 - Procedimientos:**
- Procedimiento de gestión de riesgos de IA
- Procedimiento de evaluación de impacto de IA
- Procedimiento de auditoría interna
- Procedimiento de gestión de cambios
- Procedimiento de gestión de incidentes

**Documentos de Nivel 3 - Instrucciones:**
- Instrucciones de trabajo para cada control implementado
- Plantillas de evaluación de riesgos
- Listas de verificación de revisión

**Registros obligatorios:**
- Inventario de sistemas de IA
- Registros de evaluaciones de riesgo
- Registros de capacitación
- Actas de revisión por la dirección
- Informes de auditoría interna
- Registros de incidentes y no conformidades

¿Necesitas ayuda con algún documento específico?""",
            
            'risk_analysis': """El análisis de riesgos es fundamental en ISO/IEC 42001. Aquí está el enfoque estructurado:

**1. Identificación de riesgos (Cláusula 6.1)**
   - Riesgos técnicos: sesgo, precisión, robustez
   - Riesgos éticos: privacidad, discriminación, transparencia
   - Riesgos operacionales: disponibilidad, mantenimiento
   - Riesgos de cumplimiento: regulaciones, propiedad intelectual

**2. Análisis de impacto y probabilidad**
   - Evalúa consecuencias para individuos y organización
   - Considera el ciclo de vida completo del sistema IA
   - Usa matriz de riesgo (probabilidad × impacto)

**3. Evaluación y priorización**
   - Compara con criterios de aceptación de riesgo
   - Prioriza riesgos altos e inaceptables
   - Documenta la justificación

**4. Tratamiento de riesgos**
   - Evitar: no usar IA para esa función
   - Mitigar: implementar controles (Anexo A)
   - Transferir: seguros, contratos
   - Aceptar: riesgos menores con aprobación

**5. Monitoreo continuo**
   - Revisa riesgos periódicamente
   - Actualiza cuando cambie el sistema o contexto
   - Registra todas las decisiones

¿Quieres que profundicemos en algún tipo de riesgo específico?""",
            
            'audit': """Preparación para auditoría de certificación ISO/IEC 42001:

**Antes de la auditoría:**

1. **Autoevaluación completa**
   - Verifica cumplimiento de cada requisito (cláusulas 4-10)
   - Revisa todos los controles del Anexo A aplicables
   - Realiza auditoría interna completa

2. **Documentación lista**
   - Política y objetivos aprobados y comunicados
   - Procedimientos implementados y actualizados
   - Registros de al menos 3 meses (idealmente 6)
   - Evidencias de mejora continua

3. **Personal preparado**
   - Todos conocen la política y su rol
   - Capacitación documentada
   - Responsables de IA identificados y capacitados

4. **Sistemas funcionando**
   - Controles operativos y verificables
   - Métricas e indicadores actualizados
   - No conformidades gestionadas

**Durante la auditoría:**

- **Etapa 1 (revisión documental)**: Auditor revisa documentación
- **Etapa 2 (auditoría in situ)**: Entrevistas, observaciones, muestreo

**Documentos que el auditor revisará:**
- Alcance del AIMS y contexto organizacional
- Análisis de riesgos y oportunidades
- Inventario de sistemas de IA
- Registros de evaluaciones de impacto
- Evidencias de implementación de controles
- Resultados de auditorías internas
- Actas de revisión por la dirección
- Registros de capacitación
- Gestión de incidentes y no conformidades

**Consejos:**
- Sé honesto sobre las brechas
- Muestra tendencia de mejora
- Ten evidencias accesibles y organizadas
- Demuestra conocimiento del estándar

¿Hay algún requisito específico que te preocupe?"""
        }
        
        return quick_responses.get(topic, self.chat(topic, include_history=False))
    
    def reset_conversation(self) -> None:
        """Reset conversation history."""
        self.conversation_history = []
        logger.info("Conversation history reset")
    
    def get_conversation_length(self) -> int:
        """Get number of messages in conversation history.
        
        Returns:
            Number of messages
        """
        return len(self.conversation_history)
