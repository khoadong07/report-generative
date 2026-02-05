#!/usr/bin/env python3
"""
Test script to verify setup
"""

import os
import sys
from pathlib import Path

print("="*60)
print("TESTING SETUP")
print("="*60)

# Test 1: Load .env
print("\n1. Testing .env loading...")
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"   ✅ .env file found: {env_path}")
    else:
        print(f"   ❌ .env file not found: {env_path}")
except ImportError:
    print("   ⚠️  python-dotenv not installed")
    print("   Install with: pip install python-dotenv")

# Test 2: Check API credentials
print("\n2. Checking API credentials...")
api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")

if api_key:
    print(f"   ✅ API_KEY found: {api_key[:10]}...")
else:
    print("   ❌ API_KEY not found")

if base_url:
    print(f"   ✅ BASE_URL found: {base_url}")
else:
    print("   ❌ BASE_URL not found")

# Test 3: Check data file
print("\n3. Checking data file...")
try:
    sys.path.insert(0, str(Path(__file__).parent))
    from config import FILE_PATH
    
    if os.path.exists(FILE_PATH):
        print(f"   ✅ Data file found: {FILE_PATH}")
        
        # Check file size
        size_mb = os.path.getsize(FILE_PATH) / (1024 * 1024)
        print(f"   📊 File size: {size_mb:.2f} MB")
    else:
        print(f"   ❌ Data file not found: {FILE_PATH}")
        print(f"   💡 Update FILE_PATH in test/config.py")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Check dependencies
print("\n4. Checking dependencies...")
dependencies = {
    'pandas': 'Data processing',
    'openpyxl': 'Excel file reading',
    'openai': 'LLM API client'
}

for package, description in dependencies.items():
    try:
        __import__(package)
        print(f"   ✅ {package:12} - {description}")
    except ImportError:
        print(f"   ❌ {package:12} - {description} (NOT INSTALLED)")

# Test 5: Test imports
print("\n5. Testing module imports...")
modules = [
    'config',
    'prompts',
    'data_loader',
    'llm_client',
    'slide_generators',
    'report_generator'
]

for module in modules:
    try:
        __import__(module)
        print(f"   ✅ {module}")
    except Exception as e:
        print(f"   ❌ {module}: {e}")

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)

all_good = True

if not api_key or not base_url:
    print("❌ API credentials missing")
    print("   Solution: Check test/.env file")
    all_good = False

try:
    from config import FILE_PATH
    if not os.path.exists(FILE_PATH):
        print("❌ Data file not found")
        print("   Solution: Update FILE_PATH in test/config.py")
        all_good = False
except:
    pass

try:
    import pandas, openpyxl, openai
except ImportError:
    print("❌ Some dependencies missing")
    print("   Solution: pip install pandas openpyxl openai python-dotenv")
    all_good = False

if all_good:
    print("✅ All checks passed! Ready to run.")
    print("\nNext step:")
    print("  python test/run_simple.py")
else:
    print("\n⚠️  Some issues found. Please fix them first.")

print("="*60)
