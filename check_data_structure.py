#!/usr/bin/env python3
"""
Check the structure of the Excel data to understand the format
"""

import pandas as pd

def check_data_structure():
    """Check the structure of the Excel file"""
    
    excel_file = "/Users/khoadong/Downloads/62676257da4cac5f5e14dc78_1773806481372.xlsx"
    
    print(f"📂 Analyzing data structure: {excel_file}")
    
    try:
        # Load the Excel file
        df = pd.read_excel(excel_file)
        print(f"   ✅ Loaded {len(df)} rows")
        print(f"   📋 Columns: {list(df.columns)}")
        
        # Check Type column values
        if 'Type' in df.columns:
            type_counts = df['Type'].value_counts()
            print(f"\n   📊 Type distribution:")
            for type_name, count in type_counts.items():
                print(f"     - {type_name}: {count} rows")
        
        # Check Topic column values
        if 'Topic' in df.columns:
            topic_counts = df['Topic'].value_counts()
            print(f"\n   🏷️  Topic distribution (top 10):")
            for topic_name, count in topic_counts.head(10).items():
                print(f"     - {topic_name}: {count} rows")
        
        # Check date range
        if 'PublishedDate' in df.columns:
            df['PublishedDate'] = pd.to_datetime(df['PublishedDate'])
            min_date = df['PublishedDate'].min()
            max_date = df['PublishedDate'].max()
            print(f"\n   📅 Date range: {min_date} → {max_date}")
            
            # Show recent data distribution
            recent_data = df[df['PublishedDate'] >= (max_date - pd.Timedelta(days=14))]
            print(f"   📊 Recent 14 days: {len(recent_data)} rows")
            
            if 'Type' in recent_data.columns:
                recent_types = recent_data['Type'].value_counts()
                print(f"   📊 Recent Type distribution:")
                for type_name, count in recent_types.items():
                    print(f"     - {type_name}: {count} rows")
        
        # Show sample rows
        print(f"\n   📋 Sample data (first 3 rows):")
        for i, row in df.head(3).iterrows():
            print(f"     Row {i+1}:")
            print(f"       Topic: {row.get('Topic', 'N/A')}")
            print(f"       Type: {row.get('Type', 'N/A')}")
            print(f"       Title: {str(row.get('Title', 'N/A'))[:50]}...")
            print(f"       PublishedDate: {row.get('PublishedDate', 'N/A')}")
            print()
            
    except Exception as e:
        print(f"   ❌ Error loading file: {e}")

if __name__ == "__main__":
    check_data_structure()