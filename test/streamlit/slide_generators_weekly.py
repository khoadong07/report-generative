"""
Weekly Slide generation modules for 12-slide report
"""

import pandas as pd
import re
from typing import Dict, Any, List
from datetime import timedelta, datetime

from data_loader import calculate_percentage_change, calculate_engagement
from llm_client import LLMClient
from prompts_weekly import (
    get_weekly_overview_insight_prompt,
    get_weekly_trendline_insight_prompt,
    get_weekly_channel_insight_prompt,
    get_weekly_sentiment_insight_prompt,
    get_weekly_positive_insight_prompt,
    get_weekly_negative_insight_prompt
)


class WeeklySlide1Generator:
    """Generate weekly overview slide with KPIs and 4-week comparison"""
    
    def __init__(self, llm_client: LLMClient, topic_types: List[str]):
        self.llm_client = llm_client
        self.topic_types = topic_types
    
    def generate(self, week1_df: pd.DataFrame, week2_df: pd.DataFrame,
                 week3_df: pd.DataFrame, week4_df: pd.DataFrame,
                 brand: str, week1_display: str, show_interactions: bool = True) -> Dict[str, Any]:
        """Generate slide 1 data"""
        # Calculate metrics for current week
        total_mentions = len(week1_df)
        total_engagement = week1_df["Reactions"].sum() + week1_df["Shares"].sum() + week1_df["Comments"].sum()
        total_views = week1_df["Views"].sum()
        total_reactions = week1_df["Reactions"].sum()
        total_shares = week1_df["Shares"].sum()
        total_comments = week1_df["Comments"].sum()
        
        # Calculate metrics for previous week (week2)
        prev_total_mentions = len(week2_df)
        prev_total_engagement = week2_df["Reactions"].sum() + week2_df["Shares"].sum() + week2_df["Comments"].sum()
        prev_total_views = week2_df["Views"].sum()
        prev_total_reactions = week2_df["Reactions"].sum()
        prev_total_shares = week2_df["Shares"].sum()
        prev_total_comments = week2_df["Comments"].sum()
        
        # Calculate percentage changes for all metrics
        from data_loader import calculate_percentage_change
        mentions_change = calculate_percentage_change(total_mentions, prev_total_mentions)
        engagement_change = calculate_percentage_change(total_engagement, prev_total_engagement)
        views_change = calculate_percentage_change(total_views, prev_total_views)
        reactions_change = calculate_percentage_change(total_reactions, prev_total_reactions)
        shares_change = calculate_percentage_change(total_shares, prev_total_shares)
        comments_change = calculate_percentage_change(total_comments, prev_total_comments)
        
        # Weekly comparison data with growth rates
        week4_mentions = len(week4_df)
        week3_mentions = len(week3_df)
        week2_mentions = len(week2_df)
        week1_mentions = len(week1_df)
        
        weekly_comparison = [
            {
                "week": "3 tuần trước", 
                "total_mentions": week4_mentions,
                "growth_rate": None  # No previous week for comparison
            },
            {
                "week": "2 tuần trước", 
                "total_mentions": week3_mentions,
                "growth_rate": calculate_percentage_change(week3_mentions, week4_mentions)
            },
            {
                "week": "Tuần trước", 
                "total_mentions": week2_mentions,
                "growth_rate": calculate_percentage_change(week2_mentions, week3_mentions)
            },
            {
                "week": "Tuần hiện tại", 
                "total_mentions": week1_mentions,
                "growth_rate": calculate_percentage_change(week1_mentions, week2_mentions)
            }
        ]
        
        # Generate insight
        insight = self._generate_insight(week1_df, brand, week1_display, weekly_comparison)
        
        # Build metrics list based on show_interactions flag
        if show_interactions:
            # Full metrics including interactions
            current_week_metrics = [
                {
                    "label": "Tổng đề cập", 
                    "value": total_mentions,
                    "change_percent": mentions_change
                },
                {
                    "label": "Tổng tương tác", 
                    "value": int(total_engagement),
                    "change_percent": engagement_change
                },
                {
                    "label": "Tổng lượt xem", 
                    "value": int(total_views),
                    "change_percent": views_change
                },
                {
                    "label": "Lượt reactions", 
                    "value": int(total_reactions),
                    "change_percent": reactions_change
                },
                {
                    "label": "Lượt chia sẻ", 
                    "value": int(total_shares),
                    "change_percent": shares_change
                },
                {
                    "label": "Lượt bình luận", 
                    "value": int(total_comments),
                    "change_percent": comments_change
                }
            ]
        else:
            # Only show total mentions (no interactions)
            current_week_metrics = [
                {
                    "label": "Tổng đề cập", 
                    "value": total_mentions,
                    "change_percent": mentions_change
                }
            ]
        
        return {
            "title": f"Tổng quan về {brand}",
            "subtitle": f"Giai đoạn: {week1_display}",
            "current_week_metrics": current_week_metrics,
            "weekly_comparison": weekly_comparison,
            "insight": insight,
            "show_interactions": show_interactions
        }
    
    def _generate_insight(self, week1_df: pd.DataFrame, brand: str,
                          week1_display: str, weekly_comparison: List[Dict]) -> str:
        """Generate insight using LLM"""
        print("         → Extracting top topics for insight...")
        df_topics = week1_df[week1_df["Type"].isin(self.topic_types)].copy()
        
        # Check if we have topics
        if len(df_topics) == 0:
            return f"Trong giai đoạn {week1_display}, {brand} có {len(week1_df)} lượt đề cập. Không có dữ liệu bài đăng chính (topics) để phân tích chi tiết."
        
        df_topics["engagement"] = calculate_engagement(df_topics)
        df_top = df_topics.sort_values("engagement", ascending=False).head(5)
        
        context_text = "\n\n---\n\n".join([
            f"Tiêu đề: {row['Title']}\nMô tả: {row['Description']}\nNội dung: {row['Content']}\nURL: {row['UrlTopic']}"
            for _, row in df_top.iterrows()
        ])
        
        prompt = get_weekly_overview_insight_prompt(
            brand, week1_display, weekly_comparison, context_text
        )
        
        return self.llm_client.generate_insight(prompt)


