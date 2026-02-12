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
    
    prompt = f"""Create a professional 10-slide presentation for Weekly Brand Health Analysis:

═══════════════════════════════════════════════════════════════
BRAND: {brand}
REPORT PERIOD: {week1_period} (7 days)
REPORT TYPE: Weekly Analysis
═══════════════════════════════════════════════════════════════
REPORT TYPE: Weekly Analysis
═══════════════════════════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 1 - TỔNG QUAN VỀ BRAND
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYOUT:
- Title: "{report_data['slide_1']['title']}"
- Subtitle: "{report_data['slide_1']['subtitle']}"
- 2 visualizations:
  1. Grid of 6 KPI cards (current week metrics with % change vs previous week for "Tổng đề cập" and "Tổng lượt xem")
  2. Column chart comparing 4 weeks (show absolute values on columns + growth % vs previous week)
- Bottom: Insight box

CURRENT WEEK METRICS:
"""
    
    for metric in report_data['slide_1']['current_week_metrics']:
        if 'change_percent' in metric:
            change_sign = "+" if metric['change_percent'] > 0 else ""
            prompt += f"- {metric['label']}: {format_number(metric['value'])} ({change_sign}{metric['change_percent']}% so với tuần trước)\n"
        else:
            prompt += f"- {metric['label']}: {format_number(metric['value'])}\n"
    
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

LAYOUT:
- Title: "{report_data['slide_2']['title']}"
- Subtitle: "{report_data['slide_2']['subtitle']}"
- Line chart showing 7-day trend
- Bottom: Insight box

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

LAYOUT:
- Title: "{report_data['slide_3']['title']}"
- Subtitle: "{report_data['slide_3']['subtitle']}"
- 2 visualizations:
  1. Pie chart (channel distribution) - show both absolute count and percentage
  2. Horizontal bar chart (top 10 sources)
- Bottom: Insight box

CHANNEL DISTRIBUTION (Pie Chart - hiển thị số lượng và %):
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

LAYOUT:
- Title: "{report_data['slide_4']['title']}"
- Subtitle: "{report_data['slide_4']['subtitle']}"
- Full-width table
- NO insight section

TABLE DATA:
"""
    
    for row in report_data['slide_4']['table_rows']:
        prompt += f"""
Row {row['stt']}:
- STT: {row['stt']}
- Nguồn: {row['source_name']}
- Tổng tương tác: {format_number(row['total_engagement'])}
- Likes: {format_number(row['reactions'])}
- Shares: {format_number(row['shares'])}
- Comments: {format_number(row['comments'])}
"""
    
    prompt += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 5 - TOP BÀI ĐĂNG CÓ TƯƠNG TÁC CAO NHẤT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYOUT:
- Title: "{report_data['slide_5']['title']}"
- Subtitle: "{report_data['slide_5']['subtitle']}"
- Full-width table
- NO insight section

TABLE DATA:
"""
    
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
    
    prompt += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 6 - SẮC THÁI VÀ CỤM CHỦ ĐỀ ĐỀ CẬP NỔI BẬT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYOUT:
- Title: "{report_data['slide_6']['title']}"
- Subtitle: "{report_data['slide_6']['subtitle']}"
- 2 visualizations:
  1. Two DONUT charts side-by-side (previous week vs current week sentiment) - show both absolute count and percentage
     - Left Donut: Previous week with NSR = {report_data['slide_6']['previous_nsr']}% displayed in center
     - Right Donut: Current week with NSR = {report_data['slide_6']['current_nsr']}% displayed in center
     - Between the two donuts: Display NSR growth rate = {report_data['slide_6']['nsr_growth']:+.2f}%
  2. Horizontal bar chart (top topics with sentiment breakdown)
- Bottom: Insight box

PREVIOUS WEEK SENTIMENT (Left Donut - hiển thị số lượng và %):
NSR (Tuần trước) = {report_data['slide_6']['previous_nsr']}%
"""
    
    # Calculate total for previous week percentage
    total_prev = sum(sent['count'] for sent in report_data['slide_6']['previous_sentiment'])
    for sent in report_data['slide_6']['previous_sentiment']:
        percentage = (sent['count'] / total_prev * 100) if total_prev > 0 else 0
        prompt += f"- {sent['sentiment']}: {format_number(sent['count'])} lượt ({percentage:.1f}%)\n"
    
    prompt += f"""
CURRENT WEEK SENTIMENT (Right Donut - hiển thị số lượng và %):
NSR (Tuần hiện tại) = {report_data['slide_6']['current_nsr']}%
"""
    # Calculate total for current week percentage
    total_curr = sum(sent['count'] for sent in report_data['slide_6']['current_sentiment'])
    for sent in report_data['slide_6']['current_sentiment']:
        percentage = (sent['count'] / total_curr * 100) if total_curr > 0 else 0
        prompt += f"- {sent['sentiment']}: {format_number(sent['count'])} lượt ({percentage:.1f}%)\n"
    
    nsr_growth_sign = "+" if report_data['slide_6']['nsr_growth'] > 0 else ""
    prompt += f"""
NSR GROWTH (Hiển thị giữa 2 donut charts):
{nsr_growth_sign}{report_data['slide_6']['nsr_growth']:.2f}% (so với tuần trước)

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

LAYOUT:
- Title: "{report_data['slide_7']['title']}"
- Subtitle: "{report_data['slide_7']['subtitle']}"
- Horizontal bar chart
- Bottom: Insight box

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

LAYOUT:
- Title: "{report_data['slide_9']['title']}"
- Subtitle: "{report_data['slide_9']['subtitle']}"
- Horizontal bar chart
- Bottom: Insight box

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

STYLE:
- Corporate and professional
- Clean and modern
- Data-driven and analytical
- Consistent spacing and alignment

═══════════════════════════════════════════════════════════════
END OF PROMPT
═══════════════════════════════════════════════════════════════

INSTRUCTIONS:
1. Create all 10 slides with the exact data provided above
2. Follow the design specifications precisely
3. Ensure all charts are properly formatted and labeled
4. Make insights readable with proper formatting
5. Use the specified color palette consistently
6. Ensure the presentation is professional and polished
7. Preserve all source links as clickable hyperlinks
"""
    
    return prompt
