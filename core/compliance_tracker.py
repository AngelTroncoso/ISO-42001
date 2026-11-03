"""Compliance tracking and progress calculation."""
import logging
from datetime import datetime, date, timedelta
from typing import Optional

import pandas as pd


logger = logging.getLogger(__name__)


class ComplianceTracker:
    """Manager for compliance tracking operations."""

    VALID_STATUSES = ['No iniciado', 'En progreso', 'Cumplido', 'No aplica']

    @staticmethod
    def calculate_progress(df: pd.DataFrame) -> dict[str, any]:
        """Calculate compliance progress statistics.

        Args:
            df: DataFrame with compliance data

        Returns:
            Dictionary with progress metrics
        """
        if df.empty:
            return {
                'total': 0,
                'completed': 0,
                'in_progress': 0,
                'not_started': 0,
                'not_applicable': 0,
                'completion_rate': 0.0,
                'effective_completion_rate': 0.0
            }

        total = len(df)
        completed = len(df[df['estado'] == 'Cumplido'])
        in_progress = len(df[df['estado'] == 'En progreso'])
        not_started = len(df[df['estado'] == 'No iniciado'])
        not_applicable = len(df[df['estado'] == 'No aplica'])

        # Overall completion rate
        completion_rate = (completed / total * 100) if total > 0 else 0.0

        # Effective completion rate (excluding not applicable)
        applicable = total - not_applicable
        effective_completion_rate = (
            (completed / applicable * 100) if applicable > 0 else 0.0
        )

        return {
            'total': total,
            'completed': completed,
            'in_progress': in_progress,
            'not_started': not_started,
            'not_applicable': not_applicable,
            'completion_rate': round(completion_rate, 1),
            'effective_completion_rate': round(effective_completion_rate, 1)
        }

    @staticmethod
    def get_overdue_requirements(
        df: pd.DataFrame, today: Optional[date] = None
    ) -> pd.DataFrame:
        """Get requirements past their target date.

        Args:
            df: DataFrame with compliance data
            today: Reference date. Defaults to the current date.

        Returns:
            DataFrame with overdue requirements
        """
        if df.empty or 'fecha_objetivo' not in df.columns:
            return pd.DataFrame()

        reference = pd.Timestamp(today or date.today())
        targets = pd.to_datetime(df['fecha_objetivo'], errors='coerce').dt.normalize()

        mask = (
            targets.notna()
            & (targets < reference)
            & (df['estado'] != 'Cumplido')
            & (df['estado'] != 'No aplica')
        )
        return df[mask].copy()

    @staticmethod
    def get_upcoming_requirements(
        df: pd.DataFrame, days: int = 30, today: Optional[date] = None
    ) -> pd.DataFrame:
        """Get requirements due in the next N days.

        Args:
            df: DataFrame with compliance data
            days: Number of days to look ahead
            today: Reference date. Defaults to the current date.

        Returns:
            DataFrame with upcoming requirements
        """
        if df.empty or 'fecha_objetivo' not in df.columns:
            return pd.DataFrame()

        reference = timestamp(today or date.today())
        limit = reference + timedelta(days=days)
        targets = pd.to_datetime(df['fecha_objetivo'], errors='coerce').dt.normalize()

        mask = (
            targets.notna()
            & (targets >= reference)
            & (targets <= limit)
            & (df['estado'] != 'Cumplido')
            & (df['estado'] != 'No aplica')
        )
        return df[mask].copy()

    @staticmethod
    def get_by_category(df: pd.DataFrame) -> dict[str, dict]:
        """Get progress statistics by category.

        Args:
            df: DataFrame with compliance data

        Returns:
            Dictionary with stats per category
        """
        if df.empty or 'category' not in df.columns:
            return {}

        categories = {}
        for category in df['category'].unique():
            category_df = df[df['category'] == category]
            categories[category] = ComplianceTracker.calculate_progress(category_df)

        return categories

    @staticmethod
    def validate_status(status: str) -> bool:
        """Validate that a status value is valid.

        Args:
            status: Status to validate

        Returns:
            True if valid
        """
        return status in ComplianceTracker.VALID_STATUSES

    @staticmethod
    def export_to_excel(df: pd.DataFrame, file_path: str) -> bool:
        """Export compliance data to Excel.

        Args:
            df: DataFrame to export
            file_path: Path for output file

        Returns:
            True if successful
        """
        try:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Cumplimiento')

                # Add progress sheet
                progress = ComplianceTracker.calculate_progress(df)
                progress_df = pd.DataFrame([progress])
                progress_df.to_excel(writer, index=False, sheet_name='Resumen')

            logger.info("Exported to %s", file_path)
            return True

        except Exception as error:
            logger.error("Error exporting to Excel: %s", error)
            return False

    @staticmethod
    def export_to_csv(df: pd.DataFrame, file_path: str) -> bool:
        """Export compliance data to CSV.

        Args:
            df: DataFrame to export
            file_path: Path for output file

        Returns:
            True if successful
        """
        try:
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
            logger.info("Exported to %s", file_path)
            return True

        except Exception as error:
            logger.error("Error exporting to CSV: %s", error)
            return False

    @staticmethod
    def format_date(date_value: any) -> Optional[str]:
        """Format date for display.

        Args:
            date_value: Date value to format

        Returns:
            Formatted date string or None
        """
        if pd.isna(date_value):
            return None

        if isinstance(date_value, str):
            try:
                date_obj = datetime.strptime(date_value, '%Y-%m-%d').date()
                return date_obj.strftime('%d/%m/%Y')
            except ValueError:
                return date_value

        if isinstance(date_value, (date, datetime)):
            return date_value.strftime('%d/%m/%Y')

        return str(date_value)