class WeeklySlide2Generator:
    """Generate weekly trendline slide (7 days)"""
    
    def __init__(self, llm_client: LLMClient, topic_types: List[str]):
        self.llm_client = llm_client
        self.topic_types = topic_types
    
    def generate(self, week1_df: pd.DataFrame, brand: str,
                 week1_display: str, week1_start_date: str, week1_end_date: str) -> Dict[str, Any]:
        """Generate slide 2 data with complete 7-day timeline"""
        
        # Parse start and end dates
        start_date = pd.to_datetime(week1_start_date).date()
        end_date = pd.to_datetime(week1_end_date).date()
        
        # Create complete date range (7 days)
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        complete_dates = [d.date() for d in date_range]
        
        # Group by day
        daily_trend = week1_df.groupby("PublishedDay").size().reset_index(name="mentions")
        daily_trend_dict = dict(zip(daily_trend["PublishedDay"], daily_trend["mentions"]))
        
        # Fill missing dates with 0
        trendline_data = [
            {"date": str(date), "mentions": int(daily_trend_dict.get(date, 0))}
            for date in complete_dates
        ]
        
        # Generate insight
        insight = self._generate_insight(week1_df, brand, week1_display, trendline_data)
        
        return {
            "title": f"Đường biểu diễn xu hướng đề cập về {brand}",
            "subtitle": f"Giai đoạn: {week1_display}",
            "trendline": trendline_data,
            "insight": insight
        }
    
    def _generate_insight(self, week1_df: pd.DataFrame, brand: str,
                          week1_display: str, trendline_data: List[Dict]) -> str:
        """Generate insight using LLM"""
        df_topics = week1_df[week1_df["Type"].isin(self.topic_types)].copy()
        
        # Check if we have topics
        if len(df_topics) == 0:
            return f"Xu hướng đề cập về {brand} trong giai đoạn {week1_display}. Không có dữ liệu bài đăng chính (topics) để phân tích chi tiết."
        
        df_topics["engagement"] = calculate_engagement(df_topics)
        df_top = df_topics.sort_values("engagement", ascending=False).head(3)
        
        context_text = "\n\n---\n\n".join([
            f"Tiêu đề: {row['Title']}\nNội dung: {row['Content']}\nURL: {row['UrlTopic']}"
            for _, row in df_top.iterrows()
        ])
        
        prompt = get_weekly_trendline_insight_prompt(brand, week1_display, trendline_data, context_text)
        return self.llm_client.generate_insight(prompt)


