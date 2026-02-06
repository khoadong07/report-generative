# Quick Test Guide - Slide 4 Channel Sentiment

## Quick Start (30 seconds)

```bash
# 1. Navigate to streamlit directory
cd test/streamlit

# 2. Start the app
streamlit run app.py

# 3. In browser:
# - Upload: test/Nestle_Gerber_15h_labeled.xlsx
# - Brand: Nestlé
# - Date: 2026-01-31, Time: 15:00
# - Click "Generate prompt"
# - Go to "Slide 4: Sentiment" tab
```

## What to Look For

### ✅ Slide 4 Preview Should Show:

**Layout**:
```
┌─────────────────────────────────────────────┐
│ Sentiment & Channel Breakdown               │
├──────────────────────┬──────────────────────┤
│ LEFT (50%)           │ RIGHT (50%)          │
│                      │                      │
│ Phân bố sắc thái     │ Sắc thái theo kênh  │
│ [Table]              │ [Table]              │
│ [Bar Chart]          │ [Stacked Bar Chart]  │
└──────────────────────┴──────────────────────┘
```

**Left Column**:
- Title: "Phân bố sắc thái thảo luận"
- Table with columns: Sentiment, Count
- Bar chart showing sentiment distribution

**Right Column**:
- Title: "Sắc thái thảo luận theo kênh"
- Table with columns: Channel, Negative, Neutral, Positive
- Stacked bar chart showing sentiment per channel
- Channels sorted by total count (descending)

### ✅ Generated Prompt Should Include:

**Slide 4 Section**:
```
SLIDE 4 - SENTIMENT & CHANNEL BREAKDOWN

LAYOUT:
- Two-column layout (equal width):
  * Left (50%): Pie chart (Overall Sentiment Distribution)
  * Right (50%): Stacked Bar Chart (Sentiment by Channel)

SENTIMENT BY CHANNEL (Stacked Bar Chart):

Facebook:
- Negative: X (Y%)
- Neutral: X (Y%)
- Positive: X (Y%)

[More channels...]

CHART DESIGN:

RIGHT - Stacked Bar Chart (100% Stacked, Horizontal):
- Y-axis: Channel names
- X-axis: Percentage (0-100%)
- Each bar is 100% height, divided by sentiment percentages
- All bars have equal height (100% stacked)
```

## Common Issues

### Issue: Right column shows "No channel sentiment data available"
**Solution**: Check that Excel file has "Channel" and "Sentiment" columns

### Issue: Channels not sorted correctly
**Solution**: Verify Slide4Generator sorts by total count descending

### Issue: Percentages don't add up to 100%
**Solution**: Check generate_slide4_data() percentage calculation

### Issue: Streamlit preview shows error
**Solution**: Check that slide4['channel_sentiment'] exists in JSON data

## Verification Commands

```bash
# Check syntax
python -m py_compile test/streamlit/app.py
python -m py_compile test/streamlit/slide_generators.py
python -m py_compile test/streamlit/generate_slide_prompt.py

# Verify imports
python -c "
from test.streamlit.slide_generators import Slide4Generator
from test.streamlit.prompts import get_sentiment_insight_prompt
from test.streamlit.generate_slide_prompt import generate_slide4_data
print('✅ All imports OK')
"

# Check channel_sentiment in code
grep -n "channel_sentiment" test/streamlit/slide_generators.py
grep -n "channel_sentiment" test/streamlit/prompts.py
grep -n "channel_sentiment" test/streamlit/generate_slide_prompt.py
grep -n "channel_sentiment" test/streamlit/app.py
```

## Expected Data Structure

```json
{
  "slide_4": {
    "title": "Sentiment & Channel Breakdown",
    "subtitle": "Khung giờ: 30/01/2026 15:00 → 31/01/2026 15:00",
    "sentiment_distribution": [
      {"Sentiment": "Negative", "Count": 123},
      {"Sentiment": "Neutral", "Count": 456},
      {"Sentiment": "Positive", "Count": 789}
    ],
    "channel_sentiment": [
      {
        "Channel": "Facebook",
        "Negative": 50,
        "Neutral": 200,
        "Positive": 300
      },
      {
        "Channel": "TikTok",
        "Negative": 30,
        "Neutral": 150,
        "Positive": 200
      }
    ],
    "insight": "Phân tích sentiment và channel..."
  }
}
```

## Success Criteria

- ✅ Streamlit app runs without errors
- ✅ Slide 4 preview shows two columns
- ✅ Left column: Overall sentiment table + chart
- ✅ Right column: Channel sentiment table + chart
- ✅ Channels sorted by total count (descending)
- ✅ Generated prompt includes channel sentiment data
- ✅ Prompt specifies 100% stacked bar chart
- ✅ Insight mentions channel-specific trends
- ✅ No Python syntax errors
- ✅ All imports work correctly

## Quick Debug

```python
# In Python console or Jupyter:
import pandas as pd
from test.streamlit.data_loader import DataLoader
from test.streamlit.slide_generators import Slide4Generator
from test.streamlit.llm_client import LLMClient

# Load data
loader = DataLoader('test/Nestle_Gerber_15h_labeled.xlsx')
df = loader.load_data()

# Filter by date
report_df = df[df['PublishedDay'] == pd.to_datetime('2026-01-31').date()]

# Check channel sentiment calculation
channel_sentiment = (
    report_df.groupby(["Channel", "Sentiment"])
    .size()
    .reset_index(name="Count")
)
print(channel_sentiment)

# Pivot
pivot = channel_sentiment.pivot(
    index="Channel",
    columns="Sentiment",
    values="Count"
).fillna(0)
print(pivot)

# Sort by total
pivot['Total'] = pivot.sum(axis=1)
pivot = pivot.sort_values('Total', ascending=False)
print(pivot)
```

## Files to Check

1. `test/streamlit/slide_generators.py` - Line ~400-430 (Slide4Generator)
2. `test/streamlit/prompts.py` - Line ~138-170 (get_sentiment_insight_prompt)
3. `test/streamlit/generate_slide_prompt.py` - Line ~180-220 (generate_slide4_data)
4. `test/streamlit/app.py` - Line ~295-330 (Slide 4 preview)

## Status: READY FOR TESTING ✅

All components implemented and verified. Ready for end-to-end testing.
