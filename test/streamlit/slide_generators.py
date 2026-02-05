"""
Slide generation modules for each report section
"""

import pandas as pd
import re
from typing import Dict, Any, List
from datetime import timedelta

try:
    from test.data_loader import calculate_percentage_change, calculate_engagement
    from test.llm_client import LLMClient
    from test.prompts import (
        get_overview_insight_prompt,
        get_trendline_insight_prompt,
        get_channel_breakdown_prompt,
        get_sentiment_insight_prompt
    )
except ImportError:
    from data_loader import calculate_percentage_change, calculate_engagement
    from llm_client import LLMClient
    from prompts import (
        get_overview_insight_prompt,
        get_trendline_insight_prompt,
        get_channel_breakdown_prompt,
        get_sentiment_insight_prompt
    )


class Slide1Generator:
    """Generate overview slide with KPIs"""
    
    def __init__(self, llm_client: LLMClient, topic_types: List[str], top_n: int = 6):
        """
        Initialize slide 1 generator
        
        Args:
            llm_client: LLM client for insight generation
            topic_types: List of valid topic types
            top_n: Number of top topics to analyze
        """
        self.llm_client = llm_client
        self.topic_types = topic_types
        self.top_n = top_n
    
    def generate(self, report_df: pd.DataFrame, compare_df: pd.DataFrame,
                 brand: str, report_date: str, compare_date: str) -> Dict[str, Any]:
        """
        Generate slide 1 data
        
        Args:
            report_df: Report day dataframe
            compare_df: Comparison day dataframe
            brand: Brand name
            report_date: Report date string
            compare_date: Comparison date string
            
        Returns:
            Slide 1 data dictionary
        """
        # Calculate metrics
        report_total_buzz = report_df.shape[0]
        compare_total_buzz = compare_df.shape[0]
        buzz_pct = calculate_percentage_change(report_total_buzz, compare_total_buzz)
        
        report_posts = report_df[report_df["Type"].isin(self.topic_types)].shape[0]
        compare_posts = compare_df[compare_df["Type"].isin(self.topic_types)].shape[0]
        post_pct = calculate_percentage_change(report_posts, compare_posts)
        
        today_reactions = report_df["Reactions"].sum()
        yesterday_reactions = compare_df["Reactions"].sum()
        reactions_pct = calculate_percentage_change(today_reactions, yesterday_reactions)
        
        today_shares = report_df["Shares"].sum()
        yesterday_shares = compare_df["Shares"].sum()
        shares_pct = calculate_percentage_change(today_shares, yesterday_shares)
        
        today_comments = report_total_buzz - report_posts
        yesterday_comments = compare_total_buzz - compare_posts
        comments_pct = calculate_percentage_change(today_comments, yesterday_comments)
        
        today_engagement = today_reactions + today_shares + today_comments
        yesterday_engagement = yesterday_reactions + yesterday_shares + yesterday_comments
        engagement_pct = calculate_percentage_change(today_engagement, yesterday_engagement)
        
        today_views = report_df["Views"].sum()
        yesterday_views = compare_df["Views"].sum()
        views_pct = calculate_percentage_change(today_views, yesterday_views)
        
        # Generate insight
        insight = self._generate_insight(
            report_df, brand, report_date, compare_date,
            report_total_buzz, compare_total_buzz, buzz_pct
        )
        
        return {
            "title": f"Tổng quan về thương hiệu {brand}",
            "subtitle": f"Ngày {report_date} (so sánh với {compare_date})",
            "data": [
                {
                    "type": "buzz",
                    "label": "Tổng thảo luận",
                    "today": report_total_buzz,
                    "yesterday": compare_total_buzz,
                    "change_pct": buzz_pct
                },
                {
                    "type": "post",
                    "label": "Tổng bài đăng",
                    "today": report_posts,
                    "yesterday": compare_posts,
                    "change_pct": post_pct
                },
                {
                    "type": "engagement",
                    "label": "Tổng tương tác",
                    "today": int(today_engagement),
                    "yesterday": int(yesterday_engagement),
                    "change_pct": engagement_pct
                },
                {
                    "type": "reactions",
                    "label": "Lượt reactions",
                    "today": int(today_reactions),
                    "yesterday": int(yesterday_reactions),
                    "change_pct": reactions_pct
                },
                {
                    "type": "shares",
                    "label": "Lượt chia sẻ",
                    "today": int(today_shares),
                    "yesterday": int(yesterday_shares),
                    "change_pct": shares_pct
                },
                {
                    "type": "comments",
                    "label": "Bình luận",
                    "today": today_comments,
                    "yesterday": yesterday_comments,
                    "change_pct": comments_pct
                },
                {
                    "type": "views",
                    "label": "Lượt xem",
                    "today": int(today_views),
                    "yesterday": int(yesterday_views),
                    "change_pct": views_pct
                }
            ],
            "insight": insight
        }
    
    def _generate_insight(self, report_df: pd.DataFrame, brand: str,
                          report_date: str, compare_date: str,
                          report_total_buzz: int, compare_total_buzz: int,
                          buzz_pct: float) -> str:
        """Generate insight using LLM"""
        print("         → Extracting top negative topics...")
        # Get top negative topics
        df_neg = report_df[
            (report_df["Sentiment"].str.lower() == "negative") &
            (report_df["Type"].isin(self.topic_types))
        ].copy()
        
        df_neg["engagement"] = calculate_engagement(df_neg)
        
        df_top = (
            df_neg.sort_values("engagement", ascending=False)
            .drop_duplicates(subset=["UrlTopic"])
            .head(self.top_n)
        )
        
        print(f"         → Found {len(df_top)} top negative topics")
        
        # Build context
        records = []
        for _, row in df_top.iterrows():
            records.append(
                f"""
Tiêu đề: {row.get('Title', '')}
Mô tả: {row.get('Description', '')}
Nội dung: {row.get('Content', '')}
Engagement: {row.get('engagement', 0)}
URL: {row.get('UrlTopic', '')}
""".strip()
            )
        
        context_text = "\n\n---\n\n".join(records)
        
        # Generate prompt and call LLM
        print("         → Building prompt...")
        prompt = get_overview_insight_prompt(
            brand, report_date, compare_date,
            report_total_buzz, compare_total_buzz,
            buzz_pct, context_text
        )
        
        print("         → Calling LLM API...")
        insight = self.llm_client.generate_insight(prompt)
        print("         → LLM response received")
        
        return insight