class WeeklySlide3Generator:
    """Generate channel distribution slide"""
    
    def __init__(self, llm_client: LLMClient, topic_types: List[str]):
        self.llm_client = llm_client
        self.topic_types = topic_types
    
    def generate(self, week1_df: pd.DataFrame, brand: str,
                 week1_display: str) -> Dict[str, Any]:
        """Generate slide 3 data"""
        # Channel distribution (pie chart)
        channel_dist = week1_df.groupby("Channel").size().reset_index(name="count")
        channel_dist = channel_dist.sort_values("count", ascending=False)
        
        # Top 10 sources (SiteName)
        top_sources = week1_df.groupby("SiteName").size().reset_index(name="count")
        top_sources = top_sources.sort_values("count", ascending=False).head(10)
        
        # Generate insight
        insight = self._generate_insight(week1_df, brand, week1_display, channel_dist, top_sources)
        
        return {
            "title": f"Phân bố lượt đề cập về {brand} trên các kênh truyền thông",
            "subtitle": f"Giai đoạn: {week1_display}",
            "channel_distribution": channel_dist.to_dict(orient="records"),
            "top_sources": top_sources.to_dict(orient="records"),
            "insight": insight
        }
    
    def _generate_insight(self, week1_df: pd.DataFrame, brand: str,
                          week1_display: str, channel_dist: pd.DataFrame,
                          top_sources: pd.DataFrame) -> str:
        """Generate insight using LLM"""
        df_topics = week1_df[week1_df["Type"].isin(self.topic_types)].copy()
        
        # Check if we have topics
        if len(df_topics) == 0:
            return f"Phân bố thảo luận về {brand} trên các kênh trong giai đoạn {week1_display}. Không có dữ liệu bài đăng chính (topics) để phân tích chi tiết."
        
        df_topics["engagement"] = calculate_engagement(df_topics)
        df_top = df_topics.sort_values("engagement", ascending=False).head(3)
        
        context_text = "\n\n---\n\n".join([
            f"Channel: {row['Channel']}\nSiteName: {row['SiteName']}\nTiêu đề: {row['Title']}\nURL: {row['UrlTopic']}"
            for _, row in df_top.iterrows()
        ])
        
        prompt = get_weekly_channel_insight_prompt(
            brand, week1_display, 
            channel_dist.to_string(index=False),
            top_sources.to_string(index=False),
            context_text
        )
        return self.llm_client.generate_insight(prompt)



class WeeklySlide4Generator:
    """Generate top sources by engagement (table, no insight)"""
    
    def __init__(self, topic_types: List[str], top_n: int = 10):
        self.topic_types = topic_types
        self.top_n = top_n
    
    def generate(self, week1_df: pd.DataFrame, brand: str,
                 week1_display: str, show_interactions: bool = True) -> Dict[str, Any]:
        """Generate slide 4 data"""
        # Group by SiteName and calculate total engagement
        df_topics = week1_df[week1_df["Type"].isin(self.topic_types)].copy()
        df_topics["engagement"] = calculate_engagement(df_topics)
        
        if show_interactions:
            # Full table with interaction columns
            top_sources = df_topics.groupby("SiteName").agg({
                "engagement": "sum",
                "Reactions": "sum",
                "Shares": "sum",
                "Comments": "sum"
            }).reset_index()
            
            top_sources = top_sources.sort_values("engagement", ascending=False).head(self.top_n)
            
            table_rows = []
            for idx, row in enumerate(top_sources.itertuples(), 1):
                table_rows.append({
                    "stt": idx,
                    "source_name": row.SiteName,
                    "total_engagement": int(row.engagement),
                    "reactions": int(row.Reactions),
                    "shares": int(row.Shares),
                    "comments": int(row.Comments)
                })
        else:
            # Simple table without interaction columns (only count)
            top_sources = df_topics.groupby("SiteName").size().reset_index(name="count")
            top_sources = top_sources.sort_values("count", ascending=False).head(self.top_n)
            
            table_rows = []
            for idx, row in enumerate(top_sources.itertuples(), 1):
                table_rows.append({
                    "stt": idx,
                    "source_name": row.SiteName,
                    "count": int(row.count)
                })
        
        return {
            "title": f"Top nguồn có lượng tương tác cao nhất" if show_interactions else f"Top nguồn có lượng đề cập cao nhất",
            "subtitle": f"Giai đoạn: {week1_display}",
            "table_rows": table_rows,
            "show_interactions": show_interactions
        }


