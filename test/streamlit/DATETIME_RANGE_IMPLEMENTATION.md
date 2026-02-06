# DateTime Range Implementation - 24-Hour Window Reporting

## 📋 Tổng quan

Thay đổi từ **report theo ngày** sang **report theo khung giờ 24h**.

### Ví dụ:
- **Input**: `2026-01-31 15:00:00`
- **Khung giờ 1** (Report): `2026-01-30 15:00:00` → `2026-01-31 15:00:00` (24h)
- **Khung giờ 2** (Compare): `2026-01-29 15:00:00` → `2026-01-30 15:00:00` (24h)

## 🔧 Các thay đổi cần thực hiện

### 1. DataLoader (data_loader.py)
**Thêm method mới:**
```python
def filter_by_datetime_range(self, end_datetime: str) -> pd.DataFrame:
    """
    Filter by 24-hour window: (end_datetime - 24h) to end_datetime
    
    Args:
        end_datetime: "YYYY-MM-DD HH:MM:SS"
    
    Returns:
        DataFrame filtered for 24-hour window
    """
    end_dt = pd.to_datetime(end_datetime)
    start_dt = end_dt - timedelta(hours=24)
    
    return self.df[
        (self.df["PublishedDate"] > start_dt) &
        (self.df["PublishedDate"] <= end_dt)
    ].copy()
```

**Giữ method cũ** `filter_by_date()` cho backward compatibility.

### 2. ReportGenerator (report_generator.py)

**Update generate_report():**
```python
def generate_report(self) -> Dict[str, Any]:
    # Parse datetime
    report_dt = pd.to_datetime(self.report_date)
    compare_dt = report_dt - timedelta(hours=24)
    
    # Filter by 24-hour windows
    report_df = self.data_loader.filter_by_datetime_range(
        self.report_date
    )
    compare_df = self.data_loader.filter_by_datetime_range(
        compare_dt.strftime("%Y-%m-%d %H:%M:%S")
    )
    
    # Format for display
    report_date_display = report_dt.strftime("%d/%m/%Y %H:%M")
    compare_date_display = compare_dt.strftime("%d/%m/%Y %H:%M")
```

### 3. Streamlit App (app.py)

**Update input:**
```python
# Current: date_input
report_date = st.date_input("Report date", value=datetime.now())

# New: datetime input
col1, col2 = st.columns(2)
with col1:
    report_date = st.date_input("Report date", value=datetime.now())
with col2:
    report_time = st.time_input("Report time", value=time(15, 0))

# Combine
report_datetime = datetime.combine(report_date, report_time)
report_datetime_str = report_datetime.strftime("%Y-%m-%d %H:%M:%S")
```

**Auto-calculate compare datetime:**
```python
compare_datetime = report_datetime - timedelta(hours=24)
st.caption(f"Compare: {compare_datetime.strftime('%d/%m/%Y %H:%M')} (24h trước)")
```

### 4. Prompts (prompts.py)

**Update all prompts to include time:**
```python
def get_overview_insight_prompt(...):
    return f"""
BỐI CẢNH:
- Thương hiệu: {brand}
- Khung giờ báo cáo: {report_datetime_display}
- Khung giờ so sánh: {compare_datetime_display}
- Thời gian: 24 giờ
...
"""
```

### 5. Slide Generators

**Update all subtitle formats:**
```python
# Old
"subtitle": f"Ngày {report_date}"

# New
"subtitle": f"Khung giờ: {report_datetime_display} (24h)"
```

## 📊 Format hiển thị

### Trong Insight:
- "Trong 24 giờ từ 30/01/2026 15:00 đến 31/01/2026 15:00..."
- "So với 24 giờ trước (29/01 15:00 - 30/01 15:00)..."

### Trong Subtitle:
- "Khung giờ: 31/01/2026 15:00 (24h)"
- "So sánh: 30/01/2026 15:00 (24h trước)"

## 🔄 Backward Compatibility

Giữ các method cũ:
- `filter_by_date()` - vẫn hoạt động với date only
- `filter_by_date_range()` - vẫn hoạt động

Thêm method mới:
- `filter_by_datetime_range()` - cho 24-hour window

## ⚠️ Lưu ý

1. **Data phải có PublishedDate với giờ chính xác**
   - Nếu data chỉ có ngày, giờ sẽ là 00:00:00
   - Cần kiểm tra data có đủ thông tin giờ không

2. **Timezone**
   - Hiện tại không xử lý timezone
   - Giả định tất cả datetime đều cùng timezone

3. **UI/UX**
   - User nhập datetime thay vì chỉ date
   - Auto-calculate compare datetime (không cần nhập)

## 📝 Testing

Test cases cần kiểm tra:
1. Input: `2026-01-31 15:00:00`
   - Report window: `2026-01-30 15:00:01` to `2026-01-31 15:00:00`
   - Compare window: `2026-01-29 15:00:01` to `2026-01-30 15:00:00`

2. Edge case: Midnight
   - Input: `2026-01-31 00:00:00`
   - Report window: `2026-01-30 00:00:01` to `2026-01-31 00:00:00`

3. Edge case: End of month
   - Input: `2026-02-01 15:00:00`
   - Compare window crosses month boundary

## 🚀 Implementation Steps

1. ✅ Update DataLoader with `filter_by_datetime_range()`
2. ⏳ Update ReportGenerator to use datetime
3. ⏳ Update Streamlit app UI for datetime input
4. ⏳ Update all prompts to include time info
5. ⏳ Update all slide generators subtitle format
6. ⏳ Test with sample data

---

**Status**: 🚧 In Progress
**Priority**: High
**Impact**: Breaking change - requires UI update
