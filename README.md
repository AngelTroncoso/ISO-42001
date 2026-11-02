# 🤖 ISO/IEC 42001:2023 - Sistema de Gestión de Cumplimiento

Aplicación web en Streamlit para implementar y gestionar el cumplimiento del estándar internacional **ISO/IEC 42001:2023** (Sistema de Gestión de Inteligencia Artificial).

## 📋 Descripción

Esta aplicación ayuda a organizaciones a implementar un **Sistema de Gestión de Inteligencia Artificial (AIMS)** conforme a ISO/IEC 42001:2023. Ofrece tres funcionalidades principales:

1. **📚 Consulta de la Norma con RAG**: Sube el PDF de la norma y realiza preguntas específicas con respuestas contextualizadas y citas precisas
2. **📊 Seguimiento de Cumplimiento**: Gestiona un catálogo de 59 requisitos (cláusulas 4-10 y 38 controles del Anexo A)
3. **💬 Asesor Virtual Experto**: Chatbot inteligente que guía paso a paso en la implementación del estándar

### Características Principales

- ✅ **Búsqueda semántica (RAG)** en el documento ISO 42001 con citas de cláusulas y páginas
- ✅ **Detección automática** de cláusulas numéricas (4.1, 6.1.2, A.2.2, B.6.2.4)
- ✅ **Persistencia automática** del índice vectorial (no reindexar tras reinicio)
- ✅ **Tabla editable** de requisitos con seguimiento de progreso
- ✅ **Dashboard visual** con métricas, gráficos y cronogramas
- ✅ **Chatbot asesor** con respuestas en español y guías prácticas
- ✅ **Exportación** a Excel y CSV
- ✅ **Base de datos SQLite** para persistencia
- ✅ **Interfaz en español**, código en inglés

## 🚀 Requisitos Previos

