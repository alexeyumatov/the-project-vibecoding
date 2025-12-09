"""
Tests for student analyzer utilities.
"""

import pytest
import pandas as pd
from src.analyzer import StudentAnalyzer
from src.data_generator import StudentDataGenerator


@pytest.fixture
def sample_data():
    """Generate sample data for testing."""
    generator = StudentDataGenerator(seed=42)
    return generator.generate_student_data(n_students=50)


class TestStudentAnalyzer:
    """Test cases for StudentAnalyzer class."""

    def test_initialization(self, sample_data):
        """Test analyzer initialization."""
        analyzer = StudentAnalyzer(sample_data)
        assert analyzer.data is not None
        assert len(analyzer.data) == 50

    def test_get_summary_statistics(self, sample_data):
        """Test summary statistics calculation."""
        analyzer = StudentAnalyzer(sample_data)
        stats = analyzer.get_summary_statistics()

        # Check that all expected keys are present
        expected_keys = [
            'total_students', 'at_risk_count', 'at_risk_percentage',
            'avg_final_grade', 'avg_attendance', 'avg_assignment_score',
            'avg_quiz_score', 'total_forum_posts', 'avg_time_on_platform'
        ]

        for key in expected_keys:
            assert key in stats

        # Check that values are reasonable
        assert stats['total_students'] == 50
        assert 0 <= stats['at_risk_percentage'] <= 100
        assert 0 <= stats['avg_final_grade'] <= 100

    def test_identify_at_risk_students(self, sample_data):
        """Test at-risk student identification."""
        analyzer = StudentAnalyzer(sample_data)
        at_risk = analyzer.identify_at_risk_students(threshold=60)

        # Check that returned data is DataFrame
        assert isinstance(at_risk, pd.DataFrame)

        # All students should have final_grade < 60 or attendance < 0.7
        for _, student in at_risk.iterrows():
            assert (student['final_grade'] < 60 or
                    student['attendance_rate'] < 0.7)

        # Check that risk_factors column exists
        assert 'risk_factors' in at_risk.columns

    def test_get_top_performers(self, sample_data):
        """Test top performers retrieval."""
        analyzer = StudentAnalyzer(sample_data)
        top_10 = analyzer.get_top_performers(n=10)

        assert len(top_10) == 10
        assert 'student_id' in top_10.columns
        assert 'final_grade' in top_10.columns

        # Check that grades are sorted in descending order
        grades = top_10['final_grade'].tolist()
        assert grades == sorted(grades, reverse=True)

    def test_calculate_correlations(self, sample_data):
        """Test correlation calculation."""
        analyzer = StudentAnalyzer(sample_data)
        corr = analyzer.calculate_correlations()

        assert isinstance(corr, pd.DataFrame)
        assert 'feature' in corr.columns
        assert 'correlation' in corr.columns

        # Check that correlations are between -1 and 1
        assert (corr['correlation'] >= -1).all()
        assert (corr['correlation'] <= 1).all()

    def test_analyze_performance_distribution(self, sample_data):
        """Test performance distribution analysis."""
        analyzer = StudentAnalyzer(sample_data)
        dist = analyzer.analyze_performance_distribution()

        expected_keys = [
            'excellent', 'good', 'satisfactory', 'poor',
            'mean', 'median', 'std', 'min', 'max'
        ]

        for key in expected_keys:
            assert key in dist

        # Check that category counts sum to total students
        total = (dist['excellent'] + dist['good'] +
                 dist['satisfactory'] + dist['poor'])
        assert total == 50

    def test_get_engagement_metrics(self, sample_data):
        """Test engagement metrics calculation."""
        analyzer = StudentAnalyzer(sample_data)
        metrics = analyzer.get_engagement_metrics()

        expected_keys = [
            'avg_forum_posts', 'median_forum_posts',
            'highly_engaged', 'low_engagement', 'avg_platform_time'
        ]

        for key in expected_keys:
            assert key in metrics

        assert metrics['avg_forum_posts'] >= 0
        assert metrics['avg_platform_time'] >= 0
