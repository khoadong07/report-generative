# Report Generation System

Hệ thống tạo báo cáo phân tích thương hiệu tự động từ dữ liệu social media.

## 🚀 Quick Start

### 1. Demo (30 giây - Không cần API)
```bash
pip install pandas openpyxl openai
python test/demo_without_api.py
```
Chọn option 1, sau đó mở `test/demo_report.html` trong browser.

### 2. Chạy với dữ liệu thật (Cần API)
```bash
# Set credentials
export API_KEY="your_api_key"
export BASE_URL="your_base_url"

# Update config
# Mở test/config.py và sửa FILE_PATH, REPORT_DATE, BRAND_NAME

# Run
python test/run_simple.py

# Mở test/final_report.html
```

## 📚 Documentation

| File | Mục đích |
|------|----------|
| **[START_HERE.md](START_HERE.md)** | 👈 Bắt đầu từ đây |
| [INDEX.md](INDEX.md) | Tổng quan hệ thống |
| [QUICKSTART.md](QUICKSTART.md) | Hướng dẫn nhanh 3 bước |
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | Hướng dẫn chi tiết |
| [README_refactored.md](README_refactored.md) | Kiến trúc code |
| [SUMMARY.md](SUMMARY.md) | Tóm tắt toàn bộ |

## 🏗️ Architecture

```
Config Layer (config.py)
    ↓
Prompt Layer (prompts.py)
    ↓
Data Layer (data_loader.py)
    ↓
LLM Layer (llm_client.py)
    ↓
Business Logic (slide_generators.py)
    ↓
Orchestration (report_generator.py)
    ↓
Output (JSON → HTML)
```

## 📦 Files

### Core Modules
- `config.py` - Cấu hình tập trung
- `prompts.py` - LLM prompts (dễ chỉnh sửa)
- `data_loader.py` - Load & preprocess data
- `llm_client.py` - LLM API wrapper
- `slide_generators.py` - Logic tạo slides
- `report_generator.py` - Orchestrator chính

### Scripts
- `demo_without_api.py` - Demo không cần API ⭐
- `run_simple.py` - Chạy tự động
- `template_renderer.py` - Render HTML

### Templates
- `template_parameterized.html` - HTML template
- `sample_data.json` - Sample data

## 🎯 Features

- ✅ Module hóa, dễ maintain
- ✅ Prompts tách riêng, dễ customize
- ✅ Config tập trung
- ✅ Demo mode không cần API
- ✅ Extensible architecture
- ✅ Full documentation

## 💡 Customize

### Thay đổi prompts
Chỉnh sửa `prompts.py`

### Thay đổi config
Chỉnh sửa `config.py`

### Thay đổi logic
Chỉnh sửa `slide_generators.py`

### Thay đổi template
Chỉnh sửa `template_parameterized.html`

## 🆘 Help

- Gặp vấn đề? → Đọc [SETUP_GUIDE.md](SETUP_GUIDE.md)
- Muốn hiểu code? → Đọc [README_refactored.md](README_refactored.md)
- Cần hướng dẫn nhanh? → Đọc [QUICKSTART.md](QUICKSTART.md)

## 📊 Output

Hệ thống tạo HTML report với 4 slides:
1. **Slide 1**: KPI Overview (buzz, posts, engagement, etc.)
2. **Slide 2**: Trendline Analysis (xu hướng theo thời gian)
3. **Slide 3**: Channel Breakdown (phân bổ theo kênh)
4. **Slide 4**: Sentiment & Brand Attributes

---

**👉 Bắt đầu: Đọc [START_HERE.md](START_HERE.md)**
