#!/usr/bin/env python3
"""
Slide 02 - Tổng quan thảo luận Prompt Builder
Formats the discussion overview slide with 3 charts
"""
from typing import Any, Dict
from weekly_report_masan.builders.base import BasePromptBuilder


class Slide02DiscussionPromptBuilder(BasePromptBuilder):
    """Formats the discussion overview slide prompt."""

    def build(self, s: Dict[str, Any], **kwargs) -> str:
        prompt = self._header("SLIDE 2 - TỔNG QUAN THẢO LUẬN")
        prompt += f"Tiêu đề: \"{s['title']}\"\n"
        prompt += f"Phụ đề: \"{s['subtitle']}\"\n\n"
        
        # ── LAYOUT OVERVIEW ───────────────────────────────────────────────────
        prompt += "BỐ CỤC SLIDE:\n"
        prompt += "=" * 70 + "\n"
        prompt += "PHẦN TRÊN (35%):\n"
        prompt += "  - TRÁI: Thị phần thảo luận (Biểu đồ Donut)\n"
        prompt += "  - PHẢI: So sánh tuần trước vs tuần này (Biểu đồ cột đôi)\n\n"
        prompt += "PHẦN DƯỚI (65%):\n"
        prompt += "  - Xu hướng thảo luận 2 tuần (Biểu đồ đường)\n"
        prompt += "  - Annotations tại các điểm peak với dẫn chứng\n\n"
        
        brands = s.get("brands", [])
        prompt += f"Các thương hiệu: {', '.join(brands)}\n\n"
        
        # ── CHART 1: MARKET SHARE ─────────────────────────────────────────────
        market_share = s.get("market_share", {})
        prompt += "=" * 70 + "\n"
        prompt += "CHART 1: THỊ PHẦN THẢO LUẬN (Donut - Trái trên)\n"
        prompt += "=" * 70 + "\n"
        prompt += f"Tổng thảo luận tuần này (hiển thị ở giữa donut): {self.format_number(market_share.get('total_discussions', 0))}\n\n"
        prompt += "Tỷ trọng theo thương hiệu (hiển thị % trên từng phần):\n"
        for share in market_share.get("shares", []):
            prompt += f"  - {share['brand']}: {self.format_number(share['count'])} ({share['percent']}%)\n"
        prompt += "\n"
        
        # ── CHART 2: WEEKLY COMPARISON ────────────────────────────────────────
        weekly_comp = s.get("weekly_comparison", [])
        prompt += "=" * 70 + "\n"
        prompt += "CHART 2: SO SÁNH TUẦN TRƯỚC VS TUẦN NÀY (Cột đôi - Phải trên)\n"
        prompt += "=" * 70 + "\n"
        prompt += "Mỗi thương hiệu có 2 cột: Tuần trước (màu nhạt) và Tuần này (màu đậm)\n\n"
        for comp in weekly_comp:
            change_icon = "↑" if comp['change_percent'] > 0 else "↓" if comp['change_percent'] < 0 else "→"
            prompt += f"{comp['brand']}:\n"
            prompt += f"  - Tuần trước: {self.format_number(comp['previous_week'])}\n"
            prompt += f"  - Tuần này: {self.format_number(comp['current_week'])}\n"
            prompt += f"  - Thay đổi: {change_icon} {comp['change_percent']:+.1f}%\n\n"
        
        # ── CHART 3: TREND LINES ──────────────────────────────────────────────
        trend_data = s.get("trend_lines", {})
        trends = trend_data.get("trends", {})
        peaks = trend_data.get("peak_annotations", {})
        
        prompt += "=" * 70 + "\n"
        prompt += "CHART 3: XU HƯỚNG THẢO LUẬN 2 TUẦN (Biểu đồ đường - Dưới)\n"
        prompt += "=" * 70 + "\n"
        prompt += "Mỗi thương hiệu là 1 đường, màu sắc phân biệt rõ ràng\n\n"
        
        for brand in brands:
            if brand in trends:
                prompt += f"{brand}:\n"
                trend_points = trends[brand]
                # Show first, middle, and last points
                if len(trend_points) > 0:
                    prompt += f"  Điểm đầu: {trend_points[0]['date']} = {trend_points[0]['count']}\n"
                if len(trend_points) > 2:
                    mid = len(trend_points) // 2
                    prompt += f"  Điểm giữa: {trend_points[mid]['date']} = {trend_points[mid]['count']}\n"
                if len(trend_points) > 0:
                    prompt += f"  Điểm cuối: {trend_points[-1]['date']} = {trend_points[-1]['count']}\n"
                
                # Peak annotation
                if brand in peaks:
                    peak = peaks[brand]
                    prompt += f"\n  📍 PEAK DAY: {peak['date']} ({self.format_number(peak['count'])} thảo luận)\n"
                    prompt += f"     Type: {peak['type']}\n"
                    prompt += f"     Nội dung: {peak['content']}\n"
                    prompt += f"     URL: {peak['url']}\n"
                prompt += "\n"
        
        # ── INSIGHT ───────────────────────────────────────────────────────────
        prompt += "=" * 70 + "\n"
        prompt += "INSIGHT NỔI BẬT\n"
        prompt += "=" * 70 + "\n"
        prompt += f"{s.get('insight', 'N/A')}\n\n"
        
        # ── DESIGN GUIDELINES ─────────────────────────────────────────────────
        prompt += "=" * 70 + "\n"
        prompt += "HƯỚNG DẪN THIẾT KẾ\n"
        prompt += "=" * 70 + "\n"
        prompt += "MÀU SẮC:\n"
        prompt += "  - Mỗi brand có 1 màu riêng, nhất quán trên cả 3 charts\n"
        prompt += "  - Donut: Màu phân biệt rõ ràng\n"
        prompt += "  - Cột đôi: Tuần trước (màu nhạt), Tuần này (màu đậm)\n"
        prompt += "  - Đường: Nét liền, độ dày 2-3px\n\n"
        prompt += "BIỂU ĐỒ:\n"
        prompt += "  - Donut: Tổng ở giữa, % trên từng phần\n"
        prompt += "  - Cột đôi: Số liệu ở đỉnh cột, % thay đổi bên cạnh\n"
        prompt += "  - Đường: Annotations tại peak points, có icon 📍\n\n"
        prompt += "ANNOTATIONS:\n"
        prompt += "  - Hiển thị tại điểm peak của mỗi đường\n"
        prompt += "  - Callout box với: Ngày, Type, Snippet nội dung\n"
        prompt += "  - URL dưới dạng hyperlink có thể click\n\n"
        prompt += "INSIGHT:\n"
        prompt += "  - Đặt trong khung nổi bật ở cuối slide\n"
        prompt += "  - Nền màu nhạt, viền màu brand\n"
        prompt += "  - Font size phù hợp, dễ đọc\n\n"
        
        return prompt
