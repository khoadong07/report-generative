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
    from generators.daily.report_generator import ReportGenerator
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
    """Format date to DD/MM/YYYY - handles multiple input formats"""
    if isinstance(date_str, str):
        # Try multiple formats
        formats = [
            "%Y-%m-%d %H:%M:%S",  # 2026-02-04 15:00:00
            "%Y-%m-%d",           # 2026-02-04
            "%d/%m/%Y %H:%M",     # 04/02/2026 15:00
            "%d/%m/%Y",           # 04/02/2026
        ]
        
        for fmt in formats:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime("%d/%m/%Y")
            except ValueError:
                continue
        
        # Fallback to pandas
        try:
            import pandas as pd
            date_obj = pd.to_datetime(date_str)
            return date_obj.strftime("%d/%m/%Y")
        except:
            return str(date_str)
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
    if not slide_data:
        raise ValueError("slide_data is None for Slide 1")
    
    if 'data' not in slide_data:
        raise ValueError("'data' key missing in slide_data for Slide 1")
    
    kpis = []
    for item in slide_data['data']:
        kpis.append(
            f"{item['label']}: {format_number(item['today'])} "
            f"({format_percentage(item['change_pct'])})"
        )
    
    # Convert insight with hyperlinks
    insight = convert_insight_to_hyperlink_format(slide_data.get('insight', ''))
    hyperlinks = extract_hyperlinks_from_insight(slide_data.get('insight', ''))
    
    return {
        'title': slide_data.get('title', 'Slide 1'),
        'subtitle': slide_data.get('subtitle', ''),
        'kpis': kpis,
        'insight': insight,
        'hyperlinks': hyperlinks
    }


def generate_slide2_data(slide_data):
    """Generate formatted data for Slide 2"""
    if not slide_data:
        raise ValueError("slide_data is None for Slide 2")
    
    trendline = []
    for point in slide_data.get('trendline', []):
        date_formatted = format_date(point.get('date', ''))
        trendline.append(f"{date_formatted}: {format_number(point.get('buzz', 0))}")
    
    peak_day = slide_data.get('peak_day', {})
    current_day = slide_data.get('current_day', {})
    
    peak_date = format_date(peak_day.get('date', ''))
    current_date = format_date(current_day.get('date', ''))
    
    # Convert insight with hyperlinks
    insight = convert_insight_to_hyperlink_format(slide_data.get('insight', ''))
    hyperlinks = extract_hyperlinks_from_insight(slide_data.get('insight', ''))
    
    return {
        'title': slide_data.get('title', 'Trendline'),
        'subtitle': slide_data.get('subtitle', ''),
        'trendline': trendline,
        'peak_day': f"{peak_date} - {format_number(peak_day.get('buzz', 0))} lượt",
        'current_status': f"{current_date} - {'Vẫn đang HOT 🔥' if current_day.get('is_still_hot', False) else 'Đã hạ nhiệt ❄️'}",
        'insight': insight,
        'hyperlinks': hyperlinks
    }


def generate_slide3_data(slide_data):
    """Generate formatted data for Slide 3"""
    if not slide_data:
        raise ValueError("slide_data is None for Slide 3")
    
    channels = []
    for item in slide_data.get('channel_distribution', []):
        channels.append(
            f"{item.get('Channel', 'N/A')}: {format_number(int(item.get('today_buzz', 0)))} "
            f"({format_percentage(item.get('change_pct', 0))})"
        )
    
    # Convert insight with hyperlinks
    insight = convert_insight_to_hyperlink_format(slide_data.get('insight', ''))
    hyperlinks = extract_hyperlinks_from_insight(slide_data.get('insight', ''))
    
    return {
        'title': slide_data.get('title', 'Channel Breakdown'),
        'subtitle': slide_data.get('subtitle', ''),
        'channels': channels,
        'top_channel': slide_data.get('top_channel', 'N/A'),
        'insight': insight,
        'hyperlinks': hyperlinks
    }


