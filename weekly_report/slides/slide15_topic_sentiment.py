"""
Slide 15 – Sắc thái đề cập theo Topic (multi-brand sentiment breakdown)
Input:  week1_all_df, brand, week1_display, brands_filter
Output: {title, insight, stacked_bar_chart, sentiment_legend, summary_table}

Layout (3 hàng):
  Row 1 – Title + Insight (LLM)
  Row 2 – Stacked bar chart (Positive / Neutral / Negative) + legend
  Row 3 – Summary table: N, NSR%, top-3 positive labels, top-3 negative labels per topic
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
import pandas as pd

from core.llm_client import LLMClient
from weekly_report.slides.base import SlideGenerator, InsightMixin
from weekly_report.prompts import get_slide15_topic_sentiment_insight_prompt

# ── Fixed sentiment colors ────────────────────────────────────────────────────
SENTIMENT_COLORS: Dict[str, str] = {
    "Positive": "#2A9D5C",   # green
    "Neutral":  "#ADB5BD",   # grey
    "Negative": "#E63946",   # red
}
SENTIMENT_ORDER = ["Positive", "Neutral", "Negative"]

# Number of sample posts to extract per top label
_SAMPLE_N = 5


class Slide15TopicSentiment(SlideGenerator, InsightMixin):
    """Sentiment breakdown by Topic with LLM insight and summary table."""

    def __init__(self, llm_client: LLMClient, topic_types: List[str]):
        self.llm_client = llm_client
        self.topic_types = topic_types

    def generate(
        self,
        *,
        week1_df: pd.DataFrame,
        brand: str,
        week1_display: str,
        brands_filter: Optional[List[str]] = None,
    ) -> Dict[str, Any]:

        # ── Resolve topic list (same pattern as slide 11/12/13) ──────────────
        all_topics = (
            [b for b in brands_filter if b in week1_df["Topic"].values]
            if brands_filter
            else sorted(week1_df["Topic"].dropna().unique().tolist())
        )

        df = week1_df.copy()
        # Normalise Sentiment column
        df["_sentiment"] = df["Sentiment"].fillna("Neutral").str.strip().str.capitalize()
        df["_sentiment"] = df["_sentiment"].apply(
            lambda s: s if s in SENTIMENT_COLORS else "Neutral"
        )

        # ── Stacked bar chart data ────────────────────────────────────────────
        bar_data: List[Dict] = []
        for topic in all_topics:
            df_t = df[df["Topic"] == topic]
            total = len(df_t)
            counts = df_t["_sentiment"].value_counts().to_dict()

            segments: List[Dict] = []
            for sent in SENTIMENT_ORDER:
                count = int(counts.get(sent, 0))
                pct = round(count / total * 100, 1) if total > 0 else 0.0
                segments.append({
                    "sentiment": sent,
                    "count":     count,
                    "percent":   pct,
                    "color":     SENTIMENT_COLORS[sent],
                    "show_label": pct >= 5,
                })

            bar_data.append({
                "topic":    topic,
                "total":    total,
                "segments": segments,
            })

        bar_data.sort(key=lambda x: x["total"], reverse=True)

        # ── Summary table ─────────────────────────────────────────────────────
        summary_table = self._build_summary_table(df, all_topics)

        # ── LLM insight ───────────────────────────────────────────────────────
        insight = self._generate_insight(
            df=df,
            brand=brand,
            week1_display=week1_display,
            all_topics=all_topics,
            bar_data=bar_data,
            summary_table=summary_table,
        )

        return {
            "title":   "Sắc thái đề cập",
            "subtitle": f"Giai đoạn: {week1_display}",
            "insight": insight,
            "stacked_bar_chart": {
                "title": f"Tỷ trọng sentiment theo Topic – {brand}",
                "data":  bar_data,
            },
            "sentiment_legend": [
                {"sentiment": s, "color": SENTIMENT_COLORS[s]} for s in SENTIMENT_ORDER
            ],
            "summary_table": summary_table,
        }

    # ── Summary table builder ─────────────────────────────────────────────────
    def _build_summary_table(
        self, df: pd.DataFrame, all_topics: List[str]
    ) -> Dict[str, Any]:
        """
        Returns:
          {
            topics: [str],
            rows: {
              N:              {topic: int},
              NSR:            {topic: float},   # % NSR, highest marked bold
              top_positive:   {topic: [str]},   # top-3 Labels1 where Sentiment=Positive
              top_negative:   {topic: [str]},   # top-3 Labels1 where Sentiment=Negative
              sample_posts:   {topic: [str]},   # 5 sample posts for top label
            }
          }
        """
        n_map: Dict[str, int] = {}
        nsr_map: Dict[str, float] = {}
        top_pos_map: Dict[str, List[str]] = {}
        top_neg_map: Dict[str, List[str]] = {}
        sample_map: Dict[str, List[Dict]] = {}

        for topic in all_topics:
            df_t = df[df["Topic"] == topic]
            total = len(df_t)
            n_map[topic] = total

            # NSR = (Positive - Negative) / Total * 100
            pos_count = int((df_t["_sentiment"] == "Positive").sum())
            neg_count = int((df_t["_sentiment"] == "Negative").sum())
            nsr_map[topic] = round((pos_count - neg_count) / total * 100, 1) if total > 0 else 0.0

            # Top-3 Labels1 for Positive
            df_pos = df_t[df_t["_sentiment"] == "Positive"]
            top_pos_map[topic] = (
                df_pos["Labels1"]
                .fillna("Không xác định")
                .replace("", "Không xác định")
                .value_counts()
                .head(3)
                .index.tolist()
            )

            # Top-3 Labels1 for Negative
            df_neg = df_t[df_t["_sentiment"] == "Negative"]
            top_neg_map[topic] = (
                df_neg["Labels1"]
                .fillna("Không xác định")
                .replace("", "Không xác định")
                .value_counts()
                .head(3)
                .index.tolist()
            )

            # 5 sample posts: pick top label (pos + neg combined by count)
            all_labels = (
                df_t["Labels1"]
                .fillna("Không xác định")
                .replace("", "Không xác định")
                .value_counts()
            )
            top_label = all_labels.index[0] if not all_labels.empty else None
            samples: List[Dict] = []
            if top_label:
                df_samples = df_t[
                    df_t["Labels1"].fillna("Không xác định").replace("", "Không xác định") == top_label
                ].head(_SAMPLE_N)
                for _, row in df_samples.iterrows():
                    raw = str(row.get("Title") or row.get("Content") or "").strip()
                    samples.append({
                        "text":      raw[:300],
                        "sentiment": str(row.get("_sentiment", "")),
                        "label":     top_label,
                        "url":       str(row.get("UrlTopic", "")),
                    })
            sample_map[topic] = samples

        # Mark highest NSR
        max_nsr_topic = max(nsr_map, key=lambda t: nsr_map[t]) if nsr_map else None

        return {
            "topics":       all_topics,
            "N":            n_map,
            "NSR":          nsr_map,
            "max_nsr_topic": max_nsr_topic,
            "top_positive": top_pos_map,
            "top_negative": top_neg_map,
            "sample_posts": sample_map,
        }

    # ── LLM insight ───────────────────────────────────────────────────────────
    def _generate_insight(self, *, df, brand, week1_display,
                          all_topics, bar_data, summary_table) -> str:
        prompt = get_slide15_topic_sentiment_insight_prompt(
            brand=brand,
            week_display=week1_display,
            all_topics=all_topics,
            bar_data=bar_data,
            summary_table=summary_table,
        )
        try:
            return self.llm_client.generate_insight(prompt)
        except Exception as e:
            print(f"Warning: LLM insight failed for slide 15: {e}")
            lines = []
            for topic in all_topics:
                nsr = summary_table["NSR"].get(topic, 0)
                n   = summary_table["N"].get(topic, 0)
                lines.append(f"- {topic}: {n} buzz, NSR {nsr:+.1f}%")
            return "\n".join(lines)
