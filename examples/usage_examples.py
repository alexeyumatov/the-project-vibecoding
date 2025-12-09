"""
Example usage scenarios for the Student Performance Analytics System.
"""

from src.data_generator import StudentDataGenerator
from src.analyzer import StudentAnalyzer
from src.predictor import RiskPredictor
from src.visualizer import Visualizer
import pandas as pd


def example_1_basic_analysis():
    """Example 1: Generate data and perform basic analysis."""
    print("=" * 60)
    print("EXAMPLE 1: Basic Analysis")
    print("=" * 60)

    # Generate sample data
    generator = StudentDataGenerator(seed=42)
    data = generator.generate_student_data(n_students=50)

    # Analyze
    analyzer = StudentAnalyzer(data)
    stats = analyzer.get_summary_statistics()

    print("\n📊 Summary Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Get top performers
    top_students = analyzer.get_top_performers(n=5)
    print("\n🏆 Top 5 Students:")
    print(top_students.to_string(index=False))


def example_2_risk_prediction():
    """Example 2: Train model and predict at-risk students."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Risk Prediction")
    print("=" * 60)

    # Generate data
    generator = StudentDataGenerator(seed=42)
    train_data = generator.generate_student_data(n_students=100)

    # Train predictor
    predictor = RiskPredictor()
    metrics = predictor.train(train_data, test_size=0.2)

    print("\n🤖 Model Performance:")
    print(f"  Accuracy:  {metrics['accuracy']:.3f}")
    print(f"  Precision: {metrics['precision']:.3f}")
    print(f"  Recall:    {metrics['recall']:.3f}")
    print(f"  F1-Score:  {metrics['f1_score']:.3f}")

    # Feature importance
    importance = predictor.get_feature_importance()
    print("\n📊 Most Important Features:")
    print(importance.head(3).to_string(index=False))

    # Predict on new data
    new_data = generator.generate_student_data(n_students=10)
    predictions = predictor.predict(new_data)
    probabilities = predictor.predict_proba(new_data)

    print(f"\n🔮 Predictions for 10 new students:")
    print(f"  At-risk: {predictions.sum()}")
    print(f"  Not at-risk: {len(predictions) - predictions.sum()}")


def example_3_identify_at_risk():
    """Example 3: Identify and analyze at-risk students."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: At-Risk Student Analysis")
    print("=" * 60)

    # Generate data
    generator = StudentDataGenerator(seed=42)
    data = generator.generate_student_data(n_students=80)

    # Analyze
    analyzer = StudentAnalyzer(data)
    at_risk = analyzer.identify_at_risk_students(threshold=60)

    print(f"\n⚠️  Found {len(at_risk)} at-risk students")

    if len(at_risk) > 0:
        print("\nTop 3 Most At-Risk:")
        print(at_risk[['student_id', 'name', 'final_grade',
                      'attendance_rate']].head(3).to_string(index=False))

        # Show risk factors for first student
        first_student = at_risk.iloc[0]
        print(f"\nRisk factors for {first_student['name']}:")
        for factor in first_student['risk_factors']:
            print(f"  - {factor}")


def example_4_correlations():
    """Example 4: Analyze correlations between features."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Feature Correlations")
    print("=" * 60)

    # Generate data
    generator = StudentDataGenerator(seed=42)
    data = generator.generate_student_data(n_students=100)

    # Calculate correlations
    analyzer = StudentAnalyzer(data)
    correlations = analyzer.calculate_correlations()

    print("\n🔗 Correlations with Final Grade:")
    print(correlations.to_string(index=False))

    print("\n💡 Insights:")
    strongest = correlations.iloc[0]
    print(f"  Strongest predictor: {strongest['feature']} "
          f"(r={strongest['correlation']:.3f})")


def example_5_performance_distribution():
    """Example 5: Analyze performance distribution."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Performance Distribution")
    print("=" * 60)

    # Generate data
    generator = StudentDataGenerator(seed=42)
    data = generator.generate_student_data(n_students=100)

    # Analyze distribution
    analyzer = StudentAnalyzer(data)
    dist = analyzer.analyze_performance_distribution()

    print("\n📈 Performance Categories:")
    print(f"  Excellent (≥90):     {dist['excellent']} students")
    print(f"  Good (75-89):        {dist['good']} students")
    print(f"  Satisfactory (60-74): {dist['satisfactory']} students")
    print(f"  Poor (<60):          {dist['poor']} students")

    print(f"\n📊 Statistics:")
    print(f"  Mean:   {dist['mean']:.2f}")
    print(f"  Median: {dist['median']:.2f}")
    print(f"  Std:    {dist['std']:.2f}")
    print(f"  Range:  {dist['min']:.2f} - {dist['max']:.2f}")


if __name__ == '__main__':
    # Run all examples
    example_1_basic_analysis()
    example_2_risk_prediction()
    example_3_identify_at_risk()
    example_4_correlations()
    example_5_performance_distribution()

    print("\n" + "=" * 60)
    print("✅ All examples completed successfully!")
    print("=" * 60)
