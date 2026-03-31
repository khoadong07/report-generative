"""
Slide 02 – Tổng quan thảo luận
3 charts: Market share (donut), Weekly comparison (double column), Trend line (with peak annotations)
+ LLM Insight
Input: df, brands, current_week_start, current_week_end, previous_week_start, previous_week_end, llm_client
Output: slide data with 3 charts and insight
"""
from typing import Any, Dict, List, Tuple
import pandas as pd
from datetime import datetime, timedelta

from core.llm_client import LLMClient
from weekly_report.slides.base import SlideGenerator, InsightMixin


class Slide02DiscussionOverview(SlideGenerator, InsightMixin):
    """Generate discussion overview slide with market share, comparison, and trends."""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    # ── public ────────────────────────────────────────────────────────────────
    def generate(self, *, df: pd.DataFrame, brands: List[str],
                 current_week_start: datetime, current_week_end: datetime,
                 previous_week_start: datetime, previous_week_end: datetime) -> Dict[str, Any]:
        """
        Generate slide with 3 charts:
        1. Market share (donut chart)
        2. Weekly comparison (double column chart)
        3. Trend lines with peak annotations
        """
        
        # Prepare dataframe
        df_clean = df.copy()
        df_clean["PublishedDate"] = pd.to_datetime(df_clean["PublishedDate"], errors="coerce")
        
        # Filter for brands
        df_brands = df_clean[df_clean["Topic"].isin(brands)].copy()
        
        # 1. Market Share (current week)
        market_share = self._calculate_market_share(
            df_brands, current_week_start, current_week_end, brands
        )
        
        # 2. Weekly Comparison (previous vs current)
        weekly_comparison = self._calculate_weekly_comparison(
            df_brands, brands,
            previous_week_start, previous_week_end,
            current_week_start, current_week_end
        )
        
        # 3. Trend Lines with Peak Annotations
        trend_data = self._calculate_trend_lines(
            df_brands, brands,
            previous_week_start, current_week_end
        )
        
        # 4. Generate Insight
        insight = self._generate_insight(
            market_share=market_share,
            weekly_comparison=weekly_comparison,
            trend_data=trend_data,
            brands=brands
        )
        
        return {
            "title": "Tổng quan thảo luận",
            "subtitle": f"Giai đoạn: {current_week_start.strftime('%d/%m/%Y')} - {current_week_end.strftime('%d/%m/%Y')}",
            "market_share": market_share,
            "weekly_comparison": weekly_comparison,
            "trend_lines": trend_data,
            "insight": insight,
            "brands": brands,
        }

    # ── Chart 1: Market Share ─────────────────────────────────────────────────
    def _calculate_market_share(self, df: pd.DataFrame, 
                                 start_date: datetime, end_date: datetime,
                                 brands: List[str]) -> Dict[str, Any]:
        """Calculate market share for current week (donut chart)."""
        
        # Filter current week
        df_week = df[
            (df["PublishedDate"] >= start_date) & 
            (df["PublishedDate"] <= end_date)
        ]
        
        total_discussions = len(df_week)
        
        # Calculate share by brand
        shares = []
        for brand in brands:
            count = len(df_week[df_week["Topic"] == brand])
            percent = round(count / total_discussions * 100, 1) if total_discussions > 0 else 0
            shares.append({
                "brand": brand,
                "count": count,
                "percent": percent
            })
        
        return {
            "total_discussions": total_discussions,
            "shares": shares
        }

    # ── Chart 2: Weekly Comparison ────────────────────────────────────────────
    def _calculate_weekly_comparison(self, df: pd.DataFrame, brands: List[str],
                                      prev_start: datetime, prev_end: datetime,
                                      curr_start: datetime, curr_end: datetime) -> List[Dict]:
        """Calculate weekly comparison (double column chart)."""
        
        df_prev = df[
            (df["PublishedDate"] >= prev_start) & 
            (df["PublishedDate"] <= prev_end)
        ]
        
        df_curr = df[
            (df["PublishedDate"] >= curr_start) & 
            (df["PublishedDate"] <= curr_end)
        ]
        
        comparison = []
        for brand in brands:
            prev_count = len(df_prev[df_prev["Topic"] == brand])
            curr_count = len(df_curr[df_curr["Topic"] == brand])
            
            change = ((curr_count - prev_count) / prev_count * 100) if prev_count > 0 else 0
            
            comparison.append({
                "brand": brand,
                "previous_week": prev_count,
                "current_week": curr_count,
                "change_percent": round(change, 1)
            })
        
        return comparison

    # ── Chart 3: Trend Lines with Peaks ───────────────────────────────────────
    def _calculate_trend_lines(self, df: pd.DataFrame, brands: List[str],
                                start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Calculate daily trend lines and identify peak days with evidence."""
        
        # Filter date range (2 weeks)
        df_period = df[
            (df["PublishedDate"] >= start_date) & 
            (df["PublishedDate"] <= end_date)
        ].copy()
        
        # Calculate daily counts for each brand
        trends = {}
        peak_annotations = {}
        
        for brand in brands:
            df_brand = df_period[df_period["Topic"] == brand].copy()
            
            # Group by date
            df_brand["Date"] = df_brand["PublishedDate"].dt.date
            daily_counts = df_brand.groupby("Date").size().reset_index(name="count")
            
            # Convert to list of dicts
            trend_data = []
            for _, row in daily_counts.iterrows():
                trend_data.append({
                    "date": row["Date"].strftime("%d/%m"),
                    "count": int(row["count"])
                })
            
            trends[brand] = trend_data
            
            # Find peak day
            if not daily_counts.empty:
                peak_date = daily_counts.loc[daily_counts["count"].idxmax(), "Date"]
                peak_count = int(daily_counts["count"].max())
                
                # Get evidence from peak day
                df_peak = df_brand[df_brand["Date"] == peak_date]
                
                # Get topics (Type ending with "Topic")
                df_topics = df_peak[df_peak["Type"].str.endswith("Topic", na=False)]
                
                if not df_topics.empty:
                    # Get top topic by engagement or just first one
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
                    
                    # Safely get Type
                    type_val = top_topic.get("Type", "")
                    if pd.isna(type_val):
                        type_val = ""
                    
                    peak_annotations[brand] = {
                        "date": peak_date.strftime("%d/%m/%Y"),
                        "count": peak_count,
                        "content": content,
                        "url": str(url),
                        "type": str(type_val)
                    }
                else:
                    # No topic found, use any post
                    if not df_peak.empty:
                        sample = df_peak.iloc[0]
                        
                        # Safely get content
                        content = sample.get("Content", "")
                        if pd.isna(content) or not isinstance(content, str):
                            content = sample.get("Title", "")
                        if pd.isna(content) or not isinstance(content, str):
                            content = "Không có nội dung"
                        else:
                            content = str(content)[:200]
                        
                        # Safely get URL
                        url = sample.get("UrlTopic", sample.get("UrlComment", ""))
                        if pd.isna(url):
                            url = ""
                        
                        # Safely get Type
                        type_val = sample.get("Type", "")
                        if pd.isna(type_val):
                            type_val = ""
                        
                        peak_annotations[brand] = {
                            "date": peak_date.strftime("%d/%m/%Y"),
                            "count": peak_count,
                            "content": content,
                            "url": str(url),
                            "type": str(type_val)
                        }
        
        return {
            "trends": trends,
            "peak_annotations": peak_annotations
        }

    # ── Insight Generation ────────────────────────────────────────────────────
    def _generate_insight(self, *, market_share: Dict, weekly_comparison: List[Dict],
                          trend_data: Dict, brands: List[str]) -> str:
        """Generate LLM insight about discussion overview."""
        
        # Prepare summary data
        total_discussions = market_share.get("total_discussions", 0)
        
        # Top brand by market share
        shares = market_share.get("shares", [])
        top_brand = shares[0] if shares else {"brand": "N/A", "percent": 0}
        
        # Biggest growth
        growth_list = sorted(weekly_comparison, key=lambda x: x["change_percent"], reverse=True)
        top_growth = growth_list[0] if growth_list else {"brand": "N/A", "change_percent": 0}
        
        # Peak info
        peaks = trend_data.get("peak_annotations", {})
        peak_summary = []
        for brand, peak in peaks.items():
            peak_summary.append(f"{brand}: {peak['date']} ({peak['count']} buzz)")
        
        prompt = f"""Phân tích tổng quan thảo luận:

TỔNG QUAN:
- Tổng thảo luận tuần này: {total_discussions}
- Thị phần lớn nhất: {top_brand['brand']} ({top_brand['percent']}%)
- Tăng trưởng mạnh nhất: {top_growth['brand']} ({top_growth['change_percent']:+.1f}%)

SO SÁNH TUẦN:
{chr(10).join([f"- {c['brand']}: {c['previous_week']} → {c['current_week']} ({c['change_percent']:+.1f}%)" for c in weekly_comparison])}

PEAK DAYS:
{chr(10).join(peak_summary) if peak_summary else "Không có dữ liệu peak"}

Viết insight ngắn gọn (80-100 từ):
1. Đánh giá thị phần và xu hướng
2. Phân tích sự thay đổi đáng chú ý
3. Ý nghĩa của các peak days
4. 1-2 khuyến nghị"""
        
        return self.llm_client.generate_insight(prompt)
