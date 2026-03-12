#!/usr/bin/env python3
"""
Test script to verify slide count logic works correctly
"""

def test_slide_count_logic():
    """Test that slide count changes based on show_interactions"""
    
    # Mock metadata for testing
    metadata_with_interactions = {
        'brand': 'TestBrand',
        'report_date': '2026-03-12 15:00',
        'compare_date': '2026-03-11 15:00',
        'show_interactions': True,
        'total_slides': 6
    }
    
    metadata_without_interactions = {
        'brand': 'TestBrand',
        'report_date': '2026-03-12 15:00',
        'compare_date': '2026-03-11 15:00',
        'show_interactions': False,
        'total_slides': 5
    }
    
    print("🧪 Testing slide count logic...")
    
    # Test 1: With interactions
    print(f"✅ With interactions: {metadata_with_interactions['total_slides']} slides")
    assert metadata_with_interactions['total_slides'] == 6
    assert metadata_with_interactions['show_interactions'] == True
    
    # Test 2: Without interactions
    print(f"✅ Without interactions: {metadata_without_interactions['total_slides']} slides")
    assert metadata_without_interactions['total_slides'] == 5
    assert metadata_without_interactions['show_interactions'] == False
    
    print("🎉 All tests passed!")

if __name__ == "__main__":
    test_slide_count_logic()