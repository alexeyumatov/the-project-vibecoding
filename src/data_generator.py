"""
Data generation utilities for creating synthetic student performance data.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker


class StudentDataGenerator:
    """Generate synthetic student performance data for testing and demo purposes."""

    def __init__(self, seed=42):
        """
        Initialize the data generator.

        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        np.random.seed(seed)
        self.fake = Faker()
        Faker.seed(seed)

    def generate_student_data(self, n_students=100):
        """
        Generate synthetic student data.

        Args:
            n_students: Number of students to generate

        Returns:
            pandas.DataFrame: DataFrame with student information
        """
        students = []
        for i in range(n_students):
            # Generate attendance rate (correlation with performance)
            base_attendance = np.random.uniform(0.5, 1.0)

            # Generate assignment scores
            n_assignments = 10
            assignment_scores = []
            for _ in range(n_assignments):
                # Students with better attendance tend to score higher
                score = np.random.normal(
                    loc=base_attendance * 85, scale=15
                )
                assignment_scores.append(max(0, min(100, score)))

            # Generate quiz scores
            n_quizzes = 5
            quiz_scores = []
            for _ in range(n_quizzes):
                score = np.random.normal(
                    loc=base_attendance * 80, scale=20
                )
                quiz_scores.append(max(0, min(100, score)))

            # Forum participation
            forum_posts = int(np.random.poisson(base_attendance * 10))

            # Time on platform (hours per week)
            time_on_platform = np.random.normal(
                loc=base_attendance * 8, scale=3
            )

            student = {
                'student_id': f'STU{i+1:04d}',
                'name': self.fake.name(),
                'age': np.random.randint(18, 30),
                'attendance_rate': round(base_attendance, 2),
                'avg_assignment_score': round(np.mean(assignment_scores), 2),
                'avg_quiz_score': round(np.mean(quiz_scores), 2),
                'forum_posts': forum_posts,
                'time_on_platform': round(max(0, time_on_platform), 2),
                'n_late_submissions': int(np.random.poisson((1 - base_attendance) * 3)),
                'final_grade': round(
                    0.4 * np.mean(assignment_scores) +
                    0.4 * np.mean(quiz_scores) +
                    0.2 * base_attendance * 100,
                    2
                )
            }

            # Determine if at-risk (final grade < 60 or attendance < 0.7)
            student['at_risk'] = int(
                student['final_grade'] < 60 or student['attendance_rate'] < 0.7
            )

            students.append(student)

        return pd.DataFrame(students)

    def generate_time_series_data(self, student_id, weeks=12):
        """
        Generate weekly performance data for a student.

        Args:
            student_id: Student identifier
            weeks: Number of weeks to generate

        Returns:
            pandas.DataFrame: Weekly performance metrics
        """
        start_date = datetime.now() - timedelta(weeks=weeks)
        data = []

        # Base performance with some trend
        base_performance = np.random.uniform(60, 90)
        trend = np.random.uniform(-1, 1)

        for week in range(weeks):
            week_date = start_date + timedelta(weeks=week)
            performance = base_performance + \
                trend * week + np.random.normal(0, 5)

            data.append({
                'student_id': student_id,
                'week': week + 1,
                'date': week_date.strftime('%Y-%m-%d'),
                'weekly_score': round(max(0, min(100, performance)), 2),
                'hours_studied': round(max(0, np.random.normal(8, 2)), 2),
                'assignments_completed': np.random.randint(0, 4)
            })

        return pd.DataFrame(data)
