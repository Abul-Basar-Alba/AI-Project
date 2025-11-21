#!/bin/bash

# HealthNest AI - Automated Setup Script
# This script will prepare datasets, train models, and start the application

echo "=================================================="
echo "🏥 HealthNest AI - Automated Setup"
echo "=================================================="
echo ""

# Check Python version
echo "🔍 Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi
echo "✅ Python found"
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
cd backend
pip3 install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
cd ..
echo "✅ Dependencies installed"
echo ""

# Prepare datasets
echo "📊 Preparing datasets..."
cd datasets
python3 dataset_downloader.py
if [ $? -ne 0 ]; then
    echo "❌ Dataset preparation failed"
    exit 1
fi
echo ""

echo "🔄 Processing datasets..."
python3 preprocess_datasets.py
if [ $? -ne 0 ]; then
    echo "❌ Data preprocessing failed"
    exit 1
fi
cd ..
echo "✅ Datasets ready"
echo ""

# Train models
echo "🧠 Training AI models..."
pip3 install jupyter nbconvert --quiet
cd notebooks
jupyter nbconvert --to notebook --execute train_model.ipynb --ExecutePreprocessor.timeout=600 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Jupyter execution failed, trying alternative method..."
    echo "Please run the notebook manually:"
    echo "  jupyter notebook train_model.ipynb"
fi
cd ..
echo "✅ Model training completed"
echo ""

# Final checks
echo "🔍 Verifying setup..."
echo ""

# Check if models exist
if [ -f "models/qa_vectorizer.pkl" ]; then
    echo "✅ Q&A Model found"
else
    echo "⚠️  Q&A Model not found - please train models manually"
fi

if [ -f "models/calorie_predictor.pkl" ]; then
    echo "✅ Calorie Predictor found"
else
    echo "⚠️  Calorie Predictor not found"
fi

if [ -f "models/health_knowledge.json" ]; then
    echo "✅ Health Knowledge Base found"
else
    echo "⚠️  Health Knowledge Base not found"
fi

echo ""
echo "=================================================="
echo "✅ Setup Complete!"
echo "=================================================="
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Start the backend server:"
echo "   cd backend"
echo "   python3 app.py"
echo ""
echo "2. Open frontend in browser:"
echo "   cd frontend"
echo "   python3 -m http.server 8000"
echo "   Then visit: http://localhost:8000"
echo ""
echo "Or simply open frontend/index.html in your browser"
echo ""
echo "=================================================="
