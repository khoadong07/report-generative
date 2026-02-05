# 🚀 START HERE

## Chào mừng đến với Report Generation System!

### 📍 Bạn đang ở đây: `/test/`

---

## ⚡ Chạy ngay trong 30 giây (Không cần API)

```bash
# Bước 1: Cài dependencies
pip install pandas openpyxl openai

# Bước 2: Chạy demo
python test/demo_without_api.py

# Bước 3: Chọn option 1, sau đó mở test/demo_report.html
```

**Xong!** Bạn vừa tạo một HTML report từ sample data.

---

## 🎯 Tiếp theo, bạn muốn làm gì?

### Option A: Tôi muốn hiểu hệ thống hoạt động như thế nào
👉 Đọc file: **`INDEX.md`**
- Tổng quan về tất cả files
- Workflow diagram
- Customization points

### Option B: Tôi muốn chạy với dữ liệu thật của mình
👉 Đọc file: **`QUICKSTART.md`**
- 3 bước đơn giản
- Setup API credentials
- Chạy với data thật

### Option C: Tôi cần hướng dẫn chi tiết từng bước
👉 Đọc file: **`SETUP_GUIDE.md`**
- Hướng dẫn setup đầy đủ
- Troubleshooting
- Best practices

### Option D: Tôi muốn hiểu kiến trúc code
👉 Đọc file: **`README_refactored.md`**
- Kiến trúc 6 layers
- Design patterns
- Extensibility

---

## 📂 Files trong thư mục này

### 📖 Documentation (Đọc)
- **START_HERE.md** ← Bạn đang đọc
- **INDEX.md** - Tổng quan tất cả
- **QUICKSTART.md** - Hướng dẫn nhanh
- **SETUP_GUIDE.md** - Hướng dẫn chi tiết
- **README_refactored.md** - Kiến trúc code
- **README_template.md** - Template system

### 🚀 Scripts (Chạy)
- **demo_without_api.py** - Demo không cần API ⭐
- **run_simple.py** - Chạy full pipeline
- **report_generator.py** - Generate JSON
- **template_renderer.py** - Render HTML
- **example_usage.py** - Ví dụ sử dụng

### 🏗️ Source Code (Code chính)
- **config.py** - Cấu hình
- **prompts.py** - LLM prompts
- **data_loader.py** - Load data
- **llm_client.py** - LLM wrapper
- **slide_generators.py** - Business logic
- **report_generator.py** - Orchestrator

### 🎨 Templates & Data
- **template_parameterized.html** - HTML template
- **sample_data.json** - Sample data
- **template.html** - Original template

---

## 🎓 Learning Path

```
1. Demo (5 phút)
   └─ python test/demo_without_api.py
   
2. Hiểu cấu trúc (10 phút)
   └─ Đọc INDEX.md
   
3. Chạy với data thật (20 phút)
   └─ Đọc QUICKSTART.md
   └─ Setup API & config
   └─ python test/run_simple.py
   
4. Customize (30 phút+)
   └─ Đọc README_refactored.md
   └─ Modify prompts.py
   └─ Modify config.py
```

---

## 💡 Quick Tips

### Tip 1: Test trước khi chạy thật
```bash
python test/demo_without_api.py
```
Xem HTML output để hiểu report sẽ trông như thế nào.

### Tip 2: Kiểm tra config
```python
# Mở test/config.py và kiểm tra:
FILE_PATH = "..."  # Đường dẫn đúng chưa?
REPORT_DATE = "..."  # Ngày đúng chưa?
BRAND_NAME = "..."  # Tên brand đúng chưa?
```

### Tip 3: Set API credentials
```bash
export API_KEY="your_api_key"
export BASE_URL="your_base_url"
```

### Tip 4: Chạy từ thư mục root
```bash
cd /path/to/project
python test/run_simple.py
```

---

## 🆘 Gặp vấn đề?

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

### Lỗi khác?
Đọc **SETUP_GUIDE.md** phần Troubleshooting

---

## 🎯 Recommended First Steps

1. ✅ Chạy demo: `python test/demo_without_api.py`
2. ✅ Xem output: Mở `test/demo_report.html`
3. ✅ Đọc overview: Mở `INDEX.md`
4. ✅ Hiểu workflow: Xem diagram trong `INDEX.md`
5. ✅ Setup thật: Theo `QUICKSTART.md`

---

## 📊 What This System Does

```
Input: Excel file với social media data
  ↓
Process: Analyze với LLM
  ↓
Output: Beautiful HTML report với 4 slides:
  - Slide 1: KPI Overview
  - Slide 2: Trendline Analysis
  - Slide 3: Channel Breakdown
  - Slide 4: Sentiment & Attributes
```

---

## 🎉 Ready to Start?

### Beginner? Start here:
```bash
python test/demo_without_api.py
```

### Have data & API? Start here:
```bash
# Read QUICKSTART.md first, then:
python test/run_simple.py
```

### Want to understand code? Start here:
```
Open: INDEX.md
```

---

**Good luck! 🚀**

*Nếu bạn thấy hữu ích, đừng quên customize prompts trong `prompts.py` để có insights tốt hơn!*