def generate_slide4_data(slide_data):
    """Generate formatted data for Slide 4 (Sentiment + Channel Breakdown)"""
    if not slide_data:
        raise ValueError("slide_data is None for Slide 4")
    
    sentiment = []
    for item in slide_data.get('sentiment_distribution', []):
        sentiment.append(
            f"{item.get('Sentiment', 'N/A')}: {format_number(item.get('Count', 0))}"
        )
    
    # Channel sentiment breakdown
    channels = []
    for item in slide_data.get('channel_sentiment', []):
        channel_name = item.get('Channel', 'N/A')
        neg = int(item.get('Negative', 0))
        neu = int(item.get('Neutral', 0))
        pos = int(item.get('Positive', 0))
        total = neg + neu + pos
        
        # Calculate percentages
        neg_pct = (neg / total * 100) if total > 0 else 0
        neu_pct = (neu / total * 100) if total > 0 else 0
        pos_pct = (pos / total * 100) if total > 0 else 0
        
        channels.append({
            'name': channel_name,
            'negative': neg,
            'neutral': neu,
            'positive': pos,
            'neg_pct': round(neg_pct, 1),
            'neu_pct': round(neu_pct, 1),
            'pos_pct': round(pos_pct, 1)
        })
    
    # Convert insight with hyperlinks
    insight = convert_insight_to_hyperlink_format(slide_data.get('insight', ''))
    hyperlinks = extract_hyperlinks_from_insight(slide_data.get('insight', ''))
    
    return {
        'title': slide_data.get('title', 'Sentiment Analysis'),
        'subtitle': slide_data.get('subtitle', ''),
        'sentiment': sentiment,
        'channels': channels,
        'insight': insight,
        'hyperlinks': hyperlinks
    }


def generate_slide5_data(slide_data):
    """Generate formatted data for Slide 5"""
    if not slide_data:
        raise ValueError("slide_data is None for Slide 5")
    
    if 'top_posts' not in slide_data:
        raise ValueError("'top_posts' key missing in slide_data for Slide 5")
    
    table_rows = []
    for post in slide_data['top_posts']:
        # Format date
        try:
            date_obj = datetime.strptime(post['ngay_dang'], "%Y-%m-%d %H:%M:%S")
            date_formatted = date_obj.strftime("%d/%m/%Y")
        except:
            date_formatted = str(post.get('ngay_dang', 'N/A'))
        
        # Build content with link
        content = post.get('noi_dung_bai_dang', '')
        url = post.get('url_topic', '')
        
        # Check if this is interaction mode or comment mode
        if 'luong_tuong_tac' in post:
            # Interaction mode
            luong_tuong_tac = post.get('luong_tuong_tac', {})
            if isinstance(luong_tuong_tac, dict):
                reactions = luong_tuong_tac.get('reactions', 0)
                share = luong_tuong_tac.get('share', 0)
                comments = luong_tuong_tac.get('comments', 0)
                views = luong_tuong_tac.get('views', 0)
            else:
                reactions = share = comments = views = 0
            
            table_rows.append({
                'stt': post.get('stt', 0),
                'noi_dung': content,
                'url': url,
                'ngay_dang': date_formatted,
                'kenh': post.get('kenh', 'N/A'),
                'nguoi_dang': post.get('nguoi_dang', 'N/A'),
                'reactions': format_number(reactions),
                'share': format_number(share),
                'comments': format_number(comments),
                'views': format_number(views)
            })
        else:
            # Comment mode
            table_rows.append({
                'stt': post.get('stt', 0),
                'noi_dung': content,
                'url': url,
                'ngay_dang': date_formatted,
                'kenh': post.get('kenh', 'N/A'),
                'nguoi_dang': post.get('nguoi_dang', 'N/A'),
                'comment_count': format_number(post.get('comment_count', 0))
            })
    
    return {
        'title': slide_data.get('title', 'Top 5 bài đăng'),
        'subtitle': slide_data.get('subtitle', ''),
        'table_rows': table_rows
    }


