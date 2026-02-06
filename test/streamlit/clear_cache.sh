#!/bin/bash

echo "🧹 Clearing all Python cache..."
echo ""

# Clear __pycache__ directories
echo "Removing __pycache__ directories..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo "✅ __pycache__ cleared"

# Clear .pyc files
echo "Removing .pyc files..."
find . -type f -name "*.pyc" -delete 2>/dev/null
echo "✅ .pyc files cleared"

# Clear .pyo files
echo "Removing .pyo files..."
find . -type f -name "*.pyo" -delete 2>/dev/null
echo "✅ .pyo files cleared"

# Clear Streamlit cache
echo "Clearing Streamlit cache..."
rm -rf ~/.streamlit/cache 2>/dev/null
echo "✅ Streamlit cache cleared"

echo ""
echo "✅ All cache cleared!"
echo ""
echo "Now restart Streamlit:"
echo "  streamlit run app.py"
