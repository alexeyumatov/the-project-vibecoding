# 📊 Student Performance Analytics & Prediction System

![Tests](https://github.com/alexeyumatov/the-project-vibecoding/workflows/Tests%20and%20Code%20Quality/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> Comprehensive system for analyzing student performance and predicting at-risk students using machine learning

## 🎯 Project Overview

This project provides a complete analytics pipeline for educational institutions to:

-   **Analyze** student performance across multiple metrics
-   **Predict** which students are at risk of failing
-   **Visualize** performance distributions and correlations
-   **Generate** automated weekly reports with insights
-   **Deploy** interactive dashboards to GitHub Pages

### Why This Matters

Early identification of at-risk students allows educators to:

-   Intervene before students fall behind
-   Allocate support resources effectively
-   Track intervention effectiveness over time
-   Make data-driven decisions about curriculum and teaching methods

## ✨ Features

### 📈 Analytics Capabilities

-   **Summary Statistics**: Total students, average grades, attendance rates
-   **Risk Assessment**: Automatic identification of at-risk students with specific risk factors
-   **Correlation Analysis**: Discover which factors most strongly predict performance
-   **Performance Distribution**: Categorize students into performance tiers
-   **Engagement Metrics**: Track forum participation and platform usage

### 🤖 Machine Learning

-   **Random Forest Classifier** for risk prediction
-   **Feature Importance Analysis** to identify key predictors
-   **Model Evaluation** with accuracy, precision, recall, F1-score
-   **Probability Predictions** for nuanced risk assessment
-   **Model Persistence** for deployment and reuse

### 📊 Visualizations

-   Grade distribution histograms
-   Correlation heatmaps
-   At-risk vs. not-at-risk comparisons
-   Performance category pie charts
-   Feature importance bar charts

### 🚀 Automation

-   **Scheduled Reports**: Automatic weekly analysis via GitHub Actions
-   **GitHub Pages Deployment**: Auto-published interactive reports
-   **Manual Triggers**: Run on-demand with custom parameters
-   **Artifact Storage**: Historical reports saved for trend analysis

## 📁 Project Structure

```
.
├── .github/
│   └── workflows/
│       ├── tests.yml              # CI/CD: Testing and code quality
│       └── generate-report.yml    # Scheduled analytics report generation
├── src/
│   ├── __init__.py
│   ├── data_generator.py          # Synthetic data generation
│   ├── analyzer.py                # Statistical analysis
│   ├── predictor.py               # ML risk prediction model
│   ├── visualizer.py              # Data visualization
│   └── main.py                    # Main CLI application
├── tests/
│   ├── __init__.py
│   ├── test_data_generator.py
│   ├── test_analyzer.py
│   └── test_predictor.py
├── scripts/
│   └── generate_report.py         # HTML report generation
├── data/
│   ├── raw/                       # Raw input data
│   └── processed/                 # Processed datasets
├── models/                        # Saved ML models
├── reports/                       # Generated reports and visualizations
├── .gitignore
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### Prerequisites

-   Python 3.9 or higher
-   pip or conda package manager

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/alexeyumatov/the-project-vibecoding.git
cd the-project-vibecoding
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

## 📖 Usage

### Generate Sample Data

```bash
python -m src.main --generate-data --n-students 100
```

This creates synthetic student data with realistic performance patterns.

### Run Complete Analysis

```bash
python -m src.main \
  --generate-data \
  --n-students 100 \
  --analyze \
  --train-model \
  --visualize
```

### Example Output

```
==================================================
ANALYSIS RESULTS
==================================================

📊 Summary Statistics:
  total_students: 100
  at_risk_count: 23
  at_risk_percentage: 23.0
  avg_final_grade: 76.45
  avg_attendance: 0.82
  avg_assignment_score: 74.32
  avg_quiz_score: 72.18
  total_forum_posts: 687
  avg_time_on_platform: 6.54

⚠️  At-Risk Students: 23

🔗 Feature Correlations with Final Grade:
           feature  correlation
  avg_quiz_score        0.956
  avg_assignment_score  0.943
  attendance_rate       0.892
  time_on_platform      0.745
  forum_posts           0.456
  n_late_submissions   -0.623

🤖 Model Performance:
  Accuracy: 0.950
  Precision: 0.889
  Recall: 0.941
  F1-Score: 0.914
```

## 🎨 Visualizations

The system generates professional visualizations including:

### Grade Distribution

![Grade Distribution Example](reports/grade_distribution.png)

### Correlation Heatmap

![Correlation Heatmap Example](reports/correlation_heatmap.png)

### At-Risk Comparison

![Risk Comparison Example](reports/risk_comparison.png)

## 🔧 Advanced Usage

### Using Custom Data

Prepare your CSV file with these columns:

-   `student_id`: Unique identifier
-   `attendance_rate`: 0-1 scale
-   `avg_assignment_score`: 0-100
-   `avg_quiz_score`: 0-100
-   `forum_posts`: Integer count
-   `time_on_platform`: Hours per week
-   `n_late_submissions`: Integer count
-   `final_grade`: 0-100
-   `at_risk`: 0 or 1 (for training)

Then run:

```bash
python -m src.main \
  --input-file path/to/your/data.csv \
  --analyze \
  --train-model \
  --visualize
```

### Programmatic Usage

```python
from src.data_generator import StudentDataGenerator
from src.analyzer import StudentAnalyzer
from src.predictor import RiskPredictor

# Generate data
generator = StudentDataGenerator()
data = generator.generate_student_data(n_students=200)

# Analyze
analyzer = StudentAnalyzer(data)
stats = analyzer.get_summary_statistics()
at_risk = analyzer.identify_at_risk_students()

# Predict
predictor = RiskPredictor()
metrics = predictor.train(data)
predictions = predictor.predict(data)
```

## 🧪 Testing

Run the complete test suite:

```bash
pytest
```

Run with coverage report:

```bash
pytest --cov=src --cov-report=html
```

Run specific test file:

```bash
pytest tests/test_predictor.py -v
```

## 🤖 CI/CD & Automation

### Automated Testing

Every push triggers:

-   Multi-version Python testing (3.9, 3.10, 3.11)
-   Code quality checks (flake8, black)
-   Unit test execution with coverage
-   Coverage report upload to Codecov

### Weekly Analytics Reports

The system automatically:

1. **Generates** fresh student data every Monday at 9:00 AM UTC
2. **Analyzes** performance and trains ML model
3. **Creates** visualizations and HTML report
4. **Deploys** to GitHub Pages
5. **Saves** artifacts for historical tracking

### Manual Report Generation

Trigger manually from GitHub Actions tab:

1. Go to Actions → "Generate Weekly Analytics Report"
2. Click "Run workflow"
3. Specify parameters (number of students, report type)
4. View results at `https://alexeyumatov.github.io/the-project-vibecoding/`

## 📊 Sample Reports

Live demo report: [View Report](https://alexeyumatov.github.io/the-project-vibecoding/)

Reports include:

-   Executive summary with key metrics
-   Interactive visualizations
-   At-risk student identification
-   Feature importance analysis
-   Actionable recommendations

## 🛠️ Technical Stack

-   **Python 3.9+**: Core language
-   **pandas**: Data manipulation
-   **numpy**: Numerical computing
-   **scikit-learn**: Machine learning
-   **matplotlib & seaborn**: Visualization
-   **pytest**: Testing framework
-   **GitHub Actions**: CI/CD automation
-   **GitHub Pages**: Report hosting

## 📈 Model Performance

Current model achieves:

-   **Accuracy**: ~95%
-   **Precision**: ~89%
-   **Recall**: ~94%
-   **F1-Score**: ~91%

Key predictors (by importance):

1. Average quiz score (highest)
2. Average assignment score
3. Attendance rate
4. Time on platform
5. Forum posts
6. Late submissions (negative correlation)

## 🤝 Contributing

Contributions welcome! Areas for enhancement:

-   [ ] Additional ML models (XGBoost, Neural Networks)
-   [ ] Real-time dashboard with Streamlit
-   [ ] Integration with LMS APIs (Moodle, Canvas)
-   [ ] Multi-semester trend analysis
-   [ ] Personalized intervention recommendations
-   [ ] Email alerts for at-risk students

## 📝 Requirements

See `requirements.txt` for complete dependency list. Main requirements:

```
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
seaborn>=0.12.0
pytest>=7.4.0
```

## 🔒 Data Privacy

This project uses **synthetic data** for demonstration. When using with real student data:

-   Ensure compliance with FERPA, GDPR, or applicable regulations
-   Anonymize student identifiers
-   Secure data storage and transmission
-   Obtain necessary permissions and consents

## 📜 License

MIT License - see LICENSE file for details

## 👤 Author

**Alexey Umatov**

-   GitHub: [@alexeyumatov](https://github.com/alexeyumatov)
-   Project: AI in Education Course Assignment

## 🎓 Academic Context

This project was developed as a creative programming assignment for the "AI in Education" course, demonstrating:

-   Practical application of ML to educational problems
-   Best practices in software engineering
-   DevOps automation with CI/CD
-   Comprehensive documentation and testing
-   Real-world utility for educational institutions

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star!**

Made with ❤️ for better education through data-driven insights

</div>
