# DateTime Display Logic - Comprehensive Fix

## Objective
Fix date/time display across all slides to clearly show 24-hour windows and avoid confusion.

---

## Display Strategy

### For All Slides (except Slide 2)
**Show exact 24-hour window:**
```
Khung giờ: 02/02/2026 15:00 → 03/02/2026 15:00
```

This makes it crystal clear:
- Start time: 02/02/2026 15:00
- End time: 03/02/2026 15:00
- Duration: Exactly 24 hours

### For Slide 2 (Trendline)
**Group by date only (not by hour):**
```
Khoảng thời gian: 28/01/2026 → 03/02/2026
```

Why? Trendline shows 7-day trend, grouping by hour would create too many data points and cause confusion.

---

## Implementation

### Step 1: Calculate Date Ranges (report_generator.py)

```python
if is_datetime_mode:
    # Parse datetime
    report_dt = pd.to_datetime(self.report_date)  # 2026-02-03 15:00:00
    compare_dt = report_dt - timedelta(hours=24)   # 2026-02-02 15:00:00
    
    # Keep raw format for parsing
    report_date_raw = self.report_date  # "2026-02-03 15:00:00"
    compare_date_raw = compare_dt.strftime("%Y-%m-%d %H:%M:%S")
    
    # Format for display
    report_display = report_dt.strftime("%d/%m/%Y %H:%M")    # "03/02/2026 15:00"
    compare_display = compare_dt.strftime("%d/%m/%Y %H:%M")  # "02/02/2026 15:00"
    
    # Format for subtitle (show 24h range)
    datetime_range_display = f"{compare_display} → {report_display}"
    # Result: "02/02/2026 15:00 → 03/02/2026 15:00"
```

### Step 2: Pass Correct Format to Each Slide

```python
# Slide 1, 3, 4, 5, 6: Use datetime_range_display
generate_slide1(datetime_range_display, compare_display)
generate_slide3(datetime_range_display, compare_display)
generate_slide4(datetime_range_display)
generate_slide5(datetime_range_display)
generate_slide6(datetime_range_display)

# Slide 2: Use report_date_raw (for parsing to group by date)
generate_slide2(report_date_raw)
```

---

## Slide-by-Slide Display

### Slide 1: Brand Overview
```
Title: Tổng quan về thương hiệu {Brand}
Subtitle: Khung giờ: 02/02/2026 15:00 → 03/02/2026 15:00 
          (so sánh với 01/02/2026 15:00 → 02/02/2026 15:00)
```

**Clarity**: User knows exactly which 24-hour window is being analyzed.

### Slide 2: Trendline
```
Title: Trendline | Diễn biến thảo luận
Subtitle: Khoảng thời gian: 28/01/2026 → 03/02/2026
```

**Why different?**
- Trendline shows 7-day trend
- Grouping by date (not hour) makes more sense
- Avoids 168 data points (7 days × 24 hours)
- Shows daily pattern, not hourly

**Implementation**:
```python
# In Slide2Generator
report_day = parse_date_flexible(report_date).date()  # Extract date only
start_day = report_day - timedelta(days=6)

# Group by PublishedDay (date), not PublishedDate (datetime)
trend_df = df_window.groupby("PublishedDay").size()
```

### Slide 3: Channel Breakdown
```
Title: Phân tích theo kênh thảo luận
Subtitle: Khung giờ: 02/02/2026 15:00 → 03/02/2026 15:00
          (so sánh với 01/02/2026 15:00 → 02/02/2026 15:00)
```

**Clarity**: Shows exact 24h window for channel analysis.

### Slide 4: Sentiment & Channel
```
Title: Sentiment & Channel Breakdown
Subtitle: Khung giờ: 02/02/2026 15:00 → 03/02/2026 15:00
```

**Clarity**: Sentiment analysis for specific 24h window.

### Slide 5: Top Posts
```
Title: Top 5 bài đăng có lượng tương tác cao
Subtitle: Khung giờ: 02/02/2026 15:00 → 03/02/2026 15:00
```

**Clarity**: Top posts from this specific 24h window.

### Slide 6: Deleted Posts
```
Title: Top 5 bài đăng đã xóa
Subtitle: Tất cả thời gian (không filter theo ngày)
```

**Note**: Slide 6 searches entire dataset, not filtered by date.

---

## Data Structure

### report_metadata
```json
{
  "report_metadata": {
    "brand": "Nestlé",
    "report_date": "02/02/2026 15:00 → 03/02/2026 15:00",
    "compare_date": "01/02/2026 15:00 → 02/02/2026 15:00",
    "generated_at": "2026-02-03 16:30:00"
  }
}
```

