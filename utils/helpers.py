"""Utility helper functions."""
import logging
from pathlib import Path
from typing import Optional
import streamlit as st


logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration.
    
    Args:
        level: Logging level
    """
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def ensure_directory(directory: Path) -> None:
    """Ensure a directory exists.
    
    Args:
        directory: Path to directory
    """
    directory.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directory exists: {directory}")


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def show_success_message(message: str) -> None:
    """Show a success message in Streamlit.
    
    Args:
        message: Message to display
    """
    st.success(f"✅ {message}")


def show_error_message(message: str) -> None:
    """Show an error message in Streamlit.
    
    Args:
        message: Message to display
    """
    st.error(f"❌ {message}")


def show_warning_message(message: str) -> None:
    """Show a warning message in Streamlit.
    
    Args:
        message: Message to display
    """
    st.warning(f"⚠️ {message}")


def show_info_message(message: str) -> None:
    """Show an info message in Streamlit.
    
    Args:
        message: Message to display
    """
    st.info(f"ℹ️ {message}")


def get_status_emoji(status: str) -> str:
    """Get emoji for status.
    
    Args:
        status: Status name
        
    Returns:
        Emoji character
    """
    emoji_map = {
        'No iniciado': '⚪',
        'En progreso': '🟡',
        'Cumplido': '🟢',
        'No aplica': '⚫'
    }
    return emoji_map.get(status, '⚪')


def get_status_color(status: str) -> str:
    """Get color for status.
    
    Args:
        status: Status name
        
    Returns:
        Hex color code
    """
    color_map = {
        'No iniciado': '#E0E0E0',
        'En progreso': '#FDD835',
        'Cumplido': '#4CAF50',
        'No aplica': '#9E9E9E'
    }
    return color_map.get(status, '#E0E0E0')


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if not text or len(text) <= max_length:
        return text
    return text[:max_length-3] + '...'


def validate_date_format(date_str: str) -> bool:
    """Validate date string format (YYYY-MM-DD).
    
    Args:
        date_str: Date string to validate
        
    Returns:
        True if valid
    """
    if not date_str:
        return True  # Empty is valid
    
    from datetime import datetime
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers.
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if denominator is zero
        
    Returns:
        Result of division or default
    """
    if denominator == 0:
        return default
    return numerator / denominator
