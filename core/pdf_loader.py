"""PDF loading and text extraction utilities."""
import logging
from pathlib import Path
from typing import Optional
from pypdf import PdfReader


logger = logging.getLogger(__name__)


class PDFValidationError(Exception):
    """Raised when PDF validation fails."""
    pass


def validate_pdf(file_path: Path, max_size_mb: int = 50) -> tuple[bool, Optional[str]]:
    """Validate that a PDF file is suitable for processing.
    
    Args:
        file_path: Path to PDF file
        max_size_mb: Maximum allowed file size in MB
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Check file exists
        if not file_path.exists():
            return False, "El archivo no existe."
        
        # Check file size
        size_mb = file_path.stat().st_size / (1024 * 1024)
        if size_mb > max_size_mb:
            return False, f"El archivo es demasiado grande ({size_mb:.1f} MB). Máximo permitido: {max_size_mb} MB."
        
        # Try to open and read
        reader = PdfReader(str(file_path))
        
        # Check if PDF has pages
        if len(reader.pages) == 0:
            return False, "El PDF no contiene páginas."
        
        # Check if PDF has extractable text
        has_text = False
        for page_num in range(min(3, len(reader.pages))):  # Check first 3 pages
            text = reader.pages[page_num].extract_text()
            if text and text.strip():
                has_text = True
                break
        
        if not has_text:
            return False, (
                "El PDF no contiene texto extraíble. "
                "Es posible que sea un documento escaneado. "
                "Por favor, usa un PDF con texto seleccionable o aplica OCR primero."
            )
        
        return True, None
        
    except Exception as e:
        logger.error(f"Error validating PDF: {e}")
        return False, f"Error al validar el PDF: {str(e)}"


def extract_text_with_metadata(file_path: Path) -> list[dict[str, any]]:
    """Extract text from PDF with page numbers.
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        List of dictionaries with page_num and text keys
        
    Raises:
        PDFValidationError: If PDF validation fails
    """
    # Validate first
    is_valid, error_msg = validate_pdf(file_path)
    if not is_valid:
        raise PDFValidationError(error_msg)
    
    try:
        reader = PdfReader(str(file_path))
        pages_data = []
        
        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if text and text.strip():
                pages_data.append({
                    'page_num': page_num,
                    'text': text.strip(),
                    'document_name': file_path.name
                })
        
        logger.info(f"Extracted {len(pages_data)} pages from {file_path.name}")
        return pages_data
        
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        raise PDFValidationError(f"Error al extraer texto del PDF: {str(e)}")


def get_pdf_info(file_path: Path) -> dict[str, any]:
    """Get basic information about a PDF file.
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Dictionary with PDF metadata
    """
    try:
        reader = PdfReader(str(file_path))
        
        info = {
            'num_pages': len(reader.pages),
            'file_name': file_path.name,
            'file_size_mb': round(file_path.stat().st_size / (1024 * 1024), 2),
            'metadata': reader.metadata if reader.metadata else {}
        }
        
        return info
        
    except Exception as e:
        logger.error(f"Error getting PDF info: {e}")
        return {
            'num_pages': 0,
            'file_name': file_path.name,
            'file_size_mb': 0,
            'metadata': {},
            'error': str(e)
        }
