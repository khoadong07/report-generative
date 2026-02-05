#!/usr/bin/env python3
"""
Script to generate complete prompt for slide platforms (Manuss, Gamma, etc.)
Input: Excel file, brand name, dates
Output: Complete prompt with JSON data embedded
"""

import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import re

# Load environment
load_dotenv()

# Import existing modules
try:
    from report_generator import ReportGenerator
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from report_generator import ReportGenerator


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


def extract_urls_from_text(text):
    """Extract URLs from text and return list of (url, text_snippet) tuples"""
    # Pattern to match URLs
    url_pattern = r'https?://[^\s\)\]\}]+'
    urls = re.findall(url_pattern, text)
    return urls


def convert_insight_to_hyperlink_format(insight_text):
    """
    Convert insight text with URLs to hyperlink format for slide platforms
    Example: "Check this link: https://example.com for details"
    Becomes: "Check this link: [URL](https://example.com) for details"
    """
    if not insight_text:
        return insight_text
    
    # Find all URLs in the text
    url_pattern = r'(https?://[^\s\)\]\}]+)'
    
    # Replace URLs with hyperlink format
    def replace_url(match):
        url = match.group(1)
        return f'[URL]({url})'
    
    formatted_text = re.sub(url_pattern, replace_url, insight_text)
    return formatted_text


def extract_hyperlinks_from_insight(insight_text):
    """
    Extract all hyperlinks from insight text
    Returns list of dicts with 'text' and 'url'
    """
    if not insight_text:
        return []
    
    url_pattern = r'https?://[^\s\)\]\}]+'
    urls = re.findall(url_pattern, insight_text)
    
    hyperlinks = []
    for url in urls:
        hyperlinks.append({
            'text': 'URL',
            'url': url
        })
    
    return hyperlinks


def generate_slide1_data(slide_data):
    """Generate formatted data for Slide 1"""
    kpis = []
    for item in slide_data['data']:
        kpis.append(
            f"{item['label']}: {format_number(item['today'])} "
            f"({format_percentage(item['change_pct'])})"
        )
    
    # Convert insight with hyperlinks
    insight = convert_insight_to_hyperlink_format(slide_data['insight'])
    hyperlinks = extract_hyperlinks_from_insight(slide_data['insight'])
    
    return {
        'title': slide_data['title'],
        'subtitle': slide_data['subtitle'],
        'kpis': kpis,
        'insight': insight,
        'hyperlinks': hyperlinks
    }


def generate_slide2_data(slide_data):
    """Generate formatted data for Slide 2"""
    trendline = []
    for point in slide_data['trendline']:
        date_formatted = format_date(point['date'])
        trendline.append(f"{date_formatted}: {format_number(point['buzz'])}")
    
    peak_date = format_date(slide_data['peak_day']['date'])
    current_date = format_date(slide_data['current_day']['date'])
    
    # Convert insight with hyperlinks
    insight = convert_insight_to_hyperlink_format(slide_data['insight'])
    hyperlinks = extract_hyperlinks_from_insight(slide_data['insight'])
    
    return {
        'title': slide_data['title'],
        'subtitle': slide_data['subtitle'],
        'trendline': trendline,
        'peak_day': f"{peak_date} - {format_number(slide_data['peak_day']['buzz'])} lượt",
        'current_status': f"{current_date} - {'Vẫn đang HOT 🔥' if slide_data['current_day']['is_still_hot'] else 'Đã hạ nhiệt ❄️'}",
        'insight': insight,
        'hyperlinks': hyperlinks
    }


