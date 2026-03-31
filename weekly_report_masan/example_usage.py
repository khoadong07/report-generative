#!/usr/bin/env python3
"""
Example usage of Slide01MasanMarket
Demonstrates how to use the Masan Consumer & Markets slide generator
"""
import pandas as pd
from datetime import datetime
from core.llm_client import LLMClient
from weekly_report_masan.slides.slide01_masan_market import Slide01MasanMarket
from weekly_report_masan.prompt_builder import generate_masan_prompt


def example_usage():
    """Example of how to generate Slide 1 for Masan report."""
    
    # 1. Prepare sample data (in real usage, load from your data source)
    sample_data = {
        'Id': range(100),
        'TopicId': ['topic_' + str(i % 10) for i in range(100)],
        'Topic': ['Masan Consumer'] * 40 + ['Vinamilk'] * 30 + ['Nutifood'] * 30,
        'Title': ['Sample title ' + str(i) for i in range(100)],
        'Content': ['Sample content ' + str(i) for i in range(100)],
        'Description': ['Sample description ' + str(i) for i in range(100)],
        'UrlComment': ['http://example.com/comment/' + str(i) for i in range(100)],
        'PublishedDate': pd.date_range(end='2024-03-30', periods=100, freq='H'),
        'Sentiment': ['Positive'] * 40 + ['Neutral'] * 35 + ['Negative'] * 25,
        'SiteName': ['Facebook'] * 50 + ['Forum'] * 30 + ['News'] * 20,
        'SiteId': range(100),
        'Channel': ['Social'] * 80 + ['News'] * 20,
        'UrlTopic': ['http://example.com/topic/' + str(i) for i in range(100)],
        'ParentId': [None] * 100,
        'Labels1': ['Label1'] * 100,
        'Labels2': ['Label2'] * 100,
        'Labels3': ['Label3'] * 100,
        'Labels4': ['Label4'] * 100,
        'Type': ['fbPageTopic'] * 30 + ['fbGroupComment'] * 25 + ['forumTopic'] * 25 + ['newsTopic'] * 20,
        'Level': [1] * 100,
        'Tags': ['tag1'] * 100,
        'Labels': ['label'] * 100,
        'Ngành hàng': ['FMCG'] * 100,
        'Cate': ['Food'] * 100,
        'Brand': ['Masan'] * 40 + ['Vinamilk'] * 30 + ['Nutifood'] * 30,
        'Sản phẩm': ['Product A'] * 100,
    }
    
    df = pd.DataFrame(sample_data)
    
    # 2. Initialize LLM client and slide generator
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL")
    model = os.getenv("MODEL", "meta-llama/Meta-Llama-3.1-70B-Instruct")
    
    llm_client = LLMClient(api_key=api_key, base_url=base_url, model=model)
    slide_generator = Slide01MasanMarket(llm_client)
    
    # 3. Define parameters
    main_brand = "Masan Consumer"
    competitors = ["Vinamilk", "Nutifood"]
    report_date = "2024-03-30"
    
    # 4. Generate slide data
    print("Generating Masan Consumer & Markets Report...")
    print("=" * 70)
    slide_data = slide_generator.generate(
        df=df,
        main_brand=main_brand,
        competitors=competitors,
        report_date=report_date
    )
    
    # 5. Build prompt
    prompt = generate_masan_prompt(slide_data)
    
    # 6. Output results
    print("\n" + "="*70)
    print("SLIDE DATA GENERATED")
    print("="*70)
    print(f"\nTitle: {slide_data['title']}")
    print(f"Subtitle: {slide_data['subtitle']}")
    
    print("\n--- Part 1: Main Brand Analysis ---")
    part1 = slide_data['part1_main_brand']
    print(f"Brand: {part1['brand']}")
    print(f"Weekly Buzz Trend: {len(part1['weekly_buzz_trend'])} weeks")
    print(f"Sentiment Distribution: {part1['sentiment_distribution']['total_buzz']} total buzz")
    print(f"Channel Distribution: {len(part1['channel_distribution'])} channels")
    print(f"Channel Insight: {part1['channel_insight'][:100]}...")
    
    print("\n--- Part 2: Competitor Analysis ---")
    part2 = slide_data['part2_competitors']
    print(f"Brands: {part2['brands']}")
    print(f"Number of brands analyzed: {len(part2['channel_distribution'])}")
    
    print("\n--- Conclusion ---")
    print(slide_data['conclusion'][:200] + "...")
    
    print("\n" + "="*70)
    print("PROMPT PREVIEW")
    print("="*70)
    print(prompt[:500] + "...\n")
    
    return slide_data, prompt


if __name__ == "__main__":
    # Run example
    slide_data, prompt = example_usage()
    
    # Optionally save to file
    with open("masan_slide01_prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt)
    print("\n✅ Prompt saved to: masan_slide01_prompt.txt")
    print("✅ Example completed successfully!")
