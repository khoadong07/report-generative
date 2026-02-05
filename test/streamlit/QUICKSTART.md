# 🚀 Quick Start Guide

## Chạy Streamlit App trong 3 bước

### Bước 1: Cài đặt dependencies

```bash
cd test/streamlit
pip install -r requirements.txt
```

### Bước 2: Cấu hình API

Tạo file `.env`:

```bash
# Copy từ example
cp .env.example .env

# Hoặc tạo mới
echo "API_KEY=your_api_key_here" > .env
echo "BASE_URL=your_base_url_here" >> .env
```

Hoặc copy từ parent directory:

```bash
cp ../.env .env
```

### Bước 3: Chạy app

```bash
streamlit run app.py
```

App sẽ mở tại: **http://localhost:8501**

---

## 📱 Sử dụng App

### 1. Upload Excel File
- Click "Browse files" trong sidebar
- Chọn file Excel (ví dụ: `Nestle_Gerber_15h_labeled.xlsx`)

### 2. Nhập thông tin
- **Brand Name**: Nhập tên brand (ví dụ: Nestle)
- **Report Date**: Chọn ngày báo cáo
- **Compare Date**: Tự động tính = report date - 1 ngày

### 3. Generate
- Click nút **"🚀 Generate Prompt"**
- Đợi ~1 phút (parallel processing - xử lý 4 slides cùng lúc)
- Progress bar sẽ hiển thị tiến trình

### 4. Xem kết quả
- **Tab Preview**: Xem trước prompt
- **Tab Copy**: Copy prompt để paste vào slide platforms
- **Tab Download**: Tải file .txt và .json

---

## 🎯 Sử dụng Prompt

### Manuss
1. Mở https://manuss.com
2. Paste prompt
3. Click "Generate"

### Gamma
1. Mở https://gamma.app
2. Paste prompt
3. Click "Generate"

### Beautiful.ai
1. Mở https://beautiful.ai
2. Paste prompt
3. Click "Generate"

---

## ⚠️ Troubleshooting

### Lỗi: API credentials not found
**Giải pháp**: Tạo file `.env` với API_KEY và BASE_URL

### Lỗi: Cannot import ReportGenerator
**Giải pháp**: Đảm bảo các file cần thiết tồn tại trong folder `test/streamlit/`:
- `report_generator.py`
- `data_loader.py`
- `llm_client.py`
- `slide_generators.py`
- `prompts.py`
- `config.py`

### Lỗi: File upload failed
**Giải pháp**: Kiểm tra format Excel file, đảm bảo có đúng columns

### App chạy chậm
**Bình thường**: Generate prompt mất ~1 phút với parallel processing (4 slides cùng lúc)

---

## 💡 Tips

- Kiểm tra API credentials trước khi generate
- Sử dụng file Excel có đúng format
- Chọn ngày có data trong dataset
- Save JSON data để reuse hoặc debug
- Test với data nhỏ trước khi chạy full report

---

## 📞 Cần trợ giúp?

1. Check console logs trong terminal
2. View error details trong app (expander)
3. Verify API credentials trong sidebar
4. Check Excel file format và columns