class WeeklySlide5Generator:
    """Generate top posts by comments (table, no insight)"""
    
    def __init__(self, topic_types: List[str], top_n: int = 10):
        self.topic_types = topic_types
        self.top_n = top_n
    
    def generate(self, week1_df: pd.DataFrame, brand: str,
                 week1_display: str, show_interactions: bool = True) -> Dict[str, Any]:
        """Generate slide 5 data"""
        df_topics = week1_df[week1_df["Type"].isin(self.topic_types)].copy()
        
        if show_interactions:
            # Sort by Comments and include interaction columns
            df_topics = df_topics.sort_values("Comments", ascending=False).head(self.top_n)
            
            table_rows = []
            for idx, row in enumerate(df_topics.itertuples(), 1):
                content = str(row.Content) if pd.notna(row.Content) else str(row.Title)
                table_rows.append({
                    "stt": idx,
                    "content": content,
                    "published_date": str(row.PublishedDate),
                    "channel": str(row.Channel),
                    "site_name": str(row.SiteName),
                    "reactions": int(row.Reactions),
                    "shares": int(row.Shares),
                    "comments": int(row.Comments),
                    "url": str(row.UrlTopic)
                })
        else:
            # Simple table without interaction columns
            # Can sort by any available metric or just take top N
            df_topics = df_topics.head(self.top_n)
            
            table_rows = []
            for idx, row in enumerate(df_topics.itertuples(), 1):
                content = str(row.Content) if pd.notna(row.Content) else str(row.Title)
                table_rows.append({
                    "stt": idx,
                    "content": content,
                    "published_date": str(row.PublishedDate),
                    "channel": str(row.Channel),
                    "site_name": str(row.SiteName),
                    "url": str(row.UrlTopic)
                })
        
        return {
            "title": f"Top bài đăng có tương tác cao nhất" if show_interactions else f"Top bài đăng nổi bật",
            "subtitle": f"Giai đoạn: {week1_display}",
            "table_rows": table_rows,
            "show_interactions": show_interactions
        }


