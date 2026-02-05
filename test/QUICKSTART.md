# Quick Start Guide

## 🚀 Chạy nhanh trong 3 bước

### Bước 1: Cài đặt dependencies
```bash
pip install pandas openpyxl openai
```

### Bước 2: Demo không cần API (Test ngay)
```bash
python test/demo_without_api.py
```
Chọn option 1 để render HTML từ sample data, sau đó mở `test/demo_report.html` trong browser.

### Bước 3: Chạy với dữ liệu thật (Cần API)

#### 3.1. Set API credentials
```bash
export API_KEY="your_api_key"
export BASE_URL="your_base_url"
```

#### 3.2. Cập nhật config
Mở `test/config.py` và sửa:
```python
FILE_PATH = "path/to/your/data.xlsx"
REPORT_DATE = "2026-02-01"
BRAND_NAME = "Your Brand"
```

#### 3.3. Chạy
```bash
python test/run_simple.py
```

Xong! Mở `test/final_report.html` để xem kết quả.

---

## 📁 Các file quan trọng

| File | Mục đích |
|------|----------|
| `config.py` | Cấu hình (dates, brand, file path) |
| `prompts.py` | Prompts cho LLM (dễ chỉnh sửa) |
| `report_generator.py` | Tạo report JSON |
| `template_renderer.py` | Render HTML từ JSON |
| `run_simple.py` | Script chạy tự động |
| `demo_without_api.py` | Demo không cần API |

---

## 🎯 Use Cases

### 1. Test template (Không cần API)
```bash
python test/demo_without_api.py
# Chọn option 1
```

### 2. Generate report từ data
```bash
# Set credentials
export API_KEY="..."
export BASE_URL="..."

# Run
python test/run_simple.py
```

### 3. Chỉ generate JSON (không render HTML)
```python
from test.report_generator import ReportGenerator
import os

generator = ReportGenerator(
    os.getenv("API_KEY"),
    os.getenv("BASE_URL")
)
report = generator.generate_and_save("my_report.json")
```

### 4. Chỉ render HTML từ JSON có sẵn
```python
from test.template_renderer import TemplateRenderer
import json

with open('my_report.json', 'r') as f:
    data = json.load(f)

renderer = TemplateRenderer('test/template_parameterized.html')
renderer.render_to_file(data, 'my_report.html')
```

---

## 🔧 Troubleshooting

### Lỗi: Module not found
```bash
pip install pandas openpyxl openai
```

### Lỗi: API_KEY not set
```bash
export API_KEY="your_key"
export BASE_URL="your_url"
```

### Lỗi: File not found
Kiểm tra `FILE_PATH` trong `test/config.py`

### Lỗi: Import error
```bash
# Chạy từ thư mục root của project
cd /path/to/project
python test/run_simple.py
```

---

## 📊 Cấu trúc dữ liệu Excel

Excel file cần có các columns:
- `PublishedDate` (datetime)
- `Type` (string)
- `Sentiment` (Positive/Negative/Neutral)
- `Labels` (string, phân cách bởi dấu phẩy)
- `UrlTopic` (string)
- `Title` (string)
- `Content` (string)
- `Description` (string)
- `Reactions` (number)
- `Shares` (number)
- `Comments` (number)
- `Views` (number)

---

## 🎨 Customize

### Thay đổi prompts
Chỉnh sửa `test/prompts.py`

### Thay đổi logic tính toán
Chỉnh sửa `test/slide_generators.py`

### Thay đổi template HTML
Chỉnh sửa `test/template_parameterized.html`

### Thay đổi config
Chỉnh sửa `test/config.py`

---

## 📚 Tài liệu chi tiết

- `SETUP_GUIDE.md` - Hướng dẫn setup chi tiết
- `README_refactored.md` - Kiến trúc và design
- `README_template.md` - Hướng dẫn về template system

---

## 💡 Tips

1. **Test với sample data trước**: Chạy `demo_without_api.py` để hiểu flow
2. **Kiểm tra config**: Đảm bảo dates và file path đúng
3. **Monitor API calls**: LLM sẽ được gọi cho mỗi slide
4. **Customize prompts**: Chỉnh prompts trong `prompts.py` để có insights tốt hơn
5. **Save intermediate results**: JSON output có thể reuse để render HTML nhiều lần

---

## 🆘 Need Help?

1. Đọc `SETUP_GUIDE.md` cho hướng dẫn chi tiết
2. Chạy `demo_without_api.py` để test không cần API
3. Check logs và error messages
4. Verify data format trong Excel
