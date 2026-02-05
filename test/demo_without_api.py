#!/usr/bin/env python3
"""
Demo script that works WITHOUT API credentials
Just renders HTML from sample data
"""

import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def demo_render_html():
    """Demo: Render HTML from sample data"""
    print("\n" + "="*60)
    print("DEMO: HTML RENDERING (No API Required)")
    print("="*60 + "\n")
    
    try:
        from test.template_renderer import TemplateRenderer
        
        print("Step 1: Loading sample data...")
        with open('test/sample_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✅ Sample data loaded")
        
        print("\nStep 2: Initializing renderer...")
        renderer = TemplateRenderer('test/template_parameterized.html')
        print("✅ Renderer initialized")
        
        print("\nStep 3: Rendering HTML...")
        renderer.render_to_file(data, 'test/demo_report.html')
        print("✅ HTML rendered successfully!")
        
        print("\n" + "="*60)
        print("SUCCESS!")
        print("="*60)
        print("\nGenerated file: test/demo_report.html")
        print("\nTo view:")
        print("  - Open test/demo_report.html in your browser")
        print("  - Or run: open test/demo_report.html (macOS)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def show_sample_data_structure():
    """Show the structure of sample data"""
    print("\n" + "="*60)
    print("SAMPLE DATA STRUCTURE")
    print("="*60 + "\n")
    
    try:
        with open('test/sample_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("Report contains:")
        print(f"  - Report Title: {data.get('report_title', 'N/A')}")
        print(f"  - Slide 1: {data.get('slide1', {}).get('title', 'N/A')}")
        print(f"  - Slide 2: {data.get('slide2', {}).get('title', 'N/A')}")
        print(f"  - Slide 3: {data.get('slide3', {}).get('title', 'N/A')}")
        print(f"  - Slide 4: {data.get('slide4', {}).get('title', 'N/A')}")
        
        if 'slide1' in data and 'kpi_cards' in data['slide1']:
            print(f"\nSlide 1 has {len(data['slide1']['kpi_cards'])} KPI cards:")
            for card in data['slide1']['kpi_cards']:
                print(f"  - {card['label']}: {card['value']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def create_custom_sample():
    """Create a custom sample with your own data"""
    print("\n" + "="*60)
    print("CREATE CUSTOM SAMPLE")
    print("="*60 + "\n")
    
    custom_data = {
        "report_title": "My Custom Report",
        "slide1": {
            "title": "Custom Overview",
            "subtitle": "Demo Date Range",
            "kpi_cards": [
                {
                    "label": "Total Discussions",
                    "value": "1,000",
                    "change": "+50%",
                    "change_positive": True
                },
                {
                    "label": "Total Posts",
                    "value": "500",
                    "change": "+25%",
                    "change_positive": True
                },
                {
                    "label": "Engagement",
                    "value": "10,000",
                    "change": "-10%",
                    "change_positive": False
                }
            ],
            "insight": {
                "title": "KEY INSIGHTS",
                "content": "This is a demo report showing how the system works. You can customize all the data in the JSON file."
            }
        },
        "slide2": {
            "title": "Trend Analysis",
            "subtitle": "Last 7 Days",
            "chart": {
                "title": "Discussion Trend",
                "labels": ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"],
                "dataset": {
                    "label": "Discussions",
                    "data": [100, 150, 200, 180, 250]
                }
            },
            "insight": {
                "title": "TREND ANALYSIS",
                "content": "The trend shows increasing discussions over the period."
            }
        },
        "slide3": {
            "title": "Channel Breakdown",
            "subtitle": "By Platform",
            "chart": {
                "title": "Distribution by Channel",
                "labels": ["Facebook", "Twitter", "Instagram"],
                "data": [500, 300, 200],
                "colors": ["#1877f2", "#1da1f2", "#e4405f"]
            },
            "insight": {
                "title": "CHANNEL INSIGHTS",
                "content": "Facebook is the dominant channel for discussions."
            }
        },
        "slide4": {
            "title": "Sentiment Analysis",
            "subtitle": "Overall Sentiment",
            "pie_chart": {
                "title": "Sentiment Distribution",
                "labels": ["Neutral", "Negative", "Positive"],
                "data": [500, 300, 200]
            },
            "bar_chart": {
                "title": "Sentiment by Attribute",
                "labels": ["Quality", "Price", "Service"],
                "datasets": {
                    "negative": [100, 50, 30],
                    "neutral": [200, 150, 100],
                    "positive": [50, 30, 20]
                }
            },
            "insight": {
                "title": "SENTIMENT INSIGHTS",
                "content": "Overall sentiment is mostly neutral with some negative feedback on quality."
            }
        }
    }
    
    # Save custom sample
    output_path = 'test/custom_sample.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(custom_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Custom sample created: {output_path}")
    print("\nYou can now:")
    print("  1. Edit test/custom_sample.json with your data")
    print("  2. Render it with template_renderer.py")
    
    return True


def main():
    """Main demo function"""
    print("\n" + "="*60)
    print("DEMO MODE - No API Required")
    print("="*60)
    
    while True:
        print("\nChoose an option:")
        print("  1. Render HTML from sample data")
        print("  2. Show sample data structure")
        print("  3. Create custom sample template")
        print("  4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            demo_render_html()
        elif choice == "2":
            show_sample_data_structure()
        elif choice == "3":
            create_custom_sample()
        elif choice == "4":
            print("\nGoodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