class WeeklySlide6Generator:
    """Generate sentiment analysis slide (2 pie charts + topic chart + insight)"""
    
    def __init__(self, llm_client: LLMClient, topic_types: List[str]):
        self.llm_client = llm_client
        self.topic_types = topic_types
    
    def generate(self, week1_df: pd.DataFrame, week2_df: pd.DataFrame,
                 brand: str, week1_display: str) -> Dict[str, Any]:
        """Generate slide 6 data"""
        # Normalize sentiment
        week1_df = week1_df.copy()
        week2_df = week2_df.copy()
        week1_df["Sentiment"] = week1_df["Sentiment"].str.capitalize()
        week2_df["Sentiment"] = week2_df["Sentiment"].str.capitalize()
        
        # Current week sentiment
        current_sentiment = week1_df["Sentiment"].value_counts().reset_index(name="count")
        current_sentiment.columns = ["sentiment", "count"]
        
        # Previous week sentiment
        previous_sentiment = week2_df["Sentiment"].value_counts().reset_index(name="count")
        previous_sentiment.columns = ["sentiment", "count"]
        
        # Calculate NSR for current week
        curr_total = current_sentiment["count"].sum()
        curr_negative = current_sentiment[current_sentiment["sentiment"] == "Negative"]["count"].sum()
        curr_positive = current_sentiment[current_sentiment["sentiment"] == "Positive"]["count"].sum()
        curr_negative_pct = (curr_negative / curr_total * 100) if curr_total > 0 else 0
        curr_positive_pct = (curr_positive / curr_total * 100) if curr_total > 0 else 0
        curr_nsr = ((curr_positive_pct - curr_negative_pct) / (curr_positive_pct + curr_negative_pct) * 100) if (curr_positive_pct + curr_negative_pct) > 0 else 0
        
        # Calculate NSR for previous week
        prev_total = previous_sentiment["count"].sum()
        prev_negative = previous_sentiment[previous_sentiment["sentiment"] == "Negative"]["count"].sum()
        prev_positive = previous_sentiment[previous_sentiment["sentiment"] == "Positive"]["count"].sum()
        prev_negative_pct = (prev_negative / prev_total * 100) if prev_total > 0 else 0
        prev_positive_pct = (prev_positive / prev_total * 100) if prev_total > 0 else 0
        prev_nsr = ((prev_positive_pct - prev_negative_pct) / (prev_positive_pct + prev_negative_pct) * 100) if (prev_positive_pct + prev_negative_pct) > 0 else 0
        
        # Calculate NSR growth rate
        from data_loader import calculate_percentage_change
        nsr_growth = calculate_percentage_change(curr_nsr, prev_nsr)
        
        # Topic distribution by sentiment (Labels1)
        topic_sentiment = week1_df.groupby(["Labels1", "Sentiment"]).size().reset_index(name="count")
        topic_summary = topic_sentiment.groupby("Labels1")["count"].sum().reset_index()
        topic_summary = topic_summary.sort_values("count", ascending=False).head(10)
        
        # Merge sentiment breakdown for top topics
        top_topics = []
        for topic in topic_summary["Labels1"]:
            topic_data = topic_sentiment[topic_sentiment["Labels1"] == topic]
            sentiment_breakdown = {row["Sentiment"]: int(row["count"]) for _, row in topic_data.iterrows()}
            top_topics.append({
                "topic": topic,
                "total": int(topic_summary[topic_summary["Labels1"] == topic]["count"].iloc[0]),
                "negative": sentiment_breakdown.get("Negative", 0),
                "neutral": sentiment_breakdown.get("Neutral", 0),
                "positive": sentiment_breakdown.get("Positive", 0)
            })
        
        # Generate insight
        insight = self._generate_insight(week1_df, brand, week1_display, top_topics)
        
        return {
            "title": f"Sắc thái và cụm chủ đề đề cập nổi bật",
            "subtitle": f"Giai đoạn: {week1_display}",
            "current_sentiment": current_sentiment.to_dict(orient="records"),
            "previous_sentiment": previous_sentiment.to_dict(orient="records"),
            "current_nsr": round(curr_nsr, 2),
            "previous_nsr": round(prev_nsr, 2),
            "nsr_growth": round(nsr_growth, 2),
            "top_topics_with_sentiment": top_topics,
            "insight": insight
        }
    
    def _generate_insight(self, week1_df: pd.DataFrame, brand: str,
                          week1_display: str, top_topics: List[Dict]) -> str:
        """Generate insight using LLM"""
        df_topics = week1_df[week1_df["Type"].isin(self.topic_types)].copy()
        
        # Check if we have topics
        if len(df_topics) == 0:
            return f"Phân tích sắc thái về {brand} trong giai đoạn {week1_display}. Không có dữ liệu bài đăng chính (topics) để phân tích chi tiết."
        
        df_topics["engagement"] = calculate_engagement(df_topics)
        df_top = df_topics.sort_values("engagement", ascending=False).head(5)
        
        context_text = "\n\n---\n\n".join([
            f"Labels1: {row['Labels1']}\nSentiment: {row['Sentiment']}\nTiêu đề: {row['Title']}\nNội dung: {row['Content']}\nURL: {row['UrlTopic']}"
            for _, row in df_top.iterrows()
        ])
        
        prompt = get_weekly_sentiment_insight_prompt(
            brand, week1_display, top_topics, context_text
        )
        return self.llm_client.generate_insight(prompt)


