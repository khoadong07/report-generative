#!/usr/bin/env python3
"""
Test script for the new WeeklySlide12Generator (Brand Comparison)
Using real Excel data from /Users/khoadong/Downloads/62676257da4cac5f5e14dc78_1773806481372.xlsx
"""

import pandas as pd
import sys
import os
from datetime import datetime, timedelta

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.llm_client import LLMClient
from generators.weekly.slide_generators_weekly import WeeklySlide12Generator

def load_real_data():
    """Load real data from Excel file"""
    
    excel_file = "/Users/khoadong/Downloads/62676257da4cac5f5e14dc78_1773806481372.xlsx"
    
    print(f"📂 Loading data from: {excel_file}")
    
    try:
        # Load the Excel file
        df = pd.read_excel(excel_file)
        print(f"   ✅ Loaded {len(df)} rows")
        print(f"   📋 Columns: {list(df.columns)}")
        
        # Convert PublishedDate to datetime
        if 'PublishedDate' in df.columns:
            df['PublishedDate'] = pd.to_datetime(df['PublishedDate'])
        
        # Show unique brands/topics
        if 'Topic' in df.columns:
            unique_topics = df['Topic'].unique()
            print(f"   🏷️  Unique Topics/Brands: {len(unique_topics)}")
            print(f"      {list(unique_topics)[:10]}...")  # Show first 10
        
        # Show date range
        if 'PublishedDate' in df.columns:
            min_date = df['PublishedDate'].min()
            max_date = df['PublishedDate'].max()
            print(f"   📅 Date range: {min_date} → {max_date}")
        
        # Filter for Topic type only
        if 'Type' in df.columns:
            topic_df = df[df['Type'] == 'Topic'].copy()
            print(f"   📊 Topic entries: {len(topic_df)}")
        else:
            topic_df = df.copy()
        
        # Define two weeks for comparison
        # Use the most recent data as week1, and 7 days before as week2
        if len(topic_df) > 0 and 'PublishedDate' in topic_df.columns:
            latest_date = topic_df['PublishedDate'].max()
            week1_start = latest_date - timedelta(days=6)  # Last 7 days
            week2_start = latest_date - timedelta(days=13)  # 7 days before that
            week2_end = latest_date - timedelta(days=7)
            
            print(f"   📅 Week 1 (current): {week1_start.date()} → {latest_date.date()}")
            print(f"   📅 Week 2 (previous): {week2_start.date()} → {week2_end.date()}")
            
            # Filter data for each week
            week1_df = topic_df[
                (topic_df['PublishedDate'] >= week1_start) & 
                (topic_df['PublishedDate'] <= latest_date)
            ].copy()
            
            week2_df = topic_df[
                (topic_df['PublishedDate'] >= week2_start) & 
                (topic_df['PublishedDate'] <= week2_end)
            ].copy()
            
            print(f"   📊 Week 1 data: {len(week1_df)} rows")
            print(f"   📊 Week 2 data: {len(week2_df)} rows")
            
            # Show brand distribution for each week
            if len(week1_df) > 0:
                week1_brands = week1_df['Topic'].value_counts()
                print(f"   🏆 Week 1 top brands: {dict(week1_brands.head())}")
            
            if len(week2_df) > 0:
                week2_brands = week2_df['Topic'].value_counts()
                print(f"   🏆 Week 2 top brands: {dict(week2_brands.head())}")
            
            return week1_df, week2_df, latest_date
        else:
            print("   ❌ No valid date data found")
            return pd.DataFrame(), pd.DataFrame(), None
            
    except Exception as e:
        print(f"   ❌ Error loading file: {e}")
        return pd.DataFrame(), pd.DataFrame(), None

def test_slide12_generator():
    """Test the WeeklySlide12Generator with real data"""
    
    print("🧪 Testing WeeklySlide12Generator (Brand Comparison) with Real Data")
    print("=" * 70)
    
    # Load real data
    week1_df, week2_df, latest_date = load_real_data()
    
    if len(week1_df) == 0 or len(week2_df) == 0:
        print("❌ No sufficient data found for testing")
        return
    
    # Initialize LLM client (mock for testing)
    class MockLLMClient:
        def generate_response(self, prompt):
            return "Phân tích so sánh thương hiệu cho thấy xu hướng cạnh tranh trong tuần qua. [Nguồn: https://example.com/1] Các thương hiệu hàng đầu có sự thay đổi đáng kể về lượng đề cập. [Nguồn: https://example.com/2] Xu hướng tăng trưởng được ghi nhận ở một số thương hiệu mới nổi. [Nguồn: https://example.com/3]"
    
    llm_client = MockLLMClient()
    
    # Initialize slide generator
    topic_types = ["Topic"]
    slide12_gen = WeeklySlide12Generator(llm_client, topic_types)
    
    # Get the main brand (most mentioned in week1)
    main_brand = week1_df['Topic'].value_counts().index[0] if len(week1_df) > 0 else "Unknown"
    
    # Generate slide 12
    print(f"\n🔄 Generating Slide 12 for brand: {main_brand}")
    
    week1_start = latest_date - timedelta(days=6)
    week1_display = f"{week1_start.strftime('%d/%m/%Y')} → {latest_date.strftime('%d/%m/%Y')}"
    
    result = slide12_gen.generate(
        week1_df=week1_df,
        week2_df=week2_df,
        brand=main_brand,
        week1_display=week1_display
    )
    
    print("\n✅ Slide 12 generated successfully!")
    print("\n📋 Results:")
    print(f"   Title: {result['title']}")
    print(f"   Subtitle: {result['subtitle']}")
    print(f"   Insight: {result['insight'][:150]}...")
    
    print(f"\n📊 Donut Charts:")
    week_before_data = result['donut_charts']['week_before']['data']
    current_week_data = result['donut_charts']['current_week']['data']
    
    print(f"   Week Before ({len(week_before_data)} brands):")
    for item in week_before_data[:5]:  # Show top 5
        print(f"     - {item['brand']}: {item['mentions']} mentions")
    
    print(f"   Current Week ({len(current_week_data)} brands):")
    for item in current_week_data[:5]:  # Show top 5
        print(f"     - {item['brand']}: {item['mentions']} mentions")
    
    print(f"\n📈 Bar Chart Data:")
    bar_data = result['bar_chart']['data']
    print(f"   Total brands compared: {len(bar_data)}")
    
    for item in bar_data[:8]:  # Show top 8
        change_symbol = "📈" if item['percentage_change'] >= 0 else "📉"
        print(f"     {change_symbol} {item['brand']}: {item['week_before']} → {item['current_week']} ({item['percentage_change']:+.1f}%)")
    
    print(f"\n🎨 Legend ({len(result['legend'])} colors):")
    for item in result['legend'][:5]:  # Show first 5
        print(f"   - {item['brand']}: {item['color']}")
    
    print("\n🎉 Test completed successfully!")
    
    # Save results to JSON for inspection
    import json
    with open('slide12_test_results.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    print("💾 Results saved to slide12_test_results.json")

if __name__ == "__main__":
    test_slide12_generator()