- **Python 3.12** o superior
- **Clave API de Mistral AI** (gratuita en https://console.mistral.ai/)
- **Copia legal del estándar ISO/IEC 42001:2023 en PDF** (ver sección de Derechos de Autor)

## 📦 Instalación

### 1. Clonar o descargar el proyecto

```powershell
# Si tienes el código descargado
cd c:\Users\angel\OneDrive\Escritorio\kiro
```

### 2. Crear entorno virtual

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

**Opción A: Archivo .env**

Copia `.env.example` a `.env`:

```powershell
copy .env.example .env
```

Edita `.env` y añade tu API key:
```
MISTRAL_API_KEY=tu_clave_api_aqui
MISTRAL_LLM_MODEL=mistral-small-latest
MISTRAL_EMBED_MODEL=mistral-embed
DATA_DIR=./data
CHUNK_SIZE=800
CHUNK_OVERLAP=120
```

**Opción B: Streamlit secrets**

Copia `.streamlit/secrets.toml.example` a `.streamlit/secrets.toml`:

```powershell
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
```

Edita `.streamlit/secrets.toml` con tu API key.

### 5. Obtener tu API Key de Mistral AI

1. Regístrate en https://console.mistral.ai/
2. Ve a "API Keys" en el dashboard
3. Crea una nueva API key
4. Cópiala y úsala en el paso anterior

## ▶️ Ejecución

Ejecuta la aplicación con:

```powershell
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📖 Uso Básico

### Paso 1: Cargar el Documento ISO 42001

1. Ve a **📚 Biblioteca** en el menú lateral
2. Sube tu copia en PDF del estándar ISO/IEC 42001:2023
3. El sistema validará el PDF y lo procesará (esto toma unos minutos)
4. El índice vectorial se guarda automáticamente y se carga en siguientes sesiones

⚠️ **Importante**: Debes tener tu propia copia legal del estándar. Esta aplicación NO incluye el texto de la norma por derechos de autor.

### Paso 2: Inicializar el Seguimiento de Cumplimiento

1. Ve a **📊 Seguimiento**
2. Haz clic en "🚀 Inicializar con Catálogo Predeterminado"
3. Se cargarán 59 requisitos (21 de cláusulas principales + 38 del Anexo A)
4. Edita estados, responsables, fechas y notas según tu progreso

### Paso 3: Comenzar a Usar

- **🔍 Consultar Norma**: Haz preguntas sobre el estándar y obtén respuestas con citas
- **💬 Asesor IA**: Obtén guía práctica sobre implementación, documentación y auditoría
- **📊 Seguimiento**: Actualiza el progreso y visualiza métricas

## ⚠️ Aviso de Derechos de Autor

### Importante: Esta aplicación NO incluye el texto de la norma

ISO/IEC 42001:2023 es un estándar internacional protegido por derechos de autor. **Este repositorio NO incluye ni distribuye el contenido de la norma.**

### ¿Cómo obtener el estándar?

Debes adquirir una copia legal desde:

- **ISO**: https://www.iso.org/standard/81230.html
- **Organismos nacionales de normalización** (AENOR en España, IRAM en Argentina, etc.)
- **Proveedores autorizados**

### Uso permitido

- ✅ Usar esta aplicación con tu copia legal del PDF
- ✅ Procesar el documento localmente en tu sesión
- ✅ Compartir la aplicación (código) con tu equipo
- ❌ NO redistribuir el PDF de la norma
- ❌ NO compartir extractos extensos del texto

## ✅ Preguntas de Verificación

Para verificar que el sistema RAG funciona correctamente, haz estas preguntas en la sección **🔍 Consultar Norma**:

### Pregunta 1: "¿Qué dice el control A.2.2?"

**Respuesta esperada**: Debe mencionar roles y responsabilidades de seguridad de la información, con cita a "Cláusula A.2.2, página X".

### Pregunta 2: "¿Qué es la evaluación de impacto del sistema de IA?"

**Respuesta esperada**: Debe explicar que es una evaluación sistemática para identificar impactos potenciales de un sistema de IA, referenciando la cláusula 8.2, con cita específica de página.

Si ambas preguntas se responden correctamente con citas precisas, el sistema RAG funciona correctamente.

## 🧪 Ejecutar Tests

Ejecuta todos los tests con:

```powershell
pytest tests\ -v
```

**Tests implementados**: 35 tests

- **test_clause_parser.py**: 12 tests de detección de cláusulas (4.1, 6.1.2, A.2.2, B.6.2.4)
- **test_compliance_tracker.py**: 8 tests de cálculo de métricas y progreso
- **test_database.py**: 12 tests de operaciones CRUD en SQLite
- **test_pdf_loader.py**: 2 tests de validación de PDFs
- **test_rag_persistence.py**: 3 tests de guardado y carga de índices

Todos los tests deben pasar. Si alguno falla, revisa la configuración.

## 📁 Estructura del Proyecto

```
iso-42001-compliance/
├── app.py                          # Punto de entrada principal
├── config.py                       # Carga de configuración
├── requirements.txt                # Dependencias con rangos compatibles
├── README.md                       # Este archivo
├── .env.example                    # Plantilla de variables de entorno
├── .gitignore                      # Archivos ignorados por Git
│
├── .streamlit/
│   ├── config.toml                 # Configuración de Streamlit
│   └── secrets.toml.example        # Plantilla de secrets
│
├── core/                           # Módulos principales
│   ├── pdf_loader.py               # Carga y validación de PDFs
│   ├── clause_parser.py            # Detección de cláusulas con regex
│   ├── rag_engine.py               # Motor RAG con LlamaIndex y persistencia
│   ├── agent.py                    # Chatbot asesor
│   ├── compliance_data.py          # Catálogo de 59 requisitos
│   └── compliance_tracker.py       # Lógica de seguimiento
│
├── storage/
│   └── database.py                 # Gestión de SQLite
│
├── ui/                             # Interfaces de usuario
│   ├── components.py               # Componentes reutilizables
│   ├── pages_home.py               # Página de inicio
│   ├── pages_library.py            # Gestión de documentos
│   ├── pages_search.py             # Búsqueda RAG
│   ├── pages_tracker.py            # Seguimiento de cumplimiento
│   └── pages_advisor.py            # Chatbot asesor
│
├── utils/
│   └── helpers.py                  # Funciones auxiliares
│
└── tests/                          # Tests unitarios (35 tests)
    ├── test_clause_parser.py
    ├── test_compliance_tracker.py
    ├── test_database.py
    ├── test_pdf_loader.py
    └── test_rag_persistence.py
```

## 🔧 Stack Tecnológico

| Componente | Tecnología | Versión |
|------------|------------|---------|
| Framework UI | Streamlit | >=1.29,<2 |
| RAG Framework | LlamaIndex Core | >=0.10,<0.13 |
| LLM | Mistral AI | mistral-small-latest |
| Embeddings | Mistral Embed | mistral-embed |
| PDF Processing | pypdf | >=4.0,<6 |
| Base de datos | SQLite | (stdlib) |
| Data Analysis | pandas | >=2.1,<3 |
| Visualización | Plotly | >=5.18,<6 |
| Export | openpyxl | >=3.1,<4 |
| Testing | pytest | >=7.4,<9 |
| Config | python-dotenv | >=1.0,<2 |

## 🚀 Despliegue en Streamlit Cloud

### Pasos para desplegar:

1. Sube el proyecto a GitHub (sin incluir `.env`, `data/`, `*.pdf`)
2. Ve a https://share.streamlit.io/
3. Conecta tu repositorio
4. En "Advanced settings" → "Secrets", añade:
   ```
   MISTRAL_API_KEY = "tu_clave_api"
   ```
5. Despliega

### Limitaciones en la nube:

- ⚠️ Los archivos subidos (PDFs) son **temporales** y se pierden al reiniciar
- ⚠️ El índice persistido se guarda pero puede perderse en redeploys
- 💡 **Solución**: Ejecuta localmente para uso continuo con persistencia completa

## ⚠️ Limitaciones Conocidas

1. **PDFs escaneados**: No soportados (necesitan OCR previo)
2. **Autenticación**: No implementada (single-user o confianza total)
3. **Concurrencia**: SQLite no óptimo para >10 usuarios simultáneos
4. **Catálogo**: 59 requisitos principales (simplificado para claridad)

Todas aceptables para MVP/uso interno.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo licencia MIT.

**Nota importante**: El código de esta aplicación es libre, pero **el estándar ISO/IEC 42001:2023 está protegido por derechos de autor** y debe adquirirse legalmente.

## 📞 Soporte

Para preguntas o problemas:

1. Revisa las Preguntas de Verificación en este README
2. Consulta los logs de la aplicación
3. Ejecuta `pytest tests\ -v` para verificar integridad
4. Abre un issue en el repositorio

---

**Versión**: 1.0.0  
**Última actualización**: 2024  
**Desarrollado con**: Python 3.12, Streamlit, LlamaIndex, Mistral AI
