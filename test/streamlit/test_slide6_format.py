#!/usr/bin/env python3
"""
Test Slide 6 format normalization
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from generate_slide_prompt import generate_slide6_data

# Mock slide 6 data with various deleted indicators
mock_slide6 = {
    "title": "Top 5 bài đăng đã xóa",
    "subtitle": "Tất cả thời gian",
    "total_deleted_posts": 5,
    "deleted_posts": [
        {
            "stt": 1,
            "noi_dung_bai_dang": "Test post 1",
            "ngay_dang": "2026-01-31 00:00:00",
            "kenh": "Facebook",
            "nguoi_dang": "User 1",
            "url_topic": "https://example.com/1",
            "metric_status": {
                "likes": "die",
                "shares": "die",
                "comments": "die",
                "views": "die",
                "total": "N/A"
            }
        },
        {
            "stt": 2,
            "noi_dung_bai_dang": "Test post 2",
            "ngay_dang": "2026-01-31 00:00:00",
            "kenh": "Facebook",
            "nguoi_dang": "User 2",
            "url_topic": "https://example.com/2",
            "metric_status": {
                "likes": "not exist or close group",
                "shares": "not exist or close group",
                "comments": "not exist or close group",
                "views": "not exist or close group",
                "total": "N/A"
            }
        },
        {
            "stt": 3,
            "noi_dung_bai_dang": "Test post 3",
            "ngay_dang": "2026-01-31 00:00:00",
            "kenh": "Tiktok",
            "nguoi_dang": "User 3",
            "url_topic": "https://example.com/3",
            "metric_status": {
                "likes": "deleted",
                "shares": "deleted",
                "comments": "deleted",
                "views": "deleted",
                "total": "deleted"
            }
        },
        {
            "stt": 4,
            "noi_dung_bai_dang": "Test post 4",
            "ngay_dang": "2026-01-31 00:00:00",
            "kenh": "Youtube",
            "nguoi_dang": "User 4",
            "url_topic": "https://example.com/4",
            "metric_status": {
                "likes": "removed",
                "shares": "removed",
                "comments": "removed",
                "views": "removed",
                "total": "N/A"
            }
        },
        {
            "stt": 5,
            "noi_dung_bai_dang": "Test post 5",
            "ngay_dang": "2026-01-31 00:00:00",
            "kenh": "Facebook",
            "nguoi_dang": "User 5",
            "url_topic": "https://example.com/5",
            "metric_status": {
                "likes": "unavailable",
                "shares": "unavailable",
                "comments": "unavailable",
                "views": "unavailable",
                "total": "N/A"
            }
        }
    ]
}

print("="*60)
print("TESTING SLIDE 6 FORMAT NORMALIZATION")
print("="*60)

print("\nInput deleted indicators:")
for post in mock_slide6['deleted_posts']:
    print(f"  Post {post['stt']}: {post['metric_status']['likes']}")

print("\nGenerating formatted data...")
result = generate_slide6_data(mock_slide6)

print("\n" + "="*60)
print("RESULTS")
print("="*60)

print(f"\nTitle: {result['title']}")
print(f"Total deleted: {result['total_deleted']}")
print(f"Table rows: {len(result['table_rows'])}")

print("\n" + "-"*60)
print("FORMATTED VALUES")
print("-"*60)

all_normalized = True
for row in result['table_rows']:
    print(f"\nRow {row['stt']}:")
    print(f"  - Likes: {row['likes']}")
    print(f"  - Shares: {row['shares']}")
    print(f"  - Comments: {row['comments']}")
    print(f"  - Views: {row['views']}")
    print(f"  - Total: {row['total']}")
    
    # Check if all values are normalized to "Deleted"
    if row['likes'] != 'Deleted' or row['shares'] != 'Deleted' or row['comments'] != 'Deleted' or row['views'] != 'Deleted':
        all_normalized = False
        print("  ❌ NOT all values normalized to 'Deleted'")
    else:
        print("  ✅ All values normalized to 'Deleted'")

print("\n" + "="*60)
if all_normalized:
    print("✅ SUCCESS: All deleted indicators normalized to 'Deleted'")
else:
    print("❌ FAILED: Some values not normalized")
print("="*60)