def generate_slide6_data(slide_data):
    """Generate formatted data for Slide 6"""
    if not slide_data:
        raise ValueError("slide_data is None for Slide 6")
    
    # Helper function to normalize deleted indicators
    def normalize_deleted_value(value):
        """Convert various deleted indicators to 'Deleted'"""
        value_str = str(value).lower().strip()
        deleted_indicators = ['deleted', 'not exist', 'close group', 'die', 'removed', 'unavailable']
        
        # Check if value contains any deleted indicator
        if any(indicator in value_str for indicator in deleted_indicators):
            return 'Deleted'
        return value
    
    table_rows = []
    
    # Handle both deleted_posts and posts_with_deleted_comments
    posts_data = slide_data.get('deleted_posts', []) or slide_data.get('posts_with_deleted_comments', [])
    
    for post in posts_data:
        # Format date
        try:
            date_obj = datetime.strptime(str(post.get('ngay_dang', '')), "%Y-%m-%d %H:%M:%S")
            date_formatted = date_obj.strftime("%d/%m/%Y")
        except:
            date_formatted = str(post.get('ngay_dang', 'N/A'))
        
        # Build content with link
        content = post.get('noi_dung_bai_dang', '')
        url = post.get('url_topic', '')
        
        # Check if this is deleted posts or posts with deleted comments
        if 'metric_status' in post:
            # Deleted posts mode
            metric_status = post.get('metric_status', {})
            if isinstance(metric_status, dict):
                reactions = normalize_deleted_value(metric_status.get('reactions', 'N/A'))
                shares = normalize_deleted_value(metric_status.get('shares', 'N/A'))
                comments = normalize_deleted_value(metric_status.get('comments', 'N/A'))
                views = normalize_deleted_value(metric_status.get('views', 'N/A'))
            else:
                reactions = shares = comments = views = 'Deleted'
            
            table_rows.append({
                'stt': post.get('stt', 0),
                'noi_dung': content,
                'url': url,
                'ngay_dang': date_formatted,
                'kenh': post.get('kenh', 'N/A'),
                'nguoi_dang': post.get('nguoi_dang', 'N/A'),
                'reactions': reactions,
                'shares': shares,
                'comments': comments,
                'views': views
            })
        else:
            # Posts with deleted comments mode
            table_rows.append({
                'stt': post.get('stt', 0),
                'noi_dung': content,
                'url': url,
                'ngay_dang': date_formatted,
                'kenh': post.get('kenh', 'N/A'),
                'nguoi_dang': post.get('nguoi_dang', 'N/A'),
                'deleted_comment_count': format_number(post.get('deleted_comment_count', 0))
            })
    
    return {
        'title': slide_data.get('title', 'Top 5 bài đăng đã xóa'),
        'subtitle': slide_data.get('subtitle', ''),
        'total_deleted': slide_data.get('total_deleted_posts', 0) or slide_data.get('total_deleted_comments', 0),
        'table_rows': table_rows
    }


