#!/usr/bin/env python3
"""
Script to generate complete prompt for weekly slide platforms
Input: Excel file, brand name, week dates
Output: Complete prompt with JSON data embedded (12 slides)
"""

import json
from datetime import datetime
import pandas as pd


def format_number(num):
    """Format number with commas"""
    if isinstance(num, (int, float)):
        return f"{int(num):,}"
    return str(num)


def format_date(date_str):
    """Format date to DD/MM/YYYY"""
    if isinstance(date_str, str):
        formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y"]
        for fmt in formats:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime("%d/%m/%Y")
            except ValueError:
                continue
        try:
            date_obj = pd.to_datetime(date_str)
            return date_obj.strftime("%d/%m/%Y")
        except:
            return str(date_str)
    else:
        return date_str.strftime("%d/%m/%Y")


def generate_complete_prompt(report_data):
    """Generate complete prompt with all 10 slides embedded"""
    
    metadata = report_data['report_metadata']
    brand = metadata['brand']
    week1_period = metadata['week1_period']
    
    # Check if interactions should be shown
    show_interactions = report_data['slide_1'].get('show_interactions', True)
    
    # Determine layout based on show_interactions
    if show_interactions:
        layout_desc = """- 2-COLUMN LAYOUT:
  LEFT COLUMN (50% width):
    • Column chart comparing 4 weeks (show absolute values on columns + growth % vs previous week)
  RIGHT COLUMN (50% width):
    • Grid of 6 KPI cards (2 rows × 3 columns)
    • Each card shows: metric name, value, % change vs previous week
  BOTTOM (Full width):
    • Insight box"""
    else:
        layout_desc = """- 2-COLUMN LAYOUT:
  LEFT COLUMN (50% width):
    • Column chart comparing 4 weeks (show absolute values on columns + growth % vs previous week)
  RIGHT COLUMN (50% width):
    • Single large KPI card for "Tổng đề cập" (prominent display with % change vs previous week)
  BOTTOM (Full width):
    • Insight box"""
    
    prompt = f"""Create a professional 10-slide presentation for Weekly Brand Health Analysis:

═══════════════════════════════════════════════════════════════
BRAND: {brand}
REPORT PERIOD: {week1_period} (7 days)
REPORT TYPE: Weekly Analysis
═══════════════════════════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 1 - TỔNG QUAN VỀ BRAND
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYOUT STRUCTURE:
- Title: "{report_data['slide_1']['title']}"
- Subtitle: "{report_data['slide_1']['subtitle']}"
{layout_desc}

CURRENT WEEK METRICS:
"""
    
    for metric in report_data['slide_1']['current_week_metrics']:
        if 'change_percent' in metric:
            change_sign = "+" if metric['change_percent'] > 0 else ""
            prompt += f"- {metric['label']}: {format_number(metric['value'])} ({change_sign}{metric['change_percent']}% so với tuần trước)\n"
        else:
            prompt += f"- {metric['label']}: {format_number(metric['value'])}\n"
    
    if not show_interactions:
        prompt += f"""
NOTE: Only "Tổng đề cập" metric is displayed. Interaction metrics (Views, Reactions, Shares, Comments) are hidden as per user preference.
"""
    
    prompt += f"""
WEEKLY COMPARISON (Column Chart - với giá trị absolute và % tăng trưởng):
"""
    for week in report_data['slide_1']['weekly_comparison']:
        if week['growth_rate'] is not None:
            growth_sign = "+" if week['growth_rate'] > 0 else ""
            prompt += f"- {week['week']}: {format_number(week['total_mentions'])} lượt ({growth_sign}{week['growth_rate']}% so với tuần trước đó)\n"
        else:
            prompt += f"- {week['week']}: {format_number(week['total_mentions'])} lượt\n"
    
    prompt += f"""
INSIGHT:
{report_data['slide_1']['insight']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 2 - ĐƯỜNG BIỂU DIỄN XU HƯỚNG ĐỀ CẬP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYOUT STRUCTURE:
- Title: "{report_data['slide_2']['title']}"
- Subtitle: "{report_data['slide_2']['subtitle']}"
- 1-COLUMN LAYOUT:
  TOP (Full width):
    • Line chart showing 7-day trend (X-axis: dates, Y-axis: mention count)
  BOTTOM (Full width):
    • Insight box

TRENDLINE DATA (7 days):
"""
    
    for point in report_data['slide_2']['trendline']:
        prompt += f"- {format_date(point['date'])}: {format_number(point['mentions'])} lượt\n"
    
    prompt += f"""
INSIGHT:
{report_data['slide_2']['insight']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 3 - PHÂN BỐ LƯỢT ĐỀ CẬP THEO KÊNH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYOUT STRUCTURE:
- Title: "{report_data['slide_3']['title']}"
- Subtitle: "{report_data['slide_3']['subtitle']}"
- 2-COLUMN LAYOUT:
  LEFT COLUMN (50% width):
    • Pie/Donut chart (channel distribution) - CLEAN, NO LABELS ON CHART
    • Legend list positioned BELOW or BESIDE the chart
      Format: [Color Block] [Channel Name]: [XX.X]%
  RIGHT COLUMN (50% width):
    • Horizontal bar chart showing top 10 sources (by SiteName)
  BOTTOM (Full width):
    • Insight box

PIE/DONUT CHART REQUIREMENTS (IMPORTANT):
- NO labels on the chart itself (clean chart without text)
- NO leader lines or connector lines
- NO percentages displayed on slices
- Use distinct, contrasting colors for each channel

LEGEND LIST:
- Display as a vertical list next to or below the pie chart
- Format for each item: [Color Block] [Channel Name]: [XX.X]%
- Example:
  ■ Facebook: 45.2%
  ■ YouTube: 30.5%
  ■ TikTok: 15.8%
  ■ Instagram: 8.5%
- Color blocks should match the slice colors in the chart
- Font size: Medium, readable
- Alignment: Left-aligned
- Spacing: Comfortable spacing between items

CHANNEL DISTRIBUTION DATA:
"""
    
    # Calculate total for percentage
    total_channel = sum(ch['count'] for ch in report_data['slide_3']['channel_distribution'])
    for ch in report_data['slide_3']['channel_distribution']:
        percentage = (ch['count'] / total_channel * 100) if total_channel > 0 else 0
        prompt += f"- {ch['Channel']}: {format_number(ch['count'])} lượt ({percentage:.1f}%)\n"
    
    prompt += f"""
TOP 10 SOURCES (Horizontal Bar Chart):
"""
    for src in report_data['slide_3']['top_sources']:
        prompt += f"- {src['SiteName']}: {format_number(src['count'])} lượt\n"
    
    prompt += f"""
INSIGHT:
{report_data['slide_3']['insight']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 4 - TOP NGUỒN CÓ LƯỢNG TƯƠNG TÁC CAO NHẤT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYOUT STRUCTURE:
- Title: "{report_data['slide_4']['title']}"
- Subtitle: "{report_data['slide_4']['subtitle']}"
- Full-width table
- NO insight section

TABLE COLUMN NAMES (IMPORTANT - Use exact names):
"""
    
    # Check if interactions are shown
    show_interactions_slide4 = report_data['slide_4'].get('show_interactions', True)
    
    if show_interactions_slide4:
        prompt += """
1. STT
2. Nguồn
3. Tổng tương tác
4. Reactions (NOT "React ions" or "Lượt reactions")
5. Shares (NOT "Share s" or "Lượt chia sẻ")
6. Comments (NOT "Co mm" or "Lượt bình luận")

TABLE DATA:
"""
        # Full table with interaction columns
        for row in report_data['slide_4']['table_rows']:
            prompt += f"""
Row {row['stt']}:
- STT: {row['stt']}
- Nguồn: {row['source_name']}
- Tổng tương tác: {format_number(row['total_engagement'])}
- Reactions: {format_number(row['reactions'])}
- Shares: {format_number(row['shares'])}
- Comments: {format_number(row['comments'])}
"""
    else:
        prompt += """
1. STT
2. Nguồn
3. Số lượng đề cập

TABLE DATA:
"""
        # Simple table without interaction columns
        for row in report_data['slide_4']['table_rows']:
            prompt += f"""
Row {row['stt']}:
- STT: {row['stt']}
- Nguồn: {row['source_name']}
- Số lượng đề cập: {format_number(row['count'])}
"""
    
    prompt += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 5 - TOP BÀI ĐĂNG CÓ TƯƠNG TÁC CAO NHẤT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYOUT STRUCTURE:
- Title: "{report_data['slide_5']['title']}"
- Subtitle: "{report_data['slide_5']['subtitle']}"
- Full-width table
- NO insight section

TABLE COLUMN NAMES (IMPORTANT - Use exact names):
"""
    
    # Check if interactions are shown
    show_interactions_slide5 = report_data['slide_5'].get('show_interactions', True)
    
    if show_interactions_slide5:
        prompt += """
1. STT
2. Nội dung
3. Ngày đăng
4. Kênh
5. Nguồn
6. Reactions (NOT "React ions" or "Lượt reactions")
7. Shares (NOT "Share s" or "Lượt chia sẻ")
8. Comments (NOT "Co mm" or "Lượt bình luận")

TABLE DATA:
"""
        # Full table with interaction columns
        for row in report_data['slide_5']['table_rows']:
            content_preview = row['content'][:100] + '...' if len(row['content']) > 100 else row['content']
            prompt += f"""
Row {row['stt']}:
- STT: {row['stt']}
- Nội dung: {content_preview} [Link]({row['url']})
- Ngày đăng: {format_date(row['published_date'])}
- Kênh: {row['channel']}
- Nguồn: {row['site_name']}
- Reactions: {format_number(row['reactions'])}
- Shares: {format_number(row['shares'])}
- Comments: {format_number(row['comments'])}
"""
    else:
        prompt += """
