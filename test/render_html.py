#!/usr/bin/env python3
"""
Render HTML from JSON report
Usage: cd test && python render_html.py
"""

import json
import sys
from pathlib import Path

print("="*60)
print("HTML RENDERING")
print("="*60)

# Check if report exists
if not Path("report_output.json").exists():
    print("❌ report_output.json not found")
    print("   Run generate_report.py first")
    sys.exit(1)

print("✅ Found report_output.json")

# Import modules
try:
    from template_renderer import TemplateRenderer
    from convert_report_format import convert_report_format
    print("✅ Modules imported")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Convert format
print("\n[Step 1/3] Converting report format...")
try:
    data = convert_report_format('report_output.json', 'report_converted.json')
    print("   ✅ Format converted")
except Exception as e:
    print(f"   ❌ Error converting: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Render HTML
print("\n[Step 2/3] Rendering HTML...")
try:
    renderer = TemplateRenderer('template_landing.html')
    renderer.render_to_file(data, 'final_report.html')
    print("   ✅ HTML rendered")
except Exception as e:
    print(f"   ❌ Error rendering: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n[Step 3/3] Complete!")
print("\n" + "="*60)
print("✅ SUCCESS!")
print("="*60)
print("📄 Output: final_report.html")
print("\n📌 Open in browser:")
print("   open final_report.html")
print("="*60)