def generate_complete_prompt(report_data):
    """Generate complete prompt with all data embedded"""
    
    # Extract metadata
    metadata = report_data['report_metadata']
    brand = metadata['brand']
    report_date = format_date(metadata['report_date'])
    compare_date = format_date(metadata['compare_date'])
    show_interactions = metadata.get('show_interactions', True)
    total_slides = metadata.get('total_slides', 6)
    
    # Generate data for each slide with error handling
    try:
        slide1 = generate_slide1_data(report_data.get('slide_1'))
    except (ValueError, KeyError, TypeError) as e:
        raise ValueError(f"Error generating Slide 1 data: {str(e)}")
    
    try:
        slide2 = generate_slide2_data(report_data.get('slide_2'))
    except (ValueError, KeyError, TypeError) as e:
        raise ValueError(f"Error generating Slide 2 data: {str(e)}")
    
    try:
        slide3 = generate_slide3_data(report_data.get('slide_3'))
    except (ValueError, KeyError, TypeError) as e:
        raise ValueError(f"Error generating Slide 3 data: {str(e)}")
    
    try:
        slide4 = generate_slide4_data(report_data.get('slide_4'))
    except (ValueError, KeyError, TypeError) as e:
        raise ValueError(f"Error generating Slide 4 data: {str(e)}")
    
    try:
        slide5 = generate_slide5_data(report_data.get('slide_5'))
    except (ValueError, KeyError, TypeError) as e:
        raise ValueError(f"Error generating Slide 5 data: {str(e)}")
    
    # Only generate slide 6 if it exists and show_interactions is True
    slide6 = None
    if show_interactions and 'slide_6' in report_data and report_data['slide_6']:
        try:
            slide6 = generate_slide6_data(report_data['slide_6'])
        except (ValueError, KeyError, TypeError) as e:
            print(f"Warning: Error generating Slide 6 data: {str(e)}")
            slide6 = None
    
    # Collect all hyperlinks
    all_hyperlinks = []
    for slide_num, slide in enumerate([slide1, slide2, slide3, slide4], 1):
        if slide and slide.get('hyperlinks'):
            for link in slide['hyperlinks']:
                all_hyperlinks.append({
                    'slide': slide_num,
                    'url': link['url']
                })
    
    # Add Slide 5 URLs
    if slide5 and slide5.get('table_rows'):
        for row in slide5['table_rows']:
            if row.get('url'):
                all_hyperlinks.append({
                    'slide': 5,
                    'url': row['url']
                })
    
    # Add Slide 6 URLs (only if slide 6 exists)
    if slide6 and slide6.get('table_rows'):
        for row in slide6['table_rows']:
            if row.get('url'):
                all_hyperlinks.append({
                    'slide': 6,
                    'url': row['url']
                })
    
    # Build complete prompt
    slide_count_text = f"{total_slides}-slide" if total_slides != 6 else "6-slide"
    prompt = f"""Create a professional {slide_count_text} presentation for Brand Health Analysis with the following specifications:

═══════════════════════════════════════════════════════════════
BRAND: {brand}
REPORT DATE: {report_date}
COMPARE DATE: {compare_date}
PRESENTATION MODE: {"Basic Metrics (No Interactions)" if not show_interactions else "Full Metrics (With Interactions)"}
TOTAL SLIDES: {total_slides}
═══════════════════════════════════════════════════════════════

---------------------------------------------------------------
SLIDE 1 - BRAND OVERVIEW
---------------------------------------------------------------

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
"""
    
    if slide1.get('hyperlinks'):
        prompt += f"""
HYPERLINKS IN INSIGHT:
"""
        for link in slide1['hyperlinks']:
            prompt += f"- {link['url']}\n"
    
    prompt += f"""
DESIGN:
- Style: Corporate, clean, data-focused
- Colors: Green for positive changes, Red for negative changes
- Font: Modern sans-serif, 32px title, 14px body
- Background: White with light blue insight box

-------------------------------------------------------------
SLIDE 2 - TRENDLINE
-------------------------------------------------------------

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
"""
    
    if slide2.get('hyperlinks'):
        prompt += f"""
HYPERLINKS IN INSIGHT:
"""
        for link in slide2['hyperlinks']:
            prompt += f"- {link['url']}\n"
    
    prompt += f"""
CHART DESIGN:
- Type: Line chart with markers
- Line color: Blue (#1e40af), width 3px
- Peak marker: Red circle, larger size
- Grid: Light gray, dashed
- Background: White

-------------------------------------------------------------
SLIDE 3 - CHANNEL BREAKDOWN
-------------------------------------------------------------

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
"""
    
    if slide3.get('hyperlinks'):
        prompt += f"""
HYPERLINKS IN INSIGHT:
"""
        for link in slide3['hyperlinks']:
            prompt += f"- {link['url']}\n"
    
    prompt += f"""
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

-------------------------------------------------------------
SLIDE 4 - SENTIMENT & CHANNEL BREAKDOWN
-------------------------------------------------------------

LAYOUT:
- Title: "{slide4['title']}"
- Subtitle: "{slide4['subtitle']}"
- Two-column layout (equal width):
  * Left (50%): Pie chart (Overall Sentiment Distribution)
  * Right (50%): Stacked Bar Chart (Sentiment by Channel)
- Bottom section: Insight (full width)

OVERALL SENTIMENT DISTRIBUTION:
"""
    
    for sent in slide4['sentiment']:
        prompt += f"- {sent}\n"
    
    prompt += f"""
SENTIMENT BY CHANNEL (Stacked Bar Chart):
"""
    
    for ch in slide4.get('channels', []):
        prompt += f"""
{ch['name']}:
- Negative: {ch['negative']} ({ch['neg_pct']}%)
- Neutral: {ch['neutral']} ({ch['neu_pct']}%)
- Positive: {ch['positive']} ({ch['pos_pct']}%)
"""
    
    prompt += f"""
INSIGHT:
{slide4['insight']}
"""
    
    if slide4.get('hyperlinks'):
        prompt += f"""
HYPERLINKS IN INSIGHT:
"""
        for link in slide4['hyperlinks']:
            prompt += f"- {link['url']}\n"
    
    prompt += f"""
CHART DESIGN:

LEFT - Pie Chart (Donut style):
- Segments:
  * Neutral: Gray (#6b7280)
  * Negative: Red (#dc2626)
  * Positive: Green (#16a34a)
- Show percentages on segments
- Show count values
- Legend at bottom
- Title: "Phân bố sắc thái thảo luận"

RIGHT - Stacked Bar Chart (100% Stacked, VERTICAL):
- X-axis: Channel names (Facebook Users, Facebook Pages, Facebook Groups, Tiktok, Youtube, etc.)
- Y-axis: Percentage (0-100%)
- Each bar is 100% height, divided by sentiment percentages
- Stack colors (same as pie chart):
  * Negative: Red (#dc2626) - bottom
  * Neutral: Gray (#6b7280) - middle
  * Positive: Green (#16a34a) - top
- Show percentage labels on each segment
- Legend at top
- Title: "Sắc thái thảo luận theo kênh có lượng thảo luận cao nhất"
- All bars have equal height (100% stacked)
- Bars are VERTICAL (columns), not horizontal
- Sort channels by total count (descending, left to right)
- Show top 8 channels only

IMPORTANT NOTES:
- Facebook channel is split into 3 sub-channels:
  * Facebook Users (from fbUserComment, fbUserTopic)
  * Facebook Pages (from fbPageComment, fbPageTopic)
  * Facebook Groups (from fbGroupComment, fbGroupTopic)
- Chart orientation: VERTICAL bars (columns standing up)
- NOT horizontal bars
- Only top 8 channels with highest discussion count are shown

INSIGHT SECTION:
- Full width below charts
- Professional paragraph format
- Each sentence ends with [Nguồn: URL]
- Hyperlinks styled in blue (#1e40af)
- Focus on overall sentiment + channel-specific trends
- Format: "Insight text... [Nguồn: URL]"

-------------------------------------------------------------
SLIDE 5 - TOP 5 BÀI ĐĂNG CÓ LƯỢNG TƯƠNG TÁC CAO
-------------------------------------------------------------

LAYOUT:
- Title: "{slide5['title']}"
- Subtitle: "{slide5['subtitle']}"
- Full-width table with 2-tier header
- Clean, professional table design
- NO insight section (data table only)
"""

    # Check if this is interactions mode or comment mode
    if show_interactions:
        prompt += f"""
TABLE STRUCTURE:
Header Tier 1 (Main columns):
- STT (center aligned)
- Nội dung bài đăng (left aligned, wide column)
- Ngày đăng (center aligned)
- Kênh (center aligned)
- Người đăng (center aligned)
- Lượng tương tác (colspan=4, center aligned)

Header Tier 2 (Under "Lượng tương tác"):
- Reactions (right aligned)
- Share (right aligned)
- Comments (right aligned)
- Views (right aligned)

TABLE DATA:
"""
        
        for row in slide5['table_rows']:
            # Safely handle content that might be NaN or float
            noi_dung = str(row.get('noi_dung', ''))
            if noi_dung in ['nan', 'None', '']:
                noi_dung = '[Không có nội dung]'
            
            prompt += f"""
Row {row.get('stt', 0)}:
- STT: {row.get('stt', 0)}
- Nội dung: {noi_dung[:100]}{'...' if len(noi_dung) > 100 else ''} [Link]({row.get('url', '')})
- Ngày đăng: {row.get('ngay_dang', 'N/A')}
- Kênh: {row.get('kenh', 'N/A')}
- Người đăng: {row.get('nguoi_dang', 'N/A')}
- Reactions: {row.get('reactions', '0')}
- Share: {row.get('share', '0')}
- Comments: {row.get('comments', '0')}
- Views: {row.get('views', '0')}
"""
        
        prompt += f"""
TABLE DESIGN:
- Header background: #1e40af (primary blue)
- Header text: White, bold, 14px
- Row background: Alternating white and #f9fafb
- Border: 1px solid #e5e7eb
- Cell padding: 12px vertical, 16px horizontal
- Font: 13px for body text
- Text alignment:
  * STT: Center
  * Nội dung: Left (allow text wrap, show "Link" at end)
  * Ngày đăng: Center
  * Kênh: Center
  * Người đăng: Center
  * Metrics (Reactions/Share/Comments/Views): Right aligned
- Column widths:
  * STT: 60px
  * Nội dung: 40% (flexible, allow wrap)
  * Ngày đăng: 100px
  * Kênh: 100px
  * Người đăng: 150px
  * Reactions: 80px
  * Share: 80px
  * Comments: 80px
  * Views: 100px

HYPERLINK HANDLING:
- Each row's "Nội dung" column ends with the word "Link"
- "Link" should be a clickable hyperlink to the URL
- Style: Blue (#1e40af), underline on hover
- Opens in new tab when clicked
- Format: Content text... [Link](url)

IMPORTANT NOTES:
1. Numbers are already formatted with commas - display as-is
2. Do NOT convert numbers to K/M format
3. Keep raw numbers (e.g., 4,091 not 4.1K)
4. Content text can wrap to multiple lines
5. Table should be responsive and fit slide width
6. This slide has NO insight section - only the table
"""
    else:
        # Comment mode - only show comment count
        prompt += f"""
TABLE STRUCTURE:
Header Tier 1 (Main columns):
- STT (center aligned)
- Nội dung bài đăng (left aligned, wide column)
- Ngày đăng (center aligned)
- Kênh (center aligned)
- Người đăng (center aligned)
- Số bình luận (center aligned)

TABLE DATA:
"""
        
        for row in slide5['table_rows']:
            # Safely handle content that might be NaN or float
            noi_dung = str(row.get('noi_dung', ''))
            if noi_dung in ['nan', 'None', '']:
                noi_dung = '[Không có nội dung]'
            
            prompt += f"""
Row {row.get('stt', 0)}:
- STT: {row.get('stt', 0)}
- Nội dung: {noi_dung[:100]}{'...' if len(noi_dung) > 100 else ''} [Link]({row.get('url', '')})
- Ngày đăng: {row.get('ngay_dang', 'N/A')}
- Kênh: {row.get('kenh', 'N/A')}
- Người đăng: {row.get('nguoi_dang', 'N/A')}
- Số bình luận: {row.get('comment_count', '0')}
"""
        
        prompt += f"""
TABLE DESIGN:
- Header background: #1e40af (primary blue)
- Header text: White, bold, 14px
- Row background: Alternating white and #f9fafb
- Border: 1px solid #e5e7eb
- Cell padding: 12px vertical, 16px horizontal
- Font: 13px for body text
- Text alignment:
  * STT: Center
  * Nội dung: Left (allow text wrap, show "Link" at end)
  * Ngày đăng: Center
  * Kênh: Center
  * Người đăng: Center
  * Số bình luận: Center
- Column widths:
  * STT: 60px
  * Nội dung: 45% (flexible, allow wrap)
  * Ngày đăng: 100px
  * Kênh: 100px
  * Người đăng: 150px
  * Số bình luận: 100px

HYPERLINK HANDLING:
- Each row's "Nội dung" column ends with the word "Link"
- "Link" should be a clickable hyperlink to the URL
- Style: Blue (#1e40af), underline on hover
- Opens in new tab when clicked
- Format: Content text... [Link](url)

IMPORTANT NOTES:
1. Numbers are already formatted with commas - display as-is
2. Do NOT convert numbers to K/M format
3. Keep raw numbers (e.g., 4,091 not 4.1K)
4. Content text can wrap to multiple lines
5. Table should be responsive and fit slide width
6. This slide has NO insight section - only the table
7. Posts are sorted by comment count (highest first)
"""

    # Only add Slide 6 section if slide6 exists
    if slide6:
        prompt += f"""
---------------------------------------------------------------
SLIDE 6 - TOP 5 BÀI ĐĂNG ĐÃ XÓA
---------------------------------------------------------------

LAYOUT:
- Title: "{slide6['title']}"
- Subtitle: "{slide6['subtitle']}"
- Summary: "Tổng số bài đăng đã xóa: {slide6['total_deleted']}"
- Full-width table with 2-tier header
- Clean, professional table design
- NO insight section (data table only)

TABLE STRUCTURE:
Header Tier 1 (Main columns):
- STT (center aligned)
- Nội dung bài đăng (left aligned, wide column)
- Ngày đăng (center aligned)
- Kênh (center aligned)
- Người đăng (center aligned)
- Lượng tương tác (colspan=4, center aligned)

Header Tier 2 (Under "Lượng tương tác"):
- Reactions (center aligned)
- Shares (center aligned)
- Comments (center aligned)
- Views (center aligned)

TABLE DATA:
"""
        
        for row in slide6['table_rows']:
            # Safely handle content that might be NaN or float
            noi_dung = str(row.get('noi_dung', ''))
            if noi_dung in ['nan', 'None', '']:
                noi_dung = '[Không có nội dung]'
            
            prompt += f"""
Row {row.get('stt', 0)}:
- STT: {row.get('stt', 0)}
- Nội dung: {noi_dung[:100]}{'...' if len(noi_dung) > 100 else ''} [Link]({row.get('url', '')})
- Ngày đăng: {row.get('ngay_dang', 'N/A')}
- Kênh: {row.get('kenh', 'N/A')}
- Người đăng: {row.get('nguoi_dang', 'N/A')}
- Reactions: {row.get('reactions', 'N/A')}
- Shares: {row.get('shares', 'N/A')}
- Comments: {row.get('comments', 'N/A')}
- Views: {row.get('views', 'N/A')}
"""
        
        prompt += f"""
TABLE DESIGN:
- Header background: #dc2626 (danger red - indicates deleted)
- Header text: White, bold, 14px
- Row background: Alternating white and #fef2f2 (light red tint)
- Border: 1px solid #fecaca
- Cell padding: 12px vertical, 16px horizontal
- Font: 13px for body text
- Text alignment:
  * STT: Center
  * Nội dung: Left (allow text wrap, show "Link" at end)
  * Ngày đăng: Center
  * Kênh: Center
  * Người đăng: Center
  * Metrics (all): Center
- Column widths:
  * STT: 60px
  * Nội dung: 35% (flexible, allow wrap)
  * Ngày đăng: 100px
  * Kênh: 100px
  * Người đăng: 150px
  * Reactions: 80px
  * Shares: 80px
  * Comments: 80px
  * Views: 80px
  * Total: 80px

HYPERLINK HANDLING:
- Each row's "Nội dung" column ends with the word "Link"
- "Link" should be a clickable hyperlink to the URL
- Style: Red (#dc2626), underline on hover
- Opens in new tab when clicked
- Format: Content text... [Link](url)

IMPORTANT NOTES:
1. Metrics show "deleted" status (not numbers)
2. Display metric values as-is (may be "deleted", "0", or numbers)
3. Content text can wrap to multiple lines
4. Table should be responsive and fit slide width
5. This slide has NO insight section - only the table
6. Red color scheme indicates deleted/removed content
7. Summary shows total count of deleted posts
"""

    prompt += f"""
-------------------------------------------------------------
OVERALL DESIGN THEME
-------------------------------------------------------------

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

NUMBER FORMATTING:
- Thousands separator: Comma (,)
  Examples: 2,000 | 15,500 | 1,234,567
- Decimal separator: Period (.)
  Examples: 2.3% | 15.7% | 0.5%
- Percentages: One decimal place (e.g., 45.2%, not 45.23%)
- Large numbers: Use comma separators (e.g., 1,000,000 not 1000000)

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

-------------------------------------------------------------
HYPERLINK HANDLING REQUIREMENTS
-------------------------------------------------------------
"""
    
    if all_hyperlinks:
        prompt += f"""
⚠️ IMPORTANT: This presentation contains hyperlinks in the insight sections.

HYPERLINK LOCATIONS:
"""
        for link_info in all_hyperlinks:
            prompt += f"- Slide {link_info['slide']}: {link_info['url']}\n"
        
        prompt += f"""
HYPERLINK FORMATTING INSTRUCTIONS:
1. In the insight text, URLs are marked with [URL](actual_link) format
2. Convert these to clickable hyperlinks in the final slides
3. Display text should be "URL" (styled as a link)
4. The link should open in a new tab/window when clicked
5. Style hyperlinks with:
   - Color: #1e40af (primary blue)
   - Underline on hover
   - Cursor: pointer
   - Font weight: 500 (medium)

EXAMPLE:
If insight text contains: "Xem thêm tại [URL](https://example.com) để biết chi tiết"
Display as: "Xem thêm tại URL để biết chi tiết" (where "URL" is a clickable link)

PLATFORM-SPECIFIC NOTES:
- Manuss: Use markdown format [URL](link) - it will auto-convert
- Gamma: Use markdown format [URL](link) - it will auto-convert  
- Beautiful.ai: Manually add hyperlinks after generation if needed
- Canva: Manually add hyperlinks after generation if needed

"""
    else:
        prompt += f"""
ℹ️ NOTE: This presentation does not contain any hyperlinks in the insights.
"""
    
    prompt += f"""
═══════════════════════════════════════════════════════════════
END OF PROMPT
═══════════════════════════════════════════════════════════════

INSTRUCTIONS:
1. Create all 6 slides with the exact data provided above
2. Follow the design specifications precisely
3. Ensure all charts are properly formatted and labeled
4. Make insights readable with proper formatting
5. Use the specified color palette consistently
6. Ensure the presentation is professional and polished
7. Apply number formatting rules consistently across all slides (comma for thousands, period for decimals)
8. For each slide, the Insight section must reference its source link(s). All source links must be preserved and converted into hyperlinks with the display text “URL”. Raw links must not be shown, removed, or replaced. Users must be able to click on the text “URL” to access the cited source.
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
    print("   ⏱️  This will take 3-4 minutes (calling LLM 4 times)")
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
