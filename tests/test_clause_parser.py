"""Tests for clause parser module."""
import pytest
from core.clause_parser import (
    detect_clause,
    is_valid_clause,
    extract_clauses_from_text,
    format_clause_reference,
    parse_clause_hierarchy
)


class TestDetectClause:
    """Tests for detect_clause function."""
    
    def test_detect_main_clause_single(self):
        """Test detection of main clause with single number."""
        text = "4.1 Understanding the organization and its context"
        result = detect_clause(text)
        assert result == "4.1"
    
    def test_detect_main_clause_multi_level(self):
        """Test detection of multi-level main clause."""
        text = "6.1.2 AI system impact assessment shall be performed"
        result = detect_clause(text)
        assert result == "6.1.2"
    
    def test_detect_annex_clause(self):
        """Test detection of annex clause."""
        text = "A.2.2 Information security roles and responsibilities"
        result = detect_clause(text)
        assert result == "A.2.2"
    
    def test_detect_annex_clause_b(self):
        """Test detection of B annex clause."""
        text = "B.6.2.4 Data quality for AI"
        result = detect_clause(text)
        assert result == "B.6.2.4"
    
    def test_no_clause_detected(self):
        """Test when no clause is present."""
        text = "This is just some random text without clause numbers"
        result = detect_clause(text)
        assert result is None
    
    def test_empty_text(self):
        """Test with empty text."""
        result = detect_clause("")
        assert result is None
    
    def test_none_text(self):
        """Test with None input."""
        result = detect_clause(None)
        assert result is None


class TestIsValidClause:
    """Tests for is_valid_clause function."""
    
    def test_valid_main_clause(self):
        """Test valid main clauses."""
        assert is_valid_clause("4.1") is True
        assert is_valid_clause("6.1.2") is True
        assert is_valid_clause("10.2") is True
    
    def test_valid_annex_clause(self):
        """Test valid annex clauses."""
        assert is_valid_clause("A.2.2") is True
        assert is_valid_clause("B.6.2.4") is True
        assert is_valid_clause("C.1") is True
    
    def test_invalid_high_number(self):
        """Test rejection of unrealistically high clause numbers."""
        assert is_valid_clause("99.1") is False
        assert is_valid_clause("100.2.3") is False
    
    def test_invalid_format(self):
        """Test rejection of invalid formats."""
        assert is_valid_clause("abc") is False
        assert is_valid_clause("1.2.3.4.5.6") is True  # Should still work for deep nesting


class TestExtractClausesFromText:
    """Tests for extract_clauses_from_text function."""
    
    def test_extract_multiple_clauses(self):
        """Test extracting multiple clauses from text."""
        text = """
        This document covers 4.1, 4.2, and 6.1.2 as main requirements.
        Additionally, see Annex A.2.2 and B.6.2.4 for controls.
        """
        result = extract_clauses_from_text(text)
        assert "4.1" in result
        assert "4.2" in result
        assert "6.1.2" in result
        assert "A.2.2" in result
        assert "B.6.2.4" in result
    
    def test_extract_no_clauses(self):
        """Test when no clauses are present."""
        text = "This text has no clause references at all"
        result = extract_clauses_from_text(text)
        assert len(result) == 0
    
    def test_extract_unique_clauses(self):
        """Test that duplicates are removed."""
        text = "See 4.1 and also refer to 4.1 again, and 4.1 once more"
        result = extract_clauses_from_text(text)
        assert result.count("4.1") == 1


class TestFormatClauseReference:
    """Tests for format_clause_reference function."""
    
    def test_format_reference(self):
        """Test formatting of clause reference."""
        result = format_clause_reference("6.1.2", 42)
        assert result == "Cláusula 6.1.2, página 42"
    
    def test_format_annex_reference(self):
        """Test formatting of annex reference."""
        result = format_clause_reference("A.2.2", 78)
        assert result == "Cláusula A.2.2, página 78"


class TestParseClauseHierarchy:
    """Tests for parse_clause_hierarchy function."""
    
    def test_parse_main_clause(self):
        """Test parsing main clause hierarchy."""
        result = parse_clause_hierarchy("6.1.2")
        assert result['is_annex'] is False
        assert result['annex_letter'] is None
        assert result['levels'] == ['6', '1', '2']
        assert result['depth'] == 3
        assert result['main_clause'] == '6'
    
    def test_parse_annex_clause(self):
        """Test parsing annex clause hierarchy."""
        result = parse_clause_hierarchy("A.2.3")
        assert result['is_annex'] is True
        assert result['annex_letter'] == 'A'
        assert result['levels'] == ['A', '2', '3']
        assert result['depth'] == 3
        assert result['main_clause'] == 'A.2'
    
    def test_parse_single_level(self):
        """Test parsing single level clause."""
        result = parse_clause_hierarchy("5")
        assert result['is_annex'] is False
        assert result['depth'] == 1
        assert result['main_clause'] == '5'
