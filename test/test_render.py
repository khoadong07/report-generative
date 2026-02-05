#!/usr/bin/env python3
"""
Test template rendering
"""

import json
from template_renderer import TemplateRenderer

# Load data
with open('report_converted.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Data loaded:")
print(f"  slide1.title: {data.get('slide1', {}).get('title')}")
print(f"  slide1.kpi_cards: {len(data.get('slide1', {}).get('kpi_cards', []))} items")

# Test simple replacement
renderer = TemplateRenderer('template_landing.html')

# Test nested value
print("\nTesting nested value access:")
title = renderer._get_nested_value(data, 'slide1.title')
print(f"  slide1.title = {title}")

kpi_cards = renderer._get_nested_value(data, 'slide1.kpi_cards')
print(f"  slide1.kpi_cards = {type(kpi_cards)}, length = {len(kpi_cards) if isinstance(kpi_cards, list) else 'N/A'}")

if isinstance(kpi_cards, list) and len(kpi_cards) > 0:
    print(f"  First card: {kpi_cards[0]}")

# Render
print("\nRendering template...")
html = renderer.render(data)

# Check if KPI cards are rendered
if 'Tổng thảo luận' in html:
    print("✅ KPI cards rendered successfully!")
else:
    print("❌ KPI cards NOT rendered")
    
    # Debug: Check what's in the HTML
    import re
    kpi_section = re.search(r'<div class="kpi-grid">(.*?)</div>', html, re.DOTALL)
    if kpi_section:
        content = kpi_section.group(1)[:500]
        print(f"\nKPI Grid content (first 500 chars):\n{content}")

# Save for inspection
with open('test_output.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\nTest output saved to: test_output.html")
