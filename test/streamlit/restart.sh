#!/bin/bash

echo "🧹 Clearing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
rm -rf __pycache__

echo "✅ Cache cleared!"
echo ""
echo "🚀 Starting Streamlit..."
echo "📝 Watch for debug message: '🔍 DEBUG: Slide2Generator with empty dataframe fix loaded'"
echo ""

streamlit run app.py
