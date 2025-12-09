"""
Main entry point for Student Performance Analytics System.
"""

import argparse
import os
import pandas as pd
from src.data_generator import StudentDataGenerator
from src.analyzer import StudentAnalyzer
from src.predictor import RiskPredictor
from src.visualizer import Visualizer


def main():
    """Main function to run the analytics pipeline."""
    parser = argparse.ArgumentParser(
        description='Student Performance Analytics & Prediction System'
    )
    parser.add_argument(
        '--generate-data',
        action='store_true',
        help='Generate synthetic student data'
    )
    parser.add_argument(
        '--n-students',
        type=int,
        default=100,
        help='Number of students to generate (default: 100)'
    )
    parser.add_argument(
        '--analyze',
        action='store_true',
        help='Perform data analysis'
    )
    parser.add_argument(
        '--train-model',
        action='store_true',
        help='Train risk prediction model'
    )
    parser.add_argument(
        '--visualize',
        action='store_true',
        help='Generate visualizations'
    )
    parser.add_argument(
        '--input-file',
        type=str,
        default='data/processed/student_data.csv',
        help='Input data file path'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='reports',
        help='Output directory for reports'
    )

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('models', exist_ok=True)

    # Generate data if requested
    if args.generate_data:
        print(f"Generating data for {args.n_students} students...")
        generator = StudentDataGenerator()
        data = generator.generate_student_data(n_students=args.n_students)
        data.to_csv(args.input_file, index=False)
        print(f"Data saved to {args.input_file}")

    # Load data
    if os.path.exists(args.input_file):
        print(f"Loading data from {args.input_file}...")
        data = pd.read_csv(args.input_file)
        print(f"Loaded {len(data)} student records")
    else:
        print(f"Error: Input file {args.input_file} not found!")
        print("Run with --generate-data flag to create sample data")
        return

    # Analyze data
    if args.analyze:
        print("\n" + "="*50)
        print("ANALYSIS RESULTS")
        print("="*50)

        analyzer = StudentAnalyzer(data)

        # Summary statistics
        stats = analyzer.get_summary_statistics()
        print("\n📊 Summary Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")

        # At-risk students
        at_risk = analyzer.identify_at_risk_students()
        print(f"\n⚠️  At-Risk Students: {len(at_risk)}")
        if len(at_risk) > 0:
            print("\nTop 5 Most At-Risk Students:")
            print(at_risk[['student_id', 'name', 'final_grade',
                          'attendance_rate', 'risk_factors']].head())

        # Correlations
        corr = analyzer.calculate_correlations()
        print("\n🔗 Feature Correlations with Final Grade:")
        print(corr.to_string(index=False))

        # Performance distribution
        dist = analyzer.analyze_performance_distribution()
        print("\n📈 Performance Distribution:")
        for key, value in dist.items():
            print(f"  {key}: {value}")

    # Train model
    if args.train_model:
        print("\n" + "="*50)
        print("TRAINING PREDICTION MODEL")
        print("="*50)

        predictor = RiskPredictor()
        metrics = predictor.train(data)

        print("\n🤖 Model Performance:")
        print(f"  Accuracy: {metrics['accuracy']}")
        print(f"  Precision: {metrics['precision']}")
        print(f"  Recall: {metrics['recall']}")
        print(f"  F1-Score: {metrics['f1_score']}")

        print("\n📊 Feature Importance:")
        importance = predictor.get_feature_importance()
        print(importance.to_string(index=False))

        # Save model
        model_path = 'models/risk_predictor.joblib'
        predictor.save_model(model_path)
        print(f"\n💾 Model saved to {model_path}")

    # Generate visualizations
    if args.visualize:
        print("\n" + "="*50)
        print("GENERATING VISUALIZATIONS")
        print("="*50)

        visualizer = Visualizer()
        analyzer = StudentAnalyzer(data)

        # Grade distribution
        plot_path = os.path.join(args.output_dir, 'grade_distribution.png')
        visualizer.plot_grade_distribution(data, plot_path)
        print(f"✓ Grade distribution saved to {plot_path}")

        # Correlation heatmap
        plot_path = os.path.join(args.output_dir, 'correlation_heatmap.png')
        visualizer.plot_correlation_heatmap(data, plot_path)
        print(f"✓ Correlation heatmap saved to {plot_path}")

        # Risk comparison
        plot_path = os.path.join(args.output_dir, 'risk_comparison.png')
        visualizer.plot_risk_comparison(data, plot_path)
        print(f"✓ Risk comparison saved to {plot_path}")

        # Performance categories
        dist = analyzer.analyze_performance_distribution()
        plot_path = os.path.join(args.output_dir, 'performance_categories.png')
        visualizer.plot_performance_categories(dist, plot_path)
        print(f"✓ Performance categories saved to {plot_path}")

        # Feature importance (if model exists)
        if os.path.exists('models/risk_predictor.joblib'):
            predictor = RiskPredictor()
            predictor.load_model('models/risk_predictor.joblib')
            importance = predictor.get_feature_importance()
            plot_path = os.path.join(args.output_dir, 'feature_importance.png')
            visualizer.plot_feature_importance(importance, plot_path)
            print(f"✓ Feature importance saved to {plot_path}")

    print("\n✅ Done!")


if __name__ == '__main__':
    main()