class Slide2Generator:
    """Generate trendline slide"""
    
    def __init__(self, llm_client: LLMClient, topic_types: List[str],
                 lookback_days: int = 6, top_n_peak: int = 3):
        """
        Initialize slide 2 generator
        
        Args:
            llm_client: LLM client for insight generation
            topic_types: List of valid topic types
            lookback_days: Number of days to look back
            top_n_peak: Number of peak topics to analyze
        """
        self.llm_client = llm_client
        self.topic_types = topic_types
        self.lookback_days = lookback_days
        self.top_n_peak = top_n_peak
    
    def generate(self, df: pd.DataFrame, brand: str,
                 report_date: str) -> Dict[str, Any]:
        """
        Generate slide 2 data
        
        Args:
            df: Full dataframe
            brand: Brand name
            report_date: Report date string
            
        Returns:
            Slide 2 data dictionary
        """
        report_day = pd.to_datetime(report_date).date()
        start_day = report_day - timedelta(days=self.lookback_days - 1)
        
        # Filter data for window
        df_window = df[
            (df["PublishedDay"] >= start_day) &
            (df["PublishedDay"] <= report_day)
        ].copy()
        
        # Calculate trendline
        trend_df = (
            df_window
            .groupby("PublishedDay")
            .size()
            .reset_index(name="buzz")
            .sort_values("PublishedDay")
        )
        
        trendline_data = [
            {
                "date": str(row["PublishedDay"]),
                "buzz": int(row["buzz"])
            }
            for _, row in trend_df.iterrows()
        ]
        
        # Detect peak day
        peak_row = trend_df.loc[trend_df["buzz"].idxmax()]
        peak_day = peak_row["PublishedDay"]
        peak_buzz = int(peak_row["buzz"])
        
        current_buzz = int(
            trend_df.loc[trend_df["PublishedDay"] == report_day, "buzz"].iloc[0]
        ) if report_day in trend_df["PublishedDay"].values else 0
        
        is_still_hot = current_buzz >= 0.5 * peak_buzz
        
        # Generate insight
        insight, peak_links = self._generate_insight(
            df_window, brand, str(peak_day), peak_buzz,
            report_date, current_buzz
        )
        
        return {
            "title": f"Trendline | Diễn biến thảo luận",
            "subtitle": f"Khoảng thời gian: {start_day} → {report_day}",
            "window": {
                "start_date": str(start_day),
                "end_date": str(report_day)
            },
            "trendline": trendline_data,
            "peak_day": {
                "date": str(peak_day),
                "buzz": peak_buzz,
                "links": peak_links
            },
            "current_day": {
                "date": str(report_day),
                "buzz": current_buzz,
                "is_still_hot": is_still_hot
            },
            "insight": insight
        }
    
    def _generate_insight(self, df_window: pd.DataFrame, brand: str,
                          peak_day: str, peak_buzz: int,
                          report_date: str, current_buzz: int) -> tuple:
        """Generate insight using LLM"""
        print("         → Analyzing peak day topics...")
        peak_day_date = pd.to_datetime(peak_day).date()
        
        # Get peak day negative topics
        df_peak = df_window[
            (df_window["PublishedDay"] == peak_day_date) &
            (df_window["Sentiment"].str.lower() == "negative") &
            (df_window["Type"].isin(self.topic_types))
        ].copy()
        
        df_peak["engagement"] = calculate_engagement(df_peak)
        
        df_peak_top = (
            df_peak
            .sort_values("engagement", ascending=False)
            .drop_duplicates(subset=["UrlTopic"])
            .head(self.top_n_peak)
        )
        
        print(f"         → Found {len(df_peak_top)} peak day topics")
        
        # Build context
        peak_context = []
        for _, row in df_peak_top.iterrows():
            peak_context.append(
                f"""
Tiêu đề: {row['Title']}
Mô tả: {row['Description']}
Nội dung: {row['Content']}
Engagement: {row['engagement']}
URL: {row['UrlTopic']}
""".strip()
            )
        
        peak_context_text = "\n\n---\n\n".join(peak_context)
        
        # Get peak links
        peak_links = (
            df_peak_top["UrlTopic"]
            .dropna()
            .unique()
            .tolist()
        )
        
        # Generate prompt and call LLM
        print("         → Building prompt...")
        prompt = get_trendline_insight_prompt(
            brand, peak_day, peak_buzz,
            report_date, current_buzz,
            peak_context_text
        )
        
        print("         → Calling LLM API...")
        insight = self.llm_client.generate_insight(prompt)
        print("         → LLM response received")
        
        return insight, peak_links


