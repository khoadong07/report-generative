#!/usr/bin/env python3
"""
Convert report_output.json format to template-compatible format
"""

import json
import sys


def convert_kpi_data(slide1_data):
    """Convert slide 1 data to KPI cards format"""
    kpi_cards = []
    
    for item in slide1_data:
        # Format value with commas
        value = f"{item['today']:,}"
        
        # Format change percentage
        change_pct = item['change_pct']
        change_sign = "+" if change_pct >= 0 else ""
        change = f"{change_sign}{change_pct}%"
        
        kpi_cards.append({
            "label": item['label'],
            "value": value,
            "change": change,
            "change_positive": change_pct >= 0
        })
    
    return kpi_cards


def convert_report_format(input_file, output_file):
    """Convert report format to template-compatible format"""
    
    print(f"Loading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    print("Converting format...")
    
    # Extract metadata
    metadata = report.get('report_metadata', {})
    brand = metadata.get('brand', 'Brand')
    
    # Convert Slide 1
    slide1 = report.get('slide_1', {})
    converted_slide1 = {
        "title": slide1.get('title', ''),
        "subtitle": slide1.get('subtitle', ''),
        "kpi_cards": convert_kpi_data(slide1.get('data', [])),
        "insight": {
            "title": "INSIGHT CHÍNH",
            "content": slide1.get('insight', '')
        }
    }
    
    # Convert Slide 2
    slide2 = report.get('slide_2', {})
    trendline_data = slide2.get('trendline', [])
    
    # Format dates for labels
    labels = []
    data_values = []
    for item in trendline_data:
        date_str = item['date']
        # Convert YYYY-MM-DD to DD/MM
        parts = date_str.split('-')
        if len(parts) == 3:
            labels.append(f"{parts[2]}/{parts[1]}")
        else:
            labels.append(date_str)
        data_values.append(item['buzz'])
    
    converted_slide2 = {
        "title": slide2.get('title', ''),
        "subtitle": slide2.get('subtitle', ''),
        "chart": {
            "title": "Biểu đồ biểu diễn xu hướng thảo luận / Buzz Trendline",
            "labels": labels,
            "dataset": {
                "label": "Buzz (Lượt thảo luận)",
                "data": data_values
            }
        },
        "insight": {
            "title": "PHÂN TÍCH XU HƯỚNG",
            "content": slide2.get('insight', '')
        }
    }
    
    # Convert Slide 3
    slide3 = report.get('slide_3', {})
    channel_dist = slide3.get('channel_distribution', [])
    
    labels = []
    data_values = []
    colors = {
        'Facebook': '#1877f2',
        'TikTok': '#000000',
        'YouTube': '#ff0000',
        'News': '#f59e0b',
        'Threads': '#6b7280',
        'Instagram': '#e4405f',
        'Twitter': '#1da1f2'
    }
    chart_colors = []
    
    for item in channel_dist:
        channel = item.get('Channel', 'Unknown')
        labels.append(channel)
        data_values.append(int(item.get('today_buzz', 0)))
        chart_colors.append(colors.get(channel, '#6b7280'))
    
    converted_slide3 = {
        "title": slide3.get('title', ''),
        "subtitle": slide3.get('subtitle', ''),
        "chart": {
            "title": "Biểu đồ phân bổ thảo luận theo Kênh",
            "labels": labels,
            "data": data_values,
            "colors": chart_colors
        },
        "insight": {
            "title": f"Insight cho Slide Channel Breakdown - {brand}",
            "content": slide3.get('insight', '')
        }
    }
    
    # Convert Slide 4
    slide4 = report.get('slide_4', {})
    sentiment_dist = slide4.get('sentiment_distribution', [])
    attribute_sentiment = slide4.get('attribute_sentiment', [])
    
    # Sentiment pie chart
    pie_labels = []
    pie_data = []
    for item in sentiment_dist:
        sentiment = item.get('Sentiment', 'Unknown')
        count = item.get('Count', 0)
        pie_labels.append(sentiment)
        pie_data.append(count)
    
    # Attribute bar chart
    bar_labels = []
    negative_data = []
    neutral_data = []
    positive_data = []
    
    for item in attribute_sentiment:
        label = item.get('Label_List', 'Unknown')
        bar_labels.append(label)
        negative_data.append(int(item.get('Negative', 0)))
        neutral_data.append(int(item.get('Neutral', 0)))
        positive_data.append(int(item.get('Positive', 0)))
    
    converted_slide4 = {
        "title": slide4.get('title', ''),
        "subtitle": slide4.get('subtitle', ''),
        "pie_chart": {
            "title": "Phân bổ Sentiment",
            "labels": pie_labels,
            "data": pie_data
        },
        "bar_chart": {
            "title": "Sentiment theo Thuộc tính Thương hiệu",
            "labels": bar_labels,
            "datasets": {
                "negative": negative_data,
                "neutral": neutral_data,
                "positive": positive_data
            }
        },
        "insight": {
            "title": "PHÂN TÍCH SENTIMENT",
            "content": slide4.get('insight', '')
        }
    }
    
    # Build final structure
    converted = {
        "report_title": f"Báo cáo Phân tích Thương hiệu {brand}",
        "slide1": converted_slide1,
        "slide2": converted_slide2,
        "slide3": converted_slide3,
        "slide4": converted_slide4
    }
    
    print(f"Saving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(converted, f, ensure_ascii=False, indent=2)
    
    print("✅ Conversion completed!")
    return converted


def main():
    """Main function"""
    input_file = 'report_output.json'
    output_file = 'report_converted.json'
    
    try:
        convert_report_format(input_file, output_file)
        print(f"\n📄 Converted file: {output_file}")
        print("📌 Next step:")
        print("   python render_html.py")
    except FileNotFoundError:
        print(f"❌ Error: {input_file} not found")
        print("   Run generate_report.py first")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
