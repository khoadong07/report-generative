#!/usr/bin/env python3
"""
Slide 07 Category Sentiment Prompt Builder
Formats category sentiment and NSR analysis data into prompt
"""
from typing import Any, Dict
from weekly_report_masan.builders.base import BasePromptBuilder


class Slide07SentimentPromptBuilder(BasePromptBuilder):
    """Build prompt for Slide 7: Category Sentiment & Health Analysis."""

    def build(self, slide_data: Dict[str, Any], **kwargs) -> str:
        """
        Format slide 7 data into prompt.
        
        Args:
            slide_data: Dictionary containing:
                - title, subtitle, category_name
                - sentiment_nsr: List of sentiment data by brand with NSR
                - insight: Insight text
                - total_buzz: Total discussions
        
        Returns:
            Formatted prompt string
        """
        title = slide_data.get("title", "Sắc thái và chỉ số sức khỏe")
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
            "**Layout**: Biểu đồ full size hàng ngang, insight ở dưới",
            "",
            "---",
            "",
        ]
        
        # Sentiment + NSR Chart
        lines.extend([
            "## BIỂU ĐỒ: SẮC THÁI VÀ NSR THEO THƯƠNG HIỆU",
            "",
            "**Loại biểu đồ**: Stacked Column Chart + Line Chart (overlay)",
            "**Mô tả**:",
            "- Cột xếp chồng: % Sentiment (Positive, Neutral, Negative) cho từng thương hiệu",
            "- Đường: NSR (Net Sentiment Ratio) overlay trên cột",
            "- Trục X: Thương hiệu (Topic)",
            "- Trục Y trái: % Sentiment (0-100%)",
            "- Trục Y phải: NSR (-100 đến +100)",
            "",
        ])
        
        sentiment_nsr = slide_data.get("sentiment_nsr", [])
        
        if sentiment_nsr:
            lines.append("**Dữ liệu theo thương hiệu:**")
            lines.append("")
            lines.append("| Thương hiệu | Buzz | Positive | Neutral | Negative | NSR |")
            lines.append("|-------------|------|----------|---------|----------|-----|")
            
            for item in sentiment_nsr:
                brand = item["brand"]
                total = item["total"]
                pos_pct = item["positive_pct"]
                neu_pct = item["neutral_pct"]
                neg_pct = item["negative_pct"]
                nsr = item["nsr"]
                
                nsr_str = f"{nsr:+.1f}%" if nsr is not None else "N/A"
                
                lines.append(
                    f"| {brand} | {total:,} | {pos_pct}% | {neu_pct}% | {neg_pct}% | {nsr_str} |"
                )
            
            lines.append("")
            lines.append("**Công thức NSR**:")
            lines.append("```")
            lines.append("NSR = (Positive% - Negative%) / (Positive% + Negative%) × 100")
            lines.append("```")
            lines.append("")
            lines.append("**Giải thích**:")
            lines.append("- NSR > 0: Sentiment tích cực chiếm ưu thế")
            lines.append("- NSR = 0: Cân bằng giữa tích cực và tiêu cực")
            lines.append("- NSR < 0: Sentiment tiêu cực chiếm ưu thế")
            lines.append("- NSR càng cao càng tốt (max +100)")
            
        else:
            lines.append("Không có dữ liệu sentiment")
        
        lines.extend(["", "---", ""])
        
        # Insight
        lines.extend([
            "## INSIGHT & PHÂN TÍCH",
            "",
            "**Vị trí**: Dưới biểu đồ, full width",
            ""
        ])
        
        insight = slide_data.get("insight", "Không có insight")
        lines.append(insight)
        
        lines.extend(["", "---", ""])
        
        return "\n".join(lines)
