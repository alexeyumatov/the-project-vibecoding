#!/bin/bash

# Student Performance Analytics - Quick Demo
# This script demonstrates all features of the system

echo "======================================"
echo "Student Performance Analytics - Demo"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies if needed
if ! python -c "import pandas" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt > /dev/null 2>&1
fi

echo ""
echo -e "${BLUE}Step 1: Generating sample student data${NC}"
echo "========================================"
python -m src.main --generate-data --n-students 100

echo ""
echo -e "${BLUE}Step 2: Analyzing student performance${NC}"
echo "========================================"
python -m src.main --analyze --input-file data/processed/student_data.csv

echo ""
echo -e "${BLUE}Step 3: Training ML prediction model${NC}"
echo "========================================"
python -m src.main --train-model --input-file data/processed/student_data.csv

echo ""
echo -e "${BLUE}Step 4: Generating visualizations${NC}"
echo "========================================"
python -m src.main --visualize --input-file data/processed/student_data.csv

echo ""
echo -e "${BLUE}Step 5: Creating HTML report${NC}"
echo "========================================"
python scripts/generate_report.py

echo ""
echo -e "${GREEN}✅ Demo completed successfully!${NC}"
echo ""
echo "Generated files:"
echo "  - Data: data/processed/student_data.csv"
echo "  - Model: models/risk_predictor.joblib"
echo "  - Visualizations: reports/*.png"
echo "  - HTML Report: reports/index.html"
echo ""
echo "To run tests: pytest tests/ -v"
echo "To check code quality: flake8 src tests"
echo ""
