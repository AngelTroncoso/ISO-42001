"""Tests for PDF loader module."""
import pytest
from pathlib import Path
from pypdf import PdfWriter, PageObject
from core.pdf_loader import validate_pdf, PDFValidationError


class TestValidatePDF:
    """Tests for PDF validation."""
    
    def test_nonexistent_file(self):
        """Test validation of nonexistent file."""
        fake_path = Path("nonexistent_file.pdf")
        is_valid, error_msg = validate_pdf(fake_path)
        
        assert is_valid is False
        assert "no existe" in error_msg.lower()
    
    def test_empty_pdf_without_text(self, tmp_path):
        """Test PDF without extractable text (simulated scanned PDF)."""
        # Create a minimal PDF without text content
        tmp_file = tmp_path / "empty.pdf"
        
        # Create empty PDF
        writer = PdfWriter()
        page = PageObject.create_blank_page(width=612, height=792)
        writer.add_page(page)
        
        with open(tmp_file, 'wb') as f:
            writer.write(f)
        
        # Validate - should fail due to no extractable text
        is_valid, error_msg = validate_pdf(tmp_file)
        
        assert is_valid is False
        assert "texto extraíble" in error_msg or "escaneado" in error_msg
