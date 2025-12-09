# Student Performance Analytics - Examples

This directory contains example scripts demonstrating various features of the system.

## Available Examples

### `usage_examples.py`

Comprehensive examples showing:

1. **Basic Analysis** - Generate data and compute statistics
2. **Risk Prediction** - Train ML model and make predictions
3. **At-Risk Analysis** - Identify and analyze at-risk students
4. **Correlation Analysis** - Find key performance predictors
5. **Distribution Analysis** - Analyze grade distributions

## Running Examples

```bash
python examples/usage_examples.py
```

## Individual Examples

### Example 1: Basic Analysis

```python
from src.data_generator import StudentDataGenerator
from src.analyzer import StudentAnalyzer

generator = StudentDataGenerator()
data = generator.generate_student_data(n_students=50)

analyzer = StudentAnalyzer(data)
stats = analyzer.get_summary_statistics()
print(stats)
```

### Example 2: Predict At-Risk Students

```python
from src.predictor import RiskPredictor

predictor = RiskPredictor()
metrics = predictor.train(data)
predictions = predictor.predict(new_data)
```

### Example 3: Visualize Results

```python
from src.visualizer import Visualizer

viz = Visualizer()
viz.plot_grade_distribution(data, 'grades.png')
viz.plot_correlation_heatmap(data, 'correlations.png')
```
