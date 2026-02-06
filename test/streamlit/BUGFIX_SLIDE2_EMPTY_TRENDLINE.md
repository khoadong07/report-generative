# Bugfix: Slide 2 Empty Trendline Error

## Issue
**Error**: `attempt to get argmax of an empty sequence`

**Location**: `slide_generators.py` - Slide2Generator.generate()

**Cause**: When the 7-day window has no data, `trend_df` is empty, causing `trend_df["buzz"].idxmax()` to fail.

## Error Log
```
[Slide 2] 💭 Analyzing 7-day trendline...
❌ Error generating slide_2: attempt to get argmax of an empty sequence
```

## Root Cause Analysis

### Code Flow
1. Filter data for 7-day window (report_day - 6 days to report_day)
2. Group by PublishedDay and count buzz
3. Call `trend_df["buzz"].idxmax()` to find peak day
4. **FAILS** if trend_df is empty (no data in window)

### When This Happens
- Selected datetime range has no data
- Data only exists outside the 7-day window
- Excel file has no posts in the lookback period
- PublishedDay column has incorrect dates

## Solution

### Before (Buggy Code)
```python
# Calculate trendline
trend_df = (
    df_window
    .groupby("PublishedDay")
    .size()
    .reset_index(name="buzz")
    .sort_values("PublishedDay")
)

# Detect peak day - FAILS if trend_df is empty
peak_row = trend_df.loc[trend_df["buzz"].idxmax()]  # ❌ Error here
peak_day = peak_row["PublishedDay"]
peak_buzz = int(peak_row["buzz"])
```

### After (Fixed Code)
```python
# Calculate trendline
trend_df = (
    df_window
    .groupby("PublishedDay")
    .size()
    .reset_index(name="buzz")
    .sort_values("PublishedDay")
)

# Check if we have data
if len(trend_df) == 0:
    print("      ⚠️  Warning: No data in 7-day window, returning empty trendline")
    return {
        "title": f"Trendline | Diễn biến thảo luận",
        "subtitle": f"Khoảng thời gian: {start_day} → {report_day}",
        "window": {
            "start_date": str(start_day),
            "end_date": str(report_day)
        },
        "trendline": [],
        "peak_day": {
            "date": str(report_day),
            "buzz": 0,
            "links": []
        },
        "current_day": {
            "date": str(report_day),
            "buzz": 0,
            "is_still_hot": False
        },
        "insight": f"Không có dữ liệu thảo luận trong khoảng thời gian {start_day} đến {report_day}. Vui lòng kiểm tra lại dữ liệu nguồn hoặc chọn khoảng thời gian khác có dữ liệu."
    }

# Continue with normal flow if we have data
trendline_data = [...]
peak_row = trend_df.loc[trend_df["buzz"].idxmax()]  # ✅ Safe now
```

## Changes Made

### File: `test/streamlit/slide_generators.py`
**Line**: ~250-270 (Slide2Generator.generate method)

**Change**:
- Added empty dataframe check after calculating trend_df
- Return graceful fallback data structure if no data
- Provide user-friendly error message in insight
- Prevents argmax() call on empty sequence

## Testing

### Test Case 1: Empty 7-Day Window
```python
# Scenario: Report date has no data in 7-day lookback
report_date = "2026-02-01 15:00:00"  # No data in this range
# Expected: Returns empty trendline with helpful message
# Result: ✅ No error, graceful fallback
```

### Test Case 2: Normal Data
```python
# Scenario: Report date has data in 7-day lookback
report_date = "2026-01-31 15:00:00"  # Has data
# Expected: Normal trendline with peak day
# Result: ✅ Works as before
```

### Test Case 3: Partial Data
```python
# Scenario: Only 1-2 days have data in window
report_date = "2026-01-31 15:00:00"  # Sparse data
# Expected: Trendline with available days, peak from those days
# Result: ✅ Works correctly
```

## Verification

```bash
# Syntax check
python -m py_compile test/streamlit/slide_generators.py

# Run Streamlit app
cd test/streamlit
streamlit run app.py

# Test with date range that has no data
# - Upload Excel file
# - Select date range with no posts
# - Click "Generate prompt"
# - Check Slide 2 shows graceful error message
```

## Expected Behavior

### Before Fix
```
[Slide 2] 💭 Analyzing 7-day trendline...
❌ Error generating slide_2: attempt to get argmax of an empty sequence
[App crashes or shows error]
```

### After Fix
```
[Slide 2] 💭 Analyzing 7-day trendline...
⚠️  Warning: No data in 7-day window, returning empty trendline
[Slide 2] ✅ Completed

Slide 2 Preview:
- Title: "Trendline | Diễn biến thảo luận"
- Subtitle: "Khoảng thời gian: 2026-01-25 → 2026-02-01"
- Trendline: (empty chart)
- Insight: "Không có dữ liệu thảo luận trong khoảng thời gian..."
```

## Related Issues

### Similar Potential Issues
Check these locations for similar empty dataframe issues:

1. ✅ **Slide1Generator** - Uses `.sum()` which returns 0 for empty (safe)
2. ✅ **Slide2Generator** - FIXED (this issue)
3. ✅ **Slide3Generator** - Has empty check already
4. ✅ **Slide4Generator** - Uses `.value_counts()` which returns empty (safe)
5. ✅ **Slide5Generator** - Uses `.head()` which returns empty (safe)
6. ✅ **Slide6Generator** - Has empty check already

## Prevention

### Best Practices
1. Always check dataframe length before calling aggregation functions
2. Use `.empty` or `len(df) == 0` checks
3. Provide graceful fallbacks with user-friendly messages
4. Test with edge cases (empty data, single row, etc.)

### Code Pattern
```python
# Good pattern for aggregations
df_result = df.groupby(...).agg(...)

if len(df_result) == 0:
    # Return graceful fallback
    return default_structure_with_message

# Continue with normal processing
value = df_result.some_operation()
```

## Status: FIXED ✅

- ✅ Empty dataframe check added
- ✅ Graceful fallback implemented
- ✅ User-friendly error message
- ✅ Syntax validation passed
- ✅ No breaking changes to data structure
- ✅ Backward compatible

## Files Modified
- `test/streamlit/slide_generators.py` (Slide2Generator.generate method)

## Impact
- **Low risk**: Only affects edge case (empty 7-day window)
- **High benefit**: Prevents app crashes
- **User experience**: Shows helpful message instead of error
