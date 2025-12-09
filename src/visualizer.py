"""
Visualization utilities for student performance data.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt  # noqa: E402
import seaborn as sns  # noqa: E402
import pandas as pd  # noqa: E402
from typing import Optional  # noqa: E402


class Visualizer:
    """Create visualizations for student performance analysis."""

    def __init__(self, style='seaborn-v0_8-darkgrid'):
        """
        Initialize visualizer.

        Args:
            style: Matplotlib style to use
        """
        plt.style.use('default')
        sns.set_palette("husl")

    def plot_grade_distribution(
        self,
        data: pd.DataFrame,
        save_path: Optional[str] = None
    ):
        """
        Plot distribution of final grades.

        Args:
            data: Student data
            save_path: Path to save the plot
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.hist(
            data['final_grade'],
            bins=20,
            edgecolor='black',
            alpha=0.7
        )
        ax.axvline(
            data['final_grade'].mean(),
            color='red',
            linestyle='--',
            label=f"Mean: {data['final_grade'].mean():.2f}"
        )
        ax.set_xlabel('Final Grade', fontsize=12)
        ax.set_ylabel('Number of Students', fontsize=12)
        ax.set_title('Distribution of Final Grades',
                     fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()

    def plot_correlation_heatmap(
        self,
        data: pd.DataFrame,
        save_path: Optional[str] = None
    ):
        """
        Plot correlation heatmap of features.

        Args:
            data: Student data
            save_path: Path to save the plot
        """
        numeric_cols = [
            'attendance_rate', 'avg_assignment_score', 'avg_quiz_score',
            'forum_posts', 'time_on_platform', 'final_grade'
        ]

        corr_matrix = data[numeric_cols].corr()

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(
            corr_matrix,
            annot=True,
            fmt='.2f',
            cmap='coolwarm',
            center=0,
            square=True,
            ax=ax
        )
        ax.set_title('Feature Correlation Heatmap',
                     fontsize=14, fontweight='bold')

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()

    def plot_risk_comparison(
        self,
        data: pd.DataFrame,
        save_path: Optional[str] = None
    ):
        """
        Compare at-risk vs not-at-risk students.

        Args:
            data: Student data
            save_path: Path to save the plot
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(
            'At-Risk vs Not-At-Risk Student Comparison',
            fontsize=16,
            fontweight='bold'
        )

        metrics = [
            ('attendance_rate', 'Attendance Rate'),
            ('avg_assignment_score', 'Average Assignment Score'),
            ('forum_posts', 'Forum Posts'),
            ('time_on_platform', 'Time on Platform (hours/week)')
        ]

        for idx, (metric, title) in enumerate(metrics):
            ax = axes[idx // 2, idx % 2]

            data.boxplot(
                column=metric,
                by='at_risk',
                ax=ax
            )
            ax.set_title(title)
            ax.set_xlabel('At Risk (0=No, 1=Yes)')
            ax.set_ylabel(title)
            plt.sca(ax)
            plt.xticks([1, 2], ['Not At Risk', 'At Risk'])

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()

    def plot_feature_importance(
        self,
        importance_df: pd.DataFrame,
        save_path: Optional[str] = None
    ):
        """
        Plot feature importance from model.

        Args:
            importance_df: DataFrame with feature importance
            save_path: Path to save the plot
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.barh(
            importance_df['feature'],
            importance_df['importance'],
            color='skyblue',
            edgecolor='black'
        )
        ax.set_xlabel('Importance', fontsize=12)
        ax.set_ylabel('Feature', fontsize=12)
        ax.set_title(
            'Feature Importance for Risk Prediction',
            fontsize=14,
            fontweight='bold'
        )
        ax.grid(True, alpha=0.3, axis='x')

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()

    def plot_performance_categories(
        self,
        distribution: dict,
        save_path: Optional[str] = None
    ):
        """
        Plot pie chart of performance categories.

        Args:
            distribution: Dictionary with performance distribution
            save_path: Path to save the plot
        """
        categories = ['Excellent\n(≥90)', 'Good\n(75-89)',
                      'Satisfactory\n(60-74)', 'Poor\n(<60)']
        values = [
            distribution['excellent'],
            distribution['good'],
            distribution['satisfactory'],
            distribution['poor']
        ]

        fig, ax = plt.subplots(figsize=(10, 8))

        colors = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c']
        explode = (0.1, 0, 0, 0.1)

        ax.pie(
            values,
            labels=categories,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            explode=explode,
            shadow=True
        )
        ax.set_title(
            'Student Performance Distribution',
            fontsize=14,
            fontweight='bold'
        )

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