### Slide 1
```json
{
  "slide_1": {
    "title": "Tổng quan về thương hiệu Nestlé",
    "subtitle": "Khung giờ: 02/02/2026 15:00 → 03/02/2026 15:00 (so sánh với 01/02/2026 15:00 → 02/02/2026 15:00)",
    "data": [...]
  }
}
```

### Slide 2
```json
{
  "slide_2": {
    "title": "Trendline | Diễn biến thảo luận",
    "subtitle": "Khoảng thời gian: 28/01/2026 → 03/02/2026",
    "trendline": [
      {"date": "2026-01-28", "buzz": 123},
      {"date": "2026-01-29", "buzz": 145},
      ...
    ]
  }
}
```

---

## Benefits

### 1. Clarity
- ✅ Users know exactly which 24-hour window is analyzed
- ✅ No confusion about "which day" when time is involved
- ✅ Clear start and end times

### 2. Consistency
- ✅ All slides (except Slide 2) use same format
- ✅ Slide 2 uses appropriate format for trendline
- ✅ Metadata reflects actual analysis window

### 3. Accuracy
- ✅ Data filtering matches display
- ✅ No mismatch between subtitle and actual data
- ✅ Compare window clearly shown

### 4. User Experience
- ✅ Easy to understand at a glance
- ✅ No need to calculate time ranges mentally
- ✅ Professional presentation

---

## Example Output

### Input
```
Report Date: 2026-02-03 15:00:00
```

### Output

**Slide 1-6 Subtitles:**
```
Slide 1: Khung giờ: 02/02/2026 15:00 → 03/02/2026 15:00 
         (so sánh với 01/02/2026 15:00 → 02/02/2026 15:00)

Slide 2: Khoảng thời gian: 28/01/2026 → 03/02/2026

Slide 3: Khung giờ: 02/02/2026 15:00 → 03/02/2026 15:00
         (so sánh với 01/02/2026 15:00 → 02/02/2026 15:00)

Slide 4: Khung giờ: 02/02/2026 15:00 → 03/02/2026 15:00

Slide 5: Khung giờ: 02/02/2026 15:00 → 03/02/2026 15:00

Slide 6: Tất cả thời gian (không filter theo ngày)
```

---

## Variables Reference

| Variable | Format | Example | Usage |
|----------|--------|---------|-------|
| `report_date_raw` | yyyy-mm-dd HH:MM:SS | 2026-02-03 15:00:00 | For parsing (Slide 2) |
| `compare_date_raw` | yyyy-mm-dd HH:MM:SS | 2026-02-02 15:00:00 | For parsing |
| `report_display` | dd/mm/yyyy HH:MM | 03/02/2026 15:00 | End time display |
| `compare_display` | dd/mm/yyyy HH:MM | 02/02/2026 15:00 | Start time display |
| `datetime_range_display` | dd/mm/yyyy HH:MM → dd/mm/yyyy HH:MM | 02/02/2026 15:00 → 03/02/2026 15:00 | Subtitle (Slides 1,3,4,5,6) |

---

## Testing

### Test Case 1: DateTime Mode
```python
Input: report_date = "2026-02-03 15:00:00"

Expected:
- datetime_range_display = "02/02/2026 15:00 → 03/02/2026 15:00"
- Slide 1 subtitle: "Khung giờ: 02/02/2026 15:00 → 03/02/2026 15:00..."
- Slide 2 subtitle: "Khoảng thời gian: 28/01/2026 → 03/02/2026"
- Slide 5 subtitle: "Khung giờ: 02/02/2026 15:00 → 03/02/2026 15:00"
```

### Test Case 2: Date-Only Mode (Backward Compatibility)
```python
Input: report_date = "2026-02-03"

Expected:
- datetime_range_display = "2026-02-03"
- All slides use date-only format
- No time component shown
```

---

## Status: IMPLEMENTED ✅

- ✅ report_generator.py updated
- ✅ datetime_range_display variable created
- ✅ All slides receive correct format
- ✅ Slide 2 uses raw format for date grouping
- ✅ Metadata reflects 24h window
- ✅ Backward compatible with date-only mode

---

## Files Modified

1. `test/streamlit/report_generator.py`
   - Added `datetime_range_display` variable
   - Updated all slide generator calls
   - Updated metadata

---

## Next Steps

1. Clear cache and restart Streamlit
2. Test with datetime input
3. Verify all slide subtitles show correct format
4. Check Slide 2 groups by date (not hour)
5. Confirm no date parsing errors
