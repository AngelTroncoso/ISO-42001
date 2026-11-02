"""ISO clause number detection and parsing."""
import re
import logging
from typing import Optional


logger = logging.getLogger(__name__)


# Regex pattern for clause detection
CLAUSE_PATTERN = re.compile(r'^\s*((?:[A-C]\.)?\d+(?:\.\d+)*)(?=\s|$)', re.MULTILINE)


def detect_clause(text: str) -> Optional[str]:
    """Detect ISO clause number in text.
    
    Looks for patterns like:
    - 4.1, 6.1.2, 10.2.3
    - A.2.2, B.6.2.4
    
    Args:
        text: Text to search for clause numbers
        
    Returns:
        First detected clause number or None
    """
    if not text:
        return None
    
    # Look for clause patterns in the first 500 characters
    search_text = text[:500]
    
    match = CLAUSE_PATTERN.search(search_text)
    if match:
        clause = match.group(1)
        if is_valid_clause(clause):
            return clause
    
    return None


def is_valid_clause(clause: str) -> bool:
    """Validate that a clause number looks legitimate.
    
    Args:
        clause: Clause number to validate
        
    Returns:
        True if clause looks valid
    """
    # Check for annex clauses (A.x.x, B.x.x, etc.)
    if re.match(r'^[A-Z]\.\d+', clause):
        return True
    
    # Check for main clauses (numbers only)
    if re.match(r'^\d+', clause):
        parts = clause.split('.')
        # First part should be between 1-15 (typical ISO range)
        try:
            first_num = int(parts[0])
            if 1 <= first_num <= 15:
                return True
        except ValueError:
            pass
    
    return False


def extract_clauses_from_text(text: str) -> list[str]:
    """Extract all clause numbers from text.
    
    Args:
        text: Text to search
        
    Returns:
        List of unique clause numbers found
    """
    clauses = set()
    
    for match in CLAUSE_PATTERN.finditer(text):
        clause = match.group(1)
        if is_valid_clause(clause):
            clauses.add(clause)
    
    return sorted(list(clauses))


def format_clause_reference(clause: str, page_num: int) -> str:
    """Format a clause reference for display.
    
    Args:
        clause: Clause number
        page_num: Page number
        
    Returns:
        Formatted reference string
    """
    return f"Cláusula {clause}, página {page_num}"


def parse_clause_hierarchy(clause: str) -> dict[str, any]:
    """Parse clause hierarchy levels.
    
    Args:
        clause: Clause number (e.g., "6.1.2" or "A.2.3")
        
    Returns:
        Dictionary with hierarchy information
    """
    is_annex = clause[0].isalpha()
    
    if is_annex:
        # Remove letter prefix for processing
        parts = clause[2:].split('.')
        return {
            'is_annex': True,
            'annex_letter': clause[0],
            'levels': [clause[0]] + parts,
            'depth': len(parts) + 1,
            'main_clause': f"{clause[0]}.{parts[0]}" if parts else clause[0]
        }
    else:
        parts = clause.split('.')
        return {
            'is_annex': False,
            'annex_letter': None,
            'levels': parts,
            'depth': len(parts),
            'main_clause': parts[0] if parts else clause
        }