class Slide4Generator:
    """Generate sentiment & brand attribute slide"""
    
    def __init__(self, llm_client: LLMClient, top_n_attr: int = 6):
        """
        Initialize slide 4 generator
        
        Args:
            llm_client: LLM client for insight generation
            top_n_attr: Number of top attributes to analyze
        """
        self.llm_client = llm_client
        self.top_n_attr = top_n_attr
    
    def generate(self, report_df: pd.DataFrame, brand: str,
                 report_date: str) -> Dict[str, Any]:
        """
        Generate slide 4 data
        
        Args:
            report_df: Report day dataframe
            brand: Brand name
            report_date: Report date string
            
        Returns:
            Slide 4 data dictionary
        """
        # Normalize sentiment and labels
        report_df = report_df.copy()
        report_df["Sentiment"] = report_df["Sentiment"].str.capitalize()
        report_df["Label_List"] = report_df["Labels"].apply(
            lambda x: [i.strip() for i in str(x).split(",") if i.strip()]
        )
        
        df_exploded = report_df.explode("Label_List")
        
        # Sentiment distribution
        sentiment_dist = (
            report_df["Sentiment"]
            .value_counts()
            .reset_index(name='Count')
            .rename(columns={"index": "Sentiment"})
        )
        
        # Attribute x Sentiment
        attr_sentiment = (
            df_exploded.groupby(["Label_List", "Sentiment"])
            .size()
            .reset_index(name="Count")
        )
        
        top_attrs = (
            attr_sentiment.groupby("Label_List")["Count"]
            .sum()
            .sort_values(ascending=False)
            .head(self.top_n_attr)
            .index
        )
        
        attr_sentiment_top = attr_sentiment[
            attr_sentiment["Label_List"].isin(top_attrs)
        ]
        
        pivot_df = attr_sentiment_top.pivot(
            index="Label_List",
            columns="Sentiment",
            values="Count"
        ).fillna(0)
        
        # Generate insight
        insight = self._generate_insight(
            df_exploded, top_attrs, brand, report_date,
            sentiment_dist, pivot_df
        )
        
        return {
            "title": "Sentiment & Brand Attribute",
            "subtitle": f"Ngày {report_date}",
            "sentiment_distribution": sentiment_dist.to_dict(orient="records"),
            "attribute_sentiment": pivot_df.reset_index().to_dict(orient="records"),
            "insight": insight
        }
    
    def _generate_insight(self, df_exploded: pd.DataFrame, top_attrs: pd.Index,
                          brand: str, report_date: str,
                          sentiment_dist: pd.DataFrame,
                          pivot_df: pd.DataFrame) -> str:
        """Generate insight using LLM"""
        print("         → Building evidence from top posts...")
        # Build evidence
        evidence_df = df_exploded[
            df_exploded["Label_List"].isin(top_attrs)
        ].copy()
        
        evidence_df["engagement"] = calculate_engagement(evidence_df)
        
        evidence_top = (
            evidence_df
            .sort_values("engagement", ascending=False)
            .drop_duplicates(subset=["UrlTopic"])
            .head(5)
            .reset_index(drop=True)
        )
        
        print(f"         → Found {len(evidence_top)} evidence posts")
        
        url_map = {}
        evidence_blocks = []
        
        for idx, row in evidence_top.iterrows():
            key = f"URL_{idx+1}"
            url_map[key] = row["UrlTopic"]
            
            evidence_blocks.append(
                f"""
[{key}]
Sentiment: {row['Sentiment']}
Brand Attribute: {row['Label_List']}
Tiêu đề: {row['Title']}
Mô tả: {row['Description']}
Nội dung: {row['Content']}
""".strip()
            )
        
        evidence_context = "\n\n---\n\n".join(evidence_blocks)
        url_whitelist_text = "\n".join([f"{k}: {v}" for k, v in url_map.items()])
        
        # Generate prompt and call LLM
        print("         → Building prompt...")
        prompt = get_sentiment_insight_prompt(
            brand, report_date,
            sentiment_dist.to_string(index=False),
            pivot_df.reset_index().to_string(index=False),
            evidence_context, url_whitelist_text
        )
        
        print("         → Calling LLM API...")
        raw_insight = self.llm_client.generate_insight(prompt)
        print("         → LLM response received")
        
        # Replace URL keys with real URLs
        print("         → Replacing URL placeholders...")
        final_insight = raw_insight
        for key, real_url in url_map.items():
            final_insight = re.sub(
                rf"\[Nguồn:\s*{key}\]",
                f"[Nguồn: {real_url}]",
                final_insight
            )
        
        return final_insight



