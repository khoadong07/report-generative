"""
Slide 01 – MASAN CONSUMER & MARKETS
Phần 1: Main Brand Overview (Buzz trend, Sentiment, Channel distribution)
Phần 2: Competitor Analysis (Channel & Sentiment comparison)
Input: df (full dataframe), main_brand, competitors, report_date
Output: slide data with charts and insights
"""
from typing import Any, Dict, List
import pandas as pd
from datetime import datetime, timedelta

from core.llm_client import LLMClient
from weekly_report.slides.base import SlideGenerator, InsightMixin


class Slide01MasanMarket(SlideGenerator, InsightMixin):
    """Generate Masan Consumer & Markets overview slide."""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    # ── Type mapping for channel grouping ─────────────────────────────────────
    TYPE_MAPPING = {
        "fbPageComment": "Fanpage",
        "fbPageTopic": "Fanpage",
        "fbGroupComment": "Facebook",
        "fbUserComment": "Facebook",
        "fbGroupTopic": "Facebook",
        "fbUserTopic": "Facebook",
        "forumComment": "Forum",
        "forumTopic": "Forum",
        "newsTopic": "News",
    }

    # ── public ────────────────────────────────────────────────────────────────
    def generate(self, *, df: pd.DataFrame, main_brand: str, 
                 competitors: List[str], report_date: str) -> Dict[str, Any]:
        """
        Generate slide with 2 parts:
        - Part 1: Main brand analysis (4 weeks)
        - Part 2: Competitor comparison
        """
        
        # Parse report date and calculate week ranges
        report_dt = pd.to_datetime(report_date)
        
        # Current week (week 1): last 7 days from report_date
        week1_end = report_dt
        week1_start = week1_end - timedelta(days=6)
        
        # Week 2: 7-13 days before report_date
        week2_end = week1_start - timedelta(days=1)
        week2_start = week2_end - timedelta(days=6)
        
        # Week 3: 14-20 days before
        week3_end = week2_start - timedelta(days=1)
        week3_start = week3_end - timedelta(days=6)
        
        # Week 4: 21-27 days before
        week4_end = week3_start - timedelta(days=1)
        week4_start = week4_end - timedelta(days=6)
        
        # Prepare dataframe
        df_clean = df.copy()
        df_clean["PublishedDate"] = pd.to_datetime(df_clean["PublishedDate"], errors="coerce")
        df_clean["TypeGroup"] = df_clean["Type"].map(self.TYPE_MAPPING).fillna("Khác")
        
        # Filter data for 4 weeks
        df_4weeks = df_clean[
            (df_clean["PublishedDate"] >= week4_start) & 
            (df_clean["PublishedDate"] <= week1_end)
        ].copy()
        
        # Part 1: Main Brand Analysis
        part1_data = self._generate_main_brand_analysis(
            df_4weeks, main_brand, week1_start, week1_end,
            week2_start, week2_end, week3_start, week3_end,
            week4_start, week4_end
        )
        
        # Part 2: Competitor Analysis
        part2_data = self._generate_competitor_analysis(
            df_4weeks, main_brand, competitors, week1_start, week1_end
        )
        
        # Generate overall conclusion
        conclusion = self._generate_insight(
            df_main=df_4weeks[df_4weeks["Topic"] == main_brand],
            df_competitors=df_4weeks[df_4weeks["Topic"].isin(competitors)],
            main_brand=main_brand,
            competitors=competitors,
            part1_data=part1_data,
            part2_data=part2_data,
            report_date=report_date
        )
        
        return {
            "title": "MASAN CONSUMER & MARKETS",
            "subtitle": f"Giai đoạn: {week1_start.strftime('%d/%m/%Y')} - {week1_end.strftime('%d/%m/%Y')}",
            "part1_main_brand": part1_data,
            "part2_competitors": part2_data,
            "conclusion": conclusion,
            "report_date": report_date,
        }

    # ── Part 1: Main Brand Analysis ───────────────────────────────────────────
    def _generate_main_brand_analysis(self, df: pd.DataFrame, main_brand: str,
                                       w1_start, w1_end, w2_start, w2_end,
                                       w3_start, w3_end, w4_start, w4_end) -> Dict[str, Any]:
        """Generate main brand analysis with buzz trend, sentiment, and channels."""
        
        df_brand = df[df["Topic"] == main_brand].copy()
        
        # 1. Weekly buzz trend (4 weeks)
        weekly_buzz = self._calculate_weekly_buzz(
            df_brand, w1_start, w1_end, w2_start, w2_end,
            w3_start, w3_end, w4_start, w4_end
        )
        
        # 2. Current week sentiment distribution
        df_current_week = df_brand[
            (df_brand["PublishedDate"] >= w1_start) & 
            (df_brand["PublishedDate"] <= w1_end)
        ]
        sentiment_dist = self._calculate_sentiment_distribution(df_current_week)
        
        # 3. Channel distribution (current week)
        channel_dist = self._calculate_channel_distribution(df_current_week)
        
        # 4. Generate channel insight via LLM
        channel_insight = self._generate_channel_insight(
            channel_dist, main_brand, w1_start, w1_end
        )
        
        return {
            "brand": main_brand,
            "weekly_buzz_trend": weekly_buzz,
            "sentiment_distribution": sentiment_dist,
            "channel_distribution": channel_dist,
            "channel_insight": channel_insight,
        }

    def _calculate_weekly_buzz(self, df: pd.DataFrame,
                                w1_start, w1_end, w2_start, w2_end,
                                w3_start, w3_end, w4_start, w4_end) -> List[Dict]:
        """Calculate buzz count for each week."""
        weeks = [
            ("week4", w4_start, w4_end),
            ("week3", w3_start, w3_end),
            ("week2", w2_start, w2_end),
            ("week1", w1_start, w1_end),
        ]
        
        result = []
        for week_name, start, end in weeks:
            count = len(df[(df["PublishedDate"] >= start) & (df["PublishedDate"] <= end)])
            result.append({
                "week": f"{start.strftime('%d/%m')} - {end.strftime('%d/%m')}",
                "buzz_count": count,
            })
        
        return result

    def _calculate_sentiment_distribution(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate sentiment distribution with percentages."""
        total = len(df)
        if total == 0:
            return {
                "total_buzz": 0,
                "positive": {"count": 0, "percent": 0},
                "neutral": {"count": 0, "percent": 0},
                "negative": {"count": 0, "percent": 0},
            }
        
        sentiment_counts = df["Sentiment"].value_counts().to_dict()
        pos = sentiment_counts.get("Positive", 0)
        neu = sentiment_counts.get("Neutral", 0)
        neg = sentiment_counts.get("Negative", 0)
        
        return {
            "total_buzz": total,
            "positive": {"count": pos, "percent": round(pos / total * 100, 1)},
            "neutral": {"count": neu, "percent": round(neu / total * 100, 1)},
            "negative": {"count": neg, "percent": round(neg / total * 100, 1)},
        }

    def _calculate_channel_distribution(self, df: pd.DataFrame) -> List[Dict]:
        """Calculate channel distribution with percentages."""
        total = len(df)
        if total == 0:
            return []
        
        channel_counts = df["TypeGroup"].value_counts().to_dict()
        result = []
        for channel, count in channel_counts.items():
            result.append({
                "channel": channel,
                "count": count,
                "percent": round(count / total * 100, 1),
            })
        
        return sorted(result, key=lambda x: x["count"], reverse=True)

    def _generate_channel_insight(self, channel_dist: List[Dict], 
                                   brand: str, start_date, end_date) -> str:
        """Generate LLM insight about channel distribution."""
        if not channel_dist:
            return f"Không có dữ liệu thảo luận về {brand} trong giai đoạn này."
        
        channel_summary = "\n".join([
            f"- {ch['channel']}: {ch['count']} ({ch['percent']}%)"
            for ch in channel_dist
        ])
        
        prompt = f"""Phân tích kênh thảo luận {brand} ({start_date.strftime('%d/%m')} - {end_date.strftime('%d/%m')}):

{channel_summary}

Viết insight ngắn (2-3 câu):
- Kênh nào chiếm ưu thế
- Khuyến nghị về chiến lược kênh"""
        
        return self.llm_client.generate_insight(prompt)

    # ── Part 2: Competitor Analysis ───────────────────────────────────────────
    def _generate_competitor_analysis(self, df: pd.DataFrame, main_brand: str,
                                       competitors: List[str],
                                       w1_start, w1_end) -> Dict[str, Any]:
        """Generate competitor comparison for channels and sentiment."""
        
        # Filter current week data
        df_current = df[
            (df["PublishedDate"] >= w1_start) & 
            (df["PublishedDate"] <= w1_end)
        ]
        
        # All brands to compare (main brand first, then competitors)
        all_brands = [main_brand] + competitors
        
        # 1. Channel distribution by brand (stacked column chart)
        channel_by_brand = self._calculate_channel_by_brand(df_current, all_brands)
        
        # 2. Sentiment distribution by brand (stacked column chart)
        sentiment_by_brand = self._calculate_sentiment_by_brand(df_current, all_brands)
        
        return {
            "brands": all_brands,
            "channel_distribution": channel_by_brand,
            "sentiment_distribution": sentiment_by_brand,
        }

    def _calculate_channel_by_brand(self, df: pd.DataFrame, 
                                     brands: List[str]) -> List[Dict]:
        """Calculate channel distribution for each brand (for stacked column chart)."""
        result = []
        
        for brand in brands:
            df_brand = df[df["Topic"] == brand]
            total = len(df_brand)
            
            if total == 0:
                result.append({
                    "brand": brand,
                    "total": 0,
                    "channels": [],
                })
                continue
            
            channel_counts = df_brand["TypeGroup"].value_counts().to_dict()
            channels = []
            for channel, count in channel_counts.items():
                channels.append({
                    "channel": channel,
                    "count": count,
                    "percent": round(count / total * 100, 1),
                })
            
            result.append({
                "brand": brand,
                "total": total,
                "channels": sorted(channels, key=lambda x: x["count"], reverse=True),
            })
        
        return result

    def _calculate_sentiment_by_brand(self, df: pd.DataFrame,
                                       brands: List[str]) -> List[Dict]:
        """Calculate sentiment distribution for each brand (for stacked column chart)."""
        result = []
        
        for brand in brands:
            df_brand = df[df["Topic"] == brand]
            total = len(df_brand)
            
            if total == 0:
                result.append({
                    "brand": brand,
                    "total": 0,
                    "sentiments": [],
                })
                continue
            
            sentiment_counts = df_brand["Sentiment"].value_counts().to_dict()
            sentiments = []
            for sentiment in ["Positive", "Neutral", "Negative"]:
                count = sentiment_counts.get(sentiment, 0)
                sentiments.append({
                    "sentiment": sentiment,
                    "count": count,
                    "percent": round(count / total * 100, 1),
                })
            
            result.append({
                "brand": brand,
                "total": total,
                "sentiments": sentiments,
            })
        
        return result

    # ── Overall Insight Generation ────────────────────────────────────────────
    def _generate_insight(self, *, df_main: pd.DataFrame, df_competitors: pd.DataFrame,
                          main_brand: str, competitors: List[str],
                          part1_data: Dict, part2_data: Dict,
                          report_date: str) -> str:
        """Generate overall conclusion and recommendations."""
        
        # Prepare summary data
        main_buzz = part1_data["weekly_buzz_trend"][-1]["buzz_count"]
        main_sentiment = part1_data["sentiment_distribution"]
        
        competitor_summary = []
        for brand_data in part2_data["sentiment_distribution"]:
            if brand_data["brand"] != main_brand:
                competitor_summary.append(
                    f"{brand_data['brand']}: {brand_data['total']} buzz"
                )
        
        prompt = f"""Phân tích tổng quan về thương hiệu {main_brand} và thị trường trong tuần báo cáo (kết thúc {report_date}):

PHẦN 1 - MAIN BRAND ({main_brand}):
- Tổng buzz tuần hiện tại: {main_buzz}
- Sentiment: Positive {main_sentiment['positive']['percent']}%, Neutral {main_sentiment['neutral']['percent']}%, Negative {main_sentiment['negative']['percent']}%
- Xu hướng 4 tuần: {', '.join([f"{w['buzz_count']}" for w in part1_data['weekly_buzz_trend']])}

PHẦN 2 - ĐỐI THỦ:
{chr(10).join(competitor_summary)}

Kênh thảo luận chính: {part1_data['channel_distribution'][0]['channel'] if part1_data['channel_distribution'] else 'N/A'}

Viết đánh giá ngắn gọn (100-120 từ):
1. So sánh hiệu suất vs đối thủ
2. Ý nghĩa sentiment
3. 2-3 khuyến nghị chính"""
        
        return self.llm_client.generate_insight(prompt)