class WeeklySlide7Generator:
    """Generate positive topics analysis (chart + insight)"""
    
    def __init__(self, llm_client: LLMClient, topic_types: List[str]):
        self.llm_client = llm_client
        self.topic_types = topic_types
    
    def generate(self, week1_df: pd.DataFrame, brand: str,
                 week1_display: str) -> Dict[str, Any]:
        """Generate slide 7 data"""
        # Filter positive sentiment
        df_positive = week1_df[week1_df["Sentiment"].str.lower() == "positive"].copy()
        
        # Check if we have positive data
        if len(df_positive) == 0:
            return {
                "title": f"Các chủ đề đề cập tích cực về {brand}",
                "subtitle": f"Giai đoạn: {week1_display}",
                "positive_topics": [],
                "insight": f"Không có dữ liệu đề cập tích cực về {brand} trong giai đoạn {week1_display}."
            }
        
        # Group by Labels1
        positive_topics = df_positive.groupby("Labels1").size().reset_index(name="count")
        positive_topics = positive_topics.sort_values("count", ascending=False).head(10)
        
        # Generate insight
        insight = self._generate_insight(df_positive, brand, week1_display, positive_topics)
        
        return {
            "title": f"Các chủ đề đề cập tích cực về {brand}",
            "subtitle": f"Giai đoạn: {week1_display}",
            "positive_topics": positive_topics.to_dict(orient="records"),
            "insight": insight
        }
    
    def _generate_insight(self, df_positive: pd.DataFrame, brand: str,
                          week1_display: str, positive_topics: pd.DataFrame) -> str:
        """Generate insight using LLM"""
        df_positive["engagement"] = calculate_engagement(df_positive)
        df_top = df_positive.sort_values("engagement", ascending=False).head(5)
        
        context_text = "\n\n---\n\n".join([
            f"Labels1: {row['Labels1']}\nTiêu đề: {row['Title']}\nNội dung: {row['Content']}\nURL: {row['UrlTopic']}"
            for _, row in df_top.iterrows()
        ])
        
        prompt = get_weekly_positive_insight_prompt(
            brand, week1_display, positive_topics.to_string(index=False), context_text
        )
        return self.llm_client.generate_insight(prompt)


class WeeklySlide8Generator:
    """Generate top positive mentions (table, no insight)"""
    
    def __init__(self, topic_types: List[str], top_n: int = 10):
        self.topic_types = topic_types
        self.top_n = top_n
    
    def generate(self, week1_df: pd.DataFrame, brand: str,
                 week1_display: str) -> Dict[str, Any]:
        """Generate slide 8 data"""
        df_positive = week1_df[week1_df["Sentiment"].str.lower() == "positive"].copy()
        
        # Count by Labels1
        positive_counts = df_positive.groupby("Labels1").size().reset_index(name="count")
        positive_counts = positive_counts.sort_values("count", ascending=False).head(self.top_n)
        
        table_rows = []
        for idx, row in enumerate(positive_counts.itertuples(), 1):
            table_rows.append({
                "stt": idx,
                "topic": row.Labels1,
                "count": int(row.count)
            })
        
        return {
            "title": f"Top các đề cập tích cực về {brand}",
            "subtitle": f"Giai đoạn: {week1_display}",
            "table_rows": table_rows
        }


