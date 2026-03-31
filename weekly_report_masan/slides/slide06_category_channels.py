"""
Slide 06 – Tổng quan thảo luận theo kênh (cho từng ngành hàng)
Analysis by channels for specific category
Charts: Top 5 sources, Channel distribution by brand
Input: df, category_name, week_start, week_end, llm_client
Output: slide data with 2 charts and 3-paragraph insight
"""
from typing import Any, Dict, List
import pandas as pd
from datetime import datetime

from core.llm_client import LLMClient
from weekly_report.slides.base import SlideGenerator, InsightMixin


# Channel mapping
CHANNEL_MAPPING = {
    "fbPageComment": "Fanpage",
    "fbPageTopic": "Fanpage",
    "fbGroupComment": "Facebook",
    "fbUserComment": "Facebook",
    "fbGroupTopic": "Facebook",
    "fbUserTopic": "Facebook",
    "forumComment": "Forum",
    "forumTopic": "Forum",
    "newsTopic": "News",
}


class Slide06CategoryChannels(SlideGenerator, InsightMixin):
    """Generate channel analysis for a specific product category."""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    # ── public ────────────────────────────────────────────────────────────────
    def generate(self, *, df: pd.DataFrame, category_name: str,
                 week_start: datetime, week_end: datetime) -> Dict[str, Any]:
        """
        Generate slide for specific category with:
        1. Top 5 sources by discussion (SiteName)
        2. Channel distribution by brand (Facebook, Fanpage, Forum, News, Khác)
        3. Insight (3 paragraphs about channel overview)
        """
        
        # Prepare dataframe
        df_clean = df.copy()
        df_clean["PublishedDate"] = pd.to_datetime(df_clean["PublishedDate"], errors="coerce")
        
        # Check if required columns exist
        if "Ngành hàng" not in df_clean.columns:
            return self._empty_result(category_name, week_start, week_end)
        
        # Filter by category and week
        df_category = df_clean[
            (df_clean["Ngành hàng"] == category_name) &
            (df_clean["PublishedDate"] >= week_start) & 
            (df_clean["PublishedDate"] <= week_end)
        ]
        
        if df_category.empty:
            return self._empty_result(category_name, week_start, week_end)
        
        # Map channels
        if "Type" in df_category.columns:
            df_category["Channel"] = df_category["Type"].map(CHANNEL_MAPPING).fillna("Khác")
        else:
            df_category["Channel"] = "Khác"
        
        # 1. Top 5 Sources
        top_sources = self._get_top_sources(df_category, top_n=5)
        
        # 2. Channel Distribution by Brand
        channel_distribution = self._calculate_channel_distribution(df_category)
        
        # 3. Generate Insight
        insight = self._generate_insight(
            df_category=df_category,
            category_name=category_name,
            top_sources=top_sources,
            channel_distribution=channel_distribution
        )
        
        return {
            "title": f"Tổng quan thảo luận theo kênh - {category_name}",
            "subtitle": f"Giai đoạn: {week_start.strftime('%d/%m/%Y')} - {week_end.strftime('%d/%m/%Y')}",
            "category_name": category_name,
            "top_sources": top_sources,
            "channel_distribution": channel_distribution,
            "insight": insight,
            "total_buzz": len(df_category),
        }

    def _empty_result(self, category: str, start: datetime, end: datetime) -> Dict[str, Any]:
        """Return empty result when no data."""
        return {
            "title": f"Tổng quan thảo luận theo kênh - {category}",
            "subtitle": f"Giai đoạn: {start.strftime('%d/%m/%Y')} - {end.strftime('%d/%m/%Y')}",
            "category_name": category,
            "top_sources": [],
            "channel_distribution": [],
            "insight": {
                "paragraph1": "Không có dữ liệu",
                "paragraph2": "Không có dữ liệu",
                "paragraph3": "Không có dữ liệu"
            },
            "total_buzz": 0,
        }

    # ── Chart 1: Top Sources ──────────────────────────────────────────────────
    def _get_top_sources(self, df: pd.DataFrame, top_n: int = 5) -> List[Dict]:
        """Get top N sources by discussion count (SiteName)."""
        
        if "SiteName" not in df.columns:
            return []
        
        # Filter out null values
        df_sources = df[df["SiteName"].notna()].copy()
        
        if df_sources.empty:
            return []
        
        source_counts = df_sources["SiteName"].value_counts().head(top_n).to_dict()
        
        result = []
        for rank, (source, count) in enumerate(source_counts.items(), 1):
            result.append({
                "rank": rank,
                "source": source,
                "buzz_count": count
            })
        
        return result

    # ── Chart 2: Channel Distribution by Brand ────────────────────────────────
    def _calculate_channel_distribution(self, df: pd.DataFrame) -> List[Dict]:
        """Calculate channel distribution by brand (Facebook, Fanpage, Forum, News, Khác)."""
        
        if "Brand" not in df.columns:
            return []
        
        # Get unique brands
        brands = df["Brand"].dropna().unique().tolist()
        
        if not brands:
            return []
        
        result = []
        
        for brand in brands:
            df_brand = df[df["Brand"] == brand]
            total = len(df_brand)
            
            if total == 0:
                continue
            
            # Count by channel
            channel_counts = df_brand["Channel"].value_counts().to_dict()
            
            channels = []
            for channel in ["Facebook", "Fanpage", "Forum", "News", "Khác"]:
                count = channel_counts.get(channel, 0)
                percent = round(count / total * 100, 1) if total > 0 else 0
                channels.append({
                    "channel": channel,
                    "count": count,
                    "percent": percent
                })
            
            result.append({
                "brand": brand,
                "total": total,
                "channels": channels
            })
        
        # Sort by total descending
        result.sort(key=lambda x: x["total"], reverse=True)
        
        return result

    # ── Insight Generation ────────────────────────────────────────────────────
    def _generate_insight(self, *, df_category: pd.DataFrame, category_name: str,
                          top_sources: List[Dict], channel_distribution: List[Dict]) -> Dict[str, str]:
        """Generate 3-paragraph insight about channel overview."""
        
        total_buzz = len(df_category)
        
        # Channel summary
        channel_counts = df_category["Channel"].value_counts().to_dict()
        top_channel = max(channel_counts.items(), key=lambda x: x[1]) if channel_counts else ("N/A", 0)
        least_channel = min(channel_counts.items(), key=lambda x: x[1]) if channel_counts else ("N/A", 0)
        
        # Top source
        top_source = top_sources[0] if top_sources else {"source": "N/A", "buzz_count": 0}
        
        # Brand with most diverse channels
        most_diverse_brand = None
        if channel_distribution:
            most_diverse_brand = max(
                channel_distribution,
                key=lambda x: sum(1 for ch in x["channels"] if ch["count"] > 0)
            )
        
        # Paragraph 1: Overall channel distribution
        para1_prompt = f"""Viết đoạn ngắn (25-30 từ) về tổng quan kênh thảo luận ngành {category_name}:

DỮ LIỆU:
- Tổng thảo luận: {total_buzz:,}
- Kênh nhiều nhất: {top_channel[0]} ({top_channel[1]:,} buzz)
- Kênh ít nhất: {least_channel[0]} ({least_channel[1]:,} buzz)

Phân tích xu hướng kênh chính."""
        
        # Paragraph 2: Top source analysis
        top_5_str = ", ".join([f"{s['source']} ({s['buzz_count']})" for s in top_sources[:3]]) if top_sources else "Không có"
        
        para2_prompt = f"""Viết đoạn ngắn (25-30 từ) về nguồn thảo luận nổi bật:

DỮ LIỆU:
- Nguồn top 1: {top_source['source']} ({top_source['buzz_count']:,} buzz)
- Top 3 nguồn: {top_5_str}

Đánh giá vai trò của các nguồn chính."""
        
        # Paragraph 3: Brand channel strategy
        brand_summary = ""
        if most_diverse_brand:
            brand_summary = f"{most_diverse_brand['brand']} ({most_diverse_brand['total']} buzz)"
        
        para3_prompt = f"""Viết đoạn ngắn (25-30 từ) về chiến lược kênh của các thương hiệu:

DỮ LIỆU:
- Số thương hiệu: {len(channel_distribution)}
- Thương hiệu đa dạng nhất: {brand_summary if brand_summary else 'N/A'}

Đưa ra 1 khuyến nghị về kênh."""
        
        paragraph1 = self.llm_client.generate_insight(para1_prompt)
        paragraph2 = self.llm_client.generate_insight(para2_prompt)
        paragraph3 = self.llm_client.generate_insight(para3_prompt)
        
        return {
            "paragraph1": paragraph1,
            "paragraph2": paragraph2,
            "paragraph3": paragraph3
        }
