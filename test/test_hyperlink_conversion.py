#!/usr/bin/env python3
"""
Test script to demonstrate hyperlink conversion in insights
"""

import re


def format_insight_with_hyperlinks(insight_text):
    """
    Convert URLs in insight text to markdown hyperlinks
    
    Converts:
    - [Nguồn: http://example.com] → [Nguồn](http://example.com)
    - [Nguồn: https://example.com] → [Nguồn](https://example.com)
    
    Args:
        insight_text: Original insight text with URLs
        
    Returns:
        Formatted text with markdown hyperlinks
    """
    # Pattern to match [Nguồn: URL] or [Source: URL]
    pattern = r'\[(?:Nguồn|Source):\s*(https?://[^\]]+)\]'
    
    # Replace with markdown link format
    def replace_link(match):
        url = match.group(1).strip()
        return f'[Nguồn]({url})'
    
    formatted_text = re.sub(pattern, replace_link, insight_text)
    
    return formatted_text


# Test cases
test_cases = [
    {
        "name": "Single URL",
        "input": "Lượng thảo luận tăng đột biến. [Nguồn: https://www.tiktok.com/@vtv.times/video/7601896457389591826]",
        "expected": "Lượng thảo luận tăng đột biến. [Nguồn](https://www.tiktok.com/@vtv.times/video/7601896457389591826)"
    },
    {
        "name": "Multiple URLs",
        "input": "Sự việc xoay quanh thông báo thu hồi. [Nguồn: http://facebook.com/138841156165916_1294284519398922] Nguyên nhân được xác định. [Nguồn: http://facebook.com/419555621494041_1317059697125118]",
        "expected": "Sự việc xoay quanh thông báo thu hồi. [Nguồn](http://facebook.com/138841156165916_1294284519398922) Nguyên nhân được xác định. [Nguồn](http://facebook.com/419555621494041_1317059697125118)"
    },
    {
        "name": "URL with spaces",
        "input": "Phản ứng từ cộng đồng. [Nguồn:   https://example.com/article   ]",
        "expected": "Phản ứng từ cộng đồng. [Nguồn](https://example.com/article)"
    },
    {
        "name": "Mixed http and https",
        "input": "Bài viết 1. [Nguồn: http://example.com] Bài viết 2. [Nguồn: https://example.com]",
        "expected": "Bài viết 1. [Nguồn](http://example.com) Bài viết 2. [Nguồn](https://example.com)"
    },
    {
        "name": "No URLs",
        "input": "Đây là insight không có URL.",
        "expected": "Đây là insight không có URL."
    },
    {
        "name": "Real example from report",
        "input": """Lượng thảo luận về Nestlé tăng đột biến trong ngày 2026-02-01, với 1,727 lượt đề cập, tăng hơn 104% so với ngày hôm trước, cho thấy một sự kiện tiêu cực đang thu hút sự chú ý lớn từ cộng đồng mạng. [Nguồn: https://www.tiktok.com/@vtv.times/video/7601896457389591826] Sự việc xoay quanh thông báo thu hồi tự nguyện 21 lô bánh ăn dặm Gerber® Arrowroot Biscuits tại Mỹ do phát hiện khả năng lẫn mảnh nhựa mềm hoặc giấy trong sản phẩm. [Nguồn: http://facebook.com/138841156165916_1294284519398922]""",
        "expected": """Lượng thảo luận về Nestlé tăng đột biến trong ngày 2026-02-01, với 1,727 lượt đề cập, tăng hơn 104% so với ngày hôm trước, cho thấy một sự kiện tiêu cực đang thu hút sự chú ý lớn từ cộng đồng mạng. [Nguồn](https://www.tiktok.com/@vtv.times/video/7601896457389591826) Sự việc xoay quanh thông báo thu hồi tự nguyện 21 lô bánh ăn dặm Gerber® Arrowroot Biscuits tại Mỹ do phát hiện khả năng lẫn mảnh nhựa mềm hoặc giấy trong sản phẩm. [Nguồn](http://facebook.com/138841156165916_1294284519398922)"""
    }
]


def run_tests():
    """Run all test cases"""
    print("\n" + "="*80)
    print("🧪 TESTING HYPERLINK CONVERSION")
    print("="*80)
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n[Test {i}] {test['name']}")
        print("-" * 80)
        
        result = format_insight_with_hyperlinks(test['input'])
        
        if result == test['expected']:
            print("✅ PASSED")
            passed += 1
        else:
            print("❌ FAILED")
            print(f"\nInput:\n{test['input']}")
            print(f"\nExpected:\n{test['expected']}")
            print(f"\nGot:\n{result}")
            failed += 1
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    print(f"Total: {len(test_cases)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print("="*80)
    
    return failed == 0


def demo_conversion():
    """Demo the conversion with a real example"""
    print("\n" + "="*80)
    print("🎨 DEMO: HYPERLINK CONVERSION")
    print("="*80)
    
    original = """Lượng thảo luận về Nestlé tăng đột biến trong ngày 2026-02-01, với 1,727 lượt đề cập, tăng hơn 104% so với ngày hôm trước. [Nguồn: https://www.tiktok.com/@vtv.times/video/7601896457389591826] Sự việc xoay quanh thông báo thu hồi tự nguyện 21 lô bánh ăn dặm. [Nguồn: http://facebook.com/138841156165916_1294284519398922] Nguyên nhân được xác định là do nguyên liệu bột dong riềng từ một nhà cung cấp. [Nguồn: http://facebook.com/419555621494041_1317059697125118]"""
    
    print("\n📝 ORIGINAL TEXT:")
    print("-" * 80)
    print(original)
    
    converted = format_insight_with_hyperlinks(original)
    
    print("\n✨ CONVERTED TEXT (with markdown hyperlinks):")
    print("-" * 80)
    print(converted)
    
    print("\n💡 HOW IT LOOKS IN MARKDOWN RENDERER:")
    print("-" * 80)
    print("The URLs are now clickable links that display as '[Nguồn]'")
    print("When clicked, they will open the respective URLs")
    
    print("\n🎯 BENEFITS:")
    print("-" * 80)
    print("✅ Cleaner appearance in slides")
    print("✅ Clickable links in platforms that support markdown")
    print("✅ Better user experience")
    print("✅ Professional presentation")
    print("="*80)


if __name__ == "__main__":
    # Run tests
    success = run_tests()
    
    # Show demo
    demo_conversion()
    
    # Exit with appropriate code
    exit(0 if success else 1)
