"""
Module: Slides Data Extraction
Chức năng: Tách dữ liệu cho từng slide + sample data làm bằng chứng
"""
import pandas as pd
from tqdm import tqdm


class SlideDataExtractor:
    """Trích xuất dữ liệu cho từng slide"""
    
    def __init__(self, df, progress_callback=None):
        self.df = df
        self.total_mentions = len(df)
        self.progress_callback = progress_callback
    
    def _update_progress(self, current, total, message=""):
        """Update progress callback"""
        if self.progress_callback:
            progress = 0.5 + (current / total) * 0.4  # 50-90% for extraction
            self.progress_callback(progress, message)
    
    def _get_sample_data(self, data, n=3):
        """
        Lấy sample n mẫu từ data
        
        Args:
            data: DataFrame hoặc Series
            n: Số mẫu cần lấy
            
        Returns:
            list: Danh sách mẫu dữ liệu
        """
        if isinstance(data, pd.Series):
            return data.head(n).to_dict()
        elif isinstance(data, pd.DataFrame):
            return data.head(n).to_dict('records')
        return []
    
    def _get_full_sample_records(self, df_subset, n=3, key_fields=None, sample_size=50):
        """
        Lấy random n records từ sample_size records đầu tiên, xử lý null values
        
        Args:
            df_subset: DataFrame con để lấy mẫu
            n: Số mẫu cần lấy (default 3)
            key_fields: Danh sách field ưu tiên (nếu None sẽ lấy tất cả)
            sample_size: Lấy random từ top N records (default 50)
            
        Returns:
            list: Danh sách records với đầy đủ field, null values được set thành ""
        """
        if df_subset.empty:
            return []
        
        # Lấy top sample_size records
        top_records = df_subset.head(sample_size)
        
        # Lấy random n records từ top_records
        if len(top_records) < n:
            samples = top_records
        else:
            samples = top_records.sample(n=n, random_state=None)
        
        # Nếu không chỉ định field, lấy tất cả
        if key_fields is None:
            records = samples.to_dict('records')
        else:
            # Nếu chỉ định field, lấy những field có sẵn
            available_fields = [f for f in key_fields if f in samples.columns]
            records = samples[available_fields].to_dict('records')
        
        # Xử lý null values: thay NaN/None thành empty string
        cleaned_records = []
        for record in records:
            cleaned_record = {}
            for key, value in record.items():
                # Kiểm tra null/NaN
                if pd.isna(value) or value is None:
                    cleaned_record[key] = ""
                else:
                    cleaned_record[key] = value
            cleaned_records.append(cleaned_record)
        
        return cleaned_records
    
    # ============ SLIDE 1: TỔNG QUAN ============
    def slide_1_overview(self):
        """Slide 1: Tổng quan báo cáo"""
        # Sample: random 3 từ 50 records đầu tiên với đầy đủ field
        key_fields = ["PublishedDate", "Channel", "Topic", "Labels1", "Sentiment", "Title", "Content", "Description", "Type"]
        sample_records = self._get_full_sample_records(
            self.df,
            n=3,
            key_fields=key_fields,
            sample_size=50
        )
        
        return {
            "study_period": f"{self.df['PublishedDate'].min():%d/%m/%Y} – {self.df['PublishedDate'].max():%d/%m/%Y}",
            "data_source": "Vinfast_Weekly data_test.xlsx",
            "total_channels": self.df["Channel"].nunique(),
            "total_brands": self.df["Topic"].nunique(),
            "total_topics": self.df["Labels1"].nunique(),
            "total_mentions": self.total_mentions,
            "sample_records": sample_records,
        }
    
    # ============ SLIDE 2: SHARE OF VOICE ============
    def slide_2_sov(self):
        """Slide 2: Share of Voice"""
        brand_counts = self.df["Topic"].value_counts()
        primary_brand = brand_counts.index[0]
        competitor_list = ", ".join(brand_counts.index[1:])
        
        sov_table = "\n".join(
            f"- {brand}: {count:,} ({count / self.total_mentions * 100:.1f}%)"
            for brand, count in brand_counts.items()
        )
        
        # Sample: random 3 từ 50 records của primary brand với đầy đủ field
        key_fields = ["PublishedDate", "Channel", "Topic", "Sentiment", "Labels1", "Title", "Content", "Description", "Type"]
        sample_primary = self._get_full_sample_records(
            self.df[self.df["Topic"] == primary_brand],
            n=3,
            key_fields=key_fields,
            sample_size=50
        )
        
        return {
            "primary_brand": primary_brand,
            "competitor_list": competitor_list,
            "sov_table": sov_table,
            "brand_counts": brand_counts,
            "sample_primary_brand": sample_primary,
        }
    
    # ============ SLIDE 3: DIỄN BIẾN BUZZ ============
    def slide_3_daily_buzz(self, primary_brand):
        """Slide 3: Diễn biến buzz theo thời gian (Main Brand Only)"""
        # Lọc chỉ main brand
        df_main = self.df[self.df["Topic"] == primary_brand]
        daily_buzz = df_main.groupby("Date").size()
        
        daily_buzz_table = "\n".join(
            f"- {d:%d/%m/%Y}: {c:,}" for d, c in daily_buzz.items()
        )
        
        # Sample: random 3 từ 50 records của ngày buzz cao nhất với đầy đủ field
        top_buzz_dates = daily_buzz.nlargest(3).index
        key_fields = ["Date", "Channel", "Topic", "Sentiment", "Labels1", "Title", "Content", "Description", "Type"]
        sample_buzz = self._get_full_sample_records(
            df_main[df_main["Date"].isin(top_buzz_dates)],
            n=3,
            key_fields=key_fields,
            sample_size=50
        )
        
        return {
            "daily_buzz_table": daily_buzz_table,
            "daily_buzz": daily_buzz,
            "sample_high_buzz_records": sample_buzz,
        }
    
    # ============ SLIDE 4: HIGHLIGHT BUZZ ============
    def slide_4_highlight_buzz(self, primary_brand, topic_counts, num_highlights=5):
        """Slide 4: Highlight buzz"""
        highlight_df = self.df[
            (self.df["Topic"] == primary_brand) &
            (self.df["Sentiment"].isin(["Positive", "Negative"])) &
            (self.df["Labels1"].isin(topic_counts.head(5).index))
        ].copy()
        
        highlight_df = highlight_df.drop_duplicates(subset=["Channel"])
        
        if len(highlight_df) < num_highlights:
            supplement = self.df[self.df["Topic"] == primary_brand].drop_duplicates(subset=["Channel"])
            highlight_df = pd.concat([highlight_df, supplement]).drop_duplicates()
        
        highlight_df = highlight_df.head(num_highlights)
        
        buzz_examples = []
        for _, row in highlight_df.iterrows():
            title = str(row.get("Title", "")).strip()
            content = str(row.get("Content", "")).strip()[:200]
            channel = row.get("Channel", "Unknown")
            sentiment = row.get("Sentiment", "Unknown")
            example = f"- [{channel}] ({sentiment}) {title if title else content}"
            buzz_examples.append(example)
        
        # Sample: random 3 từ 50 highlight records với đầy đủ field
        key_fields = ["Channel", "Topic", "Sentiment", "Labels1", "Title", "Content", "Description", "Type", "PublishedDate"]
        sample_highlights = self._get_full_sample_records(
            highlight_df,
            n=3,
            key_fields=key_fields,
            sample_size=50
        )
        
        return {
            "num_highlights": num_highlights,
            "highlighted_url_list": "\n".join(buzz_examples),
            "highlight_channels": ", ".join(highlight_df["Channel"].unique()),
            "interaction_metric_status": "Không có dữ liệu tương tác; highlight dựa trên brand, topic và sentiment",
            "sample_highlights": sample_highlights,
        }
    
    # ============ SLIDE 5: TỔNG QUAN CẢM XÚC ============
    def slide_5_sentiment_overview(self, primary_brand):
        """Slide 5: Tổng quan cảm xúc (Main Brand Only)"""
        # Lọc chỉ main brand
        df_main = self.df[self.df["Topic"] == primary_brand]
        sentiment_counts = df_main["Sentiment"].value_counts()
        
        sentiment_overview_table = "\n".join(
            f"- {s}: {c:,} ({c / len(df_main) * 100:.1f}%)"
            for s, c in sentiment_counts.items()
        )
        
        # Sample: random 1 từ 50 records của mỗi sentiment với đầy đủ field
        key_fields = ["Channel", "Topic", "Sentiment", "Labels1", "Title", "Content", "Description", "Type", "PublishedDate"]
        sample_sentiment = []
        for sentiment in sentiment_counts.index[:3]:
            records = self._get_full_sample_records(
                df_main[df_main["Sentiment"] == sentiment],
                n=1,
                key_fields=key_fields,
                sample_size=50
            )
            sample_sentiment.extend(records)
        
        return {
            "sentiment_overview_table": sentiment_overview_table,
            "sentiment_counts": sentiment_counts,
            "sample_sentiment_records": sample_sentiment,
        }
    
    # ============ SLIDE 6: CƠ CẤU KÊNH ============
    def slide_6_channel_mix(self, primary_brand):
        """Slide 6: Cơ cấu kênh thảo luận (Main Brand Only)"""
        # Lọc chỉ main brand
        df_main = self.df[self.df["Topic"] == primary_brand]
        channel_counts = df_main["Channel"].value_counts()
        
        channel_volume_table = "\n".join(
            f"- {ch}: {cnt:,} ({cnt / len(df_main) * 100:.1f}%)"
            for ch, cnt in channel_counts.items()
        )
        
        # Sample: random 1 từ 50 records của mỗi top channel với đầy đủ field
        key_fields = ["Channel", "Topic", "Sentiment", "Labels1", "Title", "Content", "Description", "Type", "PublishedDate"]
        sample_channels = []
        for channel in channel_counts.head(3).index:
            records = self._get_full_sample_records(
                df_main[df_main["Channel"] == channel],
                n=1,
                key_fields=key_fields,
                sample_size=50
            )
            sample_channels.extend(records)
        
        return {
            "channel_volume_table": channel_volume_table,
            "channel_counts": channel_counts,
            "sample_channel_records": sample_channels,
        }
    
    # ============ SLIDE 7: CẢM XÚC THEO KÊNH ============
    def slide_7_sentiment_by_channel(self, primary_brand):
        """Slide 7: Cảm xúc theo kênh (Main Brand Only)"""
        # Lọc chỉ main brand
        df_main = self.df[self.df["Topic"] == primary_brand]
        sent_by_channel = pd.crosstab(
            df_main["Channel"], df_main["Sentiment"], normalize="index"
        ) * 100
        
        sentiment_by_channel_table = "\n".join(
            f"- {ch}: " + " | ".join(
                f"{s} {sent_by_channel.loc[ch, s]:.1f}%"
                for s in sent_by_channel.columns
            )
            for ch in sent_by_channel.index
        )
        
        # Sample: random 3 từ 50 records với đầy đủ field
        key_fields = ["Channel", "Sentiment", "Topic", "Labels1", "Title", "Content", "Description", "Type", "PublishedDate"]
        sample_sent_channel = self._get_full_sample_records(
            df_main,
            n=3,
            key_fields=key_fields,
            sample_size=50
        )
        
        return {
            "sentiment_by_channel_table": sentiment_by_channel_table,
            "sent_by_channel": sent_by_channel,
            "sample_sentiment_channel_records": sample_sent_channel,
        }
    
    # ============ SLIDE 8: CHỦ ĐỀ NỔI BẬT ============
    def slide_8_top_topics(self, primary_brand):
        """Slide 8: Chủ đề thảo luận nổi bật (Main Brand Only)"""
        # Lọc chỉ main brand
        df_main = self.df[self.df["Topic"] == primary_brand]
        topic_counts = df_main["Labels1"].value_counts()
        
        topic_ranking_table = "\n".join(
            f"- {label}: {cnt:,} ({cnt / len(df_main) * 100:.1f}%)"
            for label, cnt in topic_counts.head(10).items()
        )
        
        focus_topic_list = ", ".join(topic_counts.head(5).index)
        
        # Sample: random 1 từ 50 records của mỗi top topic với đầy đủ field
        key_fields = ["Labels1", "Channel", "Topic", "Sentiment", "Title", "Content", "Description", "Type", "PublishedDate"]
        sample_topics = []
        for topic in topic_counts.head(3).index:
            records = self._get_full_sample_records(
                df_main[df_main["Labels1"] == topic],
                n=1,
                key_fields=key_fields,
                sample_size=50
            )
            sample_topics.extend(records)
        
        return {
            "topic_ranking_table": topic_ranking_table,
            "focus_topic_list": focus_topic_list,
            "topic_counts": topic_counts,
            "sample_topic_records": sample_topics,
        }
    
    # ============ SLIDE 9: XU HƯỚNG CHỦ ĐỀ ============
    def slide_9_topic_trend(self, primary_brand, topic_counts):
        """Slide 9: Xu hướng chủ đề theo thời gian (Main Brand Only)"""
        # Lọc chỉ main brand
        df_main = self.df[self.df["Topic"] == primary_brand]
        topic_trend = (
            df_main.groupby(["Date", "Labels1"])
            .size()
            .unstack(fill_value=0)
            .loc[:, topic_counts.head(5).index]
        )
        
        # Sample: random 3 từ 50 records của top topics với đầy đủ field
        key_fields = ["Date", "Labels1", "Channel", "Topic", "Sentiment", "Title", "Content", "Description", "Type"]
        sample_trend = self._get_full_sample_records(
            df_main[df_main["Labels1"].isin(topic_counts.head(3).index)],
            n=3,
            key_fields=key_fields,
            sample_size=50
        )
        
        return {
            "topic_trend_daily_table": topic_trend.to_string(),
            "topic_trend": topic_trend,
            "sample_trend_records": sample_trend,
        }
    
    # ============ SLIDE 10: CHỦ ĐỀ THEO KÊNH ============
    def slide_10_topic_by_channel(self, primary_brand):
        """Slide 10: Chủ đề theo kênh (Main Brand Only)"""
        # Lọc chỉ main brand
        df_main = self.df[self.df["Topic"] == primary_brand]
        topic_by_channel = pd.crosstab(
            df_main["Labels1"],
            df_main["Channel"],
            normalize="index"
        ) * 100
        
        topic_by_channel = topic_by_channel.round(1)
        
        # Sample: random 3 từ 50 records với đầy đủ field
        key_fields = ["Labels1", "Channel", "Topic", "Sentiment", "Title", "Content", "Description", "Type", "PublishedDate"]
        sample_topic_channel = self._get_full_sample_records(
            df_main,
            n=3,
            key_fields=key_fields,
            sample_size=50
        )
        
        return {
            "topic_by_channel_table": topic_by_channel.to_string(),
            "topic_by_channel": topic_by_channel,
            "sample_topic_channel_records": sample_topic_channel,
        }
    
    # ============ SLIDE 11: CẢM XÚC THEO THƯƠNG HIỆU ============
    def slide_11_sentiment_by_brand(self):
        """Slide 11: Cảm xúc theo thương hiệu"""
        sent_by_brand = pd.crosstab(
            self.df["Topic"], self.df["Sentiment"], normalize="index"
        ) * 100
        
        brand_counts = self.df["Topic"].value_counts()
        
        brand_volume_table = "\n".join(
            f"- {b}: {c:,}" for b, c in brand_counts.items()
        )
        
        # Sample: random 1 từ 50 records của mỗi top brand với đầy đủ field
        key_fields = ["Topic", "Sentiment", "Channel", "Labels1", "Title", "Content", "Description", "Type", "PublishedDate"]
        sample_brand_sentiment = []
        for brand in brand_counts.head(3).index:
            records = self._get_full_sample_records(
                self.df[self.df["Topic"] == brand],
                n=1,
                key_fields=key_fields,
                sample_size=50
            )
            sample_brand_sentiment.extend(records)
        
        return {
            "sentiment_by_brand_table": sent_by_brand.round(1).to_string(),
            "brand_volume_table": brand_volume_table,
            "sent_by_brand": sent_by_brand,
            "sample_brand_sentiment_records": sample_brand_sentiment,
        }
    
    # ============ SLIDE 12: CHỦ ĐỀ THEO THƯƠNG HIỆU ============
    def slide_12_topic_by_brand(self):
        """Slide 12: Chủ đề theo thương hiệu"""
        topic_by_brand = pd.crosstab(
            self.df["Topic"], self.df["Labels1"], normalize="index"
        ) * 100
        
        # Sample: random 3 từ 50 records với đầy đủ field
        key_fields = ["Topic", "Labels1", "Channel", "Sentiment", "Title", "Content", "Description", "Type", "PublishedDate"]
        sample_topic_brand = self._get_full_sample_records(
            self.df,
            n=3,
            key_fields=key_fields,
            sample_size=50
        )
        
        return {
            "topic_by_brand_table": topic_by_brand.round(1).to_string(),
            "topic_by_brand": topic_by_brand,
            "sample_topic_brand_records": sample_topic_brand,
        }
    
    def extract_all(self):
        """Trích xuất dữ liệu cho tất cả slides"""
        slides_list = [
            ("slide_1", self.slide_1_overview),
            ("slide_2", self.slide_2_sov),
            ("slide_3", lambda: self.slide_3_daily_buzz(self.slide_2_sov()["primary_brand"])),
            ("slide_4", lambda: self.slide_4_highlight_buzz(self.slide_2_sov()["primary_brand"], self.slide_2_sov()["brand_counts"])),
            ("slide_5", lambda: self.slide_5_sentiment_overview(self.slide_2_sov()["primary_brand"])),
            ("slide_6", lambda: self.slide_6_channel_mix(self.slide_2_sov()["primary_brand"])),
            ("slide_7", lambda: self.slide_7_sentiment_by_channel(self.slide_2_sov()["primary_brand"])),
            ("slide_8", lambda: self.slide_8_top_topics(self.slide_2_sov()["primary_brand"])),
            ("slide_9", lambda: self.slide_9_topic_trend(self.slide_2_sov()["primary_brand"], self.slide_8_top_topics(self.slide_2_sov()["primary_brand"])["topic_counts"])),
            ("slide_10", lambda: self.slide_10_topic_by_channel(self.slide_2_sov()["primary_brand"])),
            ("slide_11", self.slide_11_sentiment_by_brand),
            ("slide_12", self.slide_12_topic_by_brand),
        ]
        
        result = {}
        slide_2_data = self.slide_2_sov()
        primary_brand = slide_2_data["primary_brand"]
        
        for i, (slide_name, slide_func) in enumerate(slides_list, 1):
            self._update_progress(i, len(slides_list), f"Extracting {slide_name}...")
            
            if slide_name == "slide_1":
                result[slide_name] = self.slide_1_overview()
            elif slide_name == "slide_2":
                result[slide_name] = slide_2_data
            elif slide_name == "slide_3":
                result[slide_name] = self.slide_3_daily_buzz(primary_brand)
            elif slide_name == "slide_4":
                result[slide_name] = self.slide_4_highlight_buzz(primary_brand, slide_2_data["brand_counts"])
            elif slide_name == "slide_5":
                result[slide_name] = self.slide_5_sentiment_overview(primary_brand)
            elif slide_name == "slide_6":
                result[slide_name] = self.slide_6_channel_mix(primary_brand)
            elif slide_name == "slide_7":
                result[slide_name] = self.slide_7_sentiment_by_channel(primary_brand)
            elif slide_name == "slide_8":
                result[slide_name] = self.slide_8_top_topics(primary_brand)
            elif slide_name == "slide_9":
                slide_8_data = result["slide_8"]
                result[slide_name] = self.slide_9_topic_trend(primary_brand, slide_8_data["topic_counts"])
            elif slide_name == "slide_10":
                result[slide_name] = self.slide_10_topic_by_channel(primary_brand)
            elif slide_name == "slide_11":
                result[slide_name] = self.slide_11_sentiment_by_brand()
            elif slide_name == "slide_12":
                result[slide_name] = self.slide_12_topic_by_brand()
        
        return result
