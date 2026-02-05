#!/usr/bin/env python3
"""
Script to check available dates in Excel file
"""

import pandas as pd
import argparse
from pathlib import Path
from datetime import datetime


def check_dates(excel_path):
    """Check available dates in Excel file"""
    print("\n" + "="*60)
    print("📅 CHECKING AVAILABLE DATES")
    print("="*60)
    
    # Load Excel
    print(f"\n[1/3] Loading Excel file: {excel_path}")
    try:
        df = pd.read_excel(excel_path)
        print(f"   ✅ Loaded {len(df)} rows")
    except Exception as e:
        print(f"   ❌ Error loading Excel: {e}")
        return 1
    
    # Check for PublishedDay column
    print("\n[2/3] Checking for PublishedDay column...")
    if 'PublishedDay' not in df.columns:
        print(f"   ❌ Column 'PublishedDay' not found")
        print(f"   Available columns: {', '.join(df.columns)}")
        return 1
    
    print(f"   ✅ Found PublishedDay column")
    
    # Convert to date
    print("\n[3/3] Analyzing dates...")
    df['PublishedDay'] = pd.to_datetime(df['PublishedDay']).dt.date
    
    # Get unique dates
    unique_dates = sorted(df['PublishedDay'].unique())
    
    # Statistics
    print("\n" + "="*60)
    print("📊 DATE STATISTICS")
    print("="*60)
    print(f"Total rows: {len(df)}")
    print(f"Unique dates: {len(unique_dates)}")
    print(f"Date range: {unique_dates[0]} to {unique_dates[-1]}")
    
    # Count by date
    date_counts = df.groupby('PublishedDay').size().sort_index()
    
    print("\n" + "="*60)
    print("📅 AVAILABLE DATES (with row counts)")
    print("="*60)
    
    for date, count in date_counts.items():
        print(f"{date} - {count:,} rows")
    
    # Recommendations
    print("\n" + "="*60)
    print("💡 RECOMMENDATIONS")
    print("="*60)
    
    # Find date with most data
    max_date = date_counts.idxmax()
    max_count = date_counts.max()
    print(f"📈 Date with most data: {max_date} ({max_count:,} rows)")
    
    # Find recent dates
    recent_dates = unique_dates[-5:]
    print(f"\n📆 5 most recent dates:")
    for date in recent_dates:
        count = date_counts[date]
        print(f"   - {date} ({count:,} rows)")
    
    # Suggest report and compare dates
    if len(unique_dates) >= 2:
        suggested_report = unique_dates[-1]
        suggested_compare = unique_dates[-2]
        print(f"\n✅ SUGGESTED DATES FOR REPORT:")
        print(f"   --report-date \"{suggested_report}\"")
        print(f"   --compare-date \"{suggested_compare}\"")
        
        print(f"\n📝 EXAMPLE COMMAND:")
        print(f"   python generate_slide_prompt.py \\")
        print(f"     --excel \"{Path(excel_path).name}\" \\")
        print(f"     --brand \"Your Brand\" \\")
        print(f"     --report-date \"{suggested_report}\" \\")
        print(f"     --compare-date \"{suggested_compare}\"")
    
    print("\n" + "="*60)
    
    return 0


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Check available dates in Excel file'
    )
    parser.add_argument(
        '--excel',
        type=str,
        default='Nestle_Gerber_15h_labeled.xlsx',
        help='Path to Excel file (default: Nestle_Gerber_15h_labeled.xlsx)'
    )
    
    args = parser.parse_args()
    
    # Check if file exists
    excel_path = Path(args.excel)
    if not excel_path.exists():
        print(f"\n❌ Error: File not found: {args.excel}")
        print(f"\n💡 Tip: Make sure you're in the correct directory")
        print(f"   Current directory: {Path.cwd()}")
        return 1
    
    return check_dates(excel_path)


if __name__ == "__main__":
    exit(main())
