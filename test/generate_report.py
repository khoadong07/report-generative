#!/usr/bin/env python3
"""
Simple script to generate report - run from test directory
Usage: cd test && python generate_report.py
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Load .env
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

print("\n" + "="*60)
print("📊 REPORT GENERATION SYSTEM")
print("="*60)

# Check credentials
print("\n[Step 1/5] Checking API credentials...")
api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")

if not api_key or not base_url:
    print("❌ API credentials not found in .env file")
    sys.exit(1)

print(f"   ✅ API_KEY: {api_key[:10]}...")
print(f"   ✅ BASE_URL: {base_url}")

# Import modules
print("\n[Step 2/5] Loading modules...")
try:
    from report_generator import ReportGenerator
    print("   ✅ Modules loaded successfully")
except Exception as e:
    print(f"   ❌ Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Generate report
print("\n[Step 3/5] Initializing report generator...")
import time
start_time = time.time()

try:
    generator = ReportGenerator(api_key, base_url)
    print("   ✅ Generator initialized")
    
    print("\n[Step 4/5] Generating report...")
    print("   ⏱️  This will take 3-4 minutes (calling LLM 4 times)")
    print("   ☕ Please wait...\n")
    
    report = generator.generate_and_save("report_output.json")
    
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    
    print("\n[Step 5/5] Report completed!")
    
    print("\n" + "="*60)
    print("✅ SUCCESS!")
    print("="*60)
    print(f"⏱️  Total time: {minutes}m {seconds}s")
    print(f"📄 Output: report_output.json")
    print(f"📊 Slides generated: {len([k for k in report.keys() if k.startswith('slide')])}")
    print("\n📌 Next step:")
    print("   python render_html.py")
    print("="*60)
    
except Exception as e:
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    print(f"\n❌ Error after {minutes}m {seconds}s: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
