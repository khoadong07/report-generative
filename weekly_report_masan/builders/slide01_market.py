#!/usr/bin/env python3
"""
Slide 01 - Masan Consumer & Markets Prompt Builder
Formats a single comprehensive slide with all analysis
"""
from typing import Any, Dict
from weekly_report_masan.builders.base import BasePromptBuilder


class Slide01MarketPromptBuilder(BasePromptBuilder):
    """Formats the Masan Consumer & Markets slide as a single comprehensive slide."""

    def build(self, s: Dict[str, Any], **kwargs) -> str:
        prompt = self._header("SLIDE 1 - MASAN CONSUMER & MARKETS")
        prompt += f"Tiêu đề: \"{s['title']}\"\n"
        prompt += f"Phụ đề: \"{s['subtitle']}\"\n\n"
        
        # ── LAYOUT OVERVIEW ───────────────────────────────────────────────────
        prompt += "BỐ CỤC SLIDE (1 SLIDE DUY NHẤT):\n"
        prompt += "=" * 70 + "\n"
        prompt += "PHẦN TRÊN (40%):\n"
        prompt += "  - TRÁI: Xu hướng Buzz 4 tuần (biểu đồ cột)\n"
        prompt += "  - GIỮA: Sentiment tuần hiện tại (biểu đồ donut)\n"
        prompt += "  - PHẢI: Phân bổ Kênh (biểu đồ donut)\n\n"
        prompt += "PHẦN GIỮA (40%):\n"
        prompt += "  - TRÁI: Kênh thảo luận theo Brand (stacked column)\n"
        prompt += "  - PHẢI: Sắc thái theo Brand (stacked column)\n\n"
        prompt += "PHẦN DƯỚI (20%):\n"
        prompt += "  - Khung insight tổng quan và khuyến nghị\n\n"
        
        # ── PART 1: MAIN BRAND DATA ──────────────────────────────────────────
        part1 = s.get("part1_main_brand", {})
        prompt += "=" * 70 + "\n"
        prompt += f"DỮ LIỆU PHẦN 1: MAIN BRAND - {part1.get('brand', 'N/A')}\n"
        prompt += "=" * 70 + "\n\n"
        
        # 1.1 Weekly Buzz Trend
        prompt += "1. XU HƯỚNG BUZZ 4 TUẦN (Biểu đồ cột đứng - Trái trên)\n"
        for week_data in part1.get("weekly_buzz_trend", []):
            prompt += f"  {week_data['week']}: {self.format_number(week_data['buzz_count'])} buzz\n"
        prompt += "\n"
        
        # 1.2 Sentiment Distribution
        sentiment = part1.get("sentiment_distribution", {})
        prompt += "2. SENTIMENT TUẦN HIỆN TẠI (Donut - Giữa trên)\n"
        prompt += f"  Tổng (ở giữa donut): {self.format_number(sentiment.get('total_buzz', 0))}\n"
        prompt += f"  - Positive: {sentiment.get('positive', {}).get('count', 0)} ({sentiment.get('positive', {}).get('percent', 0)}%)\n"
        prompt += f"  - Neutral: {sentiment.get('neutral', {}).get('count', 0)} ({sentiment.get('neutral', {}).get('percent', 0)}%)\n"
        prompt += f"  - Negative: {sentiment.get('negative', {}).get('count', 0)} ({sentiment.get('negative', {}).get('percent', 0)}%)\n"
        prompt += "\n"
        
        # 1.3 Channel Distribution
        prompt += "3. PHÂN BỔ KÊNH (Donut - Phải trên)\n"
        for ch in part1.get("channel_distribution", []):
            prompt += f"  - {ch['channel']}: {self.format_number(ch['count'])} ({ch['percent']}%)\n"
        prompt += f"\nInsight kênh: {part1.get('channel_insight', 'N/A')}\n\n"
        
        # ── PART 2: COMPETITOR COMPARISON ────────────────────────────────────
        part2 = s.get("part2_competitors", {})
        brands = part2.get("brands", [])
        prompt += "=" * 70 + "\n"
        prompt += "DỮ LIỆU PHẦN 2: SO SÁNH ĐỐI THỦ\n"
        prompt += "=" * 70 + "\n"
        prompt += f"Brands: {', '.join(brands)} (Main brand đầu tiên)\n\n"
        
        # 2.1 Channel by Brand
        prompt += "4. KÊNH THEO BRAND (Stacked Column - Trái giữa)\n"
        prompt += "Mỗi cột = 1 brand, hiển thị % từng kênh\n\n"
        for brand_data in part2.get("channel_distribution", []):
            prompt += f"{brand_data['brand']} (Tổng: {self.format_number(brand_data['total'])}):\n"
            for ch in brand_data.get("channels", []):
                prompt += f"  {ch['channel']}: {ch['percent']}%\n"
            prompt += "\n"
        
        # 2.2 Sentiment by Brand
        prompt += "5. SẮC THÁI THEO BRAND (Stacked Column - Phải giữa)\n"
        prompt += "Mỗi cột = 1 brand, hiển thị % từng sentiment\n\n"
        for brand_data in part2.get("sentiment_distribution", []):
            prompt += f"{brand_data['brand']} (Tổng: {self.format_number(brand_data['total'])}):\n"
            for sent in brand_data.get("sentiments", []):
                prompt += f"  {sent['sentiment']}: {sent['percent']}%\n"
            prompt += "\n"
        
        # ── CONCLUSION ────────────────────────────────────────────────────────
        prompt += "=" * 70 + "\n"
        prompt += "6. ĐÚC KẾT VÀ KHUYẾN NGHỊ (Khung dưới cùng)\n"
        prompt += "=" * 70 + "\n"
        prompt += f"{s.get('conclusion', 'N/A')}\n\n"
        
        # ── DESIGN GUIDELINES ─────────────────────────────────────────────────
        prompt += "=" * 70 + "\n"
        prompt += "HƯỚNG DẪN THIẾT KẾ\n"
        prompt += "=" * 70 + "\n"
        prompt += "MÀU SẮC:\n"
        prompt += "  - Main brand: Xanh Masan #0045C4\n"
        prompt += "  - Đối thủ: Màu phân biệt (cam, xanh lá, tím...)\n"
        prompt += "  - Positive: Xanh lá #2A9D5C\n"
        prompt += "  - Neutral: Xám #ADB5BD\n"
        prompt += "  - Negative: Đỏ #E63946\n\n"
        prompt += "BIỂU ĐỒ:\n"
        prompt += "  - Cột đứng: Số liệu ở đỉnh cột\n"
        prompt += "  - Donut: Tổng số ở giữa, % trên từng phần\n"
        prompt += "  - Stacked column: % trên từng phần, tổng ở đỉnh\n\n"
        prompt += "LAYOUT:\n"
        prompt += "  - Font: Arial/Helvetica, rõ ràng\n"
        prompt += "  - Spacing: Cân đối, không quá tải\n"
        prompt += "  - Insight box: Nền nhạt, viền màu brand\n"
        prompt += "  - Tất cả nội dung trên 1 SLIDE DUY NHẤT\n\n"
        
        return prompt
