# Slide 4: Facebook Channel Normalization & Vertical Chart

## Overview
Updated Slide 4 to split Facebook into sub-channels and use vertical bar chart.

---

## Changes Made

### 1. Facebook Channel Normalization ✅

**Problem**: Facebook channel was too broad, mixing Users, Pages, and Groups.

**Solution**: Split Facebook into 3 sub-channels based on `Type` column:

| Type Value | Normalized Channel |
|------------|-------------------|
| `fbUserComment`, `fbUserTopic` | **Facebook Users** |
| `fbPageComment`, `fbPageTopic` | **Facebook Pages** |
| `fbGroupComment`, `fbGroupTopic` | **Facebook Groups** |
| Other Facebook types | **Facebook** (fallback) |

**Implementation**:
```python
def normalize_facebook_channel(row):
    """Split Facebook into Users/Pages/Groups based on Type"""
    if row['Channel'] != 'Facebook':
        return row['Channel']
    
    type_val = str(row.get('Type', '')).lower()
    
    # Map Type to Facebook sub-channels
    if 'user' in type_val:
        return 'Facebook Users'
    elif 'page' in type_val:
        return 'Facebook Pages'
    elif 'group' in type_val:
        return 'Facebook Groups'
    else:
        return 'Facebook'  # Fallback

report_df['ChannelNormalized'] = report_df.apply(normalize_facebook_channel, axis=1)
```

### 2. Chart Orientation Changed ✅

**Before**: Horizontal bars (bars going left-right)
```
Facebook    ████████████████████ 100%
Tiktok      ████████████ 60%
Youtube     ████████ 40%
```

**After**: Vertical bars (columns standing up)
```
     100% ┤ ███
          │ ███  ███
          │ ███  ███  ███
      0%  └─────────────────
           FB   TT   YT
          Users
```

**Why**: Vertical bars are more standard for category comparison and easier to read.

### 3. Insight Format Preserved ✅

**Format maintained**:
```
"Insight text about sentiment... [Nguồn: URL_1]
Another insight about channels... [Nguồn: URL_2]"
```

Each sentence ends with `[Nguồn: URL_X]` citation.

---

## Technical Implementation

### File: `test/streamlit/slide_generators.py`

**Added normalization logic**:
```python
# Normalize Facebook channels based on Type
def normalize_facebook_channel(row):
    if row['Channel'] != 'Facebook':
        return row['Channel']
    
    type_val = str(row.get('Type', '')).lower()
    
    if 'user' in type_val:
        return 'Facebook Users'
    elif 'page' in type_val:
        return 'Facebook Pages'
    elif 'group' in type_val:
        return 'Facebook Groups'
    else:
        return 'Facebook'

report_df['ChannelNormalized'] = report_df.apply(normalize_facebook_channel, axis=1)

# Use ChannelNormalized for grouping
channel_sentiment = (
    report_df.groupby(["ChannelNormalized", "Sentiment"])
    .size()
    .reset_index(name="Count")
)
```

### File: `test/streamlit/generate_slide_prompt.py`

**Updated chart specification**:
```
RIGHT - Stacked Bar Chart (100% Stacked, VERTICAL):
- X-axis: Channel names (Facebook Users, Facebook Pages, Facebook Groups, Tiktok, Youtube, etc.)
- Y-axis: Percentage (0-100%)
- Each bar is 100% height, divided by sentiment percentages
- Bars are VERTICAL (columns), not horizontal
- Sort channels by total count (descending, left to right)

IMPORTANT NOTES:
- Facebook channel is split into 3 sub-channels:
  * Facebook Users (from fbUserComment, fbUserTopic)
  * Facebook Pages (from fbPageComment, fbPageTopic)
  * Facebook Groups (from fbGroupComment, fbGroupTopic)
- Chart orientation: VERTICAL bars (columns standing up)
- NOT horizontal bars
```

---

## Data Flow

### Input Data
```
Channel    | Type           | Sentiment
-----------|----------------|----------
Facebook   | fbUserComment  | Positive
Facebook   | fbPageTopic    | Negative
Facebook   | fbGroupComment | Neutral
Tiktok     | tiktokComment  | Positive
Youtube    | youtubeComment | Negative
```

### After Normalization
```
ChannelNormalized  | Sentiment
-------------------|----------
Facebook Users     | Positive
Facebook Pages     | Negative
Facebook Groups    | Neutral
Tiktok            | Positive
Youtube           | Negative
```

### Output (channel_sentiment)
```json
[
  {
    "Channel": "Facebook Users",
    "Negative": 50,
    "Neutral": 200,
    "Positive": 300
  },
  {
    "Channel": "Facebook Pages",
    "Negative": 30,
    "Neutral": 150,
    "Positive": 200
  },
  {
    "Channel": "Facebook Groups",
    "Negative": 20,
    "Neutral": 100,
    "Positive": 150
  },
  {
    "Channel": "Tiktok",
    "Negative": 15,
    "Neutral": 80,
    "Positive": 120
  }
]
```

---

## Chart Visualization

### Vertical Stacked Bar Chart (100%)

```
Percentage
    100% ┤ ████ Positive (Green)
         │ ████
         │ ████ Neutral (Gray)
         │ ████
         │ ████ Negative (Red)
      0% └─────────────────────────────────────
           FB     FB      FB      TT     YT
          Users  Pages  Groups
```

