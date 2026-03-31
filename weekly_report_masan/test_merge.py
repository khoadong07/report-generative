#!/usr/bin/env python3
"""
Test script for data merge functionality
"""
import pandas as pd
from pathlib import Path
from data_processor import merge_nganh_hang, load_mapping_file, process_uploaded_file


def test_merge():
    """Test the merge function with sample data."""
    
    print("=" * 60)
    print("Testing Masan Data Merge")
    print("=" * 60)
    
    # Load mapping file
    print("\n1. Loading mapping file...")
    try:
        df_flat = load_mapping_file()
        print(f"   ✅ Loaded {len(df_flat)} mapping records")
        print(f"   Columns: {list(df_flat.columns)}")
        print(f"   Ngành hàng: {df_flat['Ngành hàng'].unique().tolist()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Create sample raw data
    print("\n2. Creating sample raw data...")
    df_raw = pd.DataFrame({
        "Id": [1, 2, 3, 4, 5],
        "Topic": ["Masan Consumer", "Vinamilk", "Nutifood", "Masan Consumer", "Vinamilk"],
        "Labels1": ["Tương ớt Chinsu", "Sữa tươi Vinamilk", "Sữa bột Nutifood", "Nước mắm Nam Ngư", "Sữa chua Vinamilk"],
        "Content": ["Test content 1", "Test content 2", "Test content 3", "Test content 4", "Test content 5"],
        "Sentiment": ["Positive", "Neutral", "Negative", "Positive", "Neutral"],
        "PublishedDate": pd.date_range("2024-01-01", periods=5),
        "Type": ["fbPageTopic", "fbGroupComment", "forumTopic", "newsTopic", "fbUserComment"]
    })
    print(f"   ✅ Created {len(df_raw)} sample records")
    
    # Test merge
    print("\n3. Testing merge function...")
    try:
        df_merged = merge_nganh_hang(df_raw, df_flat)
        print(f"   ✅ Merge successful!")
        print(f"   Output shape: {df_merged.shape}")
        print(f"   New columns: {[col for col in df_merged.columns if col not in df_raw.columns]}")
        
        # Check results
        print("\n4. Checking merge results...")
        
        # Count records with Ngành hàng
        has_nganh_hang = df_merged["Ngành hàng"].notna().sum()
        print(f"   Records with Ngành hàng: {has_nganh_hang}/{len(df_merged)}")
        
        # Count records with Brand
        if "Brand" in df_merged.columns:
            has_brand = df_merged["Brand"].notna().sum()
            print(f"   Records with Brand: {has_brand}/{len(df_merged)}")
        
        # Count records with Cate
        if "Cate" in df_merged.columns:
            has_cate = df_merged["Cate"].notna().sum()
            print(f"   Records with Cate: {has_cate}/{len(df_merged)}")
        
        # Show sample results
        print("\n5. Sample merged data:")
        print(df_merged[["Topic", "Labels1", "Ngành hàng", "Brand", "Sản phẩm"]].head())
        
        print("\n" + "=" * 60)
        print("✅ Test completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"   ❌ Error during merge: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_merge()
