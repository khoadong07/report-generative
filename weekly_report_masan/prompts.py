#!/usr/bin/env python3
"""
Masan Weekly Report Prompt Templates
Centralized prompt templates for LLM insight generation
"""


def get_masan_channel_insight_prompt(channel_summary: str, brand: str, 
                                      start_date: str, end_date: str) -> str:
    """Prompt for generating channel distribution insight."""
    return f"""Phân tích phân bổ kênh thảo luận về {brand} ({start_date} - {end_date}):

{channel_summary}

Viết insight ngắn gọn (2-3 câu):
- Kênh nào chiếm ưu thế và tại sao
- Khuyến nghị ngắn về chiến lược kênh"""


def get_masan_market_overview_prompt(main_brand: str, main_buzz: int,
                                      main_sentiment: dict, weekly_trend: list,
                                      competitor_summary: str, top_channel: str,
                                      report_date: str) -> str:
    """Prompt for generating overall market conclusion."""
    weekly_trend_str = ', '.join([f"{w['week']}: {w['buzz_count']}" for w in weekly_trend])
    
    return f"""Đánh giá {main_brand} và thị trường (tuần kết thúc {report_date}):

MAIN BRAND:
- Buzz: {main_buzz} | Sentiment: Pos {main_sentiment['positive']['percent']}%, Neg {main_sentiment['negative']['percent']}%
- Xu hướng 4 tuần: {weekly_trend_str}

ĐỐI THỦ:
{competitor_summary}

Kênh chính: {top_channel}

Viết đánh giá ngắn gọn (100-120 từ):
1. So sánh hiệu suất vs đối thủ
2. Ý nghĩa của sentiment
3. 2-3 khuyến nghị chính

Trả lời súc tích, tập trung vào insights quan trọng."""
