"""
Data analysis utilities for student performance data.
"""

import pandas as pd
from typing import Dict, List


class StudentAnalyzer:
    """Analyze student performance data and generate insights."""

    def __init__(self, data: pd.DataFrame):
        """
        Initialize analyzer with student data.

        Args:
            data: DataFrame containing student performance data
        """
        self.data = data

    def get_summary_statistics(self) -> Dict:
        """
        Calculate summary statistics for the dataset.

        Returns:
            Dictionary with summary statistics
        """
        stats = {
            'total_students': len(self.data),
            'at_risk_count': self.data['at_risk'].sum(),
            'at_risk_percentage': round(
                self.data['at_risk'].mean() * 100, 2
            ),
            'avg_final_grade': round(self.data['final_grade'].mean(), 2),
            'avg_attendance': round(self.data['attendance_rate'].mean(), 2),
            'avg_assignment_score': round(
                self.data['avg_assignment_score'].mean(), 2
            ),
            'avg_quiz_score': round(self.data['avg_quiz_score'].mean(), 2),
            'total_forum_posts': self.data['forum_posts'].sum(),
            'avg_time_on_platform': round(
                self.data['time_on_platform'].mean(), 2
            )
        }
        return stats

    def identify_at_risk_students(self, threshold: float = 60) -> pd.DataFrame:
        """
        Identify students at risk of failing.

        Args:
            threshold: Grade threshold for at-risk classification

        Returns:
            DataFrame with at-risk students
        """
        at_risk = self.data[
            (self.data['final_grade'] < threshold) |
            (self.data['attendance_rate'] < 0.7)
        ].copy()

        at_risk['risk_factors'] = at_risk.apply(
            self._identify_risk_factors, axis=1
        )

        return at_risk.sort_values('final_grade')

    def _identify_risk_factors(self, row: pd.Series) -> List[str]:
        """
        Identify specific risk factors for a student.

        Args:
            row: Student data row

        Returns:
            List of risk factors
        """
        factors = []

        if row['final_grade'] < 60:
            factors.append('Low final grade')
        if row['attendance_rate'] < 0.7:
            factors.append('Poor attendance')
        if row['avg_assignment_score'] < 60:
            factors.append('Low assignment scores')
        if row['avg_quiz_score'] < 60:
            factors.append('Low quiz scores')
        if row['n_late_submissions'] > 5:
            factors.append('Frequent late submissions')
        if row['forum_posts'] < 3:
            factors.append('Low engagement')
        if row['time_on_platform'] < 3:
            factors.append('Insufficient study time')

        return factors

    def get_top_performers(self, n: int = 10) -> pd.DataFrame:
        """
        Get top performing students.

        Args:
            n: Number of top students to return

        Returns:
            DataFrame with top performers
        """
        return self.data.nlargest(n, 'final_grade')[[
            'student_id', 'name', 'final_grade',
            'attendance_rate', 'avg_assignment_score'
        ]]

    def calculate_correlations(self) -> pd.DataFrame:
        """
        Calculate correlations between features and final grade.

        Returns:
            DataFrame with correlation values
        """
        numeric_cols = [
            'attendance_rate', 'avg_assignment_score', 'avg_quiz_score',
            'forum_posts', 'time_on_platform', 'n_late_submissions'
        ]

        correlations = []
        for col in numeric_cols:
            corr = self.data[col].corr(self.data['final_grade'])
            correlations.append({
                'feature': col,
                'correlation': round(corr, 3)
            })

        return pd.DataFrame(correlations).sort_values(
            'correlation', ascending=False, key=abs
        )

    def analyze_performance_distribution(self) -> Dict:
        """
        Analyze distribution of student performance.

        Returns:
            Dictionary with distribution statistics
        """
        grades = self.data['final_grade']

        distribution = {
            'excellent': len(grades[grades >= 90]),
            'good': len(grades[(grades >= 75) & (grades < 90)]),
            'satisfactory': len(grades[(grades >= 60) & (grades < 75)]),
            'poor': len(grades[grades < 60]),
            'mean': round(grades.mean(), 2),
            'median': round(grades.median(), 2),
            'std': round(grades.std(), 2),
            'min': round(grades.min(), 2),
            'max': round(grades.max(), 2)
        }

        return distribution

    def get_engagement_metrics(self) -> Dict:
        """
        Calculate student engagement metrics.

        Returns:
            Dictionary with engagement metrics
        """
        return {
            'avg_forum_posts': round(self.data['forum_posts'].mean(), 2),
            'median_forum_posts': self.data['forum_posts'].median(),
            'highly_engaged': len(
                self.data[self.data['forum_posts'] > 10]
            ),
            'low_engagement': len(
                self.data[self.data['forum_posts'] < 3]
            ),
            'avg_platform_time': round(
                self.data['time_on_platform'].mean(), 2
            )
        }
