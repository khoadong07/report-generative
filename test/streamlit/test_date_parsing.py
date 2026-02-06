#!/usr/bin/env python3
"""
Quick test script to verify date parsing fixes
"""

import sys
sys.path.insert(0, '.')

from slide_generators import parse_date_flexible
from generate_slide_prompt import format_date

print("="*60)
print("Testing Date Parsing Functions")
print("="*60)

# Test cases
test_cases = [
    "2026-02-04 15:00:00",  # Raw datetime format
    "2026-02-04",           # Raw date format
    "04/02/2026 15:00",     # Display datetime format
    "04/02/2026",           # Display date format
]

print("\n1. Testing parse_date_flexible():")
print("-" * 60)
for date_str in test_cases:
    try:
        result = parse_date_flexible(date_str)
        print(f"✅ '{date_str}' → {result}")
    except Exception as e:
        print(f"❌ '{date_str}' → ERROR: {e}")

print("\n2. Testing format_date():")
print("-" * 60)
for date_str in test_cases:
    try:
        result = format_date(date_str)
        print(f"✅ '{date_str}' → '{result}'")
    except Exception as e:
        print(f"❌ '{date_str}' → ERROR: {e}")

print("\n" + "="*60)
print("All tests completed!")
print("="*60)
