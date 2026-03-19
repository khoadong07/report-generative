"""
Slide 16 – Top bài đăng có bình luận cao nhất (data-only, no LLM)
Input:  week1_all_df, brand, week1_display, brands_filter
Output: {title, subtitle, table}

Logic:
  - Nếu data có cột 'Comments' (interactions): sort desc, lấy top 10
  - Nếu không có cột 'Comments': đếm theo ParentId → top 10 ParentId →
    truy ngược lên cột Id để lấy bài gốc

Table columns: STT, Topic (Thương hiệu), Content (Bài đăng),
               Channel (Kênh), SiteName+URL (Nguồn), comment_count (Bình luận)
"""
from typing import Any, Dict, List, Optional
import pandas as pd

from weekly_report.slides.base import SlideGenerator


class Slide16TopCommentedPosts(SlideGenerator):
    """Top 10 posts by comment count – no LLM required."""

    def generate(
        self,
        *,
        week1_df: pd.DataFrame,
        brand: str,
        week1_display: str,
        brands_filter: Optional[List[str]] = None,
    ) -> Dict[str, Any]:

        # Filter to relevant brands (same pattern as slide 11-15)
        if brands_filter:
            df = week1_df[week1_df["Topic"].isin(brands_filter)].copy()
        else:
            df = week1_df.copy()

        if df.empty:
            return self._empty(week1_display)

        # ── Case 1: interactions data already has a Comments column ──────────
        if "Comments" in df.columns:
            table = self._from_comments_column(df)
        # ── Case 2: count via ParentId ────────────────────────────────────────
        elif "ParentId" in df.columns and "Id" in df.columns:
            table = self._from_parent_id(df)
        else:
            return self._empty(week1_display)

        return {
            "title":    "Top bài đăng có bình luận cao nhất",
            "subtitle": f"Giai đoạn: {week1_display}",
            "table":    table,
        }

    # ── Case 1 ────────────────────────────────────────────────────────────────
    @staticmethod
    def _from_comments_column(df: pd.DataFrame, top_n: int = 10) -> List[Dict]:
        df = df.copy()
        df["Comments"] = pd.to_numeric(df["Comments"], errors="coerce").fillna(0)
        top = (
            df.sort_values("Comments", ascending=False)
            .head(top_n)
            .reset_index(drop=True)
        )
        return [
            {
                "stt":           i + 1,
                "topic":         str(row.get("Topic", "") or ""),
                "content":       _pick_content(row),
                "channel":       str(row.get("Channel", "") or ""),
                "source_name":   str(row.get("SiteName", "") or ""),
                "source_url":    str(row.get("UrlTopic", "") or ""),
                "comment_count": int(row["Comments"]),
            }
            for i, row in top.iterrows()
        ]

    # ── Case 2 ────────────────────────────────────────────────────────────────
    @staticmethod
    def _from_parent_id(df: pd.DataFrame, top_n: int = 10) -> List[Dict]:
        # Count comments per ParentId (rows whose ParentId points to a parent post)
        comment_counts = (
            df["ParentId"]
            .dropna()
            .astype(str)
            .replace("", pd.NA)
            .dropna()
            .value_counts()
            .head(top_n)
        )

        if comment_counts.empty:
            return []

        # Map Id → row for fast lookup
        df_indexed = df.copy()
        df_indexed["_id_str"] = df_indexed["Id"].astype(str)
        id_to_row = df_indexed.set_index("_id_str")

        rows = []
        for rank, (parent_id, count) in enumerate(comment_counts.items(), start=1):
            pid_str = str(parent_id)
            if pid_str in id_to_row.index:
                row = id_to_row.loc[pid_str]
                # loc may return a DataFrame if duplicate ids exist; take first
                if isinstance(row, pd.DataFrame):
                    row = row.iloc[0]
                rows.append({
                    "stt":           rank,
                    "topic":         str(row.get("Topic", "") or ""),
                    "content":       _pick_content(row),
                    "channel":       str(row.get("Channel", "") or ""),
                    "source_name":   str(row.get("SiteName", "") or ""),
                    "source_url":    str(row.get("UrlTopic", "") or ""),
                    "comment_count": int(count),
                })
            else:
                # Parent post not found in dataset – still include with id as placeholder
                rows.append({
                    "stt":           rank,
                    "topic":         "",
                    "content":       f"[ID: {pid_str}]",
                    "channel":       "",
                    "source_name":   "",
                    "source_url":    "",
                    "comment_count": int(count),
                })

        return rows

    # ── helpers ───────────────────────────────────────────────────────────────
    @staticmethod
    def _empty(week1_display: str) -> Dict[str, Any]:
        return {
            "title":    "Top bài đăng có bình luận cao nhất",
            "subtitle": f"Giai đoạn: {week1_display}",
            "table":    [],
        }


def _pick_content(row) -> str:
    """Return Content; fall back to Title then Description if empty."""
    for field in ("Content", "Title", "Description"):
        val = str(row.get(field, "") or "").strip()
        if val:
            return val
    return ""
