"""
Slide 07 – Sắc thái và chỉ số sức khỏe của các nhãn hiệu (cho từng ngành hàng)
Sentiment analysis and NSR by brand for specific category
Chart: Stacked column (sentiment %) + Line (NSR) overlay
Input: df, category_name, week_start, week_end, llm_client
Output: slide data with combined chart and insight
"""
from typing import Any, Dict, List
import pandas as pd
from datetime import datetime

from core.llm_client import LLMClient
from weekly_report.slides.base import SlideGenerator, InsightMixin


class Slide07CategorySentiment(SlideGenerator, InsightMixin):
    """Generate sentiment and health analysis for a specific product category."""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    # ── public ────────────────────────────────────────────────────────────────
    def generate(self, *, df: pd.DataFrame, category_name: str,
                 week_start: datetime, week_end: datetime) -> Dict[str, Any]:
        """
        Generate slide for specific category with:
        1. Sentiment distribution by brand (stacked column + NSR line overlay)
        2. Insight about sentiment trends and health index
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
        
        # Calculate sentiment and NSR by brand (using Topic column)
        sentiment_nsr = self._calculate_sentiment_nsr(df_category)
        
        # Generate Insight
        insight = self._generate_insight(
            df_category=df_category,
            category_name=category_name,
            sentiment_nsr=sentiment_nsr
        )
        
        return {
            "title": f"Sắc thái và chỉ số sức khỏe của các nhãn hiệu - {category_name}",
            "subtitle": f"Giai đoạn: {week_start.strftime('%d/%m/%Y')} - {week_end.strftime('%d/%m/%Y')}",
            "category_name": category_name,
            "sentiment_nsr": sentiment_nsr,
            "insight": insight,
            "total_buzz": len(df_category),
        }

    def _empty_result(self, category: str, start: datetime, end: datetime) -> Dict[str, Any]:
        """Return empty result when no data."""
        return {
            "title": f"Sắc thái và chỉ số sức khỏe của các nhãn hiệu - {category}",
            "subtitle": f"Giai đoạn: {start.strftime('%d/%m/%Y')} - {end.strftime('%d/%m/%Y')}",
            "category_name": category,
            "sentiment_nsr": [],
            "insight": "Không có dữ liệu",
            "total_buzz": 0,
        }

    # ── Chart: Sentiment + NSR ────────────────────────────────────────────────
    def _calculate_sentiment_nsr(self, df: pd.DataFrame) -> List[Dict]:
        """Calculate sentiment distribution and NSR by brand (Topic)."""
        
        if "Topic" not in df.columns or "Sentiment" not in df.columns:
            return []
        
        # Get unique brands (Topics)
        brands = df["Topic"].dropna().unique().tolist()
        
        if not brands:
            return []
        
        result = []
        
        for brand in brands:
            df_brand = df[df["Topic"] == brand]
            total = len(df_brand)
            
            if total == 0:
                continue
            
            # Count by sentiment
            sentiment_counts = df_brand["Sentiment"].value_counts().to_dict()
            
            pos = sentiment_counts.get("Positive", 0)
            neu = sentiment_counts.get("Neutral", 0)
            neg = sentiment_counts.get("Negative", 0)
            
            pos_pct = round(pos / total * 100, 1) if total > 0 else 0
            neu_pct = round(neu / total * 100, 1) if total > 0 else 0
            neg_pct = round(neg / total * 100, 1) if total > 0 else 0
            
            # Calculate NSR
            nsr = None
            if (pos_pct + neg_pct) > 0:
                nsr = round((pos_pct - neg_pct) / (pos_pct + neg_pct) * 100, 1)
            
            result.append({
                "brand": brand,
                "total": total,
                "positive": pos,
                "neutral": neu,
                "negative": neg,
                "positive_pct": pos_pct,
                "neutral_pct": neu_pct,
                "negative_pct": neg_pct,
                "nsr": nsr
            })
        
        # Sort by total descending
        result.sort(key=lambda x: x["total"], reverse=True)
        
        return result

    # ── Insight Generation ────────────────────────────────────────────────────
    def _generate_insight(self, *, df_category: pd.DataFrame, category_name: str,
                          sentiment_nsr: List[Dict]) -> str:
        """Generate insight about sentiment trends and health index."""
        
        total_buzz = len(df_category)
        
        if not sentiment_nsr:
            return "Không có dữ liệu để phân tích."
        
        # Find best and worst NSR
        brands_with_nsr = [item for item in sentiment_nsr if item["nsr"] is not None]
        
        best_nsr = None
        worst_nsr = None
        
        if brands_with_nsr:
            best_nsr = max(brands_with_nsr, key=lambda x: x["nsr"])
            worst_nsr = min(brands_with_nsr, key=lambda x: x["nsr"])
        
        # Most discussed brand
        top_brand = sentiment_nsr[0] if sentiment_nsr else None
        
        # Average NSR
        avg_nsr = None
        if brands_with_nsr:
            avg_nsr = round(sum(item["nsr"] for item in brands_with_nsr) / len(brands_with_nsr), 1)
        
        # Build prompt
        prompt = f"""Viết insight ngắn gọn (60-80 từ) về sắc thái và sức khỏe thương hiệu trong ngành {category_name}:

DỮ LIỆU:
- Tổng thảo luận: {total_buzz:,}
- Số thương hiệu: {len(sentiment_nsr)}
- NSR trung bình: {avg_nsr if avg_nsr is not None else 'N/A'}

THƯƠNG HIỆU NỔI BẬT:
- Nhiều thảo luận nhất: {top_brand['brand'] if top_brand else 'N/A'} ({top_brand['total'] if top_brand else 0} buzz)
- NSR tốt nhất: {best_nsr['brand'] if best_nsr else 'N/A'} ({best_nsr['nsr']:+.1f}% NSR)
- NSR thấp nhất: {worst_nsr['brand'] if worst_nsr else 'N/A'} ({worst_nsr['nsr']:+.1f}% NSR)

PHÂN BỐ SENTIMENT:
{chr(10).join([f"- {item['brand']}: Pos {item['positive_pct']}% | Neu {item['neutral_pct']}% | Neg {item['negative_pct']}% | NSR {item['nsr']:+.1f}%" if item['nsr'] is not None else f"- {item['brand']}: Pos {item['positive_pct']}% | Neu {item['neutral_pct']}% | Neg {item['negative_pct']}%" for item in sentiment_nsr[:5]])}

Phân tích:
1. Đánh giá tổng quan sức khỏe ngành
2. So sánh các thương hiệu
3. Xu hướng sentiment
4. 1 khuyến nghị ngắn"""
        
        return self.llm_client.generate_insight(prompt)
