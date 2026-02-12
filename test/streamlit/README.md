# Slide Prompt Generator - Streamlit App

Web interface để generate slide prompts cho Manuss, Gamma, Beautiful.ai

**Hỗ trợ 2 loại báo cáo:**
- **Daily Report** (6 slides) - Báo cáo theo ngày với cửa sổ 24 giờ
- **Weekly Report** (12 slides) - Báo cáo theo tuần với cửa sổ 7 ngày

## 🚀 Quick Start

### 1. Cài đặt dependencies

```bash
cd test/streamlit
pip install -r requirements.txt
```

### 2. Cấu hình API credentials

Tạo file `.env` trong folder `test/streamlit/`:

```bash
API_KEY=your_api_key_here
BASE_URL=your_base_url_here
```

Hoặc copy từ file `.env` ở parent directory.

### 3. Chạy ứng dụng

**Daily Report (6 slides):**
```bash
streamlit run app.py
```

**Weekly Report (12 slides):**
```bash
streamlit run app_weekly.py
```

Ứng dụng sẽ mở tại: http://localhost:8501

## 📋 Cách sử dụng

### Daily Report (6 slides)

### Bước 1: Upload Excel File
- Click "Browse files" trong sidebar
- Chọn file Excel chứa brand data
- Hỗ trợ format: `.xlsx`, `.xls`

### Bước 2: Nhập Brand Name
- Nhập tên brand (ví dụ: Vinamilk, Vinfast, Nestle)

### Bước 3: Chọn Report Date & Time
- Chọn ngày báo cáo từ date picker
- Chọn giờ cắt data (mặc định 15:00)
- Hệ thống tự động tính cửa sổ 24 giờ

### Bước 4: Generate
- Click nút "🚀 Generate prompt"
- Đợi ~1 phút (parallel processing)
- Xem kết quả trong 3 tabs

---

### Weekly Report (12 slides)

### Bước 1: Upload Excel File
- Click "Browse files" trong sidebar
- Chọn file Excel chứa brand data

### Bước 2: Nhập Brand Name
- Nhập tên brand

### Bước 3: Chọn End Date & Time
- Chọn ngày kết thúc tuần hiện tại
- Chọn giờ cắt data (mặc định 15:00)
- Hệ thống tự động tính 4 tuần (current + 3 past weeks)

### Bước 4: Generate
- Click nút "🚀 Generate weekly report"
- Đợi ~2 phút (parallel processing)
- Xem kết quả trong 3 tabs

---

### Output Tabs
- **Preview**: Xem trước prompt
- **Copy**: Copy prompt để paste vào slide platforms
- **Download**: Tải file .txt và .json

## 📊 Features

### ✅ Daily Report (6 slides)
1. **Slide 1**: Brand Overview - KPIs với so sánh 24h trước
2. **Slide 2**: Trendline - Xu hướng 7 ngày
3. **Slide 3**: Channel Breakdown - Phân bố theo kênh
4. **Slide 4**: Sentiment & Attributes - Phân tích sắc thái
5. **Slide 5**: Top 5 Posts - Bài đăng có tương tác cao
6. **Slide 6**: Top 5 Deleted Posts - Bài đăng đã xóa

### ✅ Weekly Report (12 slides)
1. **Slide 1**: Tổng quan tuần - KPIs + so sánh 4 tuần
2. **Slide 2**: Đường xu hướng - 7 ngày trong tuần
3. **Slide 3**: Phân bố kênh - Pie chart + Top 10 nguồn
4. **Slide 4**: Top nguồn tương tác cao - Bảng
5. **Slide 5**: Top bài đăng tương tác cao - Bảng
6. **Slide 6**: Sắc thái & chủ đề - 2 pie charts + chart cột
7. **Slide 7**: Chủ đề tích cực - Chart + insight
8. **Slide 8**: Top đề cập tích cực - Bảng
9. **Slide 9**: Top bài đăng tích cực - Bảng
10. **Slide 10**: Chủ đề tiêu cực - Chart + insight
11. **Slide 11**: Top đề cập tiêu cực - Bảng
12. **Slide 12**: Top bài đăng tiêu cực - Bảng