1. STT
2. Nội dung
3. Ngày đăng
4. Kênh
5. Nguồn
6. URL

TABLE DATA:
"""
        # Simple table without interaction columns
        for row in report_data['slide_5']['table_rows']:
            content_preview = row['content'][:100] + '...' if len(row['content']) > 100 else row['content']
            prompt += f"""
Row {row['stt']}:
- STT: {row['stt']}
- Nội dung: {content_preview} [Link]({row['url']})
- Ngày đăng: {format_date(row['published_date'])}
- Kênh: {row['channel']}
- Nguồn: {row['site_name']}
- URL: {row['url']}
"""
    
    prompt += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 6 - SẮC THÁI VÀ CỤM CHỦ ĐỀ ĐỀ CẬP NỔI BẬT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYOUT STRUCTURE:
- Title: "{report_data['slide_6']['title']}"
- Subtitle: "{report_data['slide_6']['subtitle']}"
- 2-COLUMN LAYOUT:
  LEFT COLUMN (50% width):
    • Two SMALL DONUT charts side-by-side horizontally (previous week | current week)
      - Left Donut: "Tuần trước" label above, NSR = {report_data['slide_6']['previous_nsr']}% in center
      - Right Donut: "Tuần này" label above, NSR = {report_data['slide_6']['current_nsr']}% in center
      - Between donuts: NSR growth rate = {report_data['slide_6']['nsr_growth']:+.2f}%
      - Each donut shows sentiment percentages with colors:
        * Positive: #00C055 (green)
        * Neutral: #6b7280 (gray)
        * Negative: #EC003F (red)
    • NSR explanation note directly below the two donuts (small, gray, italic)
      NSR (Net Sentiment Rate - Tỷ lệ sắc thái ròng) là chỉ số phản ánh mức độ quan tâm / hài lòng của thị trường theo thời gian. Dựa trên công thức tỷ lệ % giữa hiệu và tổng của Sắc thái Tích cực và Tiêu cực
  RIGHT COLUMN (50% width):
    • Stacked horizontal bar chart (top 10 topics with sentiment breakdown)
      - Each bar shows: Negative (red) | Neutral (gray) | Positive (green)
  BOTTOM (Full width):
    • Insight box

DONUT CHART SIZING:
- Make donuts SMALLER to fit side-by-side
- Each donut: approximately 150-180px diameter
- Gap between donuts: 20-30px
- Label above each donut: "Tuần trước" / "Tuần này"

PREVIOUS WEEK SENTIMENT (Left Donut - "Tuần trước"):
NSR (Tuần trước) = {report_data['slide_6']['previous_nsr']}%
"""
    
    # Calculate total for previous week percentage
    total_prev = sum(sent['count'] for sent in report_data['slide_6']['previous_sentiment'])
    for sent in report_data['slide_6']['previous_sentiment']:
        percentage = (sent['count'] / total_prev * 100) if total_prev > 0 else 0
        prompt += f"- {sent['sentiment']}: {format_number(sent['count'])} lượt ({percentage:.1f}%)\n"
    
    prompt += f"""
CURRENT WEEK SENTIMENT (Right Donut - "Tuần này"):
NSR (Tuần hiện tại) = {report_data['slide_6']['current_nsr']}%
"""
    # Calculate total for current week percentage
    total_curr = sum(sent['count'] for sent in report_data['slide_6']['current_sentiment'])
    for sent in report_data['slide_6']['current_sentiment']:
        percentage = (sent['count'] / total_curr * 100) if total_curr > 0 else 0
        prompt += f"- {sent['sentiment']}: {format_number(sent['count'])} lượt ({percentage:.1f}%)\n"
    
    nsr_growth_sign = "+" if report_data['slide_6']['nsr_growth'] > 0 else ""
    prompt += f"""
NSR GROWTH (Display between the two donut charts):
{nsr_growth_sign}{report_data['slide_6']['nsr_growth']:.2f}% (so với tuần trước)

NSR EXPLANATION NOTE STYLING:
- Position: Directly below the two donut charts (still in left column)
- Font size: Small (10-11px)
- Color: Gray (#6b7280)
- Style: Italic
- Alignment: Left-aligned or center-aligned
- Width: Full width of left column

TOP TOPICS WITH SENTIMENT (Horizontal Bar Chart):
"""
    for topic in report_data['slide_6']['top_topics_with_sentiment']:
        prompt += f"- {topic['topic']}: Total {format_number(topic['total'])} (Negative: {topic['negative']}, Neutral: {topic['neutral']}, Positive: {topic['positive']})\n"
    
    prompt += f"""
INSIGHT:
{report_data['slide_6']['insight']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 7 - CÁC CHỦ ĐỀ ĐỀ CẬP TÍCH CỰC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYOUT STRUCTURE:
- Title: "{report_data['slide_7']['title']}"
- Subtitle: "{report_data['slide_7']['subtitle']}"
- 1-COLUMN LAYOUT:
  TOP (Full width):
    • Horizontal bar chart showing top 10 positive topics
    • Color: Success Green (#00C055)
    • Sorted by count (descending)
  BOTTOM (Full width):
    • Insight box

POSITIVE TOPICS (Horizontal Bar Chart):
"""
    
    for topic in report_data['slide_7']['positive_topics']:
        prompt += f"- {topic['Labels1']}: {format_number(topic['count'])} lượt\n"
    
    prompt += f"""
INSIGHT:
{report_data['slide_7']['insight']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 8 - TOP CÁC BÀI ĐĂNG TÍCH CỰC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYOUT:
- Title: "{report_data['slide_8']['title']}"
- Subtitle: "{report_data['slide_8']['subtitle']}"
- Full-width table (sorted by positive comment count)
- NO insight section

TABLE DATA:
"""
    
    for row in report_data['slide_8']['table_rows']:
        content_preview = row['content'][:100] + '...' if len(row['content']) > 100 else row['content']
        prompt += f"""
Row {row['stt']}:
- STT: {row['stt']}
- Nội dung: {content_preview} [Link]({row['url']})
- Ngày đăng: {format_date(row['published_date'])}
- Kênh: {row['channel']}
- Nguồn: {row['site_name']}
- Positive Comments: {format_number(row['positive_comments'])}
"""
    
    prompt += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 9 - CÁC CHỦ ĐỀ ĐỀ CẬP TIÊU CỰC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYOUT STRUCTURE:
- Title: "{report_data['slide_9']['title']}"
- Subtitle: "{report_data['slide_9']['subtitle']}"
- 1-COLUMN LAYOUT:
  TOP (Full width):
    • Horizontal bar chart showing top 10 negative topics
    • Color: Danger Red (#EC003F)
    • Sorted by count (descending)
  BOTTOM (Full width):
    • Insight box

NEGATIVE TOPICS (Horizontal Bar Chart):
"""
    
    for topic in report_data['slide_9']['negative_topics']:
        prompt += f"- {topic['Labels1']}: {format_number(topic['count'])} lượt\n"
    
    prompt += f"""
INSIGHT:
{report_data['slide_9']['insight']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 10 - TOP CÁC BÀI ĐĂNG TIÊU CỰC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYOUT:
- Title: "{report_data['slide_10']['title']}"
- Subtitle: "{report_data['slide_10']['subtitle']}"
- Full-width table (sorted by negative comment count)
- NO insight section

TABLE DATA:
"""
    
    for row in report_data['slide_10']['table_rows']:
        content_preview = row['content'][:100] + '...' if len(row['content']) > 100 else row['content']
        prompt += f"""
Row {row['stt']}:
- STT: {row['stt']}
- Nội dung: {content_preview} [Link]({row['url']})
- Ngày đăng: {format_date(row['published_date'])}
- Kênh: {row['channel']}
- Nguồn: {row['site_name']}
- Negative Comments: {format_number(row['negative_comments'])}
"""
    
    prompt += f"""
═══════════════════════════════════════════════════════════════
OVERALL DESIGN THEME
═══════════════════════════════════════════════════════════════

COLOR PALETTE:
- Primary Blue: #0045C4
- Success Green: #00C055 (for positive)
- Danger Red: #EC003F (for negative)
- Neutral Gray: #6b7280
- Background: #FFFFFF

TYPOGRAPHY:
- Slide Title: 32px, Bold
- Section Title: 24px, Bold
- Body Text: 14px, Regular
- Font Family: Modern sans-serif (Inter, Roboto)

NUMBER FORMATTING:
- Thousands separator: Comma (,)
  Examples: 2,000 | 15,500 | 1,234,567
- Decimal separator: Period (.)
  Examples: 2.3% | 15.7% | 0.5%
- Percentages: One decimal place (e.g., 45.2%, not 45.23%)
- Large numbers: Use comma separators (e.g., 1,000,000 not 1000000)

LAYOUT PATTERNS SUMMARY:
- Pattern A (2-Column + Insight): Slides 1, 3, 6
  • Left column (50% width) + Right column (50% width)
  • Full-width insight box at bottom
  
- Pattern B (1-Column + Insight): Slides 2, 7, 9
  • Full-width chart at top
  • Full-width insight box at bottom
  
- Pattern C (Table Only): Slides 4, 5, 8, 10
  • Full-width table
  • NO insight box

SPACING & ALIGNMENT:
- Column gap: 24px
- Section padding: 16px
- Slide margins: 32px
- Insight box padding: 20px
- Consistent vertical spacing between elements

STYLE:
- Corporate and professional
- Clean and modern
- Data-driven and analytical
- Consistent spacing and alignment
- Clear visual hierarchy

═══════════════════════════════════════════════════════════════
END OF PROMPT
═══════════════════════════════════════════════════════════════

CRITICAL INSTRUCTIONS:
1. Create all 10 slides with the exact data provided above
2. Follow the LAYOUT STRUCTURE specifications precisely for each slide
3. Respect the 2-column vs 1-column layout patterns
4. Ensure all charts are properly formatted and labeled
5. Make insights readable with proper formatting in full-width boxes
6. Use the specified color palette consistently
7. Ensure the presentation is professional and polished
8. Preserve all source links as clickable hyperlinks
9. Apply number formatting rules consistently across all slides
10. Maintain consistent spacing and alignment throughout
"""
    
    return prompt
