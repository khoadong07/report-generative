"""
Slide 05 – Tổng quan thảo luận theo ngành hàng
Detailed analysis for each category (Gia vị, etc.)
Charts: Brand SOV donut, Product category pie, Top 10 products list
Input: df, category_name, week_start, week_end, llm_client
Output: slide data with 3 components and insight
"""
from typing import Any, Dict, List
import pandas as pd
from datetime import datetime

from core.llm_client import LLMClient
from weekly_report.slides.base import SlideGenerator, InsightMixin


class Slide05CategoryDetail(SlideGenerator, InsightMixin):
    """Generate detailed analysis for a specific product category."""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    # ── public ────────────────────────────────────────────────────────────────
    def generate(self, *, df: pd.DataFrame, category_name: str,
                 week_start: datetime, week_end: datetime) -> Dict[str, Any]:
        """
        Generate slide for specific category with:
        1. Brand SOV (Share of Voice) - donut chart
        2. Product category distribution - pie chart
        3. Top 10 products by buzz
        4. Insight (2 paragraphs about Masan Consumer in this category)
        """
        
        # Prepare dataframe
        df_clean = df.copy()
        df_clean["PublishedDate"] = pd.to_datetime(df_clean["PublishedDate"], errors="coerce")
        
        # Check if required columns exist
        if "Ngành hàng" not in df_clean.columns:
            return self._empty_result(category_name, week_start, week_end)
        
        # Filter by category and week
        df_category = df_clean[
            (df_clean["Ngành hàng"] == category_name) &
            (df_clean["PublishedDate"] >= week_start) & 
            (df_clean["PublishedDate"] <= week_end)
        ]
        
        if df_category.empty:
            return self._empty_result(category_name, week_start, week_end)
        
        # 1. Brand SOV (Share of Voice)
        brand_sov = self._calculate_brand_sov(df_category)
        
        # 2. Product Category Distribution (Cate)
        cate_distribution = self._calculate_cate_distribution(df_category)
        
        # 3. Top 10 Products
        top_products = self._get_top_products(df_category, top_n=10)
        
        # 4. Generate Insight
        insight = self._generate_insight(
            df_category=df_category,
            category_name=category_name,
            brand_sov=brand_sov,
            top_products=top_products
        )
        
        return {
            "title": f"Tổng quan thảo luận ngành {category_name}",
            "subtitle": f"Giai đoạn: {week_start.strftime('%d/%m/%Y')} - {week_end.strftime('%d/%m/%Y')}",
            "category_name": category_name,
            "brand_sov": brand_sov,
            "cate_distribution": cate_distribution,
            "top_products": top_products,
            "insight": insight,
            "total_buzz": len(df_category),
        }

    def _empty_result(self, category: str, start: datetime, end: datetime) -> Dict[str, Any]:
        """Return empty result when no data."""
        return {
            "title": f"Tổng quan thảo luận ngành {category}",
            "subtitle": f"Giai đoạn: {start.strftime('%d/%m/%Y')} - {end.strftime('%d/%m/%Y')}",
            "category_name": category,
            "brand_sov": {"total": 0, "brands": []},
            "cate_distribution": [],
            "top_products": [],
            "insight": {"paragraph1": "Không có dữ liệu", "paragraph2": "Không có dữ liệu"},
            "total_buzz": 0,
        }

    # ── Chart 1: Brand SOV ────────────────────────────────────────────────────
    def _calculate_brand_sov(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate Share of Voice by Topic (Brand) - sorted largest to smallest."""
        
        if "Topic" not in df.columns:
            return {"total": len(df), "brands": []}
        
        total = len(df)
        topic_counts = df["Topic"].value_counts().to_dict()
        
        brands = []
        for topic, count in topic_counts.items():
            if pd.notna(topic):
                percent = round(count / total * 100, 1) if total > 0 else 0
                brands.append({
                    "brand": topic,  # Using Topic as brand name
                    "buzz_count": count,
                    "percent": percent
                })
        
        # Sort by buzz_count descending
        brands.sort(key=lambda x: x["buzz_count"], reverse=True)
        
        return {
            "total": total,
            "brands": brands
        }

    # ── Chart 2: Cate Distribution ────────────────────────────────────────────
    def _calculate_cate_distribution(self, df: pd.DataFrame) -> List[Dict]:
        """Calculate distribution by Cate (product category)."""
        
        if "Cate" not in df.columns:
            return []
        
        total = len(df)
        cate_counts = df["Cate"].value_counts().to_dict()
        
        result = []
        for cate, count in cate_counts.items():
            if pd.notna(cate):
                percent = round(count / total * 100, 1) if total > 0 else 0
                result.append({
                    "cate": cate,
                    "buzz_count": count,
                    "percent": percent
                })
        
        # Sort by buzz_count descending
        result.sort(key=lambda x: x["buzz_count"], reverse=True)
        
        return result

    # ── Chart 3: Top Products ─────────────────────────────────────────────────
    def _get_top_products(self, df: pd.DataFrame, top_n: int = 10) -> List[Dict]:
        """Get top N products by buzz count."""
        
        if "Sản phẩm" not in df.columns:
            return []
        
        # Filter out null values
        df_products = df[df["Sản phẩm"].notna()].copy()
        
        if df_products.empty:
            return []
        
        product_counts = df_products["Sản phẩm"].value_counts().head(top_n).to_dict()
        
        result = []
        for rank, (product, count) in enumerate(product_counts.items(), 1):
            result.append({
                "rank": rank,
                "product": product,
                "buzz_count": count
            })
        
        return result

    # ── Insight Generation ────────────────────────────────────────────────────
    def _generate_insight(self, *, df_category: pd.DataFrame, category_name: str,
                          brand_sov: Dict, top_products: List[Dict]) -> Dict[str, str]:
        """Generate 2-paragraph insight about Masan Consumer in this category."""
        
        # Find Masan Consumer data
        masan_brands = ["Masan Consumer", "Masan", "MASAN CONSUMER"]
        df_masan = df_category[df_category["Brand"].isin(masan_brands)]
        
        masan_buzz = len(df_masan)
        total_buzz = brand_sov["total"]
        masan_percent = round(masan_buzz / total_buzz * 100, 1) if total_buzz > 0 else 0
        
        # Top brand
        top_brand = brand_sov["brands"][0] if brand_sov["brands"] else {"brand": "N/A", "percent": 0}
        
        # Top product
        top_product = top_products[0] if top_products else {"product": "N/A", "buzz_count": 0}
        
        # Masan products in top 10
        masan_products_in_top = []
        if not df_masan.empty and "Sản phẩm" in df_masan.columns:
            masan_product_list = df_masan["Sản phẩm"].dropna().unique().tolist()
            for item in top_products:
                if item["product"] in masan_product_list:
                    masan_products_in_top.append(item)
        
        # Paragraph 1: Market position
        para1_prompt = f"""Viết đoạn ngắn (30-40 từ) về vị thế Masan Consumer trong ngành {category_name}:

DỮ LIỆU:
- Tổng thảo luận ngành: {total_buzz:,}
- Masan Consumer: {masan_buzz:,} buzz ({masan_percent}%)
- Thương hiệu dẫn đầu: {top_brand['brand']} ({top_brand['percent']}%)
- Sản phẩm hot nhất: {top_product['product']} ({top_product['buzz_count']} buzz)

Phân tích vị thế và xu hướng của Masan Consumer."""
        
        # Paragraph 2: Product performance & recommendation
        masan_top_str = ", ".join([f"{p['product']} (#{p['rank']})" for p in masan_products_in_top[:3]]) if masan_products_in_top else "Không có trong top 10"
        
        para2_prompt = f"""Viết đoạn ngắn (30-40 từ) về sản phẩm và khuyến nghị cho Masan Consumer:

DỮ LIỆU:
- Sản phẩm Masan trong top 10: {masan_top_str}
- Tổng số sản phẩm được thảo luận: {len(top_products)}

Đánh giá hiệu suất sản phẩm và đưa ra 1-2 khuyến nghị."""
        
        paragraph1 = self.llm_client.generate_insight(para1_prompt)
        paragraph2 = self.llm_client.generate_insight(para2_prompt)
        
        return {
            "paragraph1": paragraph1,
            "paragraph2": paragraph2
        }
