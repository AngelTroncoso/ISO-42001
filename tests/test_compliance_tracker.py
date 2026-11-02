"""Tests for compliance tracker module."""
import pytest
import pandas as pd
from datetime import date, timedelta
from core.compliance_tracker import ComplianceTracker


class TestCalculateProgress:
    """Tests for calculate_progress function."""
    
    def test_empty_dataframe(self):
        """Test with empty dataframe."""
        df = pd.DataFrame()
        result = ComplianceTracker.calculate_progress(df)
        
        assert result['total'] == 0
        assert result['completed'] == 0
        assert result['completion_rate'] == 0.0
    
    def test_all_statuses(self):
        """Test calculation with all status types."""
        df = pd.DataFrame({
            'estado': ['Cumplido', 'Cumplido', 'En progreso', 'No iniciado', 'No aplica']
        })
        result = ComplianceTracker.calculate_progress(df)
        
        assert result['total'] == 5
        assert result['completed'] == 2
        assert result['in_progress'] == 1
        assert result['not_started'] == 1
        assert result['not_applicable'] == 1
        assert result['completion_rate'] == 40.0  # 2/5
        assert result['effective_completion_rate'] == 50.0  # 2/4 (excluding N/A)
    
    def test_all_completed(self):
        """Test when all requirements are completed."""
        df = pd.DataFrame({
            'estado': ['Cumplido', 'Cumplido', 'Cumplido']
        })
        result = ComplianceTracker.calculate_progress(df)
        
        assert result['completion_rate'] == 100.0
        assert result['effective_completion_rate'] == 100.0
    
    def test_with_not_applicable(self):
        """Test effective rate calculation with not applicable items."""
        df = pd.DataFrame({
            'estado': ['Cumplido', 'No aplica', 'No aplica']
        })
        result = ComplianceTracker.calculate_progress(df)
        
        assert result['completion_rate'] == pytest.approx(33.3, rel=0.1)
        assert result['effective_completion_rate'] == 100.0  # 1/1 applicable


class TestGetOverdueRequirements:
    """Tests for get_overdue_requirements function."""
    
    def test_no_overdue(self):
        """Test when no requirements are overdue."""
        future_date = (date.today() + timedelta(days=30)).isoformat()
        df = pd.DataFrame({
            'clause': ['4.1', '6.1'],
            'estado': ['En progreso', 'No iniciado'],
            'fecha_objetivo': [future_date, future_date]
        })
        result = ComplianceTracker.get_overdue_requirements(df)
        
        assert len(result) == 0
    
    def test_overdue_requirements(self):
        """Test detection of overdue requirements."""
        past_date = (date.today() - timedelta(days=10)).isoformat()
        future_date = (date.today() + timedelta(days=10)).isoformat()
        
        df = pd.DataFrame({
            'clause': ['4.1', '6.1', '8.1'],
            'estado': ['En progreso', 'No iniciado', 'Cumplido'],
            'fecha_objetivo': [past_date, past_date, past_date]
        })
        result = ComplianceTracker.get_overdue_requirements(df)
        
        # Should only return the first two (not completed)
        assert len(result) == 2
        assert '4.1' in result['clause'].values
        assert '6.1' in result['clause'].values
        assert '8.1' not in result['clause'].values
    
    def test_completed_not_overdue(self):
        """Test that completed requirements are not marked overdue."""
        past_date = (date.today() - timedelta(days=10)).isoformat()
        
        df = pd.DataFrame({
            'clause': ['4.1'],
            'estado': ['Cumplido'],
            'fecha_objetivo': [past_date]
        })
        result = ComplianceTracker.get_overdue_requirements(df)
        
        assert len(result) == 0


class TestGetUpcomingRequirements:
    """Tests for get_upcoming_requirements function."""
    
    def test_upcoming_in_range(self):
        """Test detection of upcoming requirements."""
        date_in_15_days = (date.today() + timedelta(days=15)).isoformat()
        date_in_50_days = (date.today() + timedelta(days=50)).isoformat()
        
        df = pd.DataFrame({
            'clause': ['4.1', '6.1'],
            'estado': ['En progreso', 'No iniciado'],
            'fecha_objetivo': [date_in_15_days, date_in_50_days]
        })
        result = ComplianceTracker.get_upcoming_requirements(df, days=30)
        
        # Only first one should be in range
        assert len(result) == 1
        assert result['clause'].values[0] == '4.1'
    
    def test_no_upcoming(self):
        """Test when no requirements are upcoming."""
        far_future = (date.today() + timedelta(days=100)).isoformat()
        
        df = pd.DataFrame({
            'clause': ['4.1'],
            'estado': ['No iniciado'],
            'fecha_objetivo': [far_future]
        })
        result = ComplianceTracker.get_upcoming_requirements(df, days=30)
        
        assert len(result) == 0


class TestValidateStatus:
    """Tests for validate_status function."""
    
    def test_valid_statuses(self):
        """Test validation of valid statuses."""
        valid_statuses = ['No iniciado', 'En progreso', 'Cumplido', 'No aplica']
        for status in valid_statuses:
            assert ComplianceTracker.validate_status(status) is True
    
    def test_invalid_statuses(self):
        """Test validation of invalid statuses."""
        invalid_statuses = ['Invalid', 'Complete', 'Started', '']
        for status in invalid_statuses:
            assert ComplianceTracker.validate_status(status) is False


class TestGetByCategory:
    """Tests for get_by_category function."""
    
    def test_category_breakdown(self):
        """Test progress calculation by category."""
        df = pd.DataFrame({
            'category': ['Contexto', 'Contexto', 'Liderazgo', 'Liderazgo'],
            'estado': ['Cumplido', 'En progreso', 'Cumplido', 'Cumplido']
        })
        result = ComplianceTracker.get_by_category(df)
        
        assert 'Contexto' in result
        assert 'Liderazgo' in result
        assert result['Contexto']['total'] == 2
        assert result['Contexto']['completed'] == 1
        assert result['Liderazgo']['total'] == 2
        assert result['Liderazgo']['completed'] == 2
