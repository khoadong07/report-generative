#!/usr/bin/env python3
"""
Masan Weekly Report Prompt Construction
Supports multiple slides including category detail slides
"""
from typing import Dict, Any
from weekly_report_masan.builders import build_masan_slide_prompt

def generate_masan_prompt(report_data: Dict[str, Any]) -> str:
    """
    Generate prompt for Masan Weekly Report.
    
    Supports:
    - slide_1_market: Consumer & Markets
    - slide_2_discussion: Discussion Overview
    - slide_3_health: Health Index & Channels
    - slide_4_products: Masan Consumer Products
    - category_slides: Category detail slides (Slide 5+)
        Each category has 4 slides:
        - detail: Brand SOV, Product categories, Top products
        - channels: Top sources, Channel distribution
        - sentiment: Sentiment % and NSR by brand
        - trends: Daily trends with peak annotations
    
    Args:
        report_data: Dictionary containing slide data
    
    Returns:
        Formatted prompt string for all slides
    """
    
    # Extract metadata
    metadata = report_data.get("report_metadata", {})
    report_date = metadata.get("report_date", report_data.get("report_date", ""))
    main_brand = metadata.get("main_brand", "")
    competitors = metadata.get("competitors", [])
    selected_categories = metadata.get("selected_categories", [])
    
    # Count total slides
    base_slides = sum(1 for k in report_data if k.startswith("slide_") and k not in ["slide_5_category", "slide_6_channels", "slide_7_sentiment", "slide_8_trends"])
    category_slide_count = 0
    if "category_slides" in report_data:
        category_slide_count = len(report_data["category_slides"]) * 4  # Each category has 4 slides
    
    total_slides = base_slides + category_slide_count
    
    # Build header
    prompt = "=" * 70 + "\n"
    prompt += "BÁO CÁO TUẦN MASAN\n"
    prompt += "=" * 70 + "\n"
    prompt += f"Ngày báo cáo: {report_date}\n"
    prompt += f"Main Brand: {main_brand}\n"
    if competitors:
        prompt += f"Đối thủ: {', '.join(competitors)}\n"
    if selected_categories:
        prompt += f"Ngành hàng phân tích: {', '.join(selected_categories)}\n"
    prompt += f"Tổng số slides: {total_slides}\n\n"
    
    # Build base slides (1-4)
    slide_count = 0
    for key in ["slide_1_market", "slide_2_discussion", "slide_3_health", "slide_4_products"]:
        if key in report_data:
            slide_count += 1
            prompt += f"\n{'=' * 70}\n"
            prompt += f"SLIDE {slide_count}\n"
            prompt += f"{'=' * 70}\n\n"
            slide_prompt = build_masan_slide_prompt(key, report_data[key])
            prompt += slide_prompt
            prompt += "\n"
    
    # Build category slides (5+)
    if "category_slides" in report_data:
        category_slides = report_data["category_slides"]
        
        for category_name, category_data_dict in category_slides.items():
            # Slide X: Category Detail
            slide_count += 1
            prompt += f"\n{'=' * 70}\n"
            prompt += f"SLIDE {slide_count}: {category_name.upper()} - CHI TIẾT\n"
            prompt += f"{'=' * 70}\n\n"
            
            detail_data = category_data_dict.get("detail", {})
            detail_prompt = build_masan_slide_prompt("slide_5_category", detail_data)
            prompt += detail_prompt
            prompt += "\n"
            
            # Slide X+1: Category Channels
            slide_count += 1
            prompt += f"\n{'=' * 70}\n"
            prompt += f"SLIDE {slide_count}: {category_name.upper()} - KÊNH THẢO LUẬN\n"
            prompt += f"{'=' * 70}\n\n"
            
            channels_data = category_data_dict.get("channels", {})
            channels_prompt = build_masan_slide_prompt("slide_6_channels", channels_data)
            prompt += channels_prompt
            prompt += "\n"
            
            # Slide X+2: Category Sentiment
            slide_count += 1
            prompt += f"\n{'=' * 70}\n"
            prompt += f"SLIDE {slide_count}: {category_name.upper()} - SẮC THÁI & SỨC KHỎE\n"
            prompt += f"{'=' * 70}\n\n"
            
            sentiment_data = category_data_dict.get("sentiment", {})
            sentiment_prompt = build_masan_slide_prompt("slide_7_sentiment", sentiment_data)
            prompt += sentiment_prompt
            prompt += "\n"
            
            # Slide X+3: Category Trends
            slide_count += 1
            prompt += f"\n{'=' * 70}\n"
            prompt += f"SLIDE {slide_count}: {category_name.upper()} - XU HƯỚNG THẢO LUẬN\n"
            prompt += f"{'=' * 70}\n\n"
            
            trends_data = category_data_dict.get("trends", {})
            trends_prompt = build_masan_slide_prompt("slide_8_trends", trends_data)
            prompt += trends_prompt
            prompt += "\n"
    
    # Add footer
    prompt += "\n" + "=" * 70 + "\n"
    prompt += "HƯỚNG DẪN THIẾT KẾ CHUNG\n"
    prompt += "=" * 70 + "\n"
    prompt += "✓ Sử dụng màu xanh Masan #0045C4 làm màu chủ đạo\n"
    prompt += "✓ Font chữ: Arial/Helvetica, rõ ràng dễ đọc\n"
    prompt += "✓ Biểu đồ: Màu sắc nhất quán, có legend rõ ràng\n"
    prompt += "✓ Số liệu: Định dạng với dấu phân cách hàng nghìn\n"
    prompt += "✓ Layout: Cân đối, không quá tải thông tin\n"
    prompt += "✓ URL: Hiển thị dưới dạng hyperlink có thể click\n"
    prompt += "✓ Insight: Ngắn gọn, súc tích, có dẫn chứng\n\n"
    
    prompt += f"Tổng số slides: {slide_count}\n"
    prompt += f"Công cụ: Masan Weekly Report Generator v2.0\n"
    
    return prompt
