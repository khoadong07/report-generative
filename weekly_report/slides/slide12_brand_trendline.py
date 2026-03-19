"""
Slide 12 – Multi-brand daily trendline + peak annotations
Input:  week1_all_df, brand, week1_display, week1_start_date, week1_end_date, brands_filter
Output: {title, subtitle, brands, trendlines, annotations}
"""
from typing import Any, Dict, List, Optional
import pandas as pd

from core.data_loader import calculate_engagement
from weekly_report.slides.base import SlideGenerator


class Slide12BrandTrendline(SlideGenerator):
    """Multi-brand trendline with peak annotations."""

    def __init__(self, topic_types: List[str]):
        self.topic_types = topic_types

    def generate(self, *, week1_df: pd.DataFrame, brand: str,
                 week1_display: str, week1_start_date: str, week1_end_date: str,
                 brands_filter: Optional[List[str]] = None) -> Dict[str, Any]:

        all_brands = (
            [b for b in brands_filter if b in week1_df["Topic"].values]
            if brands_filter
            else sorted(week1_df["Topic"].dropna().unique().tolist())
        )

        start = pd.to_datetime(week1_start_date).date()
        end   = pd.to_datetime(week1_end_date).date()
        date_range = [d.date() for d in pd.date_range(start=start, end=end, freq="D")]

        trendlines: Dict[str, List[Dict]] = {}
        for b in all_brands:
            daily = week1_df[week1_df["Topic"] == b].groupby("PublishedDay").size().to_dict()
            trendlines[b] = [{"date": str(d), "mentions": int(daily.get(d, 0))} for d in date_range]

        annotations: Dict[str, Dict] = {}
        for b in all_brands:
            df_b = week1_df[week1_df["Topic"] == b]
            if df_b.empty:
                continue
            daily_counts = df_b.groupby("PublishedDay").size()
            if daily_counts.empty:
                continue
            peak_day   = daily_counts.idxmax()
            peak_count = int(daily_counts[peak_day])

            df_peak = df_b[
                (df_b["PublishedDay"] == peak_day) &
                (df_b["Type"].isin(self.topic_types)) &
                (df_b["UrlTopic"].notna()) &
                (df_b["UrlTopic"].astype(str).str.startswith("http"))
            ].copy()

            if df_peak.empty:
                df_peak = df_b[
                    (df_b["PublishedDay"] == peak_day) &
                    (df_b["UrlTopic"].notna()) &
                    (df_b["UrlTopic"].astype(str).str.startswith("http"))
                ].copy()

            if df_peak.empty:
                continue

            df_peak["_eng"] = calculate_engagement(df_peak)
            best = df_peak.sort_values("_eng", ascending=False).iloc[0]
            raw  = str(best.get("Title") or best.get("Content") or "").strip()
            words = raw.split()
            snippet = " ".join(words[:5]) + "..." if len(words) > 5 else raw

            annotations[b] = {
                "date":     str(peak_day),
                "mentions": peak_count,
                "snippet":  snippet,
                "url":      str(best.get("UrlTopic", "")),
                "type":     str(best.get("Type", "")),
            }

        return {
            "title":       f"Đường biểu diễn xu hướng đề cập của {brand} và một số brand khác",
            "subtitle":    f"Giai đoạn: {week1_display}",
            "brands":      all_brands,
            "trendlines":  trendlines,
            "annotations": annotations,
        }