def generate_slide3_data(slide_data):
    """Generate formatted data for Slide 3"""
    channels = []
    for item in slide_data['channel_distribution']:
        channels.append(
            f"{item['Channel']}: {format_number(int(item['today_buzz']))} "
            f"({format_percentage(item['change_pct'])})"
        )
    
    # Convert insight with hyperlinks
    insight = convert_insight_to_hyperlink_format(slide_data['insight'])
    hyperlinks = extract_hyperlinks_from_insight(slide_data['insight'])
    
    return {
        'title': slide_data['title'],
        'subtitle': slide_data['subtitle'],
        'channels': channels,
        'top_channel': slide_data['top_channel'],
        'insight': insight,
        'hyperlinks': hyperlinks
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
    
    # Convert insight with hyperlinks
    insight = convert_insight_to_hyperlink_format(slide_data['insight'])
    hyperlinks = extract_hyperlinks_from_insight(slide_data['insight'])
    
    return {
        'title': slide_data['title'],
        'subtitle': slide_data['subtitle'],
        'sentiment': sentiment,
        'attributes': attributes,
        'insight': insight,
        'hyperlinks': hyperlinks
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
        description='Generate slide prompt from Excel data'
    )
    parser.add_argument(
        '--excel',
        type=str,
        required=True,
        help='Path to Excel file'
    )
    parser.add_argument(
        '--brand',
        type=str,
        required=True,
        help='Brand name'
    )
    parser.add_argument(
        '--report-date',
        type=str,
        required=True,
        help='Report date (YYYY-MM-DD)'
    )
    parser.add_argument(
        '--compare-date',
        type=str,
        required=True,
        help='Compare date (YYYY-MM-DD)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='slide_prompt.txt',
        help='Output file for prompt (default: slide_prompt.txt)'
    )
    parser.add_argument(
        '--json-output',
        type=str,
        default='report_data.json',
        help='Output file for JSON data (default: report_data.json)'
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("📊 SLIDE PROMPT GENERATOR")
    print("="*60)
    
    # Validate inputs
    print("\n[Step 1/5] Validating inputs...")
    excel_path = Path(args.excel)
    if not excel_path.exists():
        print(f"❌ Excel file not found: {args.excel}")
        return 1
    
    try:
        datetime.strptime(args.report_date, "%Y-%m-%d")
        datetime.strptime(args.compare_date, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD")
        return 1
    
    print(f"   ✅ Excel: {args.excel}")
    print(f"   ✅ Brand: {args.brand}")
    print(f"   ✅ Report Date: {args.report_date}")
    print(f"   ✅ Compare Date: {args.compare_date}")
    
    # Check API credentials
    print("\n[Step 2/5] Checking API credentials...")
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL")
    
    if not api_key or not base_url:
        print("❌ API credentials not found in .env file")
        return 1
    
    print(f"   ✅ API_KEY: {api_key[:10]}...")
    print(f"   ✅ BASE_URL: {base_url}")
    
    # Update config.py with parameters
    print("\n[Step 3/5] Updating configuration...")
    try:
        # Read current config
        config_path = Path(__file__).parent / 'config.py'
        with open(config_path, 'r', encoding='utf-8') as f:
            config_content = f.read()
        
        # Update values
        import re
        config_content = re.sub(
            r'FILE_PATH\s*=\s*["\'].*?["\']',
            f'FILE_PATH = "{excel_path.name}"',
            config_content
        )
        config_content = re.sub(
            r'BRAND_NAME\s*=\s*["\'].*?["\']',
            f'BRAND_NAME = "{args.brand}"',
            config_content
        )
        config_content = re.sub(
            r'REPORT_DATE\s*=\s*["\'].*?["\']',
            f'REPORT_DATE = "{args.report_date}"',
            config_content
        )
        config_content = re.sub(
            r'COMPARE_DATE\s*=\s*["\'].*?["\']',
            f'COMPARE_DATE = "{args.compare_date}"',
            config_content
        )
        
        # Write back
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print(f"   ✅ Config updated")
        
    except Exception as e:
        print(f"   ⚠️  Warning: Could not update config.py: {e}")
        print("   Continuing with existing config...")
    
    # Generate report
    print("\n[Step 4/5] Generating report data...")
    print("   🚀 Parallel processing: ~1 minute (4 slides simultaneously)")
    print("   ☕ Please wait...\n")
    
    try:
        generator = ReportGenerator(
            api_key=api_key,
            base_url=base_url
        )
        
        report_data = generator.generate_report()
        
        print("\n   ✅ Report data generated successfully")
        
    except Exception as e:
        print(f"\n❌ Error generating report: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Save JSON data
    print(f"\n[Step 5/6] Saving JSON data to {args.json_output}...")
    try:
        with open(args.json_output, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        print(f"   ✅ JSON saved: {args.json_output}")
    except Exception as e:
        print(f"   ❌ Error saving JSON: {e}")
        return 1
    
    # Generate prompt
    print(f"\n[Step 6/6] Generating slide prompt...")
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
    print("\n" + "="*60)
    print("✅ SUCCESS!")
    print("="*60)
    print(f"📄 JSON Data: {args.json_output}")
    print(f"📝 Slide Prompt: {args.output}")
    print(f"📊 Brand: {args.brand}")
    print(f"📅 Report Date: {args.report_date}")
    print("\n📌 Next steps:")
    print(f"   1. Open {args.output}")
    print("   2. Copy the entire content")
    print("   3. Paste into Manuss/Gamma/Beautiful.ai")
    print("   4. Click 'Generate' and wait 30-60 seconds")
    print("="*60)
    
    return 0


if __name__ == "__main__":
    exit(main())
