# Slide 6 Implementation - Top 5 Deleted Posts

## ✅ Status: COMPLETED

Slide 6 has been successfully implemented and tested. It detects and displays deleted posts from the entire dataset.

## 📊 Features

### Detection Logic
- **Searches entire dataset** (not filtered by report date)
- **Detects multiple deleted indicators**:
  - "deleted"
  - "not exist or close group"
  - "die"
  - "removed"
- **Case-insensitive partial matching** in metric columns (Reactions, Shares, Comments, Views)

### Data Handling
- **Loads raw Excel data directly** to preserve string values like "Deleted"
- **Bypasses DataLoader's numeric conversion** to avoid losing deleted indicators
- **Returns top 5 deleted posts** (or fewer if less than 5 exist)

## 🧪 Test Results

### Test Dataset: Nestle_Gerber_15h_labeled.xlsx
- **Total deleted posts found**: 27
- **Top 5 returned**: ✅
- **Deleted indicators detected**:
  - "not exist or close group" (20 posts)
  - "die" (7 posts)

### Sample Output
```
[1] Zelda Phuong (Facebook)
    Metrics: not exist or close group

[2] ytedoisong.vn (Tiktok)
    Metrics: die

[3] Phương Thảo HoaMaishop (Facebook)
    Metrics: not exist or close group
```

## 🏗️ Architecture

### File Structure
```
test/streamlit/
├── slide_generators.py      # Slide6Generator class
├── report_generator.py      # Calls Slide 6 with file_path
├── data_loader.py           # Converts metrics to numeric (reverted)
├── app.py                   # Streamlit UI with Slide 6 preview
└── generate_slide_prompt.py # Slide 6 prompt template
```

### Key Implementation Details

#### 1. Slide6Generator (slide_generators.py)
```python
def generate(self, full_df, brand, report_date, file_path=None):
    # Load raw data to preserve "Deleted" strings
    if file_path:
        df_raw = pd.read_excel(file_path)
    else:
        df_raw = full_df
    
    # Filter for deleted posts
    deleted_mask = df_topics[self.check_cols].apply(
        lambda col: col.apply(is_deleted)
    ).any(axis=1)
```

#### 2. ReportGenerator (report_generator.py)
```python
# Pass file_path to Slide 6
slide6_data = self.slide6_gen.generate(
    df, self.brand_name, self.report_date, 
    file_path=self.file_path  # ← Critical parameter
)
```

#### 3. DataLoader (data_loader.py)
```python
def ensure_numeric_columns(self):
    # Convert all metrics to numeric (no special value preservation)
    self.df[col] = pd.to_numeric(self.df[col], errors="coerce")
    self.df[col] = self.df[col].fillna(0)
```

## 🎨 Streamlit UI

### Slide 6 Preview Tab
- **Table view** with all 10 columns (STT, Nội dung, Ngày đăng, Kênh, Người đăng, Likes, Shares, Comments, Views, Total, Link)
- **Expandable details** for each deleted post
- **Metric status display** showing deleted indicators
- **Error handling** for missing data, NaN values, empty results
- **Summary info** showing total deleted posts found

### Color Scheme
- **Red theme** (#dc2626) to indicate deleted/removed content
- **Warning icons** (🗑️) for visual emphasis

## 🔄 How to Use in Streamlit

1. **Upload Excel file** with deleted posts
2. **Enter brand name** and select report date
3. **Click "Generate prompt"**
4. **Navigate to "Slide 6: Deleted Posts" tab**
5. **View table and expandable details**

## 📝 Prompt Template

The generated prompt includes:

```
SLIDE 6 - TOP 5 BÀI ĐĂNG ĐÃ XÓA
Tiêu đề: Top 5 bài đăng đã xóa
Subtitle: Tất cả thời gian (không filter theo ngày)

Bảng 10 cột:
- STT
- Nội dung bài đăng (with Link)
- Ngày đăng
- Kênh
- Người đăng
- Likes (status)
- Shares (status)
- Comments (status)
- Views (status)
- Total (status)

Color: Red (#dc2626)
```

## 🐛 Troubleshooting

### Issue: No deleted posts found
**Solution**: Check if Excel file has "Deleted", "die", "not exist or close group", or "removed" in metric columns

### Issue: Streamlit shows empty Slide 6
**Solution**: 
1. Click "🔄 Clear Cache & Refresh" button
2. Re-upload Excel file
3. Regenerate report

### Issue: TypeError when summing metrics
**Solution**: Ensure DataLoader converts all metrics to numeric (already fixed)

## ✅ Verification Checklist

- [x] Slide 6 generator loads raw data
- [x] Deleted indicators detected correctly
- [x] Top 5 posts returned
- [x] Streamlit preview displays table
- [x] Expandable details work
- [x] Prompt template includes Slide 6
- [x] DataLoader doesn't break other slides
- [x] Full report generation works
- [x] Test scripts cleaned up

## 🎯 Next Steps

The implementation is complete and ready for production use. Users can now:

1. Generate 6-slide reports (including deleted posts)
2. View deleted posts in Streamlit preview
3. Export prompts for Manus/Genspark with Slide 6 data
4. Track deleted/removed content across entire dataset

---

**Last Updated**: 2026-02-06
**Status**: ✅ Production Ready
