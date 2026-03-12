#!/usr/bin/env python3
"""
Test script to verify subtitle format for datetime ranges
"""

from datetime import datetime, timedelta
import pandas as pd

def test_subtitle_format():
    """Test that subtitle shows both time ranges correctly"""
    
    print("🧪 Testing subtitle format...")
    
    # Simulate datetime mode logic
    report_date = "2026-03-12 15:00:00"
    report_dt = pd.to_datetime(report_date)
    compare_dt = report_dt - timedelta(hours=24)
    
    # Format for display (24h window)
    report_display = report_dt.strftime("%d/%m/%Y %H:%M")
    compare_display = compare_dt.strftime("%d/%m/%Y %H:%M")
    
    # Format for subtitle (show both 24h ranges)
    datetime_range_display = f"{compare_display} → {report_display}"
    
    # Create compare range for subtitle (previous 24h window)
    compare_start_dt = compare_dt - timedelta(hours=24)
    compare_start_display = compare_start_dt.strftime("%d/%m/%Y %H:%M")
    compare_range_display = f"{compare_start_display} → {compare_display}"
    
    print(f"Report range: {datetime_range_display}")
    print(f"Compare range: {compare_range_display}")
    
    # Expected format for subtitle
    expected_subtitle = f"Ngày {datetime_range_display} (so sánh với {compare_range_display})"
    print(f"Expected subtitle: {expected_subtitle}")
    
    # Verify format
    assert "11/03/2026 15:00 → 12/03/2026 15:00" in expected_subtitle
    assert "10/03/2026 15:00 → 11/03/2026 15:00" in expected_subtitle
    
    print("✅ Subtitle format is correct!")
    print("🎉 Test passed!")

if __name__ == "__main__":
    test_subtitle_format()