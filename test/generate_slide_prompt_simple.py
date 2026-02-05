#!/usr/bin/env python3
"""
Simple script to generate complete prompt for slide platforms
Input: report_output.json (already generated)
Output: Complete prompt with JSON data embedded
"""

import json
import argparse
import re
from pathlib import Path
from datetime import datetime


def format_number(num):
    """Format number with commas"""
    if isinstance(num, (int, float)):
        return f"{int(num):,}"
    return str(num)


def format_percentage(pct):
    """Format percentage with sign"""
    if pct > 0:
        return f"+{pct:.2f}%"
    return f"{pct:.2f}%"


def format_date(date_str):
    """Format date to DD/MM/YYYY"""
    if isinstance(date_str, str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        date_obj = date_str
    return date_obj.strftime("%d/%m/%Y")


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


def generate_slide1_data(slide_data):
    """Generate formatted data for Slide 1"""
    kpis = []
    for item in slide_data['data']:
        kpis.append(
            f"{item['label']}: {format_number(item['today'])} "
            f"({format_percentage(item['change_pct'])})"
        )
    
    # Format insight with hyperlinks
    insight = format_insight_with_hyperlinks(slide_data['insight'])
    
    return {
        'title': slide_data['title'],
        'subtitle': slide_data['subtitle'],
        'kpis': kpis,
        'insight': insight
    }


def generate_slide2_data(slide_data):
    """Generate formatted data for Slide 2"""
    trendline = []
    for point in slide_data['trendline']:
        date_formatted = format_date(point['date'])
        trendline.append(f"{date_formatted}: {format_number(point['buzz'])}")
    
    peak_date = format_date(slide_data['peak_day']['date'])
    current_date = format_date(slide_data['current_day']['date'])
    
    # Format insight with hyperlinks
    insight = format_insight_with_hyperlinks(slide_data['insight'])
    
    return {
        'title': slide_data['title'],
        'subtitle': slide_data['subtitle'],
        'trendline': trendline,
        'peak_day': f"{peak_date} - {format_number(slide_data['peak_day']['buzz'])} lượt",
        'current_status': f"{current_date} - {'Vẫn đang HOT 🔥' if slide_data['current_day']['is_still_hot'] else 'Đã hạ nhiệt ❄️'}",
        'insight': insight
    }


def generate_slide3_data(slide_data):
    """Generate formatted data for Slide 3"""
    channels = []
    for item in slide_data['channel_distribution']:
        channels.append(
            f"{item['Channel']}: {format_number(int(item['today_buzz']))} "
            f"({format_percentage(item['change_pct'])})"
        )
    
    # Format insight with hyperlinks
    insight = format_insight_with_hyperlinks(slide_data['insight'])
    
    return {
        'title': slide_data['title'],
        'subtitle': slide_data['subtitle'],
        'channels': channels,
        'top_channel': slide_data['top_channel'],
        'insight': insight
    }


def generate_slide4_data(slide_data):
    """Generate formatted data for Slide 4"""
    sentiment = []
    for item in slide_data['sentiment_distribution']:
        sentiment.append(
            f"{item['Sentiment']}: {format_number(item['Count'])}"
        )
    
    attributes = []
    for item in slide_data['attribute_sentiment']:
        attr_name = item['Label_List']
        neg = int(item.get('Negative', 0))
        neu = int(item.get('Neutral', 0))
        pos = int(item.get('Positive', 0))
        attributes.append(
            f"{attr_name}: Neg {neg}, Neu {neu}, Pos {pos}"
        )
    
    # Format insight with hyperlinks
    insight = format_insight_with_hyperlinks(slide_data['insight'])
    
    return {
        'title': slide_data['title'],
        'subtitle': slide_data['subtitle'],
        'sentiment': sentiment,
        'attributes': attributes,
        'insight': insight
    }


def generate_complete_prompt(report_data):
    """Generate complete prompt with all data embedded"""
    
    # Extract metadata
    metadata = report_data['report_metadata']
    brand = metadata['brand']
    report_date = format_date(metadata['report_date'])
    compare_date = format_date(metadata['compare_date'])
    
    # Generate data for each slide
    slide1 = generate_slide1_data(report_data['slide_1'])
    slide2 = generate_slide2_data(report_data['slide_2'])
    slide3 = generate_slide3_data(report_data['slide_3'])
    slide4 = generate_slide4_data(report_data['slide_4'])
    
    # Build complete prompt
    prompt = f"""Create a professional 4-slide presentation for Brand Health Analysis with the following specifications:

═══════════════════════════════════════════════════════════════
BRAND: {brand}
REPORT DATE: {report_date}
COMPARE DATE: {compare_date}
═══════════════════════════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 1 - BRAND OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYOUT:
- Title: "{slide1['title']}"
- Subtitle: "{slide1['subtitle']}"
- 7 KPI cards in grid layout (4 top row, 3 bottom row)
- Each card shows: metric name, large number, percentage change with arrow
- Bottom section: Insight box with light blue background

KPI DATA:
"""
    
    for i, kpi in enumerate(slide1['kpis'], 1):
        prompt += f"{i}. {kpi}\n"
    
    prompt += f"""
INSIGHT:
{slide1['insight']}

DESIGN:
- Style: Corporate, clean, data-focused
- Colors: Green for positive changes, Red for negative changes
- Font: Modern sans-serif, 32px title, 14px body
- Background: White with light blue insight box

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 2 - TRENDLINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYOUT:
- Title: "{slide2['title']}"
- Subtitle: "{slide2['subtitle']}"
- Line chart showing 7-day trend
- Highlight boxes for peak day and current status
- Bottom section: Trend analysis insight

TRENDLINE DATA:
"""
    
    for point in slide2['trendline']:
        prompt += f"- {point}\n"
    
    prompt += f"""
PEAK DAY: {slide2['peak_day']}
CURRENT STATUS: {slide2['current_status']}

INSIGHT:
{slide2['insight']}

CHART DESIGN:
- Type: Line chart with markers
- Line color: Blue (#1e40af), width 3px
- Peak marker: Red circle, larger size
- Grid: Light gray, dashed
- Background: White

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 3 - CHANNEL BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYOUT:
- Title: "{slide3['title']}"
- Subtitle: "{slide3['subtitle']}"
- Horizontal bar chart
- Highlight box for top channel
- Bottom section: Channel analysis insight

CHANNEL DATA:
"""
    
    for channel in slide3['channels']:
        prompt += f"- {channel}\n"
    
    prompt += f"""
TOP CHANNEL: {slide3['top_channel']} 🏆

INSIGHT:
{slide3['insight']}

CHART DESIGN:
- Type: Horizontal bar chart
- Bar colors:
  * Facebook: #1877f2 (Facebook blue)
  * TikTok: #000000 (Black)
  * YouTube: #ff0000 (Red)
  * News: #f59e0b (Orange)
  * Others: #6b7280 (Gray)
- Show values and percentage changes on bars
- Sort by value (descending)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 4 - SENTIMENT & BRAND ATTRIBUTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYOUT:
- Title: "{slide4['title']}"
- Subtitle: "{slide4['subtitle']}"
- Two-column layout:
  * Left (40%): Pie chart (Sentiment distribution)
  * Right (60%): Stacked bar chart (Sentiment by Attribute)
- Bottom section: Sentiment analysis insight (full width)

SENTIMENT DISTRIBUTION:
"""
    
    for sent in slide4['sentiment']:
        prompt += f"- {sent}\n"
    
    prompt += f"""
BRAND ATTRIBUTES (with Sentiment breakdown):
"""
    
    for attr in slide4['attributes']:
        prompt += f"- {attr}\n"
    
    prompt += f"""
INSIGHT:
{slide4['insight']}

CHART DESIGN:
LEFT - Pie Chart (Donut style):
- Segments:
  * Neutral: Gray (#6b7280)
  * Negative: Red (#dc2626)
  * Positive: Green (#16a34a)
- Show percentages on segments
- Legend at bottom

RIGHT - Stacked Bar Chart (Horizontal):
- Y-axis: Top 6 brand attributes
- X-axis: Count
- Stack colors:
  * Negative: Red (#dc2626)
  * Neutral: Gray (#6b7280)
  * Positive: Green (#16a34a)
- Legend at top right
- Show values on hover

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OVERALL DESIGN THEME
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COLOR PALETTE:
- Primary Blue: #1e40af
- Secondary Gray: #6b7280
- Success Green: #16a34a
- Danger Red: #dc2626
- Warning Yellow: #f59e0b
- Background: #ffffff
- Light Background: #f9fafb

TYPOGRAPHY:
- Slide Title: 32px, Bold
- Section Title: 24px, Bold
- Body Text: 14px, Regular
- Small Text: 12px, Regular
- Line Height: 1.6
- Font Family: Modern sans-serif (Inter, Roboto, or similar)

SPACING:
- Slide Padding: 48px
- Section Margin: 32px
- Element Spacing: 16px
- Card Padding: 24px

STYLE:
- Corporate and professional
- Clean and modern
- Data-driven and analytical
- High contrast for readability
- Consistent spacing and alignment

═══════════════════════════════════════════════════════════════
END OF PROMPT
═══════════════════════════════════════════════════════════════

INSTRUCTIONS:
1. Create all 4 slides with the exact data provided above
2. Follow the design specifications precisely
3. Ensure all charts are properly formatted and labeled
4. Make insights readable with proper formatting
5. Use the specified color palette consistently
6. Ensure the presentation is professional and polished
"""
    
    return prompt


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Generate slide prompt from report JSON'
    )
    parser.add_argument(
        '--json',
        type=str,
        default='report_output.json',
        help='Path to report JSON file (default: report_output.json)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='slide_prompt.txt',
        help='Output file for prompt (default: slide_prompt.txt)'
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("📊 SLIDE PROMPT GENERATOR (Simple)")
    print("="*60)
    
    # Load JSON
    print(f"\n[Step 1/2] Loading report data from {args.json}...")
    json_path = Path(args.json)
    if not json_path.exists():
        print(f"❌ JSON file not found: {args.json}")
        print("\n💡 Tip: Run generate_report.py first to create report_output.json")
        return 1
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            report_data = json.load(f)
        print(f"   ✅ JSON loaded successfully")
    except Exception as e:
        print(f"   ❌ Error loading JSON: {e}")
        return 1
    
    # Generate prompt
    print(f"\n[Step 2/2] Generating slide prompt...")
    try:
        prompt = generate_complete_prompt(report_data)
        
        # Save prompt
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print(f"   ✅ Prompt saved: {args.output}")
        
    except Exception as e:
        print(f"   ❌ Error generating prompt: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Summary
    metadata = report_data['report_metadata']
    print("\n" + "="*60)
    print("✅ SUCCESS!")
    print("="*60)
    print(f"📝 Slide Prompt: {args.output}")
    print(f"📊 Brand: {metadata['brand']}")
    print(f"📅 Report Date: {metadata['report_date']}")
    print(f"📅 Compare Date: {metadata['compare_date']}")
    print("\n📌 Next steps:")
    print(f"   1. Open {args.output}")
    print("   2. Copy the entire content")
    print("   3. Paste into Manuss/Gamma/Beautiful.ai")
    print("   4. Click 'Generate' and wait 30-60 seconds")
    print("="*60)
    
    return 0


if __name__ == "__main__":
    exit(main())
