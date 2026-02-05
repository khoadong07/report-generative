"""
Example usage of the refactored report generation system
"""

import os
import json
from test.report_generator import ReportGenerator
from test.template_renderer import TemplateRenderer


def example_1_generate_report():
    """Example 1: Generate report from data"""
    print("="*60)
    print("EXAMPLE 1: Generate Report from Data")
    print("="*60)
    
    # Get API credentials
    api_key = os.getenv("API_KEY", "your_api_key_here")
    base_url = os.getenv("BASE_URL", "your_base_url_here")
    
    # Initialize generator
    generator = ReportGenerator(api_key=api_key, base_url=base_url)
    
    # Generate and save report
    report = generator.generate_and_save("test/my_report.json")
    
    print("\nReport generated successfully!")
    print(f"Slides generated: {list(report.keys())}")
    
    return report


def example_2_render_html():
    """Example 2: Render HTML from JSON data"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Render HTML from JSON")
    print("="*60)
    
    # Load report data
    with open('test/sample_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Initialize renderer
    renderer = TemplateRenderer('test/template_parameterized.html')
    
    # Render to HTML
    renderer.render_to_file(data, 'test/rendered_example.html')
    
    print("\nHTML rendered successfully!")
    print("Open 'test/rendered_example.html' in your browser")


def example_3_custom_config():
    """Example 3: Generate report with custom configuration"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Custom Configuration")
    print("="*60)
    
    # Import and modify config
    from test import config
    
    # Temporarily modify config
    original_brand = config.BRAND_NAME
    original_top_n = config.TOP_N_TOPICS
    
    config.BRAND_NAME = "Custom Brand"
    config.TOP_N_TOPICS = 10
    
    print(f"Modified config:")
    print(f"  Brand: {config.BRAND_NAME}")
    print(f"  Top N Topics: {config.TOP_N_TOPICS}")
    
    # Restore original config
    config.BRAND_NAME = original_brand
    config.TOP_N_TOPICS = original_top_n
    
    print("\nConfig restored to original values")


def example_4_individual_slides():
    """Example 4: Generate individual slides"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Generate Individual Slides")
    print("="*60)
    
    from test.data_loader import DataLoader
    from test.llm_client import LLMClient
    from test.slide_generators import Slide1Generator
    from test.config import *
    
    # Setup
    api_key = os.getenv("API_KEY", "your_api_key_here")
    base_url = os.getenv("BASE_URL", "your_base_url_here")
    
    # Load data
    print("Loading data...")
    loader = DataLoader(FILE_PATH, TEXT_COLUMNS, METRIC_COLUMNS)
    df = loader.preprocess()
    
    report_df = loader.filter_by_date(REPORT_DATE)
    compare_df = loader.filter_by_date(COMPARE_DATE)
    
    # Initialize LLM client
    llm_client = LLMClient(
        api_key=api_key,
        base_url=base_url,
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        system_prompt=LLM_SYSTEM_PROMPT
    )
    
    # Generate only Slide 1
    print("Generating Slide 1 only...")
    slide1_gen = Slide1Generator(llm_client, TOPIC_TYPES, TOP_N_TOPICS)
    slide1 = slide1_gen.generate(
        report_df, compare_df,
        BRAND_NAME, REPORT_DATE, COMPARE_DATE
    )
    
    print(f"\nSlide 1 generated:")
    print(f"  Title: {slide1['title']}")
    print(f"  Number of KPIs: {len(slide1['data'])}")
    print(f"  Insight length: {len(slide1['insight'])} characters")


def example_5_custom_prompt():
    """Example 5: Use custom prompt"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Custom Prompt")
    print("="*60)
    
    from test.llm_client import LLMClient
    
    api_key = os.getenv("API_KEY", "your_api_key_here")
    base_url = os.getenv("BASE_URL", "your_base_url_here")
    
    # Initialize client
    llm_client = LLMClient(
        api_key=api_key,
        base_url=base_url,
        model="google/gemma-3-27b-it",
        temperature=0.2,
        system_prompt="Bạn là chuyên gia phân tích dữ liệu."
    )
    
    # Custom prompt
    custom_prompt = """
    Hãy tóm tắt ngắn gọn về tình hình thương hiệu dựa trên dữ liệu sau:
    - Tổng thảo luận: 1000
    - Sentiment: 60% Neutral, 30% Negative, 10% Positive
    
    Viết 2-3 câu ngắn gọn.
    """
    
    # Generate insight
    print("Generating insight with custom prompt...")
    insight = llm_client.generate_insight(custom_prompt)
    
    print(f"\nGenerated insight:")
    print(insight)


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("REFACTORED REPORT GENERATION SYSTEM - EXAMPLES")
    print("="*60)
    
    # Check if API credentials are set
    if not os.getenv("API_KEY") or not os.getenv("BASE_URL"):
        print("\n⚠️  WARNING: API_KEY and BASE_URL not set in environment")
        print("Some examples will not work without valid credentials")
        print("\nTo set credentials:")
        print("  export API_KEY='your_key'")
        print("  export BASE_URL='your_url'")
    
    # Run examples that don't require API
    try:
        example_2_render_html()
    except Exception as e:
        print(f"Error in example 2: {e}")
    
    try:
        example_3_custom_config()
    except Exception as e:
        print(f"Error in example 3: {e}")
    
    # Examples requiring API (commented out by default)
    # Uncomment to run when you have valid credentials
    
    # try:
    #     example_1_generate_report()
    # except Exception as e:
    #     print(f"Error in example 1: {e}")
    
    # try:
    #     example_4_individual_slides()
    # except Exception as e:
    #     print(f"Error in example 4: {e}")
    
    # try:
    #     example_5_custom_prompt()
    # except Exception as e:
    #     print(f"Error in example 5: {e}")
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()
