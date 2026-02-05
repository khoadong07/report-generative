# Slide Prompt Generator - Streamlit App

Web interface để generate slide prompts cho Manuss, Gamma, Beautiful.ai

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

```bash
streamlit run app.py
```

Ứng dụng sẽ mở tại: http://localhost:8501

## 📋 Cách sử dụng

### Bước 1: Upload Excel File
- Click "Browse files" trong sidebar
- Chọn file Excel chứa brand data
- Hỗ trợ format: `.xlsx`, `.xls`

### Bước 2: Nhập Brand Name
- Nhập tên brand (ví dụ: Vinamilk, Vinfast, Nestle)

### Bước 3: Chọn Report Date
- Chọn ngày báo cáo từ date picker
- Compare date sẽ tự động tính = report date - 1 ngày

### Bước 4: Generate
- Click nút "🚀 Generate Prompt"
- Đợi 3-4 phút (app sẽ gọi LLM 4 lần)
- Xem kết quả trong 3 tabs:
  - **Preview**: Xem trước prompt
  - **Copy**: Copy prompt để paste vào slide platforms
  - **Download**: Tải file .txt và .json

## 📊 Features

### ✅ Input
- Upload Excel file
- Brand name input
- Date picker với auto-calculate compare date
- API credentials validation

### ✅ Processing
- **Parallel processing** - 4 slides generated simultaneously (~1 minute)
- Progress bar với real-time updates
- Real-time status updates
- Error handling với detailed traceback
- Dynamic file path handling

### ✅ Output
- Markdown preview với scrollable container
- Copy to clipboard functionality
- Download prompt as .txt
- Download JSON data
- Next steps guide cho 3 platforms

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
test/streamlit/
├── app.py              # Main Streamlit app
├── requirements.txt    # Python dependencies
├── .env               # API credentials (create this)
└── README.md          # This file
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

```bash
# Terminal 1: Start app
cd test/streamlit
streamlit run app.py

# Browser: http://localhost:8501
# 1. Upload: Nestle_Gerber_15h_labeled.xlsx
# 2. Brand: Nestle
# 3. Date: 2026-01-30
# 4. Click Generate
# 5. Wait 3-4 minutes
# 6. Copy/Download prompt
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
