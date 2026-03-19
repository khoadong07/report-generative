"""
Slide 08 – Top positive posts by positive-comment count (table, no LLM)
Input:  week1_df, brand, week1_display
Output: {title, subtitle, table_rows: [{stt, content, published_date, channel,
                                         site_name, positive_comments, url}]}
"""
from typing import Any, Dict, List
import pandas as pd

from weekly_report.slides.base import SlideGenerator


class Slide08PositivePosts(SlideGenerator):
    """Top posts ranked by positive comment count."""

    def __init__(self, topic_types: List[str], comment_types: List[str], top_n: int = 10):
        self.topic_types  = topic_types
        self.comment_types = comment_types
        self.top_n = top_n

    def generate(self, *, week1_df: pd.DataFrame, brand: str,
                 week1_display: str) -> Dict[str, Any]:

        df_pos_comments = week1_df[
            (week1_df["Sentiment"].str.lower() == "positive") &
            (week1_df["Type"].isin(self.comment_types))
        ].copy()

        df_topics = week1_df[week1_df["Type"].isin(self.topic_types)].copy()

        if (not df_pos_comments.empty
                and "ParentId" in df_pos_comments.columns
                and "Id" in df_topics.columns):
            counts = df_pos_comments.groupby("ParentId").size().reset_index(name="positive_comment_count")
            df_merged = (df_topics
                         .merge(counts, left_on="Id", right_on="ParentId", how="inner")
                         .sort_values("positive_comment_count", ascending=False)
                         .head(self.top_n))
        else:
            df_merged = (df_topics[df_topics["Sentiment"].str.lower() == "positive"].copy()
                         .assign(positive_comment_count=lambda d: d.get("Comments", 0))
                         .sort_values("positive_comment_count", ascending=False)
                         .head(self.top_n))

        table_rows = [
            {
                "stt":              i,
                "content":          str(r.Content) if pd.notna(r.Content) else str(r.Title),
                "published_date":   str(r.PublishedDate),
                "channel":          str(r.Channel),
                "site_name":        str(r.SiteName),
                "positive_comments": int(getattr(r, "positive_comment_count", 0)),
                "url":              str(r.UrlTopic),
            }
            for i, r in enumerate(df_merged.itertuples(), 1)
        ]

        return {
            "title":      f"Top các bài đăng tích cực về {brand}",
            "subtitle":   f"Giai đoạn: {week1_display}",
            "table_rows": table_rows,
        }
