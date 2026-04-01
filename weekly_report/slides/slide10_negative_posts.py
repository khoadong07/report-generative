"""
Slide 10 – Top negative posts (topic-type rows with Sentiment=Negative)
Input:  week1_df, brand, week1_display
Output: {title, subtitle, table_rows: [{stt, content, published_date, channel,
                                         site_name, negative_comments, url}]}
"""
from typing import Any, Dict, List
import pandas as pd

from core.data_loader import calculate_engagement
from weekly_report.slides.base import SlideGenerator


class Slide10NegativePosts(SlideGenerator):
    """Top negative posts ranked by engagement."""

    def __init__(self, topic_types: List[str], comment_types: List[str], top_n: int = 10):
        self.topic_types   = topic_types
        self.comment_types = comment_types
        self.top_n = top_n

    def generate(self, *, week1_df: pd.DataFrame, brand: str,
                 week1_display: str) -> Dict[str, Any]:

        # Lấy các bài đăng (topic) có sentiment tiêu cực
        df = week1_df[
            (week1_df["Sentiment"].str.strip().str.lower() == "negative") &
            (week1_df["Type"].isin(self.topic_types))
        ].copy()

        if df.empty:
            return {
                "title":      f"Top các bài đăng tiêu cực về {brand}",
                "subtitle":   "",
                "table_rows": [],
            }

        df["_engagement"] = calculate_engagement(df)
        df = df.sort_values("_engagement", ascending=False).head(self.top_n)

        table_rows = [
            {
                "stt":               i,
                "content":           str(r.get("Title") or r.get("Content") or "").strip(),
                "published_date":    str(r.get("PublishedDate", "")),
                "channel":           str(r.get("Channel", "")),
                "site_name":         str(r.get("SiteName", "")),
                "negative_comments": int(r.get("Comments", 0) or 0),
                "url":               str(r.get("UrlTopic", "")),
            }
            for i, (_, r) in enumerate(df.iterrows(), 1)
        ]

        return {
            "title":      f"Top các bài đăng tiêu cực về {brand}",
            "subtitle":   "",
            "table_rows": table_rows,
        }
