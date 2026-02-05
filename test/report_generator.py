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
        Slide4Generator
    )


class ReportGenerator:
    """Main report generator class"""
    
    def __init__(self, api_key: str, base_url: str):
        """
        Initialize report generator
        
        Args:
            api_key: API key for LLM
            base_url: Base URL for LLM API
        """
        # Initialize data loader
        self.data_loader = DataLoader(
            FILE_PATH,
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
            self.llm_client,
            TOP_N_ATTRIBUTES
        )
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Generate complete report with all slides (parallel processing)
        
        Returns:
            Dictionary containing all slide data
        """
        print("\n" + "="*60)
        print("📊 STARTING REPORT GENERATION (PARALLEL MODE)")
        print("="*60)
        
        print("\n[1/5] Loading data from Excel...")
        df = self.data_loader.preprocess()
        print(f"      ✅ Loaded {len(df)} rows")
        
        print("\n[2/5] Filtering data by dates...")
        report_df = self.data_loader.filter_by_date(REPORT_DATE)
        compare_df = self.data_loader.filter_by_date(COMPARE_DATE)
        print(f"      ✅ Report date ({REPORT_DATE}): {len(report_df)} rows")
        print(f"      ✅ Compare date ({COMPARE_DATE}): {len(compare_df)} rows")
        
        # Validate data availability
        if len(report_df) == 0:
            print(f"\n      ⚠️  WARNING: No data found for report date {REPORT_DATE}")
            print(f"      Available dates in dataset:")
            available_dates = sorted(df['PublishedDay'].unique())
            for date in available_dates[:10]:  # Show first 10 dates
                print(f"         - {date}")
            if len(available_dates) > 10:
                print(f"         ... and {len(available_dates) - 10} more dates")
            raise ValueError(
                f"No data available for report date {REPORT_DATE}. "
                f"Please choose a date between {available_dates[0]} and {available_dates[-1]}"
            )
        
        if len(compare_df) == 0:
            print(f"\n      ⚠️  WARNING: No data found for compare date {COMPARE_DATE}")
            print(f"      Available dates in dataset:")
            available_dates = sorted(df['PublishedDay'].unique())
            for date in available_dates[:10]:
                print(f"         - {date}")
            if len(available_dates) > 10:
                print(f"         ... and {len(available_dates) - 10} more dates")
            raise ValueError(
                f"No data available for compare date {COMPARE_DATE}. "
                f"Please choose a date between {available_dates[0]} and {available_dates[-1]}"
            )
        
        print("\n[3/5] Generating all slides in parallel...")
        print("      🚀 Starting 4 parallel tasks (this will take ~1 minute)...")
        
        # Define slide generation tasks
        def generate_slide1():
            print("      [Slide 1] 📝 Calculating KPIs...")
            print("      [Slide 1] 🤖 Calling LLM for insights...")
            result = self.slide1_gen.generate(
                report_df, compare_df,
                BRAND_NAME, REPORT_DATE, COMPARE_DATE
            )
            print("      [Slide 1] ✅ Completed")
            return ('slide_1', result)
        
        def generate_slide2():
            print("      [Slide 2] 📈 Calculating trendline data...")
            print("      [Slide 2] 🤖 Calling LLM for insights...")
            result = self.slide2_gen.generate(
                df, BRAND_NAME, REPORT_DATE
            )
            print("      [Slide 2] ✅ Completed")
            return ('slide_2', result)
        
        def generate_slide3():
            print("      [Slide 3] 📡 Analyzing channel distribution...")
            print("      [Slide 3] 🤖 Calling LLM for insights...")
            result = self.slide3_gen.generate(
                report_df, compare_df,
                BRAND_NAME, REPORT_DATE, COMPARE_DATE
            )
            print("      [Slide 3] ✅ Completed")
            return ('slide_3', result)
        
        def generate_slide4():
            print("      [Slide 4] 💭 Analyzing sentiment distribution...")
            print("      [Slide 4] 🤖 Calling LLM for insights...")
            result = self.slide4_gen.generate(
                report_df, BRAND_NAME, REPORT_DATE
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
        report = {
            "report_metadata": {
                "brand": BRAND_NAME,
                "report_date": REPORT_DATE,
                "compare_date": COMPARE_DATE,
                "generated_at": pd.Timestamp.now().isoformat(),
                "generation_mode": "parallel"
            },
            "slide_1": slides_data['slide_1'],
            "slide_2": slides_data['slide_2'],
            "slide_3": slides_data['slide_3'],
            "slide_4": slides_data['slide_4']
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
