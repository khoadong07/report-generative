"""
Slide 03 – Chỉ số sức khỏe và kênh thảo luận
Charts: Sentiment by brand (with NSR line), Channel distribution, Top sources, Health index table
Input: df, main_brand, competitors, week_start, week_end, llm_client
Output: slide data with 4 components and insight
"""
from typing import Any, Dict, List, Tuple
import pandas as pd
from datetime import datetime

from core.llm_client import LLMClient
from weekly_report.slides.base import SlideGenerator, InsightMixin


class Slide03HealthChannels(SlideGenerator, InsightMixin):
    """Generate health index and channel analysis slide."""

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
    def generate(self, *, df: pd.DataFrame, main_brand: str, competitors: List[str],
                 week_start: datetime, week_end: datetime) -> Dict[str, Any]:
        """
        Generate slide with:
        1. Sentiment by brand with NSR line
        2. Channel distribution by brand
        3. Top sources (competitors only)
        4. Health index table by Labels1
        5. Insight (2 paragraphs, 25-30 words each)
        """
        
        # Prepare dataframe
        df_clean = df.copy()
        df_clean["PublishedDate"] = pd.to_datetime(df_clean["PublishedDate"], errors="coerce")
        df_clean["TypeGroup"] = df_clean["Type"].map(self.TYPE_MAPPING).fillna("Khác")
        
        # Filter current week
        df_week = df_clean[
            (df_clean["PublishedDate"] >= week_start) & 
            (df_clean["PublishedDate"] <= week_end)
        ].copy()
        
        all_brands = [main_brand] + competitors
        
        # 1. Sentiment by brand with NSR
        sentiment_nsr = self._calculate_sentiment_nsr(df_week, all_brands)
        
        # 2. Channel distribution by brand
        channel_dist = self._calculate_channel_distribution(df_week, all_brands)
        
        # 3. Top sources (competitors only)
        top_sources = self._calculate_top_sources(df_week, competitors)
        
        # 4. Health index table by Labels1
        health_table = self._calculate_health_table(df_week, all_brands)
        
        # 5. Generate insight
        insight = self._generate_insight(
            sentiment_nsr=sentiment_nsr,
            channel_dist=channel_dist,
            top_sources=top_sources,
            health_table=health_table,
            main_brand=main_brand
        )
        
        return {
            "title": "Chỉ số sức khỏe và kênh thảo luận",
            "subtitle": f"Giai đoạn: {week_start.strftime('%d/%m/%Y')} - {week_end.strftime('%d/%m/%Y')}",
            "sentiment_nsr": sentiment_nsr,
            "channel_distribution": channel_dist,
            "top_sources": top_sources,
            "health_table": health_table,
            "insight": insight,
            "brands": all_brands,
        }

    # ── Chart 1: Sentiment with NSR ───────────────────────────────────────────
    def _calculate_sentiment_nsr(self, df: pd.DataFrame, brands: List[str]) -> List[Dict]:
        """Calculate sentiment distribution and NSR for each brand."""
        result = []
        
        for brand in brands:
            df_brand = df[df["Topic"] == brand]
            total = len(df_brand)
            
            if total == 0:
                result.append({
                    "brand": brand,
                    "total": 0,
                    "positive": 0,
                    "neutral": 0,
                    "negative": 0,
                    "positive_pct": 0,
                    "neutral_pct": 0,
                    "negative_pct": 0,
                    "nsr": None
                })
                continue
            
            sentiment_counts = df_brand["Sentiment"].value_counts().to_dict()
            pos = sentiment_counts.get("Positive", 0)
            neu = sentiment_counts.get("Neutral", 0)
            neg = sentiment_counts.get("Negative", 0)
            
            pos_pct = round(pos / total * 100, 1)
            neu_pct = round(neu / total * 100, 1)
            neg_pct = round(neg / total * 100, 1)
            
            # Calculate NSR
            nsr = None
            if (pos_pct + neg_pct) > 0:
                nsr = round((pos_pct - neg_pct) / (pos_pct + neg_pct) * 100, 1)
            
            result.append({
                "brand": brand,
                "total": total,
                "positive": pos,
                "neutral": neu,
                "negative": neg,
                "positive_pct": pos_pct,
                "neutral_pct": neu_pct,
                "negative_pct": neg_pct,
                "nsr": nsr
            })
        
        return result

    # ── Chart 2: Channel Distribution ─────────────────────────────────────────
    def _calculate_channel_distribution(self, df: pd.DataFrame, brands: List[str]) -> List[Dict]:
        """Calculate channel distribution for each brand (stacked column)."""
        result = []
        
        for brand in brands:
            df_brand = df[df["Topic"] == brand]
            total = len(df_brand)
            
            if total == 0:
                result.append({
                    "brand": brand,
                    "total": 0,
                    "channels": []
                })
                continue
            
            channel_counts = df_brand["TypeGroup"].value_counts().to_dict()
            channels = []
            for channel, count in channel_counts.items():
                channels.append({
                    "channel": channel,
                    "count": count,
                    "percent": round(count / total * 100, 1)
                })
            
            result.append({
                "brand": brand,
                "total": total,
                "channels": sorted(channels, key=lambda x: x["count"], reverse=True)
            })
        
        return result

    # ── Chart 3: Top Sources (Competitors only) ───────────────────────────────
    def _calculate_top_sources(self, df: pd.DataFrame, competitors: List[str]) -> List[Dict]:
        """Calculate top 5 sources from competitors' discussions (horizontal bar)."""
        
        # Filter competitors only
        df_competitors = df[df["Topic"].isin(competitors)]
        
        # Filter only Topics (not comments)
        df_topics = df_competitors[df_competitors["Type"].str.endswith("Topic", na=False)]
        
        if df_topics.empty:
            return []
        
        # Count by SiteName
        source_counts = df_topics["SiteName"].value_counts().head(5)
        
        result = []
        for idx, (site_name, count) in enumerate(source_counts.items(), 1):
            result.append({
                "rank": idx,
                "site_name": site_name,
                "buzz_count": int(count)
            })
        
        return result

    # ── Chart 4: Health Index Table ───────────────────────────────────────────
    def _calculate_health_table(self, df: pd.DataFrame, brands: List[str]) -> Dict[str, Any]:
        """Calculate NSR by Labels1 for each brand (table format)."""
        
        # Get top 5 Labels1 overall
        if "Labels1" not in df.columns or df["Labels1"].isna().all():
            return {
                "labels": [],
                "data": {}
            }
        
        top_labels = df["Labels1"].value_counts().head(5).index.tolist()
        
        # Calculate NSR for each brand x label combination
        data = {}
        for brand in brands:
            data[brand] = {}
            df_brand = df[df["Topic"] == brand]
            
            for label in top_labels:
                df_label = df_brand[df_brand["Labels1"] == label]
                
                if len(df_label) == 0:
                    data[brand][label] = None
                    continue
                
                sentiment_counts = df_label["Sentiment"].value_counts().to_dict()
                pos = sentiment_counts.get("Positive", 0)
                neg = sentiment_counts.get("Negative", 0)
                total = len(df_label)
                
                pos_pct = pos / total * 100 if total > 0 else 0
                neg_pct = neg / total * 100 if total > 0 else 0
                
                # Calculate NSR
                if (pos_pct + neg_pct) > 0:
                    nsr = round((pos_pct - neg_pct) / (pos_pct + neg_pct) * 100, 1)
                    data[brand][label] = nsr
                else:
                    data[brand][label] = None
        
        return {
            "labels": top_labels,
            "data": data
        }

    # ── Insight Generation ────────────────────────────────────────────────────
    def _generate_insight(self, *, sentiment_nsr: List[Dict], channel_dist: List[Dict],
                          top_sources: List[Dict], health_table: Dict,
                          main_brand: str) -> str:
        """Generate 2-paragraph insight (25-30 words each)."""
        
        # Find main brand NSR
        main_nsr = None
        for item in sentiment_nsr:
            if item["brand"] == main_brand:
                main_nsr = item["nsr"]
                break
        
        # Find top channel for main brand
        main_channel = "N/A"
        for item in channel_dist:
            if item["brand"] == main_brand and item["channels"]:
                main_channel = item["channels"][0]["channel"]
                break
        
        # Top source
        top_source = top_sources[0]["site_name"] if top_sources else "N/A"
        
        # Average NSR from health table
        health_data = health_table.get("data", {})
        avg_nsr_list = []
        if main_brand in health_data:
            for label, nsr in health_data[main_brand].items():
                if nsr is not None:
                    avg_nsr_list.append(nsr)
        avg_nsr = round(sum(avg_nsr_list) / len(avg_nsr_list), 1) if avg_nsr_list else None
        
        prompt = f"""Viết insight về sức khỏe thương hiệu {main_brand}:

DỮ LIỆU:
- NSR: {main_nsr if main_nsr is not None else 'N/A'}
- Kênh chính: {main_channel}
- Nguồn nổi bật đối thủ: {top_source}
- NSR trung bình theo chủ đề: {avg_nsr if avg_nsr is not None else 'N/A'}

Viết 2 đoạn ngắn:
Đoạn 1 (25-30 từ): Đánh giá sức khỏe thương hiệu qua NSR và sentiment
Đoạn 2 (25-30 từ): Nhận xét về kênh thảo luận và khuyến nghị

Không cần dẫn chứng số liệu buzz cụ thể."""
        
        return self.llm_client.generate_insight(prompt)