class WeeklySlide9Generator:
    """Generate top positive posts based on positive comment count (table, no insight)"""
    
    def __init__(self, topic_types: List[str], comment_types: List[str], top_n: int = 10):
        self.topic_types = topic_types
        self.comment_types = comment_types
        self.top_n = top_n
    
    def generate(self, week1_df: pd.DataFrame, brand: str,
                 week1_display: str) -> Dict[str, Any]:
        """Generate slide 9 data - top posts by positive comment count"""
        
        # Filter positive comments
        df_positive_comments = week1_df[
            (week1_df["Sentiment"].str.lower() == "positive") &
            (week1_df["Type"].isin(self.comment_types))
        ].copy()
        
        # Count positive comments by ParentId
        if len(df_positive_comments) > 0 and "ParentId" in df_positive_comments.columns:
            positive_comment_counts = df_positive_comments.groupby("ParentId").size().reset_index(name="positive_comment_count")
            
            # Get topic data
            df_topics = week1_df[week1_df["Type"].isin(self.topic_types)].copy()
            
            # Merge with topics (assuming topics have an Id column that matches ParentId)
            # If the Id column has a different name, adjust accordingly
            if "Id" in df_topics.columns:
                df_merged = df_topics.merge(
                    positive_comment_counts,
                    left_on="Id",
                    right_on="ParentId",
                    how="inner"
                )
            else:
                # Fallback: try to match by UrlTopic or other identifier
                df_merged = df_topics.copy()
                df_merged["positive_comment_count"] = 0
            
            # Sort by positive comment count
            df_merged = df_merged.sort_values("positive_comment_count", ascending=False).head(self.top_n)
        else:
            # Fallback: if no positive comments, return empty or use old logic
            df_merged = week1_df[
                (week1_df["Sentiment"].str.lower() == "positive") &
                (week1_df["Type"].isin(self.topic_types))
            ].copy()
            df_merged["positive_comment_count"] = df_merged["Comments"]
            df_merged = df_merged.sort_values("positive_comment_count", ascending=False).head(self.top_n)
        
        table_rows = []
        for idx, row in enumerate(df_merged.itertuples(), 1):
            content = str(row.Content) if pd.notna(row.Content) else str(row.Title)
            positive_count = int(row.positive_comment_count) if hasattr(row, 'positive_comment_count') else 0
            table_rows.append({
                "stt": idx,
                "content": content,
                "published_date": str(row.PublishedDate),
                "channel": str(row.Channel),
                "site_name": str(row.SiteName),
                "positive_comments": positive_count,
                "url": str(row.UrlTopic)
            })
        
        return {
            "title": f"Top các bài đăng tích cực về {brand}",
            "subtitle": f"Giai đoạn: {week1_display}",
            "table_rows": table_rows
        }
        return {
            "title": f"Top các bài đăng tích cực về {brand}",
            "subtitle": f"Giai đoạn: {week1_display}",
            "table_rows": table_rows
        }


class WeeklySlide10Generator:
    """Generate negative topics analysis (chart + insight)"""
    
    def __init__(self, llm_client: LLMClient, topic_types: List[str]):
        self.llm_client = llm_client
        self.topic_types = topic_types
    
    def generate(self, week1_df: pd.DataFrame, brand: str,
                 week1_display: str) -> Dict[str, Any]:
        """Generate slide 10 data"""
        # Filter negative sentiment
        df_negative = week1_df[week1_df["Sentiment"].str.lower() == "negative"].copy()
        
        # Check if we have negative data
        if len(df_negative) == 0:
            return {
                "title": f"Các chủ đề đề cập tiêu cực về {brand}",
                "subtitle": f"Giai đoạn: {week1_display}",
                "negative_topics": [],
                "insight": f"Không có dữ liệu đề cập tiêu cực về {brand} trong giai đoạn {week1_display}."
            }
        
        # Group by Labels1
        negative_topics = df_negative.groupby("Labels1").size().reset_index(name="count")
        negative_topics = negative_topics.sort_values("count", ascending=False).head(10)
        
        # Generate insight
        insight = self._generate_insight(df_negative, brand, week1_display, negative_topics)
        
        return {
            "title": f"Các chủ đề đề cập tiêu cực về {brand}",
            "subtitle": f"Giai đoạn: {week1_display}",
            "negative_topics": negative_topics.to_dict(orient="records"),
            "insight": insight
        }
    
    def _generate_insight(self, df_negative: pd.DataFrame, brand: str,
                          week1_display: str, negative_topics: pd.DataFrame) -> str:
        """Generate insight using LLM"""
        df_negative["engagement"] = calculate_engagement(df_negative)
        df_top = df_negative.sort_values("engagement", ascending=False).head(5)
        
        context_text = "\n\n---\n\n".join([
            f"Labels1: {row['Labels1']}\nTiêu đề: {row['Title']}\nNội dung: {row['Content']}\nURL: {row['UrlTopic']}"
            for _, row in df_top.iterrows()
        ])
        
        prompt = get_weekly_negative_insight_prompt(
            brand, week1_display, negative_topics.to_string(index=False), context_text
        )
        return self.llm_client.generate_insight(prompt)


