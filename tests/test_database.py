"""Tests for database module."""
import pytest
import tempfile
import os
from pathlib import Path
from storage.database import ComplianceDatabase


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    # Create temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_path = temp_file.name
    temp_file.close()
    
    # Create database
    db = ComplianceDatabase(db_path=temp_path)
    
    yield db
    
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


class TestDatabaseInitialization:
    """Tests for database initialization."""
    
    def test_database_creation(self, temp_db):
        """Test that database is created successfully."""
        assert temp_db is not None
        assert temp_db.get_count() == 0


class TestInsertRequirement:
    """Tests for inserting requirements."""
    
    def test_insert_single_requirement(self, temp_db):
        """Test inserting a single requirement."""
        requirement = {
            'clause': '4.1',
            'requirement': 'Test requirement',
            'description': 'Test description',
            'category': 'Test',
            'estado': 'No iniciado'
        }
        
        req_id = temp_db.insert_requirement(requirement)
        assert req_id > 0
        assert temp_db.get_count() == 1
    
    def test_insert_with_all_fields(self, temp_db):
        """Test inserting requirement with all fields."""
        requirement = {
            'clause': '6.1.2',
            'requirement': 'Risk assessment',
            'description': 'Perform risk assessment',
            'category': 'Planning',
            'estado': 'En progreso',
            'responsable': 'John Doe',
            'fecha_objetivo': '2024-12-31',
            'evidencia': 'Risk register',
            'notas': 'Important notes'
        }
        
        req_id = temp_db.insert_requirement(requirement)
        assert req_id > 0
        
        # Retrieve and verify
        retrieved = temp_db.get_requirement_by_id(req_id)
        assert retrieved['clause'] == '6.1.2'
        assert retrieved['responsable'] == 'John Doe'


class TestUpdateRequirement:
    """Tests for updating requirements."""
    
    def test_update_single_field(self, temp_db):
        """Test updating a single field."""
        # Insert first
        requirement = {
            'clause': '4.1',
            'requirement': 'Test',
            'estado': 'No iniciado'
        }
        req_id = temp_db.insert_requirement(requirement)
        
        # Update
        updates = {'estado': 'En progreso'}
        result = temp_db.update_requirement(req_id, updates)
        assert result is True
        
        # Verify
        retrieved = temp_db.get_requirement_by_id(req_id)
        assert retrieved['estado'] == 'En progreso'
    
    def test_update_multiple_fields(self, temp_db):
        """Test updating multiple fields."""
        # Insert first
        requirement = {
            'clause': '5.1',
            'requirement': 'Leadership',
            'estado': 'No iniciado'
        }
        req_id = temp_db.insert_requirement(requirement)
        
        # Update
        updates = {
            'estado': 'Cumplido',
            'responsable': 'Jane Smith',
            'evidencia': 'Completed document'
        }
        temp_db.update_requirement(req_id, updates)
        
        # Verify
        retrieved = temp_db.get_requirement_by_id(req_id)
        assert retrieved['estado'] == 'Cumplido'
        assert retrieved['responsable'] == 'Jane Smith'
        assert retrieved['evidencia'] == 'Completed document'


class TestDeleteRequirement:
    """Tests for deleting requirements."""
    
    def test_delete_existing(self, temp_db):
        """Test deleting an existing requirement."""
        # Insert first
        requirement = {
            'clause': '7.1',
            'requirement': 'Resources'
        }
        req_id = temp_db.insert_requirement(requirement)
        assert temp_db.get_count() == 1
        
        # Delete
        result = temp_db.delete_requirement(req_id)
        assert result is True
        assert temp_db.get_count() == 0
    
    def test_delete_nonexistent(self, temp_db):
        """Test deleting a non-existent requirement."""
        result = temp_db.delete_requirement(99999)
        assert result is False


class TestBulkOperations:
    """Tests for bulk operations."""
    
    def test_bulk_insert(self, temp_db):
        """Test bulk inserting requirements."""
        requirements = [
            {'clause': '4.1', 'requirement': 'Req 1', 'category': 'Context'},
            {'clause': '4.2', 'requirement': 'Req 2', 'category': 'Context'},
            {'clause': '5.1', 'requirement': 'Req 3', 'category': 'Leadership'},
        ]
        
        inserted = temp_db.bulk_insert_requirements(requirements)
        assert inserted == 3
        assert temp_db.get_count() == 3
    
    def test_bulk_insert_skip_duplicates(self, temp_db):
        """Test that bulk insert skips existing clauses."""
        # Insert first batch
        requirements1 = [
            {'clause': '4.1', 'requirement': 'Req 1'},
            {'clause': '4.2', 'requirement': 'Req 2'},
        ]
        temp_db.bulk_insert_requirements(requirements1)
        
        # Try to insert overlapping batch
        requirements2 = [
            {'clause': '4.2', 'requirement': 'Req 2 duplicate'},  # Duplicate
            {'clause': '5.1', 'requirement': 'Req 3'},  # New
        ]
        inserted = temp_db.bulk_insert_requirements(requirements2)
        
        # Only one should be inserted
        assert inserted == 1
        assert temp_db.get_count() == 3


class TestGetAllRequirements:
    """Tests for retrieving all requirements."""
    
    def test_get_all_empty(self, temp_db):
        """Test getting all requirements when database is empty."""
        df = temp_db.get_all_requirements()
        assert len(df) == 0
    
    def test_get_all_with_data(self, temp_db):
        """Test getting all requirements with data."""
        requirements = [
            {'clause': '4.1', 'requirement': 'Req 1'},
            {'clause': '6.1', 'requirement': 'Req 2'},
        ]
        temp_db.bulk_insert_requirements(requirements)
        
        df = temp_db.get_all_requirements()
        assert len(df) == 2
        assert '4.1' in df['clause'].values
        assert '6.1' in df['clause'].values


class TestRequirementExists:
    """Tests for checking requirement existence."""
    
    def test_exists_true(self, temp_db):
        """Test that existing requirement is found."""
        requirement = {'clause': '4.1', 'requirement': 'Test'}
        temp_db.insert_requirement(requirement)
        
        assert temp_db.requirement_exists('4.1') is True
    
    def test_exists_false(self, temp_db):
        """Test that non-existing requirement is not found."""
        assert temp_db.requirement_exists('99.99') is False
