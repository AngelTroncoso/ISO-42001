"""Default compliance requirements catalog for ISO 42001."""


def get_default_requirements() -> list[dict[str, str]]:
    """Get default requirements catalog for ISO 42001.
    
    Returns:
        List of requirement dictionaries with all main clauses (4-10) and 38 Annex A controls
    """
    return [
        # Cláusula 4: Contexto de la organización
        {
            'clause': '4.1',
            'requirement': 'Comprensión de la organización y su contexto',
            'description': 'Determinar cuestiones externas e internas relevantes para el propósito y dirección estratégica',
            'category': 'Contexto'
        },
        {
            'clause': '4.2',
            'requirement': 'Comprensión de necesidades de partes interesadas',
            'description': 'Identificar partes interesadas y sus requisitos relevantes para el sistema de gestión de IA',
            'category': 'Contexto'
        },
        {
            'clause': '4.3',
            'requirement': 'Determinación del alcance del AIMS',
            'description': 'Definir límites y aplicabilidad del sistema de gestión de IA',
            'category': 'Contexto'
        },
        {
            'clause': '4.4',
            'requirement': 'Sistema de gestión de IA',
            'description': 'Establecer, implementar, mantener y mejorar continuamente el AIMS',
            'category': 'Contexto'
        },
        
        # Cláusula 5: Liderazgo
        {
            'clause': '5.1',
            'requirement': 'Liderazgo y compromiso',
            'description': 'Alta dirección debe demostrar liderazgo y compromiso con el AIMS',
            'category': 'Liderazgo'
        },
        {
            'clause': '5.2',
            'requirement': 'Política',
            'description': 'Establecer política de IA alineada con propósito de la organización',
            'category': 'Liderazgo'
        },
        {
            'clause': '5.3',
            'requirement': 'Roles organizacionales',
            'description': 'Asignar responsabilidades y autoridades relevantes para el AIMS',
            'category': 'Liderazgo'
        },
        
        # Cláusula 6: Planificación
        {
            'clause': '6.1',
            'requirement': 'Acciones para abordar riesgos y oportunidades',
            'description': 'Identificar y evaluar riesgos y oportunidades de los sistemas de IA',
            'category': 'Planificación'
        },
        {
            'clause': '6.2',
            'requirement': 'Objetivos de IA y planificación',
            'description': 'Establecer objetivos medibles y planificar cómo alcanzarlos',
            'category': 'Planificación'
        },
        
        # Cláusula 7: Soporte
        {
            'clause': '7.1',
            'requirement': 'Recursos',
            'description': 'Determinar y proporcionar recursos necesarios para el AIMS',
            'category': 'Soporte'
        },
        {
            'clause': '7.2',
            'requirement': 'Competencia',
            'description': 'Asegurar competencia de personas que afectan el desempeño de IA',
            'category': 'Soporte'
        },
        {
            'clause': '7.3',
            'requirement': 'Toma de conciencia',
            'description': 'Personal debe ser consciente de la política y su contribución al AIMS',
            'category': 'Soporte'
        },
        {
            'clause': '7.4',
            'requirement': 'Comunicación',
            'description': 'Establecer comunicaciones internas y externas relevantes para el AIMS',
            'category': 'Soporte'
        },
        {
            'clause': '7.5',
            'requirement': 'Información documentada',
            'description': 'Mantener información documentada requerida por el estándar',
            'category': 'Soporte'
        },
        
        # Cláusula 8: Operación
        {
            'clause': '8.1',
            'requirement': 'Planificación y control operacional',
            'description': 'Planificar, implementar y controlar procesos necesarios',
            'category': 'Operación'
        },
        {
            'clause': '8.2',
            'requirement': 'Evaluación de impacto de IA',
            'description': 'Realizar evaluaciones de impacto para sistemas de IA',
            'category': 'Operación'
        },
        
        # Cláusula 9: Evaluación del desempeño
        {
            'clause': '9.1',
            'requirement': 'Seguimiento, medición, análisis y evaluación',
            'description': 'Monitorear y medir el desempeño del AIMS',
            'category': 'Evaluación'
        },
        {
            'clause': '9.2',
            'requirement': 'Auditoría interna',
            'description': 'Realizar auditorías internas a intervalos planificados',
            'category': 'Evaluación'
        },
        {
            'clause': '9.3',
            'requirement': 'Revisión por la dirección',
            'description': 'Alta dirección debe revisar el AIMS a intervalos planificados',
            'category': 'Evaluación'
        },
        
        # Cláusula 10: Mejora
        {
            'clause': '10.1',
            'requirement': 'No conformidad y acción correctiva',
            'description': 'Gestionar no conformidades y tomar acciones correctivas',
            'category': 'Mejora'
        },
        {
            'clause': '10.2',
            'requirement': 'Mejora continua',
            'description': 'Mejorar continuamente la idoneidad, adecuación y eficacia del AIMS',
            'category': 'Mejora'
        },
        
        # Anexo A - 38 controles
        # A.2 Gobernanza organizacional (3 controles)
        {
            'clause': 'A.2.2',
            'requirement': 'Roles y responsabilidades de seguridad de la información',
            'description': 'Asignar roles claros para la gestión de información en sistemas de IA',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.2.3',
            'requirement': 'Segregación de funciones',
            'description': 'Separar responsabilidades para reducir riesgos de uso indebido',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.2.4',
            'requirement': 'Responsabilidades de gestión',
            'description': 'Definir responsabilidades de liderazgo en el ciclo de vida de IA',
            'category': 'Anexo A'
        },
        
        # A.3 Gestión de activos (2 controles)
        {
            'clause': 'A.3.1',
            'requirement': 'Inventario de activos',
            'description': 'Mantener registro actualizado de activos vinculados a sistemas de IA',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.3.2',
            'requirement': 'Uso aceptable de activos',
            'description': 'Establecer reglas de uso apropiado de recursos de IA',
            'category': 'Anexo A'
        },
        
        # A.4 Seguridad de recursos humanos (5 controles)
        {
            'clause': 'A.4.1',
            'requirement': 'Selección',
            'description': 'Verificar antecedentes del personal que desarrolla o gestiona IA',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.4.2',
            'requirement': 'Términos y condiciones de empleo',
            'description': 'Incluir responsabilidades de seguridad de IA en contratos',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.4.3',
            'requirement': 'Concienciación, educación y formación',
            'description': 'Capacitar al personal en uso responsable y seguro de IA',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.4.4',
            'requirement': 'Proceso disciplinario',
            'description': 'Definir consecuencias ante incumplimientos en uso de IA',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.4.5',
            'requirement': 'Responsabilidades al finalizar o cambiar empleo',
            'description': 'Gestionar el acceso a sistemas de IA al término de relación laboral',
            'category': 'Anexo A'
        },
        
        # A.5 Controles físicos (4 controles)
        {
            'clause': 'A.5.1',
            'requirement': 'Perímetros de seguridad física',
            'description': 'Proteger instalaciones donde operan sistemas críticos de IA',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.5.2',
            'requirement': 'Controles de entrada física',
            'description': 'Restringir acceso físico a infraestructura de IA',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.5.3',
            'requirement': 'Seguridad de oficinas y recursos',
            'description': 'Proteger espacios de trabajo relacionados con IA',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.5.4',
            'requirement': 'Protección contra amenazas externas y ambientales',
            'description': 'Salvaguardar infraestructura de IA de desastres naturales',
            'category': 'Anexo A'
        },
        
        # A.6.1 Gestión del ciclo de vida de sistemas de IA (2 controles)
        {
            'clause': 'A.6.1.1',
            'requirement': 'Inventario de sistemas de IA',
            'description': 'Mantener registro actualizado de todos los sistemas de IA',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.6.1.2',
            'requirement': 'Decisiones sobre uso de IA',
            'description': 'Documentar decisiones clave sobre cuándo y cómo usar IA',
            'category': 'Anexo A'
        },
        
        # A.6.2 Gestión de datos para IA (7 controles)
        {
            'clause': 'A.6.2.1',
            'requirement': 'Gestión de datos para IA',
            'description': 'Implementar controles de calidad y gestión de datos de entrenamiento',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.6.2.2',
            'requirement': 'Calidad de datos',
            'description': 'Asegurar exactitud, completitud y relevancia de datos para IA',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.6.2.3',
            'requirement': 'Etiquetado de datos',
            'description': 'Etiquetar datos de manera consistente y precisa para entrenamiento',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.6.2.4',
            'requirement': 'Privacidad de datos',
            'description': 'Proteger datos personales procesados por sistemas de IA',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.6.2.5',
            'requirement': 'Sesgo en datos',
            'description': 'Identificar y mitigar sesgos en conjuntos de datos',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.6.2.6',
            'requirement': 'Proveniencia de datos',
            'description': 'Documentar origen y linaje de datos utilizados',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.6.2.7',
            'requirement': 'Seguridad de datos',
            'description': 'Proteger datos de acceso no autorizado y manipulación',
            'category': 'Anexo A'
        },
        
        # A.7 Desarrollo y despliegue de IA (5 controles)
        {
            'clause': 'A.7.1',
            'requirement': 'Diseño seguro de sistemas de IA',
            'description': 'Incorporar seguridad desde la fase de diseño',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.7.2',
            'requirement': 'Desarrollo seguro',
            'description': 'Aplicar prácticas de desarrollo seguro en ciclo de vida',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.7.3',
            'requirement': 'Supervisión humana',
            'description': 'Implementar niveles apropiados de supervisión humana',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.7.4',
            'requirement': 'Pruebas y validación',
            'description': 'Verificar funcionamiento correcto antes del despliegue',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.7.5',
            'requirement': 'Gestión de cambios',
            'description': 'Controlar modificaciones a sistemas de IA en producción',
            'category': 'Anexo A'
        },
        
        # A.8 Operación de sistemas de IA (4 controles)
        {
            'clause': 'A.8.1',
            'requirement': 'Gestión de riesgos de IA',
            'description': 'Implementar proceso formal de gestión de riesgos específico para IA',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.8.2',
            'requirement': 'Monitoreo continuo',
            'description': 'Vigilar desempeño y comportamiento de sistemas de IA',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.8.3',
            'requirement': 'Gestión de incidentes',
            'description': 'Responder a fallos o comportamientos inesperados',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.8.4',
            'requirement': 'Respaldo y recuperación',
            'description': 'Asegurar continuidad operativa de sistemas críticos de IA',
            'category': 'Anexo A'
        },
        
        # A.9 Transparencia y explicabilidad (3 controles)
        {
            'clause': 'A.9.1',
            'requirement': 'Transparencia',
            'description': 'Comunicar claramente el uso de sistemas de IA',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.9.2',
            'requirement': 'Explicabilidad',
            'description': 'Proporcionar explicaciones comprensibles de decisiones de IA',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.9.3',
            'requirement': 'Comunicación con partes interesadas',
            'description': 'Informar a usuarios y afectados sobre sistemas de IA',
            'category': 'Anexo A'
        },
        
        # A.10 Relaciones con proveedores (3 controles)
        {
            'clause': 'A.10.1',
            'requirement': 'Políticas para relaciones con proveedores',
            'description': 'Establecer requisitos para proveedores de componentes de IA',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.10.2',
            'requirement': 'Gestión de la prestación de servicios por proveedores',
            'description': 'Supervisar desempeño de proveedores de servicios de IA',
            'category': 'Anexo A'
        },
        {
            'clause': 'A.10.3',
            'requirement': 'Cambios en servicios de proveedores',
            'description': 'Gestionar modificaciones en servicios de terceros',
            'category': 'Anexo A'
        },
        
        # A.10.4 - Control adicional
        {
            'clause': 'A.10.4',
            'requirement': 'Revisión de acuerdos con proveedores',
            'description': 'Revisar periódicamente contratos y niveles de servicio',
            'category': 'Anexo A'
        },
    ]


def get_status_config() -> dict[str, dict[str, str]]:
    """Get status configuration with colors and emojis.
    
    Returns:
        Dictionary with status configurations
    """
    return {
        'No iniciado': {
            'emoji': '⚪',
            'color': '#E0E0E0',
            'description': 'Requisito no comenzado'
        },
        'En progreso': {
            'emoji': '🟡',
            'color': '#FDD835',
            'description': 'Implementación en curso'
        },
        'Cumplido': {
            'emoji': '🟢',
            'color': '#4CAF50',
            'description': 'Requisito completamente implementado'
        },
        'No aplica': {
            'emoji': '⚫',
            'color': '#9E9E9E',
            'description': 'No aplicable a esta organización'
        }
    }


def get_categories() -> list[str]:
    """Get list of requirement categories.
    
    Returns:
        List of category names
    """
    return [
        'Contexto',
        'Liderazgo',
        'Planificación',
        'Soporte',
        'Operación',
        'Evaluación',
        'Mejora',
        'Anexo A'
    ]
