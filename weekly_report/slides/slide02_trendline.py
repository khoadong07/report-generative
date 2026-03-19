"""
Slide 02 – 7-day mention trendline
Input:  week1_df, brand, week1_display, week1_start_date (YYYY-MM-DD), week1_end_date
Output: {title, subtitle, trendline: [{date, mentions}], insight}
"""
from typing import Any, Dict, List
import pandas as pd

from core.data_loader import calculate_engagement
from core.llm_client import LLMClient
from weekly_report.slides.base import SlideGenerator, InsightMixin
from weekly_report.prompts import get_weekly_trendline_insight_prompt


class Slide02Trendline(SlideGenerator, InsightMixin):
    """Generate weekly trendline slide (7 days)."""

    def __init__(self, llm_client: LLMClient, topic_types: List[str]):
        self.llm_client = llm_client
        self.topic_types = topic_types

    def generate(self, *, week1_df: pd.DataFrame, brand: str,
                 week1_display: str, week1_start_date: str,
                 week1_end_date: str) -> Dict[str, Any]:

        start = pd.to_datetime(week1_start_date).date()
        end   = pd.to_datetime(week1_end_date).date()
        date_range = [d.date() for d in pd.date_range(start=start, end=end, freq="D")]

        daily = week1_df.groupby("PublishedDay").size().to_dict()
        trendline = [{"date": str(d), "mentions": int(daily.get(d, 0))} for d in date_range]

        insight = self._generate_insight(
            week1_df=week1_df, brand=brand,
            week1_display=week1_display, trendline_data=trendline
        )

        return {
            "title":    f"Đường biểu diễn xu hướng đề cập về {brand}",
            "subtitle": f"Giai đoạn: {week1_display}",
            "trendline": trendline,
            "insight":   insight,
        }

    def _generate_insight(self, *, week1_df: pd.DataFrame, brand: str,
                          week1_display: str, trendline_data: List[Dict]) -> str:
        df_topics = week1_df[week1_df["Type"].isin(self.topic_types)].copy()
        if df_topics.empty:
            return (f"Xu hướng đề cập về {brand} trong giai đoạn {week1_display}. "
                    "Không có dữ liệu bài đăng chính (topics) để phân tích chi tiết.")

        df_topics["engagement"] = calculate_engagement(df_topics)
        df_top = df_topics.sort_values("engagement", ascending=False).head(3)
        context_text = "\n\n---\n\n".join([
            f"Tiêu đề: {r['Title']}\nNội dung: {r['Content']}\nURL: {r['UrlTopic']}"
            for _, r in df_top.iterrows()
        ])
        prompt = get_weekly_trendline_insight_prompt(brand, week1_display, trendline_data, context_text)
        return self.llm_client.generate_insight(prompt)