class Slide3Generator:
    """Generate channel breakdown slide"""
    
    def __init__(self, llm_client: LLMClient, topic_types: List[str], top_n_buzz: int = 6):
        """
        Initialize slide 3 generator
        
        Args:
            llm_client: LLM client for insight generation
            topic_types: List of valid topic types
            top_n_buzz: Number of top buzz posts to analyze
        """
        self.llm_client = llm_client
        self.topic_types = topic_types
        self.top_n_buzz = top_n_buzz
    
    def generate(self, report_df: pd.DataFrame, compare_df: pd.DataFrame,
                 brand: str, report_date: str, compare_date: str) -> Dict[str, Any]:
        """
        Generate slide 3 data
        
        Args:
            report_df: Report day dataframe
            compare_df: Comparison day dataframe
            brand: Brand name
            report_date: Report date string
            compare_date: Comparison date string
            
        Returns:
            Slide 3 data dictionary
        """
        print("      📡 Analyzing channel distribution...")
        
        # Channel distribution
        channel_today = report_df.groupby("Channel").size().reset_index(name="today_buzz")
        channel_yesterday = compare_df.groupby("Channel").size().reset_index(name="yesterday_buzz")
        
        channel_df = channel_today.merge(
            channel_yesterday, on="Channel", how="outer"
        ).fillna(0)
        
        channel_df["change_pct"] = channel_df.apply(
            lambda r: calculate_percentage_change(r["today_buzz"], r["yesterday_buzz"]), axis=1
        )
        
        channel_df = channel_df.sort_values("today_buzz", ascending=False)
        
        # Check if channel_df is empty
        if len(channel_df) == 0:
            print("      ⚠️  Warning: No channel data found")
            top_channel = "Unknown"
        else:
            top_channel = channel_df.iloc[0]["Channel"]
            print(f"      → Top channel: {top_channel}")
            print(f"      → Total channels: {len(channel_df)}")
        
        # Generate insight
        insight = self._generate_insight(
            report_df, brand, report_date, compare_date,
            top_channel, channel_df
        )
        
        return {
            "title": "Phân tích theo kênh thảo luận",
            "subtitle": f"Ngày {report_date} (so sánh với {compare_date})",
            "top_channel": top_channel,
            "channel_distribution": channel_df.to_dict(orient="records"),
            "insight": insight
        }
    
    def _generate_insight(self, report_df: pd.DataFrame, brand: str,
                          report_date: str, compare_date: str,
                          top_channel: str, channel_df: pd.DataFrame) -> str:
        """Generate insight using LLM"""
        print("         → Extracting top buzz from top channel...")
        
        # Check if we have valid top_channel
        if top_channel == "Unknown" or len(channel_df) == 0:
            print("         ⚠️  No channel data available, returning default insight")
            return f"Không có dữ liệu thảo luận cho ngày {report_date}. Vui lòng kiểm tra lại dữ liệu nguồn hoặc chọn ngày khác có dữ liệu."
        
        # Get top buzz in top channel
        df_top_channel = report_df[
            (report_df["Channel"] == top_channel) &
            (report_df["Type"].isin(self.topic_types))
        ].copy()
        
        # Check if we have data
        if len(df_top_channel) == 0:
            print("         ⚠️  No posts found in top channel, returning default insight")
            return f"Kênh {top_channel} không có bài đăng nào trong ngày {report_date}."
        
        df_top_channel["engagement"] = calculate_engagement(df_top_channel)
        
        df_top_buzz = (
            df_top_channel
            .sort_values("engagement", ascending=False)
            .drop_duplicates(subset=["UrlTopic"])
            .head(self.top_n_buzz)
            .reset_index(drop=True)
        )
        
        print(f"         → Found {len(df_top_buzz)} top buzz posts")
        
        # If still no data, return default
        if len(df_top_buzz) == 0:
            print("         ⚠️  No buzz posts found, returning default insight")
            return f"Không tìm thấy bài đăng nổi bật trên kênh {top_channel} trong ngày {report_date}."
        
        # Build URL map
        url_map = {}
        buzz_blocks = []
        
        for idx, row in df_top_buzz.iterrows():
            key = f"URL_{idx+1}"
            url_map[key] = row["UrlTopic"]
            
            buzz_blocks.append(
                f"""
[{key}]
Tiêu đề: {row['Title']}
Mô tả: {row['Description']}
Nội dung: {row['Content']}
Channel: {row['Channel']}
SiteName: {row.get('SiteName', 'N/A')}
Engagement: {row['engagement']}
""".strip()
            )
        
        buzz_context = "\n\n---\n\n".join(buzz_blocks)
        url_whitelist_text = "\n".join([f"{k}: {v}" for k, v in url_map.items()])
        
        # Generate prompt and call LLM
        print("         → Building prompt...")
        prompt = get_channel_breakdown_prompt(
            brand, report_date, top_channel,
            channel_df.to_string(index=False),
            buzz_context, url_whitelist_text
        )
        
        print("         → Calling LLM API...")
        raw_insight = self.llm_client.generate_insight(prompt)
        print("         → LLM response received")
        
        # Replace URL keys with real URLs
        print("         → Replacing URL placeholders...")
        final_insight = raw_insight
        for key, real_url in url_map.items():
            final_insight = re.sub(
                rf"\[Nguồn:\s*{key}\]",
                f"[Nguồn: {real_url}]",
                final_insight
            )
        
        return final_insight
