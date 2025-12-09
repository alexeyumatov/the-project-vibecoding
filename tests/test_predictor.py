"""
Tests for risk prediction model.
"""

import pytest
import pandas as pd
import numpy as np
from src.predictor import RiskPredictor
from src.data_generator import StudentDataGenerator


@pytest.fixture
def sample_data():
    """Generate sample data for testing."""
    generator = StudentDataGenerator(seed=42)
    return generator.generate_student_data(n_students=100)


class TestRiskPredictor:
    """Test cases for RiskPredictor class."""

    def test_initialization(self):
        """Test predictor initialization."""
        predictor = RiskPredictor()
        assert predictor.model is not None
        assert predictor.is_trained is False
        assert len(predictor.feature_columns) == 6

    def test_prepare_features(self, sample_data):
        """Test feature preparation."""
        predictor = RiskPredictor()
        features = predictor.prepare_features(sample_data)

        assert isinstance(features, pd.DataFrame)
        assert len(features) == len(sample_data)
        assert list(features.columns) == predictor.feature_columns

    def test_train_model(self, sample_data):
        """Test model training."""
        predictor = RiskPredictor()
        metrics = predictor.train(sample_data, test_size=0.2)

        # Check that model is marked as trained
        assert predictor.is_trained is True

        # Check that metrics are returned
        assert 'accuracy' in metrics
        assert 'precision' in metrics
        assert 'recall' in metrics
        assert 'f1_score' in metrics

        # Check that metrics are reasonable
        assert 0 <= metrics['accuracy'] <= 1
        assert 0 <= metrics['precision'] <= 1
        assert 0 <= metrics['recall'] <= 1
        assert 0 <= metrics['f1_score'] <= 1

    def test_predict_without_training(self, sample_data):
        """Test that prediction fails without training."""
        predictor = RiskPredictor()

        with pytest.raises(ValueError, match="Model must be trained"):
            predictor.predict(sample_data)

    def test_predict(self, sample_data):
        """Test prediction."""
        predictor = RiskPredictor()
        predictor.train(sample_data)

        predictions = predictor.predict(sample_data)

        assert len(predictions) == len(sample_data)
        assert set(predictions).issubset({0, 1})

    def test_predict_proba(self, sample_data):
        """Test probability prediction."""
        predictor = RiskPredictor()
        predictor.train(sample_data)

        probabilities = predictor.predict_proba(sample_data)

        assert len(probabilities) == len(sample_data)
        assert probabilities.shape[1] == 2  # Two classes

        # Check that probabilities sum to 1
        row_sums = probabilities.sum(axis=1)
        np.testing.assert_array_almost_equal(
            row_sums, np.ones(len(sample_data)))

    def test_get_feature_importance(self, sample_data):
        """Test feature importance retrieval."""
        predictor = RiskPredictor()
        predictor.train(sample_data)

        importance = predictor.get_feature_importance()

        assert isinstance(importance, pd.DataFrame)
        assert len(importance) == len(predictor.feature_columns)
        assert 'feature' in importance.columns
        assert 'importance' in importance.columns

        # Check that importance values sum to approximately 1
        assert 0.99 <= importance['importance'].sum() <= 1.01

    def test_feature_importance_without_training(self):
        """Test that feature importance fails without training."""
        predictor = RiskPredictor()

        with pytest.raises(ValueError, match="Model must be trained"):
            predictor.get_feature_importance()

    def test_save_and_load_model(self, sample_data, tmp_path):
        """Test model saving and loading."""
        predictor = RiskPredictor()
        predictor.train(sample_data)

        # Save model
        model_path = tmp_path / "test_model.joblib"
        predictor.save_model(str(model_path))

        assert model_path.exists()

        # Load model
        new_predictor = RiskPredictor()
        new_predictor.load_model(str(model_path))

        assert new_predictor.is_trained is True

        # Check that predictions are the same
        pred1 = predictor.predict(sample_data)
        pred2 = new_predictor.predict(sample_data)

        np.testing.assert_array_equal(pred1, pred2)
