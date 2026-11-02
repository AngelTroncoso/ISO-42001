"""SQLite database management for compliance tracking."""
import sqlite3
import logging
from pathlib import Path
from typing import Optional, List, Dict
import pandas as pd
from datetime import datetime


logger = logging.getLogger(__name__)


class ComplianceDatabase:
    """SQLite database manager for compliance tracking."""
    
    def __init__(self, db_path: str = "storage/compliance.db"):
        """Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._ensure_db_directory()
        self._init_schema()
    
    def _ensure_db_directory(self) -> None:
        """Ensure database directory exists."""
        db_file = Path(self.db_path)
        db_file.parent.mkdir(parents=True, exist_ok=True)
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection.
        
        Returns:
            SQLite connection object
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_schema(self) -> None:
        """Initialize database schema."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Create requirements table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS requirements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                clause TEXT NOT NULL,
                requirement TEXT NOT NULL,
                description TEXT,
                category TEXT,
                estado TEXT DEFAULT 'No iniciado',
                responsable TEXT,
                fecha_objetivo DATE,
                evidencia TEXT,
                notas TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create index on clause for faster lookups
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_clause ON requirements(clause)
        """)
        
        # Create index on status
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_estado ON requirements(estado)
        """)
        
        conn.commit()
        conn.close()
        
        logger.info("Database schema initialized")
    
    def insert_requirement(self, requirement: Dict[str, any]) -> int:
        """Insert a new requirement.
        
        Args:
            requirement: Dictionary with requirement data
            
        Returns:
            ID of inserted requirement
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO requirements 
            (clause, requirement, description, category, estado, responsable, 
             fecha_objetivo, evidencia, notas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            requirement.get('clause'),
            requirement.get('requirement'),
            requirement.get('description'),
            requirement.get('category'),
            requirement.get('estado', 'No iniciado'),
            requirement.get('responsable'),
            requirement.get('fecha_objetivo'),
            requirement.get('evidencia'),
            requirement.get('notas')
        ))
        
        req_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Inserted requirement {requirement.get('clause')}")
        return req_id
    
    def update_requirement(self, req_id: int, updates: Dict[str, any]) -> bool:
        """Update an existing requirement.
        
        Args:
            req_id: Requirement ID
            updates: Dictionary with fields to update
            
        Returns:
            True if successful
        """
        if not updates:
            return False
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Build update query dynamically
        set_clause = ', '.join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values())
        values.append(req_id)
        
        cursor.execute(f"""
            UPDATE requirements 
            SET {set_clause}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, values)
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        logger.info(f"Updated requirement ID {req_id}")
        return rows_affected > 0
    
    def delete_requirement(self, req_id: int) -> bool:
        """Delete a requirement.
        
        Args:
            req_id: Requirement ID
            
        Returns:
            True if successful
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM requirements WHERE id = ?", (req_id,))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        logger.info(f"Deleted requirement ID {req_id}")
        return rows_affected > 0
    
    def get_all_requirements(self) -> pd.DataFrame:
        """Get all requirements as DataFrame.
        
        Returns:
            DataFrame with all requirements
        """
        conn = self._get_connection()
        
        df = pd.read_sql_query("""
            SELECT id, clause, requirement, description, category, estado, 
                   responsable, fecha_objetivo, evidencia, notas,
                   created_at, updated_at
            FROM requirements
            ORDER BY clause
        """, conn)
        
        conn.close()
        
        return df
    
    def get_requirement_by_id(self, req_id: int) -> Optional[Dict[str, any]]:
        """Get a single requirement by ID.
        
        Args:
            req_id: Requirement ID
            
        Returns:
            Dictionary with requirement data or None
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, clause, requirement, description, category, estado,
                   responsable, fecha_objetivo, evidencia, notas,
                   created_at, updated_at
            FROM requirements
            WHERE id = ?
        """, (req_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def requirement_exists(self, clause: str) -> bool:
        """Check if a requirement with given clause exists.
        
        Args:
            clause: Clause number to check
            
        Returns:
            True if exists
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM requirements WHERE clause = ?
        """, (clause,))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0
    
    def bulk_insert_requirements(self, requirements: List[Dict[str, any]]) -> int:
        """Insert multiple requirements at once.
        
        Args:
            requirements: List of requirement dictionaries
            
        Returns:
            Number of inserted requirements
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        inserted = 0
        for req in requirements:
            # Check if already exists
            if self.requirement_exists(req.get('clause')):
                logger.info(f"Requirement {req.get('clause')} already exists, skipping")
                continue
            
            cursor.execute("""
                INSERT INTO requirements 
                (clause, requirement, description, category, estado, responsable,
                 fecha_objetivo, evidencia, notas)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                req.get('clause'),
                req.get('requirement'),
                req.get('description'),
                req.get('category'),
                req.get('estado', 'No iniciado'),
                req.get('responsable'),
                req.get('fecha_objetivo'),
                req.get('evidencia'),
                req.get('notas')
            ))
            inserted += 1
        
        conn.commit()
        conn.close()
        
        logger.info(f"Bulk inserted {inserted} requirements")
        return inserted
    
    def clear_all_requirements(self) -> bool:
        """Delete all requirements. Use with caution!
        
        Returns:
            True if successful
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM requirements")
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        logger.warning(f"Cleared {rows_affected} requirements from database")
        return True
    
    def get_count(self) -> int:
        """Get total number of requirements.
        
        Returns:
            Count of requirements
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM requirements")
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
