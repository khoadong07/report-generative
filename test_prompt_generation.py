#!/usr/bin/env python3
"""
Test script to verify that Slide 12 is properly integrated into the final prompt generation
"""

import json
from generators.weekly.generate_slide_prompt_weekly import generate_complete_prompt

def test_prompt_with_slide12():
    """Test prompt generation with Slide 12 data"""
    
    print("🧪 Testing Prompt Generation with Slide 12")
    print("=" * 60)
    
    # Load the test results from our previous test
    try:
        with open('slide12_test_results.json', 'r', encoding='utf-8') as f:
            slide12_data = json.load(f)
        print("✅ Loaded Slide 12 test data")
    except FileNotFoundError:
        print("❌ slide12_test_results.json not found. Please run test_slide12_simple.py first.")
        return
    
    # Create a minimal report_data structure for testing
    report_data = {
        'report_metadata': {
            'brand': 'Manulife',
            'week1_period': '12/03/2026 → 18/03/2026'
        },
        'slide_1': {
            'title': 'Tổng quan về Brand Manulife',
            'subtitle': 'Giai đoạn: 12/03/2026 → 18/03/2026',
            'show_interactions': True,
            'current_week_metrics': [
                {'label': 'Tổng đề cập', 'value': 5446, 'change_percent': -12.4}
            ],
            'weekly_comparison': [
                {'week': 'Tuần này', 'total_mentions': 5446, 'growth_rate': -12.4}
            ],
            'insight': 'Test insight for slide 1'
        },
        'slide_2': {
            'title': 'Xu hướng đề cập',
            'subtitle': 'Giai đoạn: 12/03/2026 → 18/03/2026',
            'trendline': [
                {'date': '2026-03-12', 'mentions': 800},
                {'date': '2026-03-13', 'mentions': 750}
            ],
            'insight': 'Test insight for slide 2'
        },
        'slide_3': {
            'title': 'Phân bố theo kênh',
            'subtitle': 'Giai đoạn: 12/03/2026 → 18/03/2026',
            'channel_distribution': [
                {'Channel': 'Facebook', 'count': 3000}
            ],
            'top_sources': [
                {'SiteName': 'Facebook Page', 'count': 1500}
            ],
            'insight': 'Test insight for slide 3'
        },
        'slide_4': {
            'title': 'Top nguồn tương tác',
            'subtitle': 'Giai đoạn: 12/03/2026 → 18/03/2026',
            'show_interactions': True,
            'table_rows': [
                {
                    'stt': 1,
                    'source_name': 'Test Source',
                    'total_engagement': 1000,
                    'reactions': 500,
                    'shares': 200,
                    'comments': 300,
                    'count': 10
                }
            ]
        },
        'slide_5': {
            'title': 'Top bài đăng tương tác',
            'subtitle': 'Giai đoạn: 12/03/2026 → 18/03/2026',
            'show_interactions': True,
            'table_rows': [
                {
                    'stt': 1,
                    'content': 'Test content',
                    'published_date': '2026-03-15',
                    'channel': 'Facebook',
                    'site_name': 'Test Site',
                    'reactions': 100,
                    'shares': 50,
                    'comments': 25,
                    'url': 'https://example.com'
                }
            ]
        },
        'slide_6': {
            'title': 'Sắc thái và chủ đề',
            'subtitle': 'Giai đoạn: 12/03/2026 → 18/03/2026',
            'previous_nsr': 15.5,
            'current_nsr': 18.2,
            'nsr_growth': 2.7,
            'previous_sentiment': [
                {'sentiment': 'Positive', 'count': 1000},
                {'sentiment': 'Neutral', 'count': 2000},
                {'sentiment': 'Negative', 'count': 500}
            ],
            'current_sentiment': [
                {'sentiment': 'Positive', 'count': 1200},
                {'sentiment': 'Neutral', 'count': 2200},
                {'sentiment': 'Negative', 'count': 400}
            ],
            'top_topics_with_sentiment': [
                {'topic': 'Test Topic', 'total': 100, 'negative': 20, 'neutral': 50, 'positive': 30}
            ],
            'insight': 'Test insight for slide 6'
        },
        'slide_7': {
            'title': 'Chủ đề tích cực',
            'subtitle': 'Giai đoạn: 12/03/2026 → 18/03/2026',
            'positive_topics': [
                {'Labels1': 'Positive Topic', 'count': 100}
            ],
            'insight': 'Test insight for slide 7'
        },
        'slide_8': {
            'title': 'Top bài đăng tích cực',
            'subtitle': 'Giai đoạn: 12/03/2026 → 18/03/2026',
            'table_rows': [
                {
                    'stt': 1,
                    'content': 'Positive content',
                    'published_date': '2026-03-15',
                    'channel': 'Facebook',
                    'site_name': 'Test Site',
                    'positive_comments': 50,
                    'url': 'https://example.com'
                }
            ]
        },
        'slide_9': {
            'title': 'Chủ đề tiêu cực',
            'subtitle': 'Giai đoạn: 12/03/2026 → 18/03/2026',
            'negative_topics': [
                {'Labels1': 'Negative Topic', 'count': 50}
            ],
            'insight': 'Test insight for slide 9'
        },
        'slide_10': {
            'title': 'Top bài đăng tiêu cực',
            'subtitle': 'Giai đoạn: 12/03/2026 → 18/03/2026',
            'table_rows': [
                {
                    'stt': 1,
                    'content': 'Negative content',
                    'published_date': '2026-03-15',
                    'channel': 'Facebook',
                    'site_name': 'Test Site',
                    'negative_comments': 25,
                    'url': 'https://example.com'
                }
            ]
        },
        'slide_12': slide12_data  # Add our Slide 12 data
    }
    
    print("🔄 Generating complete prompt with Slide 12...")
    
    try:
        prompt = generate_complete_prompt(report_data)
        print("✅ Prompt generated successfully!")
        
        # Check if Slide 12 content is in the prompt
        if "SLIDE 12 - TỔNG QUAN ĐỀ CẬP VỀ THƯƠNG HIỆU VỚI CÁC ĐỐI THỦ" in prompt:
            print("✅ Slide 12 section found in prompt")
        else:
            print("❌ Slide 12 section NOT found in prompt")
            
        # Check for key Slide 12 elements
        slide12_elements = [
            "DONUT CHARTS",
            "BAR CHART",
            "LEGEND",
            "Tuần trước",
            "Tuần hiện tại",
            "percentage_change"
        ]
        
        found_elements = []
        for element in slide12_elements:
            if element in prompt:
                found_elements.append(element)
        
        print(f"✅ Found {len(found_elements)}/{len(slide12_elements)} key Slide 12 elements:")
        for element in found_elements:
            print(f"   - {element}")
        
        # Save the full prompt for inspection
        with open('full_prompt_with_slide12.txt', 'w', encoding='utf-8') as f:
            f.write(prompt)
        print("💾 Full prompt saved to full_prompt_with_slide12.txt")
        
        # Show prompt length and slide count
        slide_count = prompt.count("SLIDE ")
        print(f"\n📊 Prompt Statistics:")
        print(f"   - Total length: {len(prompt):,} characters")
        print(f"   - Number of slides: {slide_count}")
        print(f"   - Contains Slide 12: {'Yes' if 'SLIDE 12' in prompt else 'No'}")
        
        print("\n🎉 Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error generating prompt: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_prompt_with_slide12()