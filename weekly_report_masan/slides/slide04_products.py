"""
Slide 04 – Sản phẩm Masan Consumer
Analysis by "Ngành hàng" (Product categories)
Charts: Weekly comparison, Market share, Trend lines, Overall sentiment
Input: df, current_week_start, current_week_end, previous_week_start, previous_week_end, llm_client
Output: slide data with 4 charts and 2-part insight with evidence
"""
from typing import Any, Dict, List, Tuple
import pandas as pd
from datetime import datetime, timedelta

from core.llm_client import LLMClient
from weekly_report.slides.base import SlideGenerator, InsightMixin


class Slide04Products(SlideGenerator, InsightMixin):
    """Generate Masan Consumer products analysis by category."""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    # ── public ────────────────────────────────────────────────────────────────
    def generate(self, *, df: pd.DataFrame,
                 current_week_start: datetime, current_week_end: datetime,
                 previous_week_start: datetime, previous_week_end: datetime) -> Dict[str, Any]:
        """
        Generate slide with:
        1. Weekly comparison by category
        2. Market share by category
        3. Trend lines with peak annotations
        4. Overall sentiment + NSR
        5. Insight (2 parts: positive + negative with evidence)
        """
        
        # Prepare dataframe
        df_clean = df.copy()
        df_clean["PublishedDate"] = pd.to_datetime(df_clean["PublishedDate"], errors="coerce")
        
        # Check if Ngành hàng column exists
        if "Ngành hàng" not in df_clean.columns:
            return self._empty_result(current_week_start, current_week_end)
        
        # Get categories
        categories = df_clean["Ngành hàng"].dropna().unique().tolist()
        if not categories:
            return self._empty_result(current_week_start, current_week_end)
        
        # Filter data for current and previous week
        df_curr = df_clean[
            (df_clean["PublishedDate"] >= current_week_start) & 
            (df_clean["PublishedDate"] <= current_week_end)
        ]
        df_prev = df_clean[
            (df_clean["PublishedDate"] >= previous_week_start) & 
            (df_clean["PublishedDate"] <= previous_week_end)
        ]
        
        # 1. Weekly Comparison
        weekly_comparison = self._calculate_weekly_comparison(df_prev, df_curr, categories)
        
        # 2. Market Share
        market_share = self._calculate_market_share(df_curr, categories)
        
        # 3. Trend Lines (2 weeks)
        trend_data = self._calculate_trends(
            df_clean, categories, previous_week_start, current_week_end
        )
        
        # 4. Overall Sentiment
        overall_sentiment = self._calculate_overall_sentiment(df_curr)
        
        # 5. Generate Insight with Evidence
        insight = self._generate_insight(
            df_curr=df_curr,
            weekly_comparison=weekly_comparison,
            market_share=market_share,
            overall_sentiment=overall_sentiment
        )
        
        return {
            "title": "Sản phẩm Masan Consumer",
            "subtitle": f"Giai đoạn: {current_week_start.strftime('%d/%m/%Y')} - {current_week_end.strftime('%d/%m/%Y')}",
            "weekly_comparison": weekly_comparison,
            "market_share": market_share,
            "trend_lines": trend_data,
            "overall_sentiment": overall_sentiment,
            "insight": insight,
            "categories": categories,
        }

    def _empty_result(self, start: datetime, end: datetime) -> Dict[str, Any]:
        """Return empty result when no data."""
        return {
            "title": "Sản phẩm Masan Consumer",
            "subtitle": f"Giai đoạn: {start.strftime('%d/%m/%Y')} - {end.strftime('%d/%m/%Y')}",
            "weekly_comparison": [],
            "market_share": [],
            "trend_lines": {"trends": {}, "peak_annotations": {}},
            "overall_sentiment": {},
            "insight": {"positive": "Không có dữ liệu", "negative": "Không có dữ liệu"},
            "categories": [],
        }

    # ── Chart 1: Weekly Comparison ────────────────────────────────────────────
    def _calculate_weekly_comparison(self, df_prev: pd.DataFrame, 
                                      df_curr: pd.DataFrame, 
                                      categories: List[str]) -> List[Dict]:
        """Compare previous week vs current week by category."""
        result = []
        
        for category in categories:
            prev_count = len(df_prev[df_prev["Ngành hàng"] == category])
            curr_count = len(df_curr[df_curr["Ngành hàng"] == category])
            
            change = ((curr_count - prev_count) / prev_count * 100) if prev_count > 0 else 0
            
            result.append({
                "category": category,
                "previous_week": prev_count,
                "current_week": curr_count,
                "change_percent": round(change, 1)
            })
        
        return result

    # ── Chart 2: Market Share ─────────────────────────────────────────────────
    def _calculate_market_share(self, df: pd.DataFrame, categories: List[str]) -> List[Dict]:
        """Calculate market share by category (sorted by total buzz)."""
        result = []
        total = len(df)
        
        for category in categories:
            count = len(df[df["Ngành hàng"] == category])
            percent = round(count / total * 100, 1) if total > 0 else 0
            
            result.append({
                "category": category,
                "buzz_count": count,
                "percent": percent
            })
        
        # Sort by buzz_count descending
        result.sort(key=lambda x: x["buzz_count"], reverse=True)
        
        return result

    # ── Chart 3: Trend Lines ──────────────────────────────────────────────────
    def _calculate_trends(self, df: pd.DataFrame, categories: List[str],
                          start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Calculate daily trends with peak annotations."""
        
        df_period = df[
            (df["PublishedDate"] >= start_date) & 
            (df["PublishedDate"] <= end_date)
        ].copy()
        
        trends = {}
        peak_annotations = {}
        
        # Get all dates in range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        for category in categories:
            df_cat = df_period[df_period["Ngành hàng"] == category].copy()
            
            if df_cat.empty:
                continue
            
            # Group by date
            df_cat["Date"] = df_cat["PublishedDate"].dt.date
            daily_counts = df_cat.groupby("Date").size().reset_index(name="count")
            
            # Fill missing dates with 0
            trend_data = []
            for date in date_range:
                date_obj = date.date()
                count = daily_counts[daily_counts["Date"] == date_obj]["count"].values
                count = int(count[0]) if len(count) > 0 else 0
                trend_data.append({
                    "date": date.strftime("%d/%m"),
                    "count": count
                })
            
            trends[category] = trend_data
            
            # Find peak day
            if not daily_counts.empty:
                peak_date = daily_counts.loc[daily_counts["count"].idxmax(), "Date"]
                peak_count = int(daily_counts["count"].max())
                
                # Get evidence from peak day (Type = Topic)
                df_peak = df_cat[df_cat["Date"] == peak_date]
                df_topics = df_peak[df_peak["Type"].str.endswith("Topic", na=False)]
                
                if not df_topics.empty:
                    top_topic = df_topics.iloc[0]
                    
                    # Safely get content
                    content = top_topic.get("Content", "")
                    if pd.isna(content) or not isinstance(content, str):
                        content = top_topic.get("Title", "")
                    if pd.isna(content) or not isinstance(content, str):
                        content = "Không có nội dung"
                    else:
                        content = str(content)[:200]
                    
                    # Safely get URL
                    url = top_topic.get("UrlTopic", "")
                    if pd.isna(url):
                        url = ""
                    
                    peak_annotations[category] = {
                        "date": peak_date.strftime("%d/%m/%Y"),
                        "count": peak_count,
                        "content": content,
                        "url": str(url)
                    }
        
        return {
            "trends": trends,
            "peak_annotations": peak_annotations
        }

    # ── Chart 4: Overall Sentiment ────────────────────────────────────────────
    def _calculate_overall_sentiment(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate overall sentiment across all categories."""
        
        total = len(df)
        if total == 0:
            return {
                "total": 0,
                "positive": 0,
                "neutral": 0,
                "negative": 0,
                "positive_pct": 0,
                "neutral_pct": 0,
                "negative_pct": 0,
                "nsr": None
            }
        
        sentiment_counts = df["Sentiment"].value_counts().to_dict()
        pos = sentiment_counts.get("Positive", 0)
        neu = sentiment_counts.get("Neutral", 0)
        neg = sentiment_counts.get("Negative", 0)
        
        pos_pct = round(pos / total * 100, 1)
        neu_pct = round(neu / total * 100, 1)
        neg_pct = round(neg / total * 100, 1)
        
        # Calculate NSR
        nsr = None
        if (pos_pct + neg_pct) > 0:
            nsr = round((pos_pct - neg_pct) / (pos_pct + neg_pct) * 100, 1)
        
        return {
            "total": total,
            "positive": pos,
            "neutral": neu,
            "negative": neg,
            "positive_pct": pos_pct,
            "neutral_pct": neu_pct,
            "negative_pct": neg_pct,
            "nsr": nsr
        }

    # ── Insight Generation ────────────────────────────────────────────────────
    def _generate_insight(self, *, df_curr: pd.DataFrame, weekly_comparison: List[Dict],
                          market_share: List[Dict], overall_sentiment: Dict) -> Dict[str, str]:
        """Generate 2-part insight with evidence (positive + negative)."""
        
        # Get positive comments (Type = Comment)
        df_pos = df_curr[
            (df_curr["Sentiment"] == "Positive") & 
            (df_curr["Type"].str.contains("Comment", na=False))
        ]
        positive_evidence = []
        if not df_pos.empty:
            samples = df_pos.sample(min(5, len(df_pos)))
            for _, row in samples.iterrows():
                content = row.get("Content", "")
                if pd.notna(content) and isinstance(content, str) and len(content.strip()) > 10:
                    positive_evidence.append(str(content)[:150])
        
        # Get negative comments (Type = Comment)
        df_neg = df_curr[
            (df_curr["Sentiment"] == "Negative") & 
            (df_curr["Type"].str.contains("Comment", na=False))
        ]
        negative_evidence = []
        if not df_neg.empty:
            samples = df_neg.sample(min(5, len(df_neg)))
            for _, row in samples.iterrows():
                content = row.get("Content", "")
                if pd.notna(content) and isinstance(content, str) and len(content.strip()) > 10:
                    negative_evidence.append(str(content)[:150])
        
        # Top category
        top_cat = market_share[0]["category"] if market_share else "N/A"
        
        # Positive insight
        pos_prompt = f"""Viết insight về điểm tích cực của Masan Consumer:

DỮ LIỆU:
- NSR: {overall_sentiment.get('nsr', 'N/A')}
- Positive: {overall_sentiment.get('positive_pct', 0)}%
- Ngành hàng nổi bật: {top_cat}

BÌNH LUẬN TÍCH CỰC MẪU:
{chr(10).join([f"- {e}" for e in positive_evidence[:4]]) if positive_evidence else "Không có"}

Viết 1 đoạn ngắn (40-50 từ) về điểm mạnh và phản hồi tích cực."""
        
        # Negative insight
        neg_prompt = f"""Viết insight về điểm cần cải thiện của Masan Consumer:

DỮ LIỆU:
- Negative: {overall_sentiment.get('negative_pct', 0)}%

BÌNH LUẬN TIÊU CỰC MẪU:
{chr(10).join([f"- {e}" for e in negative_evidence[:4]]) if negative_evidence else "Không có"}

Viết 1 đoạn ngắn (40-50 từ) về vấn đề và khuyến nghị cải thiện."""
        
        positive_insight = self.llm_client.generate_insight(pos_prompt)
        negative_insight = self.llm_client.generate_insight(neg_prompt)
        
        return {
            "positive": positive_insight,
            "negative": negative_insight,
            "positive_evidence": positive_evidence[:4],
            "negative_evidence": negative_evidence[:4]
        }
