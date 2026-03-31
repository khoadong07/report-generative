#!/usr/bin/env python3
"""
Slide 03 - Chỉ số sức khỏe và kênh thảo luận Prompt Builder
"""
from typing import Any, Dict
from weekly_report_masan.builders.base import BasePromptBuilder


class Slide03HealthPromptBuilder(BasePromptBuilder):
    """Formats the health index and channel analysis slide prompt."""

    def build(self, s: Dict[str, Any], **kwargs) -> str:
        prompt = self._header("SLIDE 3 - CHỈ SỐ SỨC KHỎE VÀ KÊNH THẢO LUẬN")
        prompt += f"Tiêu đề: \"{s['title']}\"\n"
        prompt += f"Phụ đề: \"{s['subtitle']}\"\n\n"
        
        brands = s.get("brands", [])
        prompt += f"Các thương hiệu: {', '.join(brands)}\n"
        prompt += f"(Main brand: {brands[0] if brands else 'N/A'})\n\n"
        
        # ── LAYOUT OVERVIEW ───────────────────────────────────────────────────
        prompt += "BỐ CỤC SLIDE:\n"
        prompt += "=" * 70 + "\n"
        prompt += "PHẦN TRÁI (50%):\n"
        prompt += "  - TRÊN: Sắc thái thảo luận + NSR (Cột + Đường)\n"
        prompt += "  - DƯỚI: Tỉ trọng kênh thảo luận (Cột xếp chồng)\n\n"
        prompt += "PHẦN PHẢI (50%):\n"
        prompt += "  - TRÊN: Top nguồn thảo luận (Cột ngang)\n"
        prompt += "  - DƯỚI: Bảng chỉ số sức khỏe theo chủ đề\n\n"
        prompt += "PHẦN CUỐI: Insight (2 đoạn)\n\n"
        
        # ── CHART 1: SENTIMENT + NSR ──────────────────────────────────────────
        sentiment_nsr = s.get("sentiment_nsr", [])
        prompt += "=" * 70 + "\n"
        prompt += "CHART 1: SẮC THÁI THẢO LUẬN + NSR (Trái trên)\n"
        prompt += "=" * 70 + "\n"
        prompt += "Biểu đồ kết hợp: Cột xếp chồng (Sentiment) + Đường (NSR)\n"
        prompt += "Main brand luôn là cột đầu tiên\n\n"
        
        for item in sentiment_nsr:
            prompt += f"{item['brand']} (Tổng: {self.format_number(item['total'])}):\n"
            prompt += f"  - Positive: {item['positive_pct']}%\n"
            prompt += f"  - Neutral: {item['neutral_pct']}%\n"
            prompt += f"  - Negative: {item['negative_pct']}%\n"
            prompt += f"  - NSR: {item['nsr'] if item['nsr'] is not None else '-'}\n\n"
        
        prompt += "Lưu ý: NSR hiển thị dưới dạng đường nối các điểm trên mỗi cột\n\n"
        
        # ── CHART 2: CHANNEL DISTRIBUTION ─────────────────────────────────────
        channel_dist = s.get("channel_distribution", [])
        prompt += "=" * 70 + "\n"
        prompt += "CHART 2: TỈ TRỌNG KÊNH THẢO LUẬN (Trái dưới)\n"
        prompt += "=" * 70 + "\n"
        prompt += "Biểu đồ cột xếp chồng (Stacked Column)\n"
        prompt += "Main brand luôn đứng đầu\n\n"
        
        for item in channel_dist:
            prompt += f"{item['brand']} (Tổng: {self.format_number(item['total'])}):\n"
            for ch in item.get("channels", []):
                prompt += f"  - {ch['channel']}: {ch['percent']}%\n"
            prompt += "\n"
        
        # ── CHART 3: TOP SOURCES ──────────────────────────────────────────────
        top_sources = s.get("top_sources", [])
        prompt += "=" * 70 + "\n"
        prompt += "CHART 3: TOP NGUỒN THẢO LUẬN NỔI BẬT (Phải trên)\n"
        prompt += "=" * 70 + "\n"
        prompt += "Biểu đồ cột ngang (Horizontal Bar)\n"
        prompt += "Chỉ lấy từ đối thủ (không bao gồm main brand)\n"
        prompt += "Top 5 nguồn theo SiteName\n\n"
        
        if top_sources:
            for source in top_sources:
                prompt += f"{source['rank']}. {source['site_name']}: {self.format_number(source['buzz_count'])} buzz\n"
        else:
            prompt += "Không có dữ liệu\n"
        prompt += "\n"
        
        # ── TABLE: HEALTH INDEX ───────────────────────────────────────────────
        health_table = s.get("health_table", {})
        labels = health_table.get("labels", [])
        data = health_table.get("data", {})
        
        prompt += "=" * 70 + "\n"
        prompt += "BẢNG: CHỈ SỐ SỨC KHỎE THEO CHỦ ĐỀ (Phải dưới)\n"
        prompt += "=" * 70 + "\n"
        prompt += "Bảng NSR theo Labels1 (Top 5)\n"
        prompt += "Cột: Topic (brands)\n"
        prompt += "Dòng: Labels1\n"
        prompt += "Giá trị: NSR (hoặc '-' nếu không tính được)\n\n"
        
        if labels and data:
            # Header
            prompt += "Labels1".ljust(25) + " | " + " | ".join([b[:15].ljust(15) for b in brands]) + "\n"
            prompt += "-" * 70 + "\n"
            
            # Rows
            for label in labels:
                row = label[:25].ljust(25) + " | "
                values = []
                for brand in brands:
                    nsr = data.get(brand, {}).get(label)
                    if nsr is not None:
                        values.append(f"{nsr:+.1f}".ljust(15))
                    else:
                        values.append("-".ljust(15))
                row += " | ".join(values)
                prompt += row + "\n"
        else:
            prompt += "Không có dữ liệu Labels1\n"
        prompt += "\n"
        
        # ── INSIGHT ───────────────────────────────────────────────────────────
        prompt += "=" * 70 + "\n"
        prompt += "INSIGHT (2 đoạn, mỗi đoạn 25-30 từ)\n"
        prompt += "=" * 70 + "\n"
        prompt += f"{s.get('insight', 'N/A')}\n\n"
        
        # ── DESIGN GUIDELINES ─────────────────────────────────────────────────
        prompt += "=" * 70 + "\n"
        prompt += "HƯỚNG DẪN THIẾT KẾ\n"
        prompt += "=" * 70 + "\n"
        prompt += "MÀU SẮC:\n"
        prompt += "  - Sentiment: Positive (xanh lá), Neutral (xám), Negative (đỏ)\n"
        prompt += "  - NSR line: Màu đậm, nét liền, có markers\n"
        prompt += "  - Main brand: Màu xanh Masan #0045C4\n\n"
        prompt += "BIỂU ĐỒ:\n"
        prompt += "  - Cột xếp chồng: % trên từng phần, tổng ở đỉnh\n"
        prompt += "  - Đường NSR: Hiển thị giá trị tại mỗi điểm\n"
        prompt += "  - Cột ngang: Buzz count ở cuối thanh\n\n"
        prompt += "BẢNG:\n"
        prompt += "  - Header: Bold, nền màu nhạt\n"
        prompt += "  - NSR dương: Màu xanh\n"
        prompt += "  - NSR âm: Màu đỏ\n"
        prompt += "  - Không có dữ liệu: '-'\n\n"
        prompt += "INSIGHT:\n"
        prompt += "  - 2 đoạn riêng biệt\n"
        prompt += "  - Mỗi đoạn 25-30 từ\n"
        prompt += "  - Đặt trong khung nổi bật\n\n"
        
        return prompt