### ✅ Technical Features
- **Parallel processing** - Slides generated simultaneously
- **24-hour window** (Daily) - Chính xác đến giờ
- **7-day window** (Weekly) - Tự động tính 4 tuần
- **Progress tracking** - Real-time updates
- **Error handling** - Detailed traceback
- **Auto-cleanup** - Temp files removed

## 🎨 UI Features

- **Responsive layout** - Wide mode với sidebar
- **Custom styling** - Professional color scheme
- **Progress tracking** - Visual feedback cho user
- **Success/Error boxes** - Clear status indicators
- **Tabs navigation** - Organized output display
- **Download buttons** - Easy file export

## 🔧 Technical Details

### File Structure
```
/
├── app.py                          # Daily report app (6 slides)
├── app_weekly.py                   # Weekly report app (12 slides)
├── report_generator.py             # Daily report generator
├── report_generator_weekly.py      # Weekly report generator
├── slide_generators.py             # Daily slide generators
├── slide_generators_weekly.py      # Weekly slide generators (12 classes)
├── generate_slide_prompt.py        # Daily prompt generator
├── generate_slide_prompt_weekly.py # Weekly prompt generator
├── prompts.py                      # Daily LLM prompts
├── prompts_weekly.py               # Weekly LLM prompts
├── data_loader.py                  # Shared data loader
├── llm_client.py                   # Shared LLM client
├── config.py                       # Shared configuration
├── requirements.txt                # Python dependencies
├── .env                           # API credentials
└── README.md                      # This file
```

### Dependencies
- `streamlit` - Web framework
- `pandas` - Data processing
- `openpyxl` - Excel file handling
- `python-dotenv` - Environment variables
- `requests` - API calls (via ReportGenerator)

### Import Strategy
App imports từ parent directory:
- `generate_slide_prompt.py` - Core functions
- `report_generator.py` - LLM integration
- `config.py` - Configuration (auto-updated)

## 🐛 Troubleshooting

### Error: Cannot import ReportGenerator
**Solution**: Đảm bảo file `report_generator.py` tồn tại trong folder `test/`

### Error: API credentials not found
**Solution**: Tạo file `.env` với API_KEY và BASE_URL

### Error: Excel file not valid
**Solution**: Kiểm tra format Excel file, đảm bảo có đúng columns

### App chạy chậm
**Normal**: Generate prompt mất 3-4 phút do gọi LLM 4 lần

## 📝 Example Usage

### Daily Report
```bash
# Terminal: Start app
streamlit run app.py

# Browser: http://localhost:8501
# 1. Upload: brand_data.xlsx
# 2. Brand: Vinamilk
# 3. Date: 2026-02-10, Time: 15:00
# 4. Click Generate
# 5. Wait ~1 minute
# 6. Copy/Download prompt
```

### Weekly Report
```bash
# Terminal: Start app
streamlit run app_weekly.py

# Browser: http://localhost:8501
# 1. Upload: brand_data.xlsx
# 2. Brand: Vinamilk
# 3. End Date: 2026-02-10, Time: 15:00
# 4. System auto-calculates 4 weeks
# 5. Click Generate
# 6. Wait ~2 minutes
# 7. Copy/Download prompt
```

## 🎯 Next Steps After Generation

### Manuss
1. Open https://manuss.com
2. Paste prompt
3. Click "Generate"
4. Wait 30-60 seconds

### Gamma
1. Open https://gamma.app
2. Paste prompt
3. Click "Generate"
4. Wait 30-60 seconds

### Beautiful.ai
1. Open https://beautiful.ai
2. Paste prompt
3. Click "Generate"
4. Manually add hyperlinks if needed

## 💡 Tips

- **Save JSON data** - Để reuse hoặc debug
- **Check preview** - Trước khi copy
- **Test with small data** - Để verify setup
- **Keep .env secure** - Đừng commit API keys

## 🔐 Security

- API credentials loaded từ `.env`
- Temp files auto-cleanup
- No data persistence (session-based)
- Safe file upload handling

## 📞 Support

Nếu gặp vấn đề:
1. Check console logs
2. View error details trong expander
3. Verify API credentials
4. Check Excel file format
