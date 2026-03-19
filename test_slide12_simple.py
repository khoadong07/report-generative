#!/usr/bin/env python3
"""
Simple test script for the new WeeklySlide12Generator (Brand Comparison)
This version doesn't require LLM dependencies
"""

import pandas as pd
import sys
import os
from datetime import datetime, timedelta
import json

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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
            # Use the actual topic types from the data
            topic_types = ["fbUserTopic", "fbPageTopic", "fbGroupTopic", "newsTopic", "tiktokTopic", 
                          "threadsTopic", "snsTopic", "youtubeTopic", "forumTopic", "linkedinTopic"]
            topic_df = df[df['Type'].isin(topic_types)].copy()
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

def generate_slide12_data_only(week1_df, week2_df, brand, week1_display):
    """Generate slide 12 data without LLM (data processing only)"""
    
    # Use the actual topic types from the data (matching config.py)
    topic_types = ["fbUserTopic", "fbPageTopic", "fbGroupTopic", "newsTopic", "tiktokTopic", 
                   "threadsTopic", "snsTopic", "youtubeTopic", "forumTopic", "linkedinTopic"]
    
    # Get all brands from both weeks
    all_brands_week1 = set(week1_df[week1_df["Type"].isin(topic_types)]["Topic"].unique())
    all_brands_week2 = set(week2_df[week2_df["Type"].isin(topic_types)]["Topic"].unique())
    all_brands = sorted(list(all_brands_week1.union(all_brands_week2)))
    
    # Calculate mentions for each brand in both weeks
    brand_mentions_week1 = {}
    brand_mentions_week2 = {}
    
    for brand_name in all_brands:
        # Week 1 (current week)
        week1_brand_data = week1_df[
            (week1_df["Type"].isin(topic_types)) &
            (week1_df["Topic"] == brand_name)
        ]
        brand_mentions_week1[brand_name] = len(week1_brand_data)
        
        # Week 2 (previous week)
        week2_brand_data = week2_df[
            (week2_df["Type"].isin(topic_types)) &
            (week2_df["Topic"] == brand_name)
        ]
        brand_mentions_week2[brand_name] = len(week2_brand_data)
    
    # Generate donut chart data
    donut_data_week1 = []
    donut_data_week2 = []
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F"]
    
    for i, brand_name in enumerate(all_brands):
        color = colors[i % len(colors)]
        
        donut_data_week1.append({
            "brand": brand_name,
            "mentions": brand_mentions_week1.get(brand_name, 0),
            "color": color
        })
        
        donut_data_week2.append({
            "brand": brand_name,
            "mentions": brand_mentions_week2.get(brand_name, 0),
            "color": color
        })
    
    # Generate bar chart data with percentage changes
    bar_chart_data = []
    for brand_name in all_brands:
        week1_count = brand_mentions_week1.get(brand_name, 0)
        week2_count = brand_mentions_week2.get(brand_name, 0)
        
        # Calculate percentage change
        if week2_count > 0:
            percentage_change = ((week1_count - week2_count) / week2_count) * 100
        elif week1_count > 0:
            percentage_change = 100  # New mentions this week
        else:
            percentage_change = 0
        
        bar_chart_data.append({
            "brand": brand_name,
            "week_before": week2_count,
            "current_week": week1_count,
            "percentage_change": round(percentage_change, 1),
            "change_color": "green" if percentage_change >= 0 else "red"
        })
    
    # Sort by current week mentions (descending)
    bar_chart_data.sort(key=lambda x: x["current_week"], reverse=True)
    
    return {
        "title": f"Tổng quan đề cập về thương hiệu {brand} với các đối thủ",
        "subtitle": f"Giai đoạn: {week1_display}",
        "insight": f"Phân tích so sánh thương hiệu {brand} với các đối thủ trong giai đoạn {week1_display}.",
        "donut_charts": {
            "week_before": {
                "title": "Tuần trước",
                "data": donut_data_week2
            },
            "current_week": {
                "title": "Tuần hiện tại", 
                "data": donut_data_week1
            }
        },
        "legend": [{"brand": item["brand"], "color": item["color"]} for item in donut_data_week1],
        "bar_chart": {
            "title": "Tổng đề cập của các thương hiệu",
            "data": bar_chart_data
        }
    }

def test_slide12_generator():
    """Test the WeeklySlide12Generator with real data (data processing only)"""
    
    print("🧪 Testing WeeklySlide12Generator (Brand Comparison) with Real Data")
    print("=" * 70)
    
    # Load real data
    week1_df, week2_df, latest_date = load_real_data()
    
    if len(week1_df) == 0 or len(week2_df) == 0:
        print("❌ No sufficient data found for testing")
        return
    
    # Get the main brand (most mentioned in week1)
    main_brand = week1_df['Topic'].value_counts().index[0] if len(week1_df) > 0 else "Unknown"
    
    # Generate slide 12
    print(f"\n🔄 Generating Slide 12 for brand: {main_brand}")
    
    week1_start = latest_date - timedelta(days=6)
    week1_display = f"{week1_start.strftime('%d/%m/%Y')} → {latest_date.strftime('%d/%m/%Y')}"
    
    result = generate_slide12_data_only(
        week1_df=week1_df,
        week2_df=week2_df,
        brand=main_brand,
        week1_display=week1_display
    )
    
    print("\n✅ Slide 12 generated successfully!")
    print("\n📋 Results:")
    print(f"   Title: {result['title']}")
    print(f"   Subtitle: {result['subtitle']}")
    
    print(f"\n📊 Donut Charts:")
    week_before_data = result['donut_charts']['week_before']['data']
    current_week_data = result['donut_charts']['current_week']['data']
    
    print(f"   Week Before ({len(week_before_data)} brands):")
    for item in sorted(week_before_data, key=lambda x: x['mentions'], reverse=True)[:5]:
        print(f"     - {item['brand']}: {item['mentions']} mentions")
    
    print(f"   Current Week ({len(current_week_data)} brands):")
    for item in sorted(current_week_data, key=lambda x: x['mentions'], reverse=True)[:5]:
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
    with open('slide12_test_results.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    print("💾 Results saved to slide12_test_results.json")

if __name__ == "__main__":
    test_slide12_generator()