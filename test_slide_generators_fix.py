#!/usr/bin/env python3
"""
Test script to verify that all slide generators have correct method signatures
"""

import pandas as pd
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_slide_generator_signatures():
    """Test that all slide generators have correct method signatures"""
    
    print("🧪 Testing Slide Generator Method Signatures")
    print("=" * 60)
    
    # Create minimal test data
    test_data = {
        'Topic': ['Brand A', 'Brand B'],
        'Type': ['fbPageTopic', 'fbUserTopic'],
        'PublishedDate': ['2026-03-15', '2026-03-16'],
        'Sentiment': ['positive', 'negative'],
        'Labels1': ['Topic 1', 'Topic 2'],
        'Content': ['Test content 1', 'Test content 2'],
        'Title': ['Test title 1', 'Test title 2'],
        'Channel': ['Facebook', 'Facebook'],
        'SiteName': ['Site 1', 'Site 2'],
        'UrlTopic': ['https://example.com/1', 'https://example.com/2'],
        'Comments': [10, 5],
        'Id': [1, 2],
        'ParentId': [1, 2]
    }
    
    week1_df = pd.DataFrame(test_data)
    week2_df = pd.DataFrame(test_data)
    
    brand = "Brand A"
    week1_display = "15/03/2026 → 21/03/2026"
    
    # Mock LLM Client
    class MockLLMClient:
        def generate_response(self, prompt):
            return "Mock insight response"
    
    llm_client = MockLLMClient()
    topic_types = ["fbPageTopic", "fbUserTopic"]
    comment_types = ["fbPageComment", "fbUserComment"]
    
    try:
        # Test WeeklySlide8Generator
        from generators.weekly.slide_generators_weekly import WeeklySlide8Generator
        slide8_gen = WeeklySlide8Generator(topic_types, top_n=5)
        result8 = slide8_gen.generate(week1_df, brand, week1_display)
        print("✅ WeeklySlide8Generator.generate() - OK")
        
        # Test WeeklySlide9Generator  
        from generators.weekly.slide_generators_weekly import WeeklySlide9Generator
        slide9_gen = WeeklySlide9Generator(topic_types, comment_types, top_n=5)
        result9 = slide9_gen.generate(week1_df, brand, week1_display)
        print("✅ WeeklySlide9Generator.generate() - OK")
        
        # Test WeeklySlide10Generator
        from generators.weekly.slide_generators_weekly import WeeklySlide10Generator
        slide10_gen = WeeklySlide10Generator(llm_client, topic_types)
        result10 = slide10_gen.generate(week1_df, brand, week1_display)
        print("✅ WeeklySlide10Generator.generate() - OK")
        
        # Test WeeklySlide12Generator
        from generators.weekly.slide_generators_weekly import WeeklySlide12Generator
        slide12_gen = WeeklySlide12Generator(llm_client, topic_types)
        result12 = slide12_gen.generate(week1_df, week2_df, brand, week1_display)
        print("✅ WeeklySlide12Generator.generate() - OK")
        
        print("\n🎉 All slide generator signatures are correct!")
        
        # Show sample results
        print(f"\n📊 Sample Results:")
        print(f"   Slide 8 title: {result8['title']}")
        print(f"   Slide 9 title: {result9['title']}")
        print(f"   Slide 10 title: {result10['title']}")
        print(f"   Slide 12 title: {result12['title']}")
        
    except Exception as e:
        print(f"❌ Error testing slide generators: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_slide_generator_signatures()