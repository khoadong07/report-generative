#!/bin/bash
# Quick start script for Streamlit app

echo "🚀 Starting Slide Prompt Generator..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "❗ Please edit .env and add your API credentials"
    echo ""
fi

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate venv
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Run streamlit
echo "🎉 Starting Streamlit app..."
echo "📍 App will open at: http://localhost:8501"
echo ""
streamlit run app.py
