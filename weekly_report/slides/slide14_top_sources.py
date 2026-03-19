"""
Slide 14 - Top nguồn có lượng thảo luận cao nhất
Input:  week1_all_df, brand, week1_display, brands_filter
Output: {title, subtitle, table}
  table: [{stt, source_name, channel, total}] - top 10
"""
from typing import Any, Dict, List, Optional
import pandas as pd

from weekly_report.slides.base import SlideGenerator


class Slide14TopSources(SlideGenerator):
    """Top 10 sources by mention count across all brands (data-only, no LLM)."""

    def generate(
        self,
        *,
        week1_df: pd.DataFrame,
        brand: str,
        week1_display: str,
        brands_filter: Optional[List[str]] = None,
    ) -> Dict[str, Any]:

        # Filter to relevant brands (same logic as slide 11/12/13)
        if brands_filter:
            df = week1_df[week1_df["Topic"].isin(brands_filter)].copy()
        else:
            df = week1_df.copy()

        if df.empty or "SiteName" not in df.columns:
            return {
                "title":    "Top nguồn có lượng thảo luận cao nhất",
                "subtitle": f"Giai doan: {week1_display}",
                "table":    [],
            }

        # Group by SiteName + Channel, count mentions
        grp = (
            df.groupby(["SiteName", "Channel"], dropna=False)
            .size()
            .reset_index(name="total")
            .sort_values("total", ascending=False)
            .head(10)
            .reset_index(drop=True)
        )

        table = [
            {
                "stt":         i + 1,
                "source_name": row["SiteName"],
                "channel":     row["Channel"] if pd.notna(row["Channel"]) else "",
                "total":       int(row["total"]),
            }
            for i, row in grp.iterrows()
        ]

        return {
            "title":    "Top nguồn có lượng thảo luận cao nhất",
            "subtitle": f"Giai doan: {week1_display}",
            "table":    table,
        }
