#!/usr/bin/env python3
"""
Slide 04 Products Prompt Builder
Formats product category analysis data into prompt
"""
from typing import Any, Dict
from weekly_report_masan.builders.base import BasePromptBuilder


class Slide04ProductsPromptBuilder(BasePromptBuilder):
    """Build prompt for Slide 4: Masan Consumer Products."""

    def build(self, slide_data: Dict[str, Any], **kwargs) -> str:
        """
        Format slide 4 data into prompt.
        
        Args:
            slide_data: Dictionary containing:
                - title, subtitle
                - weekly_comparison: List of category comparisons
                - market_share: List of category market shares
                - trend_lines: Dict with trends and peak_annotations
                - overall_sentiment: Dict with sentiment stats and NSR
                - insight: Dict with positive/negative insights and evidence
                - categories: List of product categories
        
        Returns:
            Formatted prompt string
        """
        title = slide_data.get("title", "Sản phẩm Masan Consumer")
        subtitle = slide_data.get("subtitle", "")
        categories = slide_data.get("categories", [])
        
        lines = [
            f"# {title}",
            f"{subtitle}",
            "",
            "## 1. TỔNG THẢO LUẬN - So sánh tuần trước vs tuần này",
            ""
        ]
        
        # Weekly Comparison
        weekly_comp = slide_data.get("weekly_comparison", [])
        if weekly_comp:
            lines.append("| Ngành hàng | Tuần trước | Tuần này | Thay đổi |")
            lines.append("|------------|------------|----------|----------|")
            for item in weekly_comp:
                cat = item["category"]
                prev = item["previous_week"]
                curr = item["current_week"]
                change = item["change_percent"]
                change_str = f"{change:+.1f}%" if change != 0 else "0%"
                lines.append(f"| {cat} | {prev:,} | {curr:,} | {change_str} |")
        else:
            lines.append("Không có dữ liệu")
        
        lines.extend(["", "## 2. THỊ PHẦN THẢO LUẬN THEO NGÀNH HÀNG", ""])
        
        # Market Share
        market_share = slide_data.get("market_share", [])
        if market_share:
            lines.append("Sắp xếp từ lớn đến bé:")
            lines.append("")
            for idx, item in enumerate(market_share, 1):
                cat = item["category"]
                count = item["buzz_count"]
                pct = item["percent"]
                lines.append(f"{idx}. **{cat}**: {count:,} buzz ({pct}%)")
        else:
            lines.append("Không có dữ liệu")
        
        lines.extend(["", "## 3. XU HƯỚNG THẢO LUẬN (2 tuần)", ""])
        
        # Trend Lines
        trend_data = slide_data.get("trend_lines", {})
        trends = trend_data.get("trends", {})
        peaks = trend_data.get("peak_annotations", {})
        
        if trends:
            for category in categories:
                if category not in trends:
                    continue
                
                lines.append(f"### {category}")
                trend_points = trends[category]
                
                # Show trend data
                dates = [p["date"] for p in trend_points]
                counts = [p["count"] for p in trend_points]
                lines.append(f"Dates: {', '.join(dates)}")
                lines.append(f"Buzz: {', '.join(map(str, counts))}")
                
                # Peak annotation
                if category in peaks:
                    peak = peaks[category]
                    
                    # Safely get content (already processed in slide generator)
                    content = peak.get("content", "Không có nội dung")
                    url = peak.get("url", "")
                    
                    lines.append(f"**Peak Day**: {peak['date']} ({peak['count']} buzz)")
                    lines.append(f"Bài đăng nổi bật: {content}")
                    if url:
                        lines.append(f"Link: {url}")
                
                lines.append("")
        else:
            lines.append("Không có dữ liệu xu hướng")
        
        lines.extend(["", "## 4. SẮC THÁI THẢO LUẬN", ""])
        
        # Overall Sentiment
        sentiment = slide_data.get("overall_sentiment", {})
        if sentiment:
            total = sentiment.get("total", 0)
            pos_pct = sentiment.get("positive_pct", 0)
            neu_pct = sentiment.get("neutral_pct", 0)
            neg_pct = sentiment.get("negative_pct", 0)
            nsr = sentiment.get("nsr")
            
            lines.append(f"**Tổng thảo luận**: {total:,}")
            lines.append(f"- Positive: {pos_pct}%")
            lines.append(f"- Neutral: {neu_pct}%")
            lines.append(f"- Negative: {neg_pct}%")
            if nsr is not None:
                lines.append(f"- **NSR**: {nsr:+.1f}%")
        else:
            lines.append("Không có dữ liệu sentiment")
        
        lines.extend(["", "## 5. INSIGHT & PHÂN TÍCH", ""])
        
        # Insight
        insight = slide_data.get("insight", {})
        
        # Positive
        lines.append("### Điểm tích cực")
        pos_insight = insight.get("positive", "Không có insight")
        lines.append(pos_insight)
        
        pos_evidence = insight.get("positive_evidence", [])
        if pos_evidence:
            lines.append("")
            lines.append("**Dẫn chứng tích cực:**")
            for idx, ev in enumerate(pos_evidence, 1):
                lines.append(f"{idx}. \"{ev}\"")
        
        lines.append("")
        
        # Negative
        lines.append("### Điểm cần cải thiện")
        neg_insight = insight.get("negative", "Không có insight")
        lines.append(neg_insight)
        
        neg_evidence = insight.get("negative_evidence", [])
        if neg_evidence:
            lines.append("")
            lines.append("**Dẫn chứng tiêu cực:**")
            for idx, ev in enumerate(neg_evidence, 1):
                lines.append(f"{idx}. \"{ev}\"")
        
        lines.append("")
        lines.append("---")
        lines.append("")
        
        return "\n".join(lines)
