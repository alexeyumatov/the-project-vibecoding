"""
Machine learning predictor for identifying at-risk students.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)
import joblib
from typing import Dict


class RiskPredictor:
    """Predict student risk using machine learning."""

    def __init__(self):
        """Initialize the predictor."""
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.feature_columns = [
            'attendance_rate', 'avg_assignment_score', 'avg_quiz_score',
            'forum_posts', 'time_on_platform', 'n_late_submissions'
        ]
        self.is_trained = False

    def prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare features for training or prediction.

        Args:
            data: Raw student data

        Returns:
            Feature matrix
        """
        return data[self.feature_columns].copy()

    def train(
        self,
        data: pd.DataFrame,
        test_size: float = 0.2
    ) -> Dict:
        """
        Train the risk prediction model.

        Args:
            data: Student data with 'at_risk' labels
            test_size: Proportion of data for testing

        Returns:
            Dictionary with training metrics
        """
        X = self.prepare_features(data)
        y = data['at_risk']

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        self.model.fit(X_train, y_train)
        self.is_trained = True

        # Evaluate
        y_pred = self.model.predict(X_test)

        metrics = {
            'accuracy': round(accuracy_score(y_test, y_pred), 3),
            'precision': round(precision_score(y_test, y_pred), 3),
            'recall': round(recall_score(y_test, y_pred), 3),
            'f1_score': round(f1_score(y_test, y_pred), 3),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'classification_report': classification_report(
                y_test, y_pred, output_dict=True
            ),
            'train_size': len(X_train),
            'test_size': len(X_test)
        }

        return metrics

    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """
        Predict risk for students.

        Args:
            data: Student data

        Returns:
            Array of predictions (0 or 1)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")

        X = self.prepare_features(data)
        return self.model.predict(X)

    def predict_proba(self, data: pd.DataFrame) -> np.ndarray:
        """
        Predict risk probabilities for students.

        Args:
            data: Student data

        Returns:
            Array of probabilities
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")

        X = self.prepare_features(data)
        return self.model.predict_proba(X)

    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance from the trained model.

        Returns:
            DataFrame with feature importance scores
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first")

        importance_df = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)

        importance_df['importance'] = importance_df['importance'].round(3)

        return importance_df

    def save_model(self, filepath: str):
        """
        Save the trained model to disk.

        Args:
            filepath: Path to save the model
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")

        joblib.dump(self.model, filepath)

    def load_model(self, filepath: str):
        """
        Load a trained model from disk.

        Args:
            filepath: Path to the saved model
        """
        self.model = joblib.load(filepath)
        self.is_trained = True