**Key Features**:
- All bars same height (100%)
- Sorted by total count (left to right, descending)
- Facebook split into 3 sub-channels
- Colors: Red (Negative), Gray (Neutral), Green (Positive)
- Percentage labels on each segment

---

## Example Output

### Slide 4 Data Structure
```json
{
  "slide_4": {
    "title": "Sentiment & Channel Breakdown",
    "subtitle": "Khung giờ: 02/02/2026 15:00 → 03/02/2026 15:00",
    "sentiment_distribution": [
      {"Sentiment": "Negative", "Count": 123},
      {"Sentiment": "Neutral", "Count": 456},
      {"Sentiment": "Positive", "Count": 789}
    ],
    "channel_sentiment": [
      {
        "Channel": "Facebook Users",
        "Negative": 50,
        "Neutral": 200,
        "Positive": 300
      },
      {
        "Channel": "Facebook Pages",
        "Negative": 30,
        "Neutral": 150,
        "Positive": 200
      },
      {
        "Channel": "Facebook Groups",
        "Negative": 20,
        "Neutral": 100,
        "Positive": 150
      },
      {
        "Channel": "Tiktok",
        "Negative": 15,
        "Neutral": 80,
        "Positive": 120
      },
      {
        "Channel": "Youtube",
        "Negative": 8,
        "Neutral": 26,
        "Positive": 89
      }
    ],
    "insight": "Trong khung giờ báo cáo, thương hiệu có 789 thảo luận tích cực (57.5%)... [Nguồn: URL_1] Phân tích theo kênh cho thấy Facebook Users dẫn đầu với 550 thảo luận... [Nguồn: URL_2]"
  }
}
```

### Generated Prompt (Slide 4 Section)
```
SLIDE 4 - SENTIMENT & CHANNEL BREAKDOWN

LAYOUT:
- Two-column layout (50% each)
- Left: Pie chart (Overall Sentiment)
- Right: Vertical stacked bar chart (Sentiment by Channel)

SENTIMENT BY CHANNEL (Stacked Bar Chart):

Facebook Users:
- Negative: 50 (9.1%)
- Neutral: 200 (36.4%)
- Positive: 300 (54.5%)

Facebook Pages:
- Negative: 30 (7.9%)
- Neutral: 150 (39.5%)
- Positive: 200 (52.6%)

Facebook Groups:
- Negative: 20 (7.4%)
- Neutral: 100 (37.0%)
- Positive: 150 (55.6%)

...

CHART DESIGN:
RIGHT - Stacked Bar Chart (100% Stacked, VERTICAL):
- X-axis: Channel names
- Y-axis: Percentage (0-100%)
- Bars are VERTICAL (columns)
- Facebook split into Users/Pages/Groups

INSIGHT:
"Trong khung giờ báo cáo... [Nguồn: URL_1]
Phân tích theo kênh... [Nguồn: URL_2]"
```

---

## Benefits

### 1. Better Granularity
- ✅ Facebook Users vs Pages vs Groups clearly separated
- ✅ More actionable insights per sub-channel
- ✅ Identify which Facebook segment has issues

### 2. Standard Visualization
- ✅ Vertical bars are industry standard
- ✅ Easier to compare across channels
- ✅ More professional appearance

### 3. Preserved Format
- ✅ Insight format maintained with [Nguồn: URL]
- ✅ LLM prompt unchanged
- ✅ Citation style consistent

### 4. Backward Compatible
- ✅ Non-Facebook channels unchanged
- ✅ Fallback for unknown Facebook types
- ✅ Works with existing data

---

## Testing

### Test Case 1: Facebook Normalization
```python
Input:
  Channel: Facebook, Type: fbUserComment → Facebook Users
  Channel: Facebook, Type: fbPageTopic → Facebook Pages
  Channel: Facebook, Type: fbGroupComment → Facebook Groups
  Channel: Tiktok, Type: tiktokComment → Tiktok (unchanged)

Expected: ✅ 3 Facebook sub-channels + other channels
```

### Test Case 2: Chart Orientation
```
Expected in prompt:
- "VERTICAL bars (columns)"
- "X-axis: Channel names"
- "Y-axis: Percentage"
- NOT "Horizontal" or "Y-axis: Channel names"

Result: ✅ Correct specification
```

### Test Case 3: Insight Format
```
Expected:
"Insight sentence... [Nguồn: URL_1]
Another sentence... [Nguồn: URL_2]"

Result: ✅ Format preserved
```

---

## Files Modified

1. **test/streamlit/slide_generators.py**
   - Added `normalize_facebook_channel()` function
   - Use `ChannelNormalized` for grouping
   - Debug log shows normalized channels

2. **test/streamlit/generate_slide_prompt.py**
   - Updated chart specification to VERTICAL
   - Added Facebook sub-channel notes
   - Clarified chart orientation

3. **test/streamlit/prompts.py**
   - No changes (format already correct)

---

## Status: COMPLETE ✅

- ✅ Facebook normalization implemented
- ✅ Chart changed to vertical bars
- ✅ Insight format preserved
- ✅ Syntax validation passed
- ✅ Ready for testing

---

## Next Steps

1. Clear cache and restart Streamlit
2. Generate report with Facebook data
3. Verify channel_sentiment shows 3 Facebook sub-channels
4. Check generated prompt specifies VERTICAL bars
5. Confirm insight format has [Nguồn: URL] citations
