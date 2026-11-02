"""RAG (Retrieval Augmented Generation) engine using LlamaIndex and Mistral AI."""
import logging
from pathlib import Path
from typing import Optional
from llama_index.core import (
    VectorStoreIndex,
    Document,
    Settings,
    StorageContext,
    load_index_from_storage
)
from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from core.pdf_loader import extract_text_with_metadata
from core.clause_parser import detect_clause


logger = logging.getLogger(__name__)


class RAGEngine:
    """RAG engine for querying ISO 42001 documents."""
    
    def __init__(
        self,
        api_key: str,
        llm_model: str = "mistral-small-latest",
        embed_model: str = "mistral-embed",
        chunk_size: int = 800,
        chunk_overlap: int = 120
    ):
        """Initialize RAG engine.
        
        Args:
            api_key: Mistral API key
            llm_model: LLM model name
            embed_model: Embedding model name
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.api_key = api_key
        self.llm_model = llm_model
        self.embed_model = embed_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Configure LlamaIndex settings
        Settings.llm = MistralAI(api_key=api_key, model=llm_model)
        Settings.embed_model = MistralAIEmbedding(
            api_key=api_key,
            model_name=embed_model
        )
        Settings.chunk_size = chunk_size
        Settings.chunk_overlap = chunk_overlap
        
        self.index: Optional[VectorStoreIndex] = None
        self.documents_loaded = []
        
        logger.info(f"RAG engine initialized with {llm_model}")
    
    def load_pdf(self, pdf_path: Path, persist_dir: Path) -> int:
        """Load and index a PDF document.
        
        Args:
            pdf_path: Path to PDF file
            persist_dir: Directory to persist index
            
        Returns:
            Number of chunks created
            
        Raises:
            Exception if loading fails
        """
        try:
            # Extract text with metadata
            pages_data = extract_text_with_metadata(pdf_path)
            
            # Create LlamaIndex documents with metadata
            documents = []
            for page_data in pages_data:
                # Detect clause in page text
                clause = detect_clause(page_data['text'])
                
                metadata = {
                    'page_num': page_data['page_num'],
                    'document_name': page_data['document_name'],
                }
                
                if clause:
                    metadata['clause'] = clause
                
                doc = Document(
                    text=page_data['text'],
                    metadata=metadata
                )
                documents.append(doc)
            
            # Create index
            self.index = VectorStoreIndex.from_documents(
                documents,
                show_progress=True
            )
            
            self.documents_loaded.append(pdf_path.name)
            
            # Persist index automatically
            self.save_index(persist_dir)
            
            logger.info(f"Loaded {len(documents)} pages from {pdf_path.name}")
            return len(documents)
            
        except Exception as e:
            logger.error(f"Error loading PDF: {e}")
            raise
    
    def query(
        self,
        question: str,
        top_k: int = 5,
        similarity_threshold: float = 0.5
    ) -> dict[str, any]:
        """Query the indexed documents.
        
        Args:
            question: User question
            top_k: Number of relevant chunks to retrieve
            similarity_threshold: Minimum similarity score
            
        Returns:
            Dictionary with answer and sources
        """
        if not self.index:
            return {
                'answer': 'No hay documentos cargados. Por favor, sube un PDF primero.',
                'sources': [],
                'error': 'No index available'
            }
        
        try:
            # Create query engine
            query_engine = self.index.as_query_engine(
                similarity_top_k=top_k,
                response_mode='compact'
            )
            
            # Execute query
            response = query_engine.query(question)
            
            # Extract sources with citations
            sources = []
            for node in response.source_nodes:
                metadata = node.node.metadata
                
                citation = f"Página {metadata.get('page_num', 'N/A')}"
                if 'clause' in metadata:
                    citation = f"Cláusula {metadata['clause']}, {citation}"
                
                sources.append({
                    'text': node.node.text[:300] + '...' if len(node.node.text) > 300 else node.node.text,
                    'citation': citation,
                    'score': node.score if hasattr(node, 'score') else None,
                    'metadata': metadata
                })
            
            return {
                'answer': str(response),
                'sources': sources,
                'error': None
            }
            
        except Exception as e:
            logger.error(f"Error during query: {e}")
            return {
                'answer': f'Error al procesar la consulta: {str(e)}',
                'sources': [],
                'error': str(e)
            }
    
    def get_index_stats(self) -> dict[str, any]:
        """Get statistics about the loaded index.
        
        Returns:
            Dictionary with index statistics
        """
        if not self.index:
            return {
                'num_documents': 0,
                'documents_loaded': [],
                'is_ready': False
            }
        
        return {
            'num_documents': len(self.documents_loaded),
            'documents_loaded': self.documents_loaded,
            'is_ready': True
        }
    
    def save_index(self, persist_dir: Path) -> None:
        """Save index to disk.
        
        Args:
            persist_dir: Directory to save index
        """
        if not self.index:
            logger.warning("No index to save")
            return
        
        try:
            persist_dir.mkdir(parents=True, exist_ok=True)
            self.index.storage_context.persist(persist_dir=str(persist_dir))
            logger.info(f"Index saved to {persist_dir}")
        except Exception as e:
            logger.error(f"Error saving index: {e}")
            raise
    
    def load_index(self, persist_dir: Path) -> bool:
        """Load index from disk.
        
        Args:
            persist_dir: Directory containing saved index
            
        Returns:
            True if loaded successfully
        """
        try:
            if not persist_dir.exists():
                logger.warning(f"Persist directory {persist_dir} does not exist")
                return False
            
            storage_context = StorageContext.from_defaults(persist_dir=str(persist_dir))
            self.index = load_index_from_storage(storage_context)
            logger.info(f"Index loaded from {persist_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading index: {e}")
            return False
