# 🚀 Cách chạy source code

## Bước 1: Cài dependencies
```bash
pip install pandas openpyxl openai python-dotenv
```

## Bước 2: Kiểm tra setup
```bash
cd test
python test_setup.py
```

Nếu tất cả đều ✅ thì tiếp tục bước 3.

## Bước 3: Generate report
```bash
cd test
python generate_report.py
```

Chờ khoảng 1-2 phút để LLM generate insights.

Output: `report_output.json`

## Bước 4: Render HTML
```bash
cd test
python render_html.py
```

Output: `final_report.html`

## Bước 5: Xem kết quả
```bash
open final_report.html
```

Hoặc mở file `test/final_report.html` trong browser.

---

## ⚡ Quick Commands

```bash
# Tất cả trong 1 lần
cd test
python generate_report.py && python render_html.py && open final_report.html
```

---

## 🔧 Troubleshooting

### Lỗi: Module not found
```bash
pip install pandas openpyxl openai python-dotenv
```

### Lỗi: API_KEY not found
Kiểm tra file `test/.env`:
```
API_KEY=your_key_here
BASE_URL=your_url_here
```

### Lỗi: File not found
Kiểm tra file `test/config.py` - đảm bảo `FILE_PATH` đúng.

### Lỗi khác
Chạy `python test_setup.py` để kiểm tra setup.

---

## 📁 Files quan trọng

- `.env` - API credentials
- `config.py` - Cấu hình (dates, brand, file path)
- `generate_report.py` - Script generate report
- `render_html.py` - Script render HTML
- `test_setup.py` - Script kiểm tra setup

---

## 🎯 Workflow

```
1. Check setup
   python test_setup.py
   
2. Generate JSON
   python generate_report.py
   
3. Render HTML
   python render_html.py
   
4. View result
   open final_report.html
```

---

## 💡 Tips

- Chạy từ thư mục `test/`
- Đảm bảo `.env` có API credentials
- Kiểm tra `config.py` trước khi chạy
- Chờ 1-2 phút cho LLM generate insights
