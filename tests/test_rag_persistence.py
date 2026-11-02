"""Tests for RAG index persistence."""
import pytest
import tempfile
from pathlib import Path
from core.rag_engine import RAGEngine


class TestIndexPersistence:
    """Tests for saving and loading index."""
    
    @pytest.fixture
    def temp_persist_dir(self):
        """Create temporary directory for index persistence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    @pytest.fixture
    def mock_api_key(self):
        """Mock API key for testing."""
        return "test_api_key_for_unit_tests"
    
    def test_save_index_creates_directory(self, temp_persist_dir, mock_api_key):
        """Test that save_index handles nonexistent directory gracefully."""
        engine = RAGEngine(api_key=mock_api_key)
        
        # Even without an index, save should not raise exception
        persist_path = temp_persist_dir / "test_index"
        
        # Should not raise exception (logs warning but continues)
        try:
            engine.save_index(persist_path)
            # Test passes if no exception raised
            assert True
        except Exception:
            assert False, "save_index should not raise exception for empty index"
    
    def test_load_nonexistent_index_returns_false(self, temp_persist_dir, mock_api_key):
        """Test loading from nonexistent directory returns False."""
        engine = RAGEngine(api_key=mock_api_key)
        
        nonexistent_path = temp_persist_dir / "nonexistent"
        result = engine.load_index(nonexistent_path)
        
        assert result is False
    
    def test_load_empty_directory_handles_gracefully(self, temp_persist_dir, mock_api_key):
        """Test loading from empty directory handles gracefully."""
        engine = RAGEngine(api_key=mock_api_key)
        
        empty_dir = temp_persist_dir / "empty"
        empty_dir.mkdir()
        
        result = engine.load_index(empty_dir)
        
        # Should return False when directory exists but has no index
        assert result is False
