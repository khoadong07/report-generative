"""
Main report generator orchestrating all slides
"""

import json
import pandas as pd
import os
from typing import Dict, Any
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load .env file if exists
try:
    from dotenv import load_dotenv
    # Try to load .env from test directory
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    else:
        load_dotenv()  # Try to load from current directory
except ImportError:
    print("⚠️  python-dotenv not installed. Using environment variables only.")
    print("   Install with: pip install python-dotenv")

try:
    from test.config import *
    from test.data_loader import DataLoader
    from test.llm_client import LLMClient
    from test.slide_generators import (
        Slide1Generator,
        Slide2Generator,
        Slide3Generator,
        Slide4Generator
    )
except ImportError:
    # If running from test directory
    from config import *
    from data_loader import DataLoader
    from llm_client import LLMClient
    from slide_generators import (
        Slide1Generator,
        Slide2Generator,
        Slide3Generator,
        Slide4Generator,
        Slide5Generator,
        Slide6Generator
    )


class ReportGenerator:
    """Main report generator class"""
    
    def __init__(self, api_key: str, base_url: str, file_path: str = None, 
                 brand_name: str = None, report_date: str = None, compare_date: str = None):
        """
        Initialize report generator
        
        Args:
            api_key: API key for LLM
            base_url: Base URL for LLM API
            file_path: Path to Excel file (optional, uses config if not provided)
            brand_name: Brand name (optional, uses config if not provided)
            report_date: Report date (optional, uses config if not provided)
            compare_date: Compare date (optional, uses config if not provided)
        """
        # Use provided values or fall back to config
        self.file_path = file_path or FILE_PATH
        self.brand_name = brand_name or BRAND_NAME
        self.report_date = report_date or REPORT_DATE
        self.compare_date = compare_date or COMPARE_DATE
        
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
        self.slide1_gen = Slide1Generator(
            self.llm_client,
            TOPIC_TYPES,
            TOP_N_TOPICS
        )
        
        self.slide2_gen = Slide2Generator(
            self.llm_client,
            TOPIC_TYPES,
            LOOKBACK_DAYS,
            TOP_N_PEAK_TOPICS
        )
        
        self.slide3_gen = Slide3Generator(
            self.llm_client,
            TOPIC_TYPES,
            TOP_N_TOPICS
        )
        
        self.slide4_gen = Slide4Generator(
            self.llm_client
        )
        
        self.slide5_gen = Slide5Generator(
            TOPIC_TYPES,
            top_n=5
        )
        
        self.slide6_gen = Slide6Generator(
            TOPIC_TYPES,
            top_n=5
        )
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Generate complete report with all slides (parallel processing)
        Supports both date-only and datetime formats
        
        Returns:
            Dictionary containing all slide data
        """
        print("\n" + "="*60)
        print("📊 STARTING REPORT GENERATION (PARALLEL MODE)")
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
        
        # Detect if using datetime or date-only format
        is_datetime_mode = len(self.report_date) > 10  # "YYYY-MM-DD HH:MM:SS" vs "YYYY-MM-DD"
        
        print("\n[2/5] Filtering data by datetime ranges...")
        
        if is_datetime_mode:
            # DateTime mode: 24-hour windows
            from datetime import datetime, timedelta
            import pandas as pd
            
            report_dt = pd.to_datetime(self.report_date)
            compare_dt = report_dt - timedelta(hours=24)
            
            report_df = self.data_loader.filter_by_datetime_range(self.report_date)
            compare_df = self.data_loader.filter_by_datetime_range(
                compare_dt.strftime("%Y-%m-%d %H:%M:%S")
            )
            
            # Keep both raw and display formats
            report_date_raw = self.report_date  # For parsing: "2026-02-03 15:00:00"
            compare_date_raw = compare_dt.strftime("%Y-%m-%d %H:%M:%S")
            
            # Format for display (24h window)
            report_display = report_dt.strftime("%d/%m/%Y %H:%M")
            compare_display = compare_dt.strftime("%d/%m/%Y %H:%M")
            
            # Format for subtitle (show 24h range)
            datetime_range_display = f"{compare_display} → {report_display}"
            
            print(f"      ✅ Report window: {datetime_range_display} (24h)")
            print(f"      ✅ Report data: {len(report_df)} rows")
            print(f"      ✅ Compare data: {len(compare_df)} rows")
        else:
            # Date-only mode: backward compatibility
            report_df = self.data_loader.filter_by_date(self.report_date)
            compare_df = self.data_loader.filter_by_date(self.compare_date)
            
            report_date_raw = self.report_date
            compare_date_raw = self.compare_date
            report_display = self.report_date
            compare_display = self.compare_date
            datetime_range_display = report_display
            
            print(f"      ✅ Report date ({self.report_date}): {len(report_df)} rows")
            print(f"      ✅ Compare date ({self.compare_date}): {len(compare_df)} rows")
        
        # Validate data availability
        if len(report_df) == 0:
            print(f"\n      ⚠️  WARNING: No data found for report period")
            print(f"      Available dates in dataset:")
            available_dates = sorted(df['PublishedDay'].unique())
            for date in available_dates[:10]:
                print(f"         - {date}")
            if len(available_dates) > 10:
                print(f"         ... and {len(available_dates) - 10} more dates")
            raise ValueError(
                f"No data available for report period. "
                f"Please choose a date between {available_dates[0]} and {available_dates[-1]}"
            )
        
        if len(compare_df) == 0:
            print(f"\n      ⚠️  WARNING: No data found for compare period")
            raise ValueError("No data available for compare period.")
        
        print("\n[3/5] Generating all slides in parallel...")
        print("      🚀 Starting 4 parallel tasks (this will take ~1 minute)...")
        
        # Define slide generation tasks
        def generate_slide1():
            print("      [Slide 1] 📝 Calculating KPIs...")
            print("      [Slide 1] 🤖 Calling LLM for insights...")
            result = self.slide1_gen.generate(
                report_df, compare_df,
                self.brand_name, datetime_range_display, compare_display
            )
            print("      [Slide 1] ✅ Completed")
            return ('slide_1', result)
        
        def generate_slide2():
            print("      [Slide 2] 📈 Calculating trendline data...")
            print("      [Slide 2] 🤖 Calling LLM for insights...")
            result = self.slide2_gen.generate(
                df, self.brand_name, report_date_raw  # Pass raw format for parsing
            )
            print("      [Slide 2] ✅ Completed")
            return ('slide_2', result)
        
        def generate_slide3():
            print("      [Slide 3] 📡 Analyzing channel distribution...")
            print("      [Slide 3] 🤖 Calling LLM for insights...")
            result = self.slide3_gen.generate(
                report_df, compare_df,
                self.brand_name, datetime_range_display, compare_display
            )
            print("      [Slide 3] ✅ Completed")
            return ('slide_3', result)
        
        def generate_slide4():
            print("      [Slide 4] 💭 Analyzing sentiment distribution...")
            print("      [Slide 4] 🤖 Calling LLM for insights...")
            result = self.slide4_gen.generate(
                report_df, self.brand_name, datetime_range_display
            )
            print("      [Slide 4] ✅ Completed")
            return ('slide_4', result)
        
        # Execute all slides in parallel
        slides_data = {}
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit all tasks
            futures = {
                executor.submit(generate_slide1): 'slide_1',
                executor.submit(generate_slide2): 'slide_2',
                executor.submit(generate_slide3): 'slide_3',
                executor.submit(generate_slide4): 'slide_4'
            }
            
            # Collect results as they complete
            completed = 0
            for future in as_completed(futures):
                try:
                    slide_name, slide_data = future.result()
                    slides_data[slide_name] = slide_data
                    completed += 1
                    print(f"      ⏱️  Progress: {completed}/4 slides completed")
                except Exception as e:
                    slide_name = futures[future]
                    print(f"      ❌ Error generating {slide_name}: {e}")
                    raise
        
        print("\n[4/5] All slides generated successfully!")
        
        print("\n[5/5] Combining all slides...")
        
        # Generate Slide 5 (no LLM needed, so run after parallel tasks)
        print("      [Slide 5] 📊 Generating top posts table...")
        slide5_data = self.slide5_gen.generate(
            report_df, self.brand_name, datetime_range_display
        )
        print("      [Slide 5] ✅ Completed")
        
        # Generate Slide 6 (deleted posts - from entire dataset, not filtered by date)
        print("      [Slide 6] 🗑️  Generating deleted posts table (all dates)...")
        slide6_data = self.slide6_gen.generate(
            df, self.brand_name, datetime_range_display, file_path=self.file_path
        )
        print("      [Slide 6] ✅ Completed")
        
        report = {
            "report_metadata": {
                "brand": self.brand_name,
                "report_date": datetime_range_display,  # Show 24h range
                "compare_date": compare_display,
                "generated_at": pd.Timestamp.now().isoformat(),
                "generation_mode": "parallel"
            },
            "slide_1": slides_data['slide_1'],
            "slide_2": slides_data['slide_2'],
            "slide_3": slides_data['slide_3'],
            "slide_4": slides_data['slide_4'],
            "slide_5": slide5_data,
            "slide_6": slide6_data
        }
        print("      ✅ Report structure created")
        
        print("\n" + "="*60)
        print("✅ REPORT GENERATION COMPLETED!")
        print("="*60)
        
        return report
    
    def save_report(self, report: Dict[str, Any], output_path: str):
        """
        Save report to JSON file
        
        Args:
            report: Report data dictionary
            output_path: Path to save JSON file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"Report saved to: {output_path}")
    
    def generate_and_save(self, output_path: str = "report_output.json"):
        """
        Generate report and save to file
        
        Args:
            output_path: Path to save JSON file
        """
        report = self.generate_report()
        self.save_report(report, output_path)
        return report


def main():
    """Main function to run report generation"""
    import os
    
    # Get API credentials from environment
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL")
    
    if not api_key or not base_url:
        raise ValueError("API_KEY and BASE_URL must be set in environment variables")
    
    # Generate report
    generator = ReportGenerator(api_key, base_url)
    report = generator.generate_and_save("test/report_output.json")
    
    print("\n" + "="*50)
    print("Report generation completed successfully!")
    print("="*50)
    
    return report


if __name__ == "__main__":
    main()
