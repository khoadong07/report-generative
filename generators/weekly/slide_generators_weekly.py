"""
Weekly Slide generation modules for 11-slide report
"""

import pandas as pd
import re
from typing import Dict, Any, List
from datetime import timedelta, datetime

from core.data_loader import calculate_percentage_change, calculate_engagement
from core.llm_client import LLMClient
from generators.weekly.prompts_weekly import (
    get_weekly_overview_insight_prompt,
    get_weekly_trendline_insight_prompt,
    get_weekly_channel_insight_prompt,
    get_weekly_sentiment_insight_prompt,
    get_weekly_positive_insight_prompt,
    get_weekly_negative_insight_prompt,
    get_weekly_brand_comparison_insight_prompt
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
        from core.data_loader import calculate_percentage_change
        
        if show_interactions:
            # Full metrics including interactions (existing logic)
            total_mentions = len(week1_df)
            prev_total_mentions = len(week2_df)
            mentions_change = calculate_percentage_change(total_mentions, prev_total_mentions)
            
            total_engagement = week1_df["Reactions"].sum() + week1_df["Shares"].sum() + week1_df["Comments"].sum()
            total_views = week1_df["Views"].sum()
            total_reactions = week1_df["Reactions"].sum()
            total_shares = week1_df["Shares"].sum()
            total_comments = week1_df["Comments"].sum()
            
            # Calculate metrics for previous week (week2)
            prev_total_engagement = week2_df["Reactions"].sum() + week2_df["Shares"].sum() + week2_df["Comments"].sum()
            prev_total_views = week2_df["Views"].sum()
            prev_total_reactions = week2_df["Reactions"].sum()
            prev_total_shares = week2_df["Shares"].sum()
            prev_total_comments = week2_df["Comments"].sum()
            
            # Calculate percentage changes for interaction metrics
            engagement_change = calculate_percentage_change(total_engagement, prev_total_engagement)
            views_change = calculate_percentage_change(total_views, prev_total_views)
            reactions_change = calculate_percentage_change(total_reactions, prev_total_reactions)
            shares_change = calculate_percentage_change(total_shares, prev_total_shares)
            comments_change = calculate_percentage_change(total_comments, prev_total_comments)
            
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
            # Basic metrics only: Tổng bài đăng, Tổng bình luận, Tổng thảo luận
            # 1. Tổng bài đăng (Type ending with 'Topic')
            week1_posts = len(week1_df[week1_df['Type'].str.endswith('Topic', na=False)])
            week2_posts = len(week2_df[week2_df['Type'].str.endswith('Topic', na=False)])
            posts_change = calculate_percentage_change(week1_posts, week2_posts)
            
            # 2. Tổng bình luận (Type ending with 'Comment')
            week1_comments = len(week1_df[week1_df['Type'].str.endswith('Comment', na=False)])
            week2_comments = len(week2_df[week2_df['Type'].str.endswith('Comment', na=False)])
            comments_change = calculate_percentage_change(week1_comments, week2_comments)
            
            # 3. Tổng thảo luận = Tổng bài đăng + Tổng bình luận
            total_mentions = week1_posts + week1_comments
            prev_total_mentions = week2_posts + week2_comments
            mentions_change = calculate_percentage_change(total_mentions, prev_total_mentions)
            
            current_week_metrics = [
                {
                    "label": "Tổng bài đăng", 
                    "value": week1_posts,
                    "change_percent": posts_change
                },
                {
                    "label": "Tổng bình luận", 
                    "value": week1_comments,
                    "change_percent": comments_change
                },
                {
                    "label": "Tổng thảo luận", 
                    "value": total_mentions,
                    "change_percent": mentions_change
                }
            ]
        
        # Weekly comparison data with growth rates (using same logic as current week)
        if show_interactions:
            # Use total records for weekly comparison when showing interactions
            week4_mentions = len(week4_df)
            week3_mentions = len(week3_df)
            week2_mentions = len(week2_df)
            week1_mentions = len(week1_df)
        else:
            # Use posts + comments for weekly comparison when not showing interactions
            week4_posts = len(week4_df[week4_df['Type'].str.endswith('Topic', na=False)])
            week4_comments = len(week4_df[week4_df['Type'].str.endswith('Comment', na=False)])
            week4_mentions = week4_posts + week4_comments
            
            week3_posts = len(week3_df[week3_df['Type'].str.endswith('Topic', na=False)])
            week3_comments = len(week3_df[week3_df['Type'].str.endswith('Comment', na=False)])
            week3_mentions = week3_posts + week3_comments
            
            week2_posts = len(week2_df[week2_df['Type'].str.endswith('Topic', na=False)])
            week2_comments = len(week2_df[week2_df['Type'].str.endswith('Comment', na=False)])
            week2_mentions = week2_posts + week2_comments
            
            week1_mentions = total_mentions  # Already calculated above
        
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
            # Check if interaction columns exist
            has_reactions = "Reactions" in df_topics.columns
            has_shares = "Shares" in df_topics.columns
            has_comments = "Comments" in df_topics.columns
            
            if has_reactions and has_shares and has_comments:
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
                # Fallback to simple count if interaction columns don't exist
                top_sources = df_topics.groupby("SiteName").size().reset_index(name="count")
                top_sources = top_sources.sort_values("count", ascending=False).head(self.top_n)
                
                table_rows = []
                for idx, row in enumerate(top_sources.itertuples(), 1):
                    table_rows.append({
                        "stt": idx,
                        "source_name": row.SiteName,
                        "count": int(row.count)
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
            # Check if interaction columns exist
            has_reactions = "Reactions" in df_topics.columns
            has_shares = "Shares" in df_topics.columns
            has_comments = "Comments" in df_topics.columns
            
            if has_comments:
                # Sort by Comments and include interaction columns
                df_topics = df_topics.sort_values("Comments", ascending=False).head(self.top_n)
                
                table_rows = []
                for idx, row in enumerate(df_topics.itertuples(), 1):
                    content = str(row.Content) if pd.notna(row.Content) else str(row.Title)
                    row_data = {
                        "stt": idx,
                        "content": content,
                        "published_date": str(row.PublishedDate),
                        "channel": str(row.Channel),
                        "site_name": str(row.SiteName),
                        "url": str(row.UrlTopic)
                    }
                    # Only add interaction columns if they exist
                    if has_reactions:
                        row_data["reactions"] = int(row.Reactions)
                    if has_shares:
                        row_data["shares"] = int(row.Shares)
                    if has_comments:
                        row_data["comments"] = int(row.Comments)
                    table_rows.append(row_data)
            else:
                # Fallback if Comments column doesn't exist
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
        else:
            # Simple table without interaction columns
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
        from core.data_loader import calculate_percentage_change
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
        # Filter positive sentiment with topic types
        df_positive = week1_df[
            (week1_df["Sentiment"].str.lower() == "positive") &
            (week1_df["Type"].isin(self.topic_types))
        ].copy()
        
        # Handle null/NaN Labels1 values - replace with "Không xác định"
        if len(df_positive) > 0:
            df_positive["Labels1"] = df_positive["Labels1"].fillna("Không xác định")
            df_positive["Labels1"] = df_positive["Labels1"].replace("", "Không xác định")
        
        # Check if we have positive data
        if len(df_positive) == 0:
            # Create default "Không xác định" entry when no positive data
            positive_topics = [{"Labels1": "Không xác định", "count": 0}]
            insight = f"Không có dữ liệu đề cập tích cực về {brand} trong giai đoạn {week1_display}."
        else:
            # Group by Labels1
            positive_topics = df_positive.groupby("Labels1").size().reset_index(name="count")
            positive_topics = positive_topics.sort_values("count", ascending=False).head(10)
            positive_topics_df = positive_topics.copy()
            positive_topics = positive_topics.to_dict(orient="records")
            
            # Generate insight
            insight = self._generate_insight(df_positive, brand, week1_display, positive_topics_df)
        
        return {
            "title": f"Các chủ đề đề cập tích cực về {brand}",
            "subtitle": f"Giai đoạn: {week1_display}",
            "positive_topics": positive_topics,
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
        # Filter negative sentiment - handle both "Negative" and "negative" cases
        df_negative = week1_df[
            (week1_df["Sentiment"].str.lower() == "negative") &
            (week1_df["Type"].isin(self.topic_types))
        ].copy()
        
        print(f"      [DEBUG] Total rows in week1_df: {len(week1_df)}")
        print(f"      [DEBUG] Rows with negative sentiment: {len(df_negative)}")
        if len(df_negative) > 0:
            print(f"      [DEBUG] Sample negative data Labels1: {df_negative['Labels1'].value_counts().head()}")
        
        # Handle null/NaN Labels1 values - replace with "Không xác định"
        if len(df_negative) > 0:
            df_negative["Labels1"] = df_negative["Labels1"].fillna("Không xác định")
            df_negative["Labels1"] = df_negative["Labels1"].replace("", "Không xác định")
        
        # Check if we have negative data
        if len(df_negative) == 0:
            # Create default "Không xác định" entry when no negative data
            negative_topics = [{"Labels1": "Không xác định", "count": 0}]
            insight = f"Không có dữ liệu đề cập tiêu cực về {brand} trong giai đoạn {week1_display}."
        else:
            # Group by Labels1
            negative_topics = df_negative.groupby("Labels1").size().reset_index(name="count")
            negative_topics = negative_topics.sort_values("count", ascending=False).head(10)
            negative_topics = negative_topics.to_dict(orient="records")
            
            # Generate insight
            insight = self._generate_insight(df_negative, brand, week1_display, pd.DataFrame(negative_topics))
        
        return {
            "title": f"Các chủ đề đề cập tiêu cực về {brand}",
            "subtitle": f"Giai đoạn: {week1_display}",
            "negative_topics": negative_topics,
            "insight": insight
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
        df_negative = week1_df[
            (week1_df["Sentiment"].str.lower() == "negative") &
            (week1_df["Type"].isin(self.topic_types))
        ].copy()
        
        print(f"      [DEBUG Slide11] Total rows in week1_df: {len(week1_df)}")
        print(f"      [DEBUG Slide11] Rows with negative sentiment: {len(df_negative)}")
        
        # Handle null/NaN Labels1 values - replace with "Không xác định"
        if len(df_negative) > 0:
            df_negative["Labels1"] = df_negative["Labels1"].fillna("Không xác định")
            df_negative["Labels1"] = df_negative["Labels1"].replace("", "Không xác định")
        
        # Count by Labels1
        if len(df_negative) == 0:
            # Create default entry when no negative data
            table_rows = [{
                "stt": 1,
                "topic": "Không xác định",
                "count": 0
            }]
        else:
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

class WeeklyNegativePostsGenerator:
    """Generate top negative posts by negative comment count (for slide 10 UI)"""

    def __init__(self, topic_types: List[str], comment_types: List[str], top_n: int = 10):
        self.topic_types = topic_types
        self.comment_types = comment_types
        self.top_n = top_n

    def generate(self, week1_df: pd.DataFrame, brand: str,
                 week1_display: str) -> Dict[str, Any]:
        """Generate top posts sorted by negative comment count"""

        df_neg_comments = week1_df[
            (week1_df["Sentiment"].str.lower() == "negative") &
            (week1_df["Type"].isin(self.comment_types))
        ].copy()

        df_topics = week1_df[week1_df["Type"].isin(self.topic_types)].copy()

        if len(df_neg_comments) > 0 and "ParentId" in df_neg_comments.columns and "Id" in df_topics.columns:
            neg_counts = df_neg_comments.groupby("ParentId").size().reset_index(name="negative_comment_count")
            df_merged = df_topics.merge(neg_counts, left_on="Id", right_on="ParentId", how="inner")
            df_merged = df_merged.sort_values("negative_comment_count", ascending=False).head(self.top_n)
        else:
            df_merged = df_topics[df_topics["Sentiment"].str.lower() == "negative"].copy()
            df_merged["negative_comment_count"] = df_merged.get("Comments", 0)
            df_merged = df_merged.sort_values("negative_comment_count", ascending=False).head(self.top_n)

        table_rows = []
        for idx, row in enumerate(df_merged.itertuples(), 1):
            content = str(row.Content) if pd.notna(row.Content) else str(row.Title)
            neg_count = int(row.negative_comment_count) if hasattr(row, "negative_comment_count") else 0
            table_rows.append({
                "stt": idx,
                "content": content,
                "published_date": str(row.PublishedDate),
                "channel": str(row.Channel),
                "site_name": str(row.SiteName),
                "negative_comments": neg_count,
                "url": str(row.UrlTopic),
            })

        return {
            "title": f"Top các bài đăng tiêu cực về {brand}",
            "subtitle": f"Giai đoạn: {week1_display}",
            "table_rows": table_rows,
        }


class WeeklySlide12Generator:
    """Generate brand comparison overview with donut charts and bar charts"""
    
    def __init__(self, llm_client: LLMClient, topic_types: List[str]):
        self.llm_client = llm_client
        self.topic_types = topic_types
    
    def generate(self, week1_df: pd.DataFrame, week2_df: pd.DataFrame, brand: str,
                 week1_display: str, brands_filter: List[str] = None) -> Dict[str, Any]:
        """Generate slide 11 data - brand comparison overview
        
        Args:
            brands_filter: Nếu có, chỉ so sánh các brand trong danh sách này.
                           Nếu None, lấy tất cả Topic có trong data.
        """
        
        # Get all brands to compare
        if brands_filter:
            all_brands = [b for b in brands_filter if b in week1_df["Topic"].values or b in week2_df["Topic"].values]
        else:
            all_brands_week1 = set(week1_df["Topic"].dropna().unique())
            all_brands_week2 = set(week2_df["Topic"].dropna().unique())
            all_brands = sorted(list(all_brands_week1.union(all_brands_week2)))
        
        # Calculate mentions for each brand in both weeks (toàn bộ buzz)
        brand_mentions_week1 = {}
        brand_mentions_week2 = {}
        
        for brand_name in all_brands:
            brand_mentions_week1[brand_name] = len(week1_df[week1_df["Topic"] == brand_name])
            brand_mentions_week2[brand_name] = len(week2_df[week2_df["Topic"] == brand_name])
        
        # Palette 12 màu phân biệt rõ ràng, không trùng/gần giống nhau
        # Chọn theo perceptual distance: đỏ, xanh dương, cam, tím, xanh lá, hồng,
        # nâu vàng, xanh navy, vàng đậm, xanh ngọc đậm, tím hồng, xanh olive
        DISTINCT_COLORS = [
            "#E63946",  # đỏ tươi
            "#1D6FA4",  # xanh dương đậm
            "#F4A261",  # cam
            "#7B2D8B",  # tím đậm
            "#2A9D5C",  # xanh lá đậm
            "#E76F51",  # cam đỏ
            "#264653",  # xanh navy
            "#F4C430",  # vàng đậm
            "#0077B6",  # xanh biển
            "#C77DFF",  # tím nhạt
            "#6A994E",  # xanh olive
            "#D62828",  # đỏ đậm
        ]
        
        # Generate donut chart data
        donut_data_week1 = []
        donut_data_week2 = []

        for i, brand_name in enumerate(all_brands):
            color = DISTINCT_COLORS[i % len(DISTINCT_COLORS)]
            
            donut_data_week1.append({
                "brand": brand_name,
                "mentions": brand_mentions_week1.get(brand_name, 0),
                "color": color
            })
            
            donut_data_week2.append({
                "brand": brand_name,
                "mentions": brand_mentions_week2.get(brand_name, 0),
                "color": color
            })
        
        # Generate bar chart data with percentage changes
        bar_chart_data = []
        for brand_name in all_brands:
            week1_count = brand_mentions_week1.get(brand_name, 0)
            week2_count = brand_mentions_week2.get(brand_name, 0)
            
            # Calculate percentage change
            if week2_count > 0:
                percentage_change = ((week1_count - week2_count) / week2_count) * 100
            elif week1_count > 0:
                percentage_change = 100  # New mentions this week
            else:
                percentage_change = 0
            
            bar_chart_data.append({
                "brand": brand_name,
                "week_before": week2_count,
                "current_week": week1_count,
                "percentage_change": round(percentage_change, 1),
                "change_color": "green" if percentage_change >= 0 else "red"
            })
        
        # Sort by current week mentions (descending)
        bar_chart_data.sort(key=lambda x: x["current_week"], reverse=True)
        
        # Generate insight using LLM
        insight = self._generate_insight(week1_df, week2_df, brand, week1_display, all_brands, brand_mentions_week1, brand_mentions_week2)
        
        return {
            "title": f"Tổng quan đề cập về thương hiệu {brand} với các đối thủ",
            "subtitle": f"Giai đoạn: {week1_display}",
            "insight": insight,
            "donut_charts": {
                "week_before": {
                    "title": "Tuần trước",
                    "data": donut_data_week2
                },
                "current_week": {
                    "title": "Tuần hiện tại", 
                    "data": donut_data_week1
                }
            },
            "legend": [{"brand": item["brand"], "color": item["color"]} for item in donut_data_week1],
            "bar_chart": {
                "title": "Tổng đề cập của các thương hiệu",
                "data": bar_chart_data
            }
        }
    
    def _generate_insight(self, week1_df: pd.DataFrame, week2_df: pd.DataFrame, brand: str, 
                         week1_display: str, all_brands: List[str], 
                         brand_mentions_week1: Dict[str, int], brand_mentions_week2: Dict[str, int]) -> str:
        """Generate LLM-based insight for brand comparison"""
        
        # Prepare brand comparison data for prompt
        brand_comparison_lines = []
        for brand_name in all_brands:
            week1_count = brand_mentions_week1.get(brand_name, 0)
            week2_count = brand_mentions_week2.get(brand_name, 0)
            
            if week2_count > 0:
                change_pct = ((week1_count - week2_count) / week2_count) * 100
                change_text = f"+{change_pct:.1f}%" if change_pct >= 0 else f"{change_pct:.1f}%"
            elif week1_count > 0:
                change_text = "+100% (mới xuất hiện)"
            else:
                change_text = "0%"
            
            brand_comparison_lines.append(
                f"- {brand_name}: Tuần trước {week2_count} lượt → Tuần này {week1_count} lượt ({change_text})"
            )
        
        brand_comparison_data = "\n".join(brand_comparison_lines)
        
        # Get sample data (Title, Type, UrlTopic) from current week, per brand
        context_lines = []
        for brand_name in all_brands:
            brand_data = week1_df[
                (week1_df["Topic"] == brand_name) &
                (week1_df["UrlTopic"].notna())
            ].head(3)
            for _, row in brand_data.iterrows():
                title = str(row.get("Title", ""))[:120]
                type_val = str(row.get("Type", ""))
                url = str(row.get("UrlTopic", ""))
                context_lines.append(f"[{brand_name}] Title: {title} | Type: {type_val} | URL: {url}")

        context_text = "\n".join(context_lines)

        prompt = get_weekly_brand_comparison_insight_prompt(
            brand, week1_display, brand_comparison_data, context_text
        )

        try:
            return self.llm_client.generate_insight(prompt)
        except Exception as e:
            print(f"Warning: LLM insight generation failed: {e}")
            return f"Phân tích so sánh thương hiệu {brand} với các đối thủ trong giai đoạn {week1_display}."


class WeeklySlide13Generator:
    """Slide 12 – Multi-brand trendline with peak annotations"""

    def __init__(self, topic_types: List[str]):
        self.topic_types = topic_types

    def generate(self, week1_df: pd.DataFrame, brand: str,
                 week1_display: str, week1_start_date: str, week1_end_date: str,
                 brands_filter: List[str] = None) -> Dict[str, Any]:
        """
        Generate slide 12 data: daily trendline per brand + peak annotation.

        For each brand, find the day with the highest mention count, then pick
        the single highest-engagement xxxTopic post on that day as the annotation.
        """
        from core.data_loader import calculate_engagement

        # Determine brands to include
        if brands_filter:
            all_brands = [b for b in brands_filter
                          if b in week1_df["Topic"].values]
        else:
            all_brands = sorted(week1_df["Topic"].dropna().unique().tolist())

        # Build complete date range
        start_date = pd.to_datetime(week1_start_date).date()
        end_date   = pd.to_datetime(week1_end_date).date()
        date_range = [d.date() for d in pd.date_range(start=start_date, end=end_date, freq='D')]

        # ── Trendline per brand ───────────────────────────────────────────────
        trendlines: Dict[str, List[Dict]] = {}
        for b in all_brands:
            df_b = week1_df[week1_df["Topic"] == b]
            daily = df_b.groupby("PublishedDay").size().to_dict()
            trendlines[b] = [
                {"date": str(d), "mentions": int(daily.get(d, 0))}
                for d in date_range
            ]

        # ── Peak annotation per brand ─────────────────────────────────────────
        annotations: Dict[str, Dict] = {}
        for b in all_brands:
            df_b = week1_df[week1_df["Topic"] == b]
            if df_b.empty:
                continue

            # Find peak day
            daily_counts = df_b.groupby("PublishedDay").size()
            if daily_counts.empty:
                continue
            peak_day = daily_counts.idxmax()
            peak_count = int(daily_counts[peak_day])

            # Pick best xxxTopic post on that day
            df_peak_topics = df_b[
                (df_b["PublishedDay"] == peak_day) &
                (df_b["Type"].isin(self.topic_types)) &
                (df_b["UrlTopic"].notna()) &
                (df_b["UrlTopic"].astype(str).str.startswith("http"))
            ].copy()

            if df_peak_topics.empty:
                # fallback: any post on peak day with URL
                df_peak_topics = df_b[
                    (df_b["PublishedDay"] == peak_day) &
                    (df_b["UrlTopic"].notna()) &
                    (df_b["UrlTopic"].astype(str).str.startswith("http"))
                ].copy()

            if df_peak_topics.empty:
                continue

            df_peak_topics["_eng"] = calculate_engagement(df_peak_topics)
            best = df_peak_topics.sort_values("_eng", ascending=False).iloc[0]

            # Snippet: first 5 words + (...)
            raw_text = str(best.get("Title") or best.get("Content") or "").strip()
            words = raw_text.split()
            snippet = " ".join(words[:5]) + "..." if len(words) > 5 else raw_text

            annotations[b] = {
                "date":      str(peak_day),
                "mentions":  peak_count,
                "snippet":   snippet,
                "url":       str(best.get("UrlTopic", "")),
                "type":      str(best.get("Type", "")),
            }

        return {
            "title":    f"Đường biểu diễn xu hướng đề cập của {brand} và một số brand khác",
            "subtitle": f"Giai đoạn: {week1_display}",
            "brands":   all_brands,
            "trendlines":   trendlines,   # {brand: [{date, mentions}, ...]}
            "annotations":  annotations,  # {brand: {date, mentions, snippet, url, type}}
        }


# ── Channel mapping cố định dùng chung ───────────────────────────────────────
CHANNEL_GROUP_MAP = {
    "Facebook":  ["fbPageComment", "fbUserTopic", "fbGroupTopic",
                  "fbGroupComment", "fbPageTopic", "fbUserComment"],
    "Fanpage":   ["fbPageComment", "fbPageTopic"],
    "News":      ["newsTopic", "newsComment"],
    "Tiktok":    ["tiktokComment", "tiktokTopic"],
    "Youtube":   ["youtubeComment", "youtubeTopic"],
}
CHANNEL_COLORS = {
    "Facebook": "#1877F2",
    "Fanpage":  "#0D47A1",
    "News":     "#E63946",
    "Tiktok":   "#010101",
    "Youtube":  "#FF0000",
    "Others":   "#9E9E9E",
}

def _map_channel_group(type_val: str) -> str:
    """Map a Type value to its display channel group."""
    for group, types in CHANNEL_GROUP_MAP.items():
        if type_val in types:
            return group
    return "Others"


class WeeklySlide14Generator:
    """Slide 13 – Channel distribution across brands (stacked bar + insight)"""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def generate(self, week1_df: pd.DataFrame, brand: str,
                 week1_display: str,
                 brands_filter: List[str] = None) -> Dict[str, Any]:

        # Determine brands
        if brands_filter:
            all_brands = [b for b in brands_filter if b in week1_df["Topic"].values]
        else:
            all_brands = sorted(week1_df["Topic"].dropna().unique().tolist())

        df = week1_df[week1_df["Topic"].isin(all_brands)].copy()
        df["ChannelGroup"] = df["Type"].apply(_map_channel_group)

        # ── Stacked bar: topic × channel group ───────────────────────────────
        stacked = (
            df.groupby(["Topic", "ChannelGroup"])
            .size()
            .reset_index(name="count")
        )
        # Build per-brand rows
        channel_groups = list(CHANNEL_COLORS.keys())
        stacked_rows = []
        for b in all_brands:
            row = {"topic": b}
            sub = stacked[stacked["Topic"] == b]
            total = sub["count"].sum()
            for cg in channel_groups:
                cnt = int(sub[sub["ChannelGroup"] == cg]["count"].sum())
                row[cg] = cnt
            row["total"] = int(total)
            stacked_rows.append(row)
        # Sort descending by total
        stacked_rows.sort(key=lambda x: x["total"], reverse=True)

        # ── Insight: top-3 channels overall ──────────────────────────────────
        channel_totals = df.groupby("ChannelGroup").size().sort_values(ascending=False)
        top3_channels = channel_totals.head(3).index.tolist()

        channel_insights = {}
        for ch in top3_channels:
            # Types belonging to this channel group
            ch_types = CHANNEL_GROUP_MAP.get(ch, [])
            # For Facebook/Fanpage/News: filter by type; Others: everything else
            if ch == "Others":
                all_known = [t for types in CHANNEL_GROUP_MAP.values() for t in types]
                df_ch = df[~df["Type"].isin(all_known)]
            else:
                df_ch = df[df["Type"].isin(ch_types)]

            # Top 3 topics by count in this channel
            top_topics = (
                df_ch.groupby("Topic").size()
                .sort_values(ascending=False)
                .head(3)
            )
            total_ch = len(df_ch)

            topic_summaries = []
            for topic_name, topic_count in top_topics.items():
                pct = (topic_count / total_ch * 100) if total_ch > 0 else 0
                # Random 2 buzz on peak day for this topic in this channel
                df_tp = df_ch[df_ch["Topic"] == topic_name]
                if len(df_tp) > 0:
                    peak_day = df_tp.groupby("PublishedDay").size().idxmax()
                    df_peak = df_tp[df_tp["PublishedDay"] == peak_day]
                    samples = df_peak.sample(min(2, len(df_peak)), random_state=42)
                    sample_texts = []
                    for _, row in samples.iterrows():
                        txt = str(row.get("Title") or row.get("Content") or "").strip()
                        words = txt.split()
                        sample_texts.append(" ".join(words[:8]) + "..." if len(words) > 8 else txt)
                else:
                    sample_texts = []

                topic_summaries.append({
                    "topic":        topic_name,
                    "count":        int(topic_count),
                    "pct":          round(pct, 1),
                    "peak_samples": sample_texts,
                })

            channel_insights[ch] = {
                "total":          int(total_ch),
                "top_topics":     topic_summaries,
            }

        return {
            "title":            f"Phân bổ đề cập trên các kênh truyền thông",
            "subtitle":         f"Giai đoạn: {week1_display}",
            "top3_channels":    top3_channels,
            "channel_insights": channel_insights,   # {channel: {total, top_topics}}
            "stacked_rows":     stacked_rows,        # [{topic, Facebook, Fanpage, ...}]
            "channel_colors":   CHANNEL_COLORS,
        }


# ── Channel mapping cố định dùng chung ───────────────────────────────────────
CHANNEL_GROUP_MAP = {
    "Facebook": ["fbPageComment", "fbUserTopic", "fbGroupTopic",
                 "fbGroupComment", "fbPageTopic", "fbUserComment"],
    "Fanpage":  ["fbPageComment", "fbPageTopic"],
    "News":     ["newsTopic", "newsComment"],
    "Tiktok":   ["tiktokComment", "tiktokTopic"],
    "Youtube":  ["youtubeComment", "youtubeTopic"],
}
CHANNEL_COLORS = {
    "Facebook": "#1877F2",
    "Fanpage":  "#0D47A1",
    "News":     "#E63946",
    "Tiktok":   "#010101",
    "Youtube":  "#FF0000",
    "Others":   "#9E9E9E",
}


def _map_channel_group(type_val: str) -> str:
    """Map a Type value to its display channel group."""
    for group, types in CHANNEL_GROUP_MAP.items():
        if type_val in types:
            return group
    return "Others"


class WeeklySlide14Generator:
    """Slide 13 – Channel distribution across brands (stacked bar % + insight)"""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def generate(self, week1_df: pd.DataFrame, brand: str,
                 week1_display: str,
                 brands_filter: List[str] = None) -> Dict[str, Any]:

        # Determine brands
        if brands_filter:
            all_brands = [b for b in brands_filter if b in week1_df["Topic"].values]
        else:
            all_brands = sorted(week1_df["Topic"].dropna().unique().tolist())

        df = week1_df[week1_df["Topic"].isin(all_brands)].copy()
        df["ChannelGroup"] = df["Type"].apply(_map_channel_group)

        # ── Stacked bar: topic x channel group ───────────────────────────────
        stacked = (
            df.groupby(["Topic", "ChannelGroup"])
            .size()
            .reset_index(name="count")
        )

        channel_groups = list(CHANNEL_COLORS.keys())
        stacked_rows = []      # raw counts
        stacked_pct_rows = []  # % ty le (dung de ve chart)

        for b in all_brands:
            row_cnt = {"topic": b}
            row_pct = {"topic": b}
            sub = stacked[stacked["Topic"] == b]
            total = int(sub["count"].sum())
            for cg in channel_groups:
                cnt = int(sub[sub["ChannelGroup"] == cg]["count"].sum())
                row_cnt[cg] = cnt
                row_pct[cg] = round(cnt / total * 100, 1) if total > 0 else 0.0
            row_cnt["total"] = total
            row_pct["total"] = 100.0
            stacked_rows.append(row_cnt)
            stacked_pct_rows.append(row_pct)

        # Sort descending by total
        stacked_rows.sort(key=lambda x: x["total"], reverse=True)
        stacked_pct_rows.sort(key=lambda x: x["total"], reverse=True)

        # ── Insight: top-3 channels overall ──────────────────────────────────
        channel_totals = df.groupby("ChannelGroup").size().sort_values(ascending=False)
        top3_channels = channel_totals.head(3).index.tolist()

        channel_insights = {}
        for ch in top3_channels:
            ch_types = CHANNEL_GROUP_MAP.get(ch, [])
            if ch == "Others":
                all_known = [t for types in CHANNEL_GROUP_MAP.values() for t in types]
                df_ch = df[~df["Type"].isin(all_known)]
            else:
                df_ch = df[df["Type"].isin(ch_types)]

            top_topics = (
                df_ch.groupby("Topic").size()
                .sort_values(ascending=False)
                .head(3)
            )
            total_ch = len(df_ch)

            topic_summaries = []
            for topic_name, topic_count in top_topics.items():
                pct = (topic_count / total_ch * 100) if total_ch > 0 else 0
                df_tp = df_ch[df_ch["Topic"] == topic_name]
                if len(df_tp) > 0:
                    peak_day = df_tp.groupby("PublishedDay").size().idxmax()
                    df_peak = df_tp[df_tp["PublishedDay"] == peak_day]
                    samples = df_peak.sample(min(2, len(df_peak)), random_state=42)
                    sample_texts = []
                    for _, r in samples.iterrows():
                        txt = str(r.get("Title") or r.get("Content") or "").strip()
                        words = txt.split()
                        sample_texts.append(" ".join(words[:8]) + "..." if len(words) > 8 else txt)
                else:
                    sample_texts = []

                topic_summaries.append({
                    "topic":        topic_name,
                    "count":        int(topic_count),
                    "pct":          round(pct, 1),
                    "peak_samples": sample_texts,
                })

            channel_insights[ch] = {
                "total":      int(total_ch),
                "top_topics": topic_summaries,
            }

        return {
            "title":            "Phân bổ đề cập trên các kênh truyền thông",
            "subtitle":         f"Giai đoạn: {week1_display}",
            "top3_channels":    top3_channels,
            "channel_insights": channel_insights,
            "stacked_rows":     stacked_rows,       # raw counts
            "stacked_pct_rows": stacked_pct_rows,   # % ty le -> dung de ve chart
            "channel_colors":   CHANNEL_COLORS,
        }


# ── Channel mapping cố định ───────────────────────────────────────────────────
CHANNEL_GROUP_MAP = {
    "Facebook": [
        "fbPageComment", "fbUserTopic", "fbGroupTopic",
        "fbGroupComment", "fbPageTopic", "fbUserComment",
    ],
    "Fanpage":  ["fbPageComment", "fbPageTopic"],
    "News":     ["newsTopic", "newsComment"],
    "Tiktok":   ["tiktokComment", "tiktokTopic"],
    "Youtube":  ["youtubeComment", "youtubeTopic"],
}

CHANNEL_COLORS = {
    "Facebook": "#1877F2",
    "Fanpage":  "#0D47A1",
    "News":     "#E63946",
    "Tiktok":   "#2D2D2D",
    "Youtube":  "#FF0000",
    "Others":   "#9E9E9E",
}


def _map_channel_group(type_val: str) -> str:
    for group, types in CHANNEL_GROUP_MAP.items():
        if type_val in types:
            return group
    return "Others"


class WeeklySlide14Generator:
    """Slide 13 – Channel distribution (stacked % bar + 3-channel insight)"""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def generate(
        self,
        week1_df: pd.DataFrame,
        brand: str,
        week1_display: str,
        brands_filter: List[str] = None,
    ) -> Dict[str, Any]:

        # ── Brands scope ──────────────────────────────────────────────────────
        if brands_filter:
            all_brands = [b for b in brands_filter if b in week1_df["Topic"].values]
        else:
            all_brands = sorted(week1_df["Topic"].dropna().unique().tolist())

        df = week1_df[week1_df["Topic"].isin(all_brands)].copy()
        df["ChannelGroup"] = df["Type"].apply(_map_channel_group)

        # ── Stacked bar data ──────────────────────────────────────────────────
        stacked = (
            df.groupby(["Topic", "ChannelGroup"])
            .size()
            .reset_index(name="count")
        )

        channel_groups = list(CHANNEL_COLORS.keys())
        stacked_rows: List[Dict] = []      # raw counts
        stacked_pct_rows: List[Dict] = []  # % tỷ lệ → dùng để vẽ chart

        for b in all_brands:
            sub = stacked[stacked["Topic"] == b]
            total = int(sub["count"].sum())
            row_cnt: Dict = {"topic": b, "total": total}
            row_pct: Dict = {"topic": b, "total": 100.0}
            for cg in channel_groups:
                cnt = int(sub[sub["ChannelGroup"] == cg]["count"].sum())
                row_cnt[cg] = cnt
                row_pct[cg] = round(cnt / total * 100, 1) if total > 0 else 0.0
            stacked_rows.append(row_cnt)
            stacked_pct_rows.append(row_pct)

        stacked_rows.sort(key=lambda x: x["total"], reverse=True)
        stacked_pct_rows.sort(key=lambda x: x["total"], reverse=True)

        # ── Top-3 channel insights ────────────────────────────────────────────
        channel_totals = df.groupby("ChannelGroup").size().sort_values(ascending=False)
        top3_channels = channel_totals.head(3).index.tolist()

        channel_insights: Dict = {}
        for ch in top3_channels:
            ch_types = CHANNEL_GROUP_MAP.get(ch, [])
            if ch == "Others":
                all_known = [t for ts in CHANNEL_GROUP_MAP.values() for t in ts]
                df_ch = df[~df["Type"].isin(all_known)]
            else:
                df_ch = df[df["Type"].isin(ch_types)]

            top_topics = (
                df_ch.groupby("Topic").size()
                .sort_values(ascending=False)
                .head(3)
            )
            total_ch = len(df_ch)

            topic_summaries = []
            for topic_name, topic_count in top_topics.items():
                pct = round(topic_count / total_ch * 100, 1) if total_ch > 0 else 0.0
                df_tp = df_ch[df_ch["Topic"] == topic_name]
                sample_texts: List[str] = []
                if len(df_tp) > 0:
                    peak_day = df_tp.groupby("PublishedDay").size().idxmax()
                    df_peak = df_tp[df_tp["PublishedDay"] == peak_day]
                    samples = df_peak.sample(min(2, len(df_peak)), random_state=42)
                    for _, r in samples.iterrows():
                        txt = str(r.get("Title") or r.get("Content") or "").strip()
                        words = txt.split()
                        sample_texts.append(
                            " ".join(words[:8]) + "..." if len(words) > 8 else txt
                        )
                topic_summaries.append({
                    "topic":        topic_name,
                    "count":        int(topic_count),
                    "pct":          pct,
                    "peak_samples": sample_texts,
                })

            channel_insights[ch] = {
                "total":      int(total_ch),
                "top_topics": topic_summaries,
            }

        return {
            "title":            "Phân bổ đề cập trên các kênh truyền thông",
            "subtitle":         f"Giai đoạn: {week1_display}",
            "top3_channels":    top3_channels,
            "channel_insights": channel_insights,
            "stacked_rows":     stacked_rows,       # raw counts
            "stacked_pct_rows": stacked_pct_rows,   # % tỷ lệ → vẽ chart
            "channel_colors":   CHANNEL_COLORS,
        }
