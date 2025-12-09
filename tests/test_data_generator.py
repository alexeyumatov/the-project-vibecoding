"""
Tests for data generation utilities.
"""

import pandas as pd
from src.data_generator import StudentDataGenerator


class TestStudentDataGenerator:
    """Test cases for StudentDataGenerator class."""

    def test_initialization(self):
        """Test generator initialization."""
        generator = StudentDataGenerator(seed=42)
        assert generator.seed == 42
        assert generator.fake is not None

    def test_generate_student_data_count(self):
        """Test that correct number of students is generated."""
        generator = StudentDataGenerator()
        n_students = 50
        data = generator.generate_student_data(n_students=n_students)

        assert len(data) == n_students
        assert isinstance(data, pd.DataFrame)

    def test_generate_student_data_columns(self):
        """Test that all required columns are present."""
        generator = StudentDataGenerator()
        data = generator.generate_student_data(n_students=10)

        required_columns = [
            'student_id', 'name', 'age', 'attendance_rate',
            'avg_assignment_score', 'avg_quiz_score', 'forum_posts',
            'time_on_platform', 'n_late_submissions', 'final_grade', 'at_risk'
        ]

        for col in required_columns:
            assert col in data.columns

    def test_student_id_format(self):
        """Test student ID format."""
        generator = StudentDataGenerator()
        data = generator.generate_student_data(n_students=5)

        for student_id in data['student_id']:
            assert student_id.startswith('STU')
            assert len(student_id) == 7  # STU + 4 digits

    def test_data_ranges(self):
        """Test that generated values are within expected ranges."""
        generator = StudentDataGenerator()
        data = generator.generate_student_data(n_students=100)

        # Attendance rate should be between 0 and 1
        assert data['attendance_rate'].min() >= 0
        assert data['attendance_rate'].max() <= 1

        # Scores should be between 0 and 100
        assert data['avg_assignment_score'].min() >= 0
        assert data['avg_assignment_score'].max() <= 100
        assert data['avg_quiz_score'].min() >= 0
        assert data['avg_quiz_score'].max() <= 100
        assert data['final_grade'].min() >= 0
        assert data['final_grade'].max() <= 100

        # Age should be reasonable
        assert data['age'].min() >= 18
        assert data['age'].max() <= 30

    def test_at_risk_logic(self):
        """Test at-risk classification logic."""
        generator = StudentDataGenerator()
        data = generator.generate_student_data(n_students=100)

        # Students with low grades should be at-risk
        low_grade_students = data[data['final_grade'] < 60]
        assert (low_grade_students['at_risk'] == 1).all()

        # Students with low attendance should be at-risk
        low_attendance = data[data['attendance_rate'] < 0.7]
        assert (low_attendance['at_risk'] == 1).all()

    def test_generate_time_series_data(self):
        """Test time series data generation."""
        generator = StudentDataGenerator()
        weeks = 12
        data = generator.generate_time_series_data('STU0001', weeks=weeks)

        assert len(data) == weeks
        assert 'student_id' in data.columns
        assert 'week' in data.columns
        assert 'weekly_score' in data.columns
        assert data['week'].min() == 1
        assert data['week'].max() == weeks

    def test_reproducibility(self):
        """Test that same seed produces consistent structure."""
        gen1 = StudentDataGenerator(seed=42)
        gen2 = StudentDataGenerator(seed=42)

        data1 = gen1.generate_student_data(n_students=10)
        data2 = gen2.generate_student_data(n_students=10)

        # Check that data has same structure and ranges
        assert len(data1) == len(data2)
        assert list(data1.columns) == list(data2.columns)

        # Both should have similar distributions
        assert abs(data1['final_grade'].mean() -
                   data2['final_grade'].mean()) < 20
