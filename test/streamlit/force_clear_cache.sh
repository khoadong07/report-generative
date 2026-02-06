#!/bin/bash

echo "🧹 FORCE CLEARING ALL CACHE..."
echo ""

# Kill all Python/Streamlit processes
echo "1. Killing all Python/Streamlit processes..."
pkill -f streamlit 2>/dev/null
pkill -f python 2>/dev/null
sleep 1
echo "   ✅ Processes killed"

# Clear __pycache__
echo "2. Clearing __pycache__ directories..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo "   ✅ __pycache__ cleared"

# Clear .pyc files
echo "3. Clearing .pyc files..."
find . -type f -name "*.pyc" -delete 2>/dev/null
echo "   ✅ .pyc files cleared"

# Clear .pyo files
echo "4. Clearing .pyo files..."
find . -type f -name "*.pyo" -delete 2>/dev/null
echo "   ✅ .pyo files cleared"

# Clear Streamlit cache
echo "5. Clearing Streamlit cache..."
rm -rf ~/.streamlit/cache 2>/dev/null
echo "   ✅ Streamlit cache cleared"

# Clear Python import cache
echo "6. Clearing Python import cache..."
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null
find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null
echo "   ✅ Import cache cleared"

echo ""
echo "✅ ALL CACHE CLEARED!"
echo ""
echo "Now restart Streamlit:"
echo "  streamlit run app.py"
echo ""
echo "Look for these debug messages:"
echo "  → Total channels available: X"
echo "  → Filtered to top 8 channels: [...]"
echo "  → Number of channels in output: 8"
