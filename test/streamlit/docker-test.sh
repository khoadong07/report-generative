#!/bin/bash
# Test Docker setup before building

set -e

echo "🧪 Docker Setup Test"
echo "===================="

# Check if we're in the right directory
if [ ! -f "Dockerfile" ]; then
    echo "❌ Error: Dockerfile not found"
    echo "Please run this script from test/streamlit/ directory"
    exit 1
fi

# Check required files
echo ""
echo "📋 Checking required files..."

required_files=(
    "Dockerfile"
    "docker-compose.yml"
    "requirements.txt"
    "app.py"
    ".env.example"
)

missing_files=()

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (missing)"
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    echo ""
    echo "❌ Missing files: ${missing_files[*]}"
    exit 1
fi

# Check .env file
echo ""
echo "🔐 Checking .env file..."
if [ -f ".env" ]; then
    echo "  ✅ .env exists"
    
    # Check if API_KEY and BASE_URL are set
    if grep -q "API_KEY=" .env && grep -q "BASE_URL=" .env; then
        echo "  ✅ API credentials configured"
    else
        echo "  ⚠️  Warning: API credentials may not be configured"
        echo "     Please check .env file"
    fi
else
    echo "  ⚠️  .env not found (will use .env.example)"
fi

# Check Docker
echo ""
echo "🐳 Checking Docker..."
if command -v docker &> /dev/null; then
    echo "  ✅ Docker installed: $(docker --version)"
    
    if docker info &> /dev/null; then
        echo "  ✅ Docker daemon running"
    else
        echo "  ❌ Docker daemon not running"
        echo "     Please start Docker and try again"
        exit 1
    fi
else
    echo "  ❌ Docker not installed"
    echo "     Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check Docker Compose
echo ""
echo "🐳 Checking Docker Compose..."
if command -v docker-compose &> /dev/null; then
    echo "  ✅ Docker Compose installed: $(docker-compose --version)"
elif docker compose version &> /dev/null; then
    echo "  ✅ Docker Compose (plugin) installed: $(docker compose version)"
else
    echo "  ❌ Docker Compose not installed"
    echo "     Please install Docker Compose"
    exit 1
fi

# Check .dockerignore
echo ""
echo "📝 Checking .dockerignore..."
if [ -f ".dockerignore" ]; then
    echo "  ✅ .dockerignore exists"
    
    # Check if requirements.txt is not ignored
    if grep -q "^\*.txt$" .dockerignore && ! grep -q "^!requirements.txt$" .dockerignore; then
        echo "  ⚠️  Warning: requirements.txt might be ignored"
        echo "     Make sure .dockerignore has: !requirements.txt"
    else
        echo "  ✅ requirements.txt not ignored"
    fi
else
    echo "  ⚠️  .dockerignore not found (optional)"
fi

# Test build context
echo ""
echo "🔍 Testing build context..."
echo "  Files that will be copied to Docker:"
echo ""

# List files (excluding .dockerignore patterns)
find . -maxdepth 1 -type f ! -name ".*" | head -20 | while read file; do
    echo "    - $file"
done

echo ""
echo "✅ All checks passed!"
echo ""
echo "📌 Next steps:"
echo "   1. Build image:  make build  (or docker-compose build)"
echo "   2. Run app:      make run    (or docker-compose up -d)"
echo "   3. View logs:    make logs-f (or docker-compose logs -f)"
echo "   4. Access app:   http://localhost:8501"
