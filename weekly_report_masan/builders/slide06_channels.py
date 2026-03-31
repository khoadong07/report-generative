#!/usr/bin/env python3
"""
Slide 06 Category Channels Prompt Builder
Formats category channel analysis data into prompt
"""
from typing import Any, Dict
from weekly_report_masan.builders.base import BasePromptBuilder


class Slide06ChannelsPromptBuilder(BasePromptBuilder):
    """Build prompt for Slide 6: Category Channel Analysis."""

    def build(self, slide_data: Dict[str, Any], **kwargs) -> str:
        """
        Format slide 6 data into prompt.
        
        Args:
            slide_data: Dictionary containing:
                - title, subtitle, category_name
                - top_sources: List of top 5 sources
                - channel_distribution: List of channel data by brand
                - insight: Dict with paragraph1, paragraph2, paragraph3
                - total_buzz: Total discussions
        
        Returns:
            Formatted prompt string
        """
        title = slide_data.get("title", "Tổng quan thảo luận theo kênh")
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
            "**Layout**: 2 charts trên cùng 1 hàng, insight ở dưới",
            "",
            "---",
            "",
        ]
        
        # Top Sources
        lines.extend([
            "## Chart 1: TOP NGUỒN THEO THẢO LUẬN",
            "",
            "**Vị trí**: Bên trái",
            "**Loại biểu đồ**: Horizontal bar chart",
            ""
        ])
        
        top_sources = slide_data.get("top_sources", [])
        
        if top_sources:
            lines.append("**Top 5 nguồn (cao đến thấp):**")
            lines.append("")
            lines.append("| # | Nguồn | Buzz |")
            lines.append("|---|-------|------|")
            for item in top_sources:
                rank = item["rank"]
                source = item["source"]
                count = item["buzz_count"]
                lines.append(f"| {rank} | {source} | {count:,} |")
        else:
            lines.append("Không có dữ liệu nguồn")
        
        lines.extend(["", "---", ""])
        
        # Channel Distribution
        lines.extend([
            "## Chart 2: TỈ TRỌNG THẢO LUẬN TRÊN CÁC KÊNH",
            "",
            "**Vị trí**: Bên phải",
            "**Loại biểu đồ**: Stacked column chart",
            "**Kênh hiển thị**: Facebook, Fanpage, Forum, News, Khác",
            ""
        ])
        
        channel_dist = slide_data.get("channel_distribution", [])
        
        if channel_dist:
            lines.append("**Phân bổ kênh theo thương hiệu:**")
            lines.append("")
            
            for brand_data in channel_dist:
                brand = brand_data["brand"]
                total = brand_data["total"]
                channels = brand_data["channels"]
                
                lines.append(f"### {brand} ({total:,} buzz)")
                lines.append("")
                
                for ch in channels:
                    channel = ch["channel"]
                    count = ch["count"]
                    pct = ch["percent"]
                    if count > 0:
                        lines.append(f"- **{channel}**: {count:,} ({pct}%)")
                
                lines.append("")
        else:
            lines.append("Không có dữ liệu kênh")
        
        lines.extend(["", "---", ""])
        
        # Insight
        lines.extend([
            "## INSIGHT & PHÂN TÍCH",
            "",
            "**Vị trí**: Dưới cùng, full width",
            ""
        ])
        
        insight = slide_data.get("insight", {})
        para1 = insight.get("paragraph1", "Không có insight")
        para2 = insight.get("paragraph2", "Không có insight")
        para3 = insight.get("paragraph3", "Không có insight")
        
        lines.append("### Đoạn 1: Tổng quan kênh")
        lines.append(para1)
        lines.append("")
        
        lines.append("### Đoạn 2: Nguồn nổi bật")
        lines.append(para2)
        lines.append("")
        
        lines.append("### Đoạn 3: Chiến lược kênh & Khuyến nghị")
        lines.append(para3)
        
        lines.extend(["", "---", ""])
        
        return "\n".join(lines)
