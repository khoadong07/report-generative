#!/usr/bin/env python3
"""
Slide 08 Category Trends Prompt Builder
Formats category trend analysis data into prompt
"""
from typing import Any, Dict
from weekly_report_masan.builders.base import BasePromptBuilder


class Slide08TrendsPromptBuilder(BasePromptBuilder):
    """Build prompt for Slide 8: Category Trend Analysis."""

    def build(self, slide_data: Dict[str, Any], **kwargs) -> str:
        """
        Format slide 8 data into prompt.
        
        Args:
            slide_data: Dictionary containing:
                - title, subtitle, category_name
                - trends: Dict of daily trends by brand
                - peak_annotations: Dict of peak info by brand
                - insight: Insight text
                - total_buzz: Total discussions
        
        Returns:
            Formatted prompt string
        """
        title = slide_data.get("title", "Xu hướng thảo luận")
        subtitle = slide_data.get("subtitle", "")
        category = slide_data.get("category_name", "")
        total_buzz = slide_data.get("total_buzz", 0)
        
        lines = [
            f"# {title}",
            f"{subtitle}",
            "",
            f"**Ngành hàng**: {category}",
            f"**Tổng thảo luận**: {total_buzz:,}",
            "",
            "---",
            "",
        ]
        
        # Trend Lines
        lines.extend([
            "## BIỂU ĐỒ: XU HƯỚNG THẢO LUẬN THEO NGÀY",
            "",
            "**Loại biểu đồ**: Line Chart",
            "**Mô tả**:",
            "- Mỗi đường: 1 thương hiệu (Topic)",
            "- Trục X: Ngày (dd/mm)",
            "- Trục Y: Số lượng thảo luận",
            "- Điểm peak: Highlight với annotation",
            "",
        ])
        
        trends = slide_data.get("trends", {})
        peaks = slide_data.get("peak_annotations", {})
        
        if trends:
            lines.append("**Dữ liệu xu hướng theo thương hiệu:**")
            lines.append("")
            
            for brand, trend_points in trends.items():
                lines.append(f"### {brand}")
                lines.append("")
                
                # Show trend data
                dates = [p["date"] for p in trend_points]
                counts = [p["count"] for p in trend_points]
                
                lines.append(f"**Dates**: {', '.join(dates)}")
                lines.append(f"**Buzz**: {', '.join(map(str, counts))}")
                lines.append("")
                
                # Peak annotation
                if brand in peaks:
                    peak = peaks[brand]
                    lines.append(f"**Peak Day**: {peak['date']} ({peak['count']} buzz)")
                    lines.append(f"**Type**: {peak['type']}")
                    lines.append(f"**Content**: {peak['content']}")
                    if peak['url']:
                        lines.append(f"**Link**: {peak['url']}")
                    lines.append("")
                else:
                    lines.append("*Không có peak nổi bật*")
                    lines.append("")
        else:
            lines.append("Không có dữ liệu xu hướng")
        
        lines.extend(["", "---", ""])
        
        # Insight
        lines.extend([
            "## INSIGHT & PHÂN TÍCH",
            "",
        ])
        
        insight = slide_data.get("insight", "Không có insight")
        lines.append(insight)
        
        lines.extend(["", "---", ""])
        
        return "\n".join(lines)
