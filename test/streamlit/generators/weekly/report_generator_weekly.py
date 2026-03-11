"""
Weekly Report Generator - orchestrating all 12 slides
"""

import json
import pandas as pd
import os
from typing import Dict, Any
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta

try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    else:
        load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed")

from core.config import *
from core.data_loader import DataLoader
from core.llm_client import LLMClient
from generators.weekly.slide_generators_weekly import (
    WeeklySlide1Generator,
    WeeklySlide2Generator,
    WeeklySlide3Generator,
    WeeklySlide4Generator,
    WeeklySlide5Generator,
    WeeklySlide6Generator,
    WeeklySlide7Generator,
    WeeklySlide8Generator,
    WeeklySlide9Generator,
    WeeklySlide10Generator,
    WeeklySlide11Generator,
    WeeklySlide12Generator
)


class WeeklyReportGenerator:
    """Weekly report generator class"""
    
    def __init__(self, api_key: str, base_url: str, file_path: str = None, 
                 brand_name: str = None, week1_end: str = None, 
                 week2_end: str = None, week3_end: str = None, week4_end: str = None,
                 show_interactions: bool = True):
        """
        Initialize weekly report generator
        
        Args:
            api_key: API key for LLM
            base_url: Base URL for LLM API
            file_path: Path to Excel file
            brand_name: Brand name
            week1_end: End datetime of current week (YYYY-MM-DD HH:MM:SS)
            week2_end: End datetime of week 2 (1 week before)
            week3_end: End datetime of week 3 (2 weeks before)
            week4_end: End datetime of week 4 (3 weeks before)
            show_interactions: Show interaction metrics in Slide 1 (default: True)
        """
        self.file_path = file_path or FILE_PATH
        self.brand_name = brand_name or BRAND_NAME
        self.week1_end = week1_end
        self.week2_end = week2_end
        self.week3_end = week3_end
        self.week4_end = week4_end
        self.show_interactions = show_interactions
        
        # Initialize data loader
        self.data_loader = DataLoader(
            self.file_path,
            TEXT_COLUMNS,
            METRIC_COLUMNS
        )
        
        # Initialize LLM client
        self.llm_client = LLMClient(
            api_key=api_key,
            base_url=base_url,
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            system_prompt=LLM_SYSTEM_PROMPT
        )
        
        # Initialize slide generators
        self.slide1_gen = WeeklySlide1Generator(self.llm_client, TOPIC_TYPES)
        self.slide2_gen = WeeklySlide2Generator(self.llm_client, TOPIC_TYPES)
        self.slide3_gen = WeeklySlide3Generator(self.llm_client, TOPIC_TYPES)
        self.slide4_gen = WeeklySlide4Generator(TOPIC_TYPES, top_n=10)
        self.slide5_gen = WeeklySlide5Generator(TOPIC_TYPES, top_n=10)
        self.slide6_gen = WeeklySlide6Generator(self.llm_client, TOPIC_TYPES)
        self.slide7_gen = WeeklySlide7Generator(self.llm_client, TOPIC_TYPES)
        self.slide8_gen = WeeklySlide8Generator(TOPIC_TYPES, top_n=10)
        self.slide9_gen = WeeklySlide9Generator(TOPIC_TYPES, COMMENT_TYPES, top_n=10)
        self.slide10_gen = WeeklySlide10Generator(self.llm_client, TOPIC_TYPES)
        self.slide11_gen = WeeklySlide11Generator(TOPIC_TYPES, top_n=10)
        self.slide12_gen = WeeklySlide12Generator(TOPIC_TYPES, COMMENT_TYPES, top_n=10)
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Generate complete weekly report with all 12 slides (parallel processing)
        
        Returns:
            Dictionary containing all slide data
        """
        print("\n" + "="*60)
        print("📊 STARTING WEEKLY REPORT GENERATION (PARALLEL MODE)")
        print("="*60)
        
        print("\n[1/5] Loading data from Excel...")
        df = self.data_loader.preprocess()
        print(f"      ✅ Loaded {len(df)} rows")
        
        # Filter by brand/topic BEFORE time filtering
        print(f"\n[1.5/5] Filtering data by brand: {self.brand_name}...")
        if "Topic" not in df.columns:
            raise ValueError("Column 'Topic' not found in data. Cannot filter by brand.")
        
        df = df[df["Topic"] == self.brand_name].copy()
        print(f"      ✅ Filtered to {len(df)} rows for brand '{self.brand_name}'")
        
        if len(df) == 0:
            raise ValueError(f"No data found for brand '{self.brand_name}'. Please check the brand name.")
        
        # Update data_loader's df with filtered data
        self.data_loader.df = df
        
        print("\n[2/5] Filtering data by 4 weekly windows...")
        
        # Calculate start times (7 days before each end time)
        week1_end_dt = pd.to_datetime(self.week1_end)
        week1_start_dt = week1_end_dt - timedelta(days=7)
        
        week2_end_dt = pd.to_datetime(self.week2_end)
        week2_start_dt = week2_end_dt - timedelta(days=7)
        
        week3_end_dt = pd.to_datetime(self.week3_end)
        week3_start_dt = week3_end_dt - timedelta(days=7)
        
        week4_end_dt = pd.to_datetime(self.week4_end)
        week4_start_dt = week4_end_dt - timedelta(days=7)
        
        # Filter data for each week (7 days)
        week1_df = self.data_loader.filter_by_datetime_range(self.week1_end, days=7)
        week2_df = self.data_loader.filter_by_datetime_range(self.week2_end, days=7)
        week3_df = self.data_loader.filter_by_datetime_range(self.week3_end, days=7)
        week4_df = self.data_loader.filter_by_datetime_range(self.week4_end, days=7)
        
        print(f"      ✅ Week 1 ({week1_start_dt.strftime('%d/%m')} → {week1_end_dt.strftime('%d/%m')}): {len(week1_df)} rows")
        print(f"      ✅ Week 2 ({week2_start_dt.strftime('%d/%m')} → {week2_end_dt.strftime('%d/%m')}): {len(week2_df)} rows")
        print(f"      ✅ Week 3 ({week3_start_dt.strftime('%d/%m')} → {week3_end_dt.strftime('%d/%m')}): {len(week3_df)} rows")
        print(f"      ✅ Week 4 ({week4_start_dt.strftime('%d/%m')} → {week4_end_dt.strftime('%d/%m')}): {len(week4_df)} rows")
        
        # Validate data
        if len(week1_df) == 0:
            raise ValueError(f"No data for current week ({week1_start_dt.strftime('%d/%m')} → {week1_end_dt.strftime('%d/%m')})")
        
        # Format display strings
        week1_display = f"{week1_start_dt.strftime('%d/%m/%Y')} → {week1_end_dt.strftime('%d/%m/%Y')}"
        week2_display = f"{week2_start_dt.strftime('%d/%m/%Y')} → {week2_end_dt.strftime('%d/%m/%Y')}"
        week3_display = f"{week3_start_dt.strftime('%d/%m/%Y')} → {week3_end_dt.strftime('%d/%m/%Y')}"
        week4_display = f"{week4_start_dt.strftime('%d/%m/%Y')} → {week4_end_dt.strftime('%d/%m/%Y')}"
        
        print("\n[3/5] Generating all slides in parallel...")
        print("      🚀 Starting parallel tasks (this will take ~2 minutes)...")
        
        # Define slide generation tasks (slides with LLM)
        def generate_slide1():
            print("      [Slide 1] 📝 Calculating weekly KPIs...")
            result = self.slide1_gen.generate(
                week1_df, week2_df, week3_df, week4_df,
                self.brand_name, week1_display, self.show_interactions
            )
            print("      [Slide 1] ✅ Completed")
            return ('slide_1', result)
        
        def generate_slide2():
            print("      [Slide 2] 📈 Calculating weekly trendline...")
            result = self.slide2_gen.generate(
                week1_df, self.brand_name, week1_display,
                week1_start_dt.strftime('%Y-%m-%d'),
                week1_end_dt.strftime('%Y-%m-%d')
            )
            print("      [Slide 2] ✅ Completed")
            return ('slide_2', result)
        
        def generate_slide3():
            print("      [Slide 3] 📡 Analyzing channel distribution...")
            result = self.slide3_gen.generate(
                week1_df, self.brand_name, week1_display
            )
            print("      [Slide 3] ✅ Completed")
            return ('slide_3', result)
        
        def generate_slide6():
            print("      [Slide 6] 💭 Analyzing sentiment...")
            result = self.slide6_gen.generate(
                week1_df, week2_df, self.brand_name, week1_display
            )
            print("      [Slide 6] ✅ Completed")
            return ('slide_6', result)
        
        def generate_slide7():
            print("      [Slide 7] 😊 Analyzing positive topics...")
            result = self.slide7_gen.generate(
                week1_df, self.brand_name, week1_display
            )
            print("      [Slide 7] ✅ Completed")
            return ('slide_7', result)
        
        def generate_slide9():
            print("      [Slide 9] 😞 Analyzing negative topics...")
            result = self.slide10_gen.generate(
                week1_df, self.brand_name, week1_display
            )
            print("      [Slide 9] ✅ Completed")
            return ('slide_9', result)
        
        # Execute slides with LLM in parallel
        slides_data = {}
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = {
                executor.submit(generate_slide1): 'slide_1',
                executor.submit(generate_slide2): 'slide_2',
                executor.submit(generate_slide3): 'slide_3',
                executor.submit(generate_slide6): 'slide_6',
                executor.submit(generate_slide7): 'slide_7',
                executor.submit(generate_slide9): 'slide_9'
            }
            
            completed = 0
            for future in as_completed(futures):
                try:
                    slide_name, slide_data = future.result()
                    slides_data[slide_name] = slide_data
                    completed += 1
                    print(f"      ⏱️  Progress: {completed}/6 LLM slides completed")
                except Exception as e:
                    slide_name = futures[future]
                    print(f"      ❌ Error generating {slide_name}: {e}")
                    raise
        
        print("\n[4/5] All LLM slides generated successfully!")
        
        print("\n[5/5] Generating data-only slides...")
        
        # Generate data-only slides (no LLM)
        print("      [Slide 4] 📊 Generating top sources by engagement...")
        slide4_data = self.slide4_gen.generate(week1_df, self.brand_name, week1_display, self.show_interactions)
        print("      [Slide 4] ✅ Completed")
        
        print("      [Slide 5] 📊 Generating top posts by engagement...")
        slide5_data = self.slide5_gen.generate(week1_df, self.brand_name, week1_display, self.show_interactions)
        print("      [Slide 5] ✅ Completed")
        
        print("      [Slide 8] 📊 Generating top positive posts...")
        slide8_data = self.slide9_gen.generate(week1_df, self.brand_name, week1_display)
        print("      [Slide 8] ✅ Completed")
        
        print("      [Slide 10] 📊 Generating top negative posts...")
        slide10_data = self.slide12_gen.generate(week1_df, self.brand_name, week1_display)
        print("      [Slide 10] ✅ Completed")
        
        report = {
            "report_metadata": {
                "brand": self.brand_name,
                "report_type": "weekly",
                "week1_period": week1_display,
                "week2_period": week2_display,
                "week3_period": week3_display,
                "week4_period": week4_display,
                "generated_at": pd.Timestamp.now().isoformat(),
                "generation_mode": "parallel"
            },
            "slide_1": slides_data['slide_1'],
            "slide_2": slides_data['slide_2'],
            "slide_3": slides_data['slide_3'],
            "slide_4": slide4_data,
            "slide_5": slide5_data,
            "slide_6": slides_data['slide_6'],
            "slide_7": slides_data['slide_7'],
            "slide_8": slide8_data,
            "slide_9": slides_data['slide_9'],
            "slide_10": slide10_data
        }
        
        print("\n" + "="*60)
        print("✅ WEEKLY REPORT GENERATION COMPLETED!")
        print("="*60)
        
        return report