class WeeklySlide11Generator:
    """Generate top negative mentions (table, no insight)"""
    
    def __init__(self, topic_types: List[str], top_n: int = 10):
        self.topic_types = topic_types
        self.top_n = top_n
    
    def generate(self, week1_df: pd.DataFrame, brand: str,
                 week1_display: str) -> Dict[str, Any]:
        """Generate slide 11 data"""
        df_negative = week1_df[week1_df["Sentiment"].str.lower() == "negative"].copy()
        
        # Count by Labels1
        negative_counts = df_negative.groupby("Labels1").size().reset_index(name="count")
        negative_counts = negative_counts.sort_values("count", ascending=False).head(self.top_n)
        
        table_rows = []
        for idx, row in enumerate(negative_counts.itertuples(), 1):
            table_rows.append({
                "stt": idx,
                "topic": row.Labels1,
                "count": int(row.count)
            })
        
        return {
            "title": f"Top các đề cập tiêu cực về {brand}",
            "subtitle": f"Giai đoạn: {week1_display}",
            "table_rows": table_rows
        }


class WeeklySlide12Generator:
    """Generate top negative posts based on negative comment count (table, no insight)"""
    
    def __init__(self, topic_types: List[str], comment_types: List[str], top_n: int = 10):
        self.topic_types = topic_types
        self.comment_types = comment_types
        self.top_n = top_n
    
    def generate(self, week1_df: pd.DataFrame, brand: str,
                 week1_display: str) -> Dict[str, Any]:
        """Generate slide 12 data - top posts by negative comment count"""
        
        # Filter negative comments
        df_negative_comments = week1_df[
            (week1_df["Sentiment"].str.lower() == "negative") &
            (week1_df["Type"].isin(self.comment_types))
        ].copy()
        
        # Count negative comments by ParentId
        if len(df_negative_comments) > 0 and "ParentId" in df_negative_comments.columns:
            negative_comment_counts = df_negative_comments.groupby("ParentId").size().reset_index(name="negative_comment_count")
            
            # Get topic data
            df_topics = week1_df[week1_df["Type"].isin(self.topic_types)].copy()
            
            # Merge with topics (assuming topics have an Id column that matches ParentId)
            if "Id" in df_topics.columns:
                df_merged = df_topics.merge(
                    negative_comment_counts,
                    left_on="Id",
                    right_on="ParentId",
                    how="inner"
                )
            else:
                # Fallback: try to match by UrlTopic or other identifier
                df_merged = df_topics.copy()
                df_merged["negative_comment_count"] = 0
            
            # Sort by negative comment count
            df_merged = df_merged.sort_values("negative_comment_count", ascending=False).head(self.top_n)
        else:
            # Fallback: if no negative comments, return empty or use old logic
            df_merged = week1_df[
                (week1_df["Sentiment"].str.lower() == "negative") &
                (week1_df["Type"].isin(self.topic_types))
            ].copy()
            df_merged["negative_comment_count"] = df_merged["Comments"]
            df_merged = df_merged.sort_values("negative_comment_count", ascending=False).head(self.top_n)
        
        table_rows = []
        for idx, row in enumerate(df_merged.itertuples(), 1):
            content = str(row.Content) if pd.notna(row.Content) else str(row.Title)
            negative_count = int(row.negative_comment_count) if hasattr(row, 'negative_comment_count') else 0
            table_rows.append({
                "stt": idx,
                "content": content,
                "published_date": str(row.PublishedDate),
                "channel": str(row.Channel),
                "site_name": str(row.SiteName),
                "negative_comments": negative_count,
                "url": str(row.UrlTopic)
            })
        
        return {
            "title": f"Top các bài đăng tiêu cực về {brand}",
            "subtitle": f"Giai đoạn: {week1_display}",
            "table_rows": table_rows
        }
