#!/usr/bin/env python3
"""
Slide 05 Category Detail Prompt Builder
Formats category-specific analysis data into prompt
"""
from typing import Any, Dict
from weekly_report_masan.builders.base import BasePromptBuilder


class Slide05CategoryPromptBuilder(BasePromptBuilder):
    """Build prompt for Slide 5: Category Detail Analysis."""

    def build(self, slide_data: Dict[str, Any], **kwargs) -> str:
        """
        Format slide 5 data into prompt.
        
        Args:
            slide_data: Dictionary containing:
                - title, subtitle, category_name
                - brand_sov: Dict with total and brands list
                - cate_distribution: List of product categories
                - top_products: List of top 10 products
                - insight: Dict with paragraph1 and paragraph2
                - total_buzz: Total discussions
        
        Returns:
            Formatted prompt string
        """
        title = slide_data.get("title", "Tổng quan thảo luận ngành")
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
        
        # Brand SOV
        lines.extend([
            "## 1. THỊ PHẦN THẢO LUẬN CỦA CÁC THƯƠNG HIỆU",
            "",
            "**Loại biểu đồ**: Donut chart (tổng thảo luận ở giữa)",
            ""
        ])
        
        brand_sov = slide_data.get("brand_sov", {})
        brands = brand_sov.get("brands", [])
        
        if brands:
            lines.append("**Share of Voice (SOV) theo thương hiệu:**")
            lines.append("")
            lines.append("| Thứ hạng | Thương hiệu | Buzz | % |")
            lines.append("|----------|-------------|------|---|")
            for idx, brand in enumerate(brands, 1):
                name = brand["brand"]
                count = brand["buzz_count"]
                pct = brand["percent"]
                lines.append(f"| {idx} | {name} | {count:,} | {pct}% |")
            lines.append("")
            lines.append(f"**Tổng**: {brand_sov.get('total', 0):,} thảo luận")
        else:
            lines.append("Không có dữ liệu thương hiệu")
        
        lines.extend(["", "---", ""])
        
        # Cate Distribution
        lines.extend([
            "## 2. THỊ PHẦN THẢO LUẬN THEO NHÓM SẢN PHẨM",
            "",
            "**Loại biểu đồ**: Pie chart",
            ""
        ])
        
        cate_dist = slide_data.get("cate_distribution", [])
        
        if cate_dist:
            lines.append("**Phân bố theo Cate:**")
            lines.append("")
            for idx, item in enumerate(cate_dist, 1):
                cate = item["cate"]
                count = item["buzz_count"]
                pct = item["percent"]
                lines.append(f"{idx}. **{cate}**: {count:,} buzz ({pct}%)")
        else:
            lines.append("Không có dữ liệu nhóm sản phẩm")
        
        lines.extend(["", "---", ""])
        
        # Top Products
        lines.extend([
            "## 3. TOP SẢN PHẨM THEO LƯỢNG THẢO LUẬN",
            "",
            "**Top 10 sản phẩm được thảo luận nhiều nhất:**",
            ""
        ])
        
        top_products = slide_data.get("top_products", [])
        
        if top_products:
            lines.append("| # | Sản phẩm | Buzz |")
            lines.append("|---|----------|------|")
            for item in top_products:
                rank = item["rank"]
                product = item["product"]
                count = item["buzz_count"]
                lines.append(f"| {rank} | {product} | {count:,} |")
        else:
            lines.append("Không có dữ liệu sản phẩm")
        
        lines.extend(["", "---", ""])
        
        # Insight
        lines.extend([
            "## 4. INSIGHT & PHÂN TÍCH",
            ""
        ])
        
        insight = slide_data.get("insight", {})
        para1 = insight.get("paragraph1", "Không có insight")
        para2 = insight.get("paragraph2", "Không có insight")
        
        lines.append("### Vị thế thị trường")
        lines.append(para1)
        lines.append("")
        
        lines.append("### Hiệu suất sản phẩm & Khuyến nghị")
        lines.append(para2)
        
        lines.extend(["", "---", ""])
        
        return "\n".join(lines)
