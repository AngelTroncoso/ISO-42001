"""Configuration loader for the ISO 42001 application.

This module handles loading configuration from Streamlit secrets or environment variables.
"""
import os
from typing import Optional

import streamlit as st
from dotenv import load_dotenv


def _read_setting(key: str, default: str = "") -> str:
    """Read a setting from Streamlit secrets, falling back to environment variables.

    Accessing st.secrets raises StreamlitSecretNotFoundError when no
    secrets.toml exists (the normal case on a local machine), so the
    lookup is guarded and falls back to the .env file.

    Args:
        key: Name of the setting.
        default: Value used when the setting is not defined anywhere.

    Returns:
        The configured value as a string.
    """
    try:
        if key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return os.getenv(key, default)


def load_config() -> dict[str, object]:
    """Load configuration from Streamlit secrets or environment variables.

    Priority order:
    1. Streamlit secrets (st.secrets)
    2. Environment variables (.env file)
    3. Default values

    Returns:
        Dictionary with configuration values.
    """
    load_dotenv()

    return {
        "MISTRAL_API_KEY": _read_setting("MISTRAL_API_KEY"),
        "MISTRAL_LLM_MODEL": _read_setting("MISTRAL_LLM_MODEL", "mistral-small-latest"),
        "MISTRAL_EMBED_MODEL": _read_setting("MISTRAL_EMBED_MODEL", "mistral-embed"),
        "DATA_DIR": _read_setting("DATA_DIR", "./data"),
        "CHUNK_SIZE": int(_read_setting("CHUNK_SIZE", "800")),
        "CHUNK_OVERLAP": int(_read_setting("CHUNK_OVERLAP", "120")),
    }


def validate_config(config: dict[str, object]) -> tuple[bool, Optional[str]]:
    """Validate that required configuration is present.

    Args:
        config: Configuration dictionary.

    Returns:
        Tuple of (is_valid, error_message).
    """
    if not config.get("MISTRAL_API_KEY"):
        return False, "Falta la clave API de Mistral. Por favor configura MISTRAL_API_KEY."

    return True, None
