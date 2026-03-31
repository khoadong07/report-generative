#!/usr/bin/env python3
"""
Test script to verify all builders work correctly
"""

def test_imports():
    """Test that all builders can be imported."""
    print("Testing builder imports...")
    
    try:
        from weekly_report_masan.builders.slide01_market import Slide01MarketPromptBuilder
        print("  ✅ Slide01MarketPromptBuilder")
    except Exception as e:
        print(f"  ❌ Slide01MarketPromptBuilder: {e}")
        return False
    
    try:
        from weekly_report_masan.builders.slide02_discussion import Slide02DiscussionPromptBuilder
        print("  ✅ Slide02DiscussionPromptBuilder")
    except Exception as e:
        print(f"  ❌ Slide02DiscussionPromptBuilder: {e}")
        return False
    
    try:
        from weekly_report_masan.builders.slide03_health import Slide03HealthPromptBuilder
        print("  ✅ Slide03HealthPromptBuilder")
    except Exception as e:
        print(f"  ❌ Slide03HealthPromptBuilder: {e}")
        return False
    
    try:
        from weekly_report_masan.builders.slide04_products import Slide04ProductsPromptBuilder
        print("  ✅ Slide04ProductsPromptBuilder")
    except Exception as e:
        print(f"  ❌ Slide04ProductsPromptBuilder: {e}")
        return False
    
    try:
        from weekly_report_masan.builders.slide05_category import Slide05CategoryPromptBuilder
        print("  ✅ Slide05CategoryPromptBuilder")
    except Exception as e:
        print(f"  ❌ Slide05CategoryPromptBuilder: {e}")
        return False
    
    return True


def test_slide_generators():
    """Test that all slide generators can be imported."""
    print("\nTesting slide generator imports...")
    
    try:
        from weekly_report_masan.slides.slide01_masan_market import Slide01MasanMarket
        print("  ✅ Slide01MasanMarket")
    except Exception as e:
        print(f"  ❌ Slide01MasanMarket: {e}")
        return False
    
    try:
        from weekly_report_masan.slides.slide02_discussion_overview import Slide02DiscussionOverview
        print("  ✅ Slide02DiscussionOverview")
    except Exception as e:
        print(f"  ❌ Slide02DiscussionOverview: {e}")
        return False
    
    try:
        from weekly_report_masan.slides.slide03_health_channels import Slide03HealthChannels
        print("  ✅ Slide03HealthChannels")
    except Exception as e:
        print(f"  ❌ Slide03HealthChannels: {e}")
        return False
    
    try:
        from weekly_report_masan.slides.slide04_products import Slide04Products
        print("  ✅ Slide04Products")
    except Exception as e:
        print(f"  ❌ Slide04Products: {e}")
        return False
    
    try:
        from weekly_report_masan.slides.slide05_category_detail import Slide05CategoryDetail
        print("  ✅ Slide05CategoryDetail")
    except Exception as e:
        print(f"  ❌ Slide05CategoryDetail: {e}")
        return False
    
    return True


def test_data_processor():
    """Test data processor import."""
    print("\nTesting data processor...")
    
    try:
        from weekly_report_masan.data_processor import merge_nganh_hang, load_mapping_file
        print("  ✅ Data processor functions")
    except Exception as e:
        print(f"  ❌ Data processor: {e}")
        return False
    
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("Masan Weekly Report - Module Test")
    print("=" * 60)
    
    all_passed = True
    
    if not test_imports():
        all_passed = False
    
    if not test_slide_generators():
        all_passed = False
    
    if not test_data_processor():
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    print("=" * 60)
