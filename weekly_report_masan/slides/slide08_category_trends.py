"""
Slide 08 – Xu hướng thảo luận (cho từng ngành hàng)
Trend analysis by brand for specific category with peak annotations
Chart: Line chart with daily data and peak highlights
Input: df, category_name, week_start, week_end, llm_client
Output: slide data with trend lines and peak annotations
"""
from typing import Any, Dict, List
import pandas as pd
from datetime import datetime, timedelta

from core.llm_client import LLMClient
from weekly_report.slides.base import SlideGenerator, InsightMixin


class Slide08CategoryTrends(SlideGenerator, InsightMixin):
    """Generate trend analysis for a specific product category."""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    # ── public ────────────────────────────────────────────────────────────────
    def generate(self, *, df: pd.DataFrame, category_name: str,
                 week_start: datetime, week_end: datetime) -> Dict[str, Any]:
        """
        Generate slide for specific category with:
        1. Daily trend lines by brand (Topic)
        2. Peak annotations with post evidence (Type, Content, URL)
        3. Insight about trends
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
        
        # Calculate trends and peaks
        trend_data = self._calculate_trends(df_category, week_start, week_end)
        
        # Generate Insight
        insight = self._generate_insight(
            df_category=df_category,
            category_name=category_name,
            trend_data=trend_data
        )
        
        return {
            "title": f"Xu hướng thảo luận - {category_name}",
            "subtitle": f"Giai đoạn: {week_start.strftime('%d/%m/%Y')} - {week_end.strftime('%d/%m/%Y')}",
            "category_name": category_name,
            "trends": trend_data["trends"],
            "peak_annotations": trend_data["peak_annotations"],
            "insight": insight,
            "total_buzz": len(df_category),
        }

    def _empty_result(self, category: str, start: datetime, end: datetime) -> Dict[str, Any]:
        """Return empty result when no data."""
        return {
            "title": f"Xu hướng thảo luận - {category}",
            "subtitle": f"Giai đoạn: {start.strftime('%d/%m/%Y')} - {end.strftime('%d/%m/%Y')}",
            "category_name": category,
            "trends": {},
            "peak_annotations": {},
            "insight": "Không có dữ liệu",
            "total_buzz": 0,
        }

    # ── Trend Lines with Peaks ────────────────────────────────────────────────
    def _calculate_trends(self, df: pd.DataFrame, 
                          start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Calculate daily trends with peak annotations by brand (Topic)."""
        
        if "Topic" not in df.columns:
            return {"trends": {}, "peak_annotations": {}}
        
        # Get unique brands (Topics)
        brands = df["Topic"].dropna().unique().tolist()
        
        if not brands:
            return {"trends": {}, "peak_annotations": {}}
        
        # Get all dates in range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        trends = {}
        peak_annotations = {}
        
        for brand in brands:
            df_brand = df[df["Topic"] == brand].copy()
            
            if df_brand.empty:
                continue
            
            # Group by date
            df_brand["Date"] = df_brand["PublishedDate"].dt.date
            daily_counts = df_brand.groupby("Date").size().reset_index(name="count")
            
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
            
            trends[brand] = trend_data
            
            # Find peak day
            if not daily_counts.empty and daily_counts["count"].max() > 0:
                peak_date = daily_counts.loc[daily_counts["count"].idxmax(), "Date"]
                peak_count = int(daily_counts["count"].max())
                
                # Get evidence from peak day (Type = Topic preferred)
                df_peak = df_brand[df_brand["Date"] == peak_date]
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
                    
                    # Safely get Type
                    type_val = top_topic.get("Type", "")
                    if pd.isna(type_val):
                        type_val = ""
                    
                    peak_annotations[brand] = {
                        "date": peak_date.strftime("%d/%m/%Y"),
                        "count": peak_count,
                        "type": str(type_val),
                        "content": content,
                        "url": str(url)
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
                            "type": str(type_val),
                            "content": content,
                            "url": str(url)
                        }
        
        return {
            "trends": trends,
            "peak_annotations": peak_annotations
        }

    # ── Insight Generation ────────────────────────────────────────────────────
    def _generate_insight(self, *, df_category: pd.DataFrame, category_name: str,
                          trend_data: Dict) -> str:
        """Generate insight about trend patterns."""
        
        total_buzz = len(df_category)
        trends = trend_data.get("trends", {})
        peaks = trend_data.get("peak_annotations", {})
        
        if not trends:
            return "Không có dữ liệu để phân tích xu hướng."
        
        # Find brand with highest peak
        highest_peak_brand = None
        highest_peak_count = 0
        
        for brand, peak in peaks.items():
            if peak["count"] > highest_peak_count:
                highest_peak_count = peak["count"]
                highest_peak_brand = brand
        
        # Calculate average daily buzz per brand
        brand_avg = {}
        for brand, trend_points in trends.items():
            total = sum(point["count"] for point in trend_points)
            avg = round(total / len(trend_points), 1) if trend_points else 0
            brand_avg[brand] = avg
        
        # Most consistent brand (highest average)
        most_consistent = max(brand_avg.items(), key=lambda x: x[1]) if brand_avg else (None, 0)
        
        # Build prompt
        peak_summary = []
        for brand, peak in peaks.items():
            peak_summary.append(f"{brand}: {peak['date']} ({peak['count']} buzz)")
        
        prompt = f"""Viết insight ngắn gọn (60-80 từ) về xu hướng thảo luận trong ngành {category_name}:

DỮ LIỆU:
- Tổng thảo luận: {total_buzz:,}
- Số thương hiệu: {len(trends)}

XU HƯỚNG:
- Peak cao nhất: {highest_peak_brand if highest_peak_brand else 'N/A'} ({highest_peak_count} buzz)
- Thương hiệu ổn định nhất: {most_consistent[0] if most_consistent[0] else 'N/A'} (TB {most_consistent[1]} buzz/ngày)

PEAK DAYS:
{chr(10).join(peak_summary[:5]) if peak_summary else "Không có peak nổi bật"}

Phân tích:
1. Đánh giá xu hướng chung
2. So sánh các thương hiệu
3. Ý nghĩa của peak days
4. 1 khuyến nghị về timing"""
        
        return self.llm_client.generate_insight(prompt)
