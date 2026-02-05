# Report Generation System - Index

## 📖 Tài liệu

| File | Mô tả | Khi nào dùng |
|------|-------|--------------|
| **QUICKSTART.md** | Hướng dẫn nhanh 3 bước | Bắt đầu ngay, muốn chạy nhanh |
| **SETUP_GUIDE.md** | Hướng dẫn setup chi tiết | Cần hiểu rõ từng bước setup |
| **README_refactored.md** | Kiến trúc và design | Muốn hiểu cấu trúc code |
| **README_template.md** | Template system | Muốn customize HTML template |

## 🚀 Scripts để chạy

| Script | Mô tả | Cần API? |
|--------|-------|----------|
| **demo_without_api.py** | Demo render HTML từ sample data | ❌ Không |
| **run_simple.py** | Chạy full pipeline tự động | ✅ Có |
| **report_generator.py** | Generate report JSON | ✅ Có |
| **template_renderer.py** | Render HTML từ JSON | ❌ Không |
| **example_usage.py** | Các ví dụ sử dụng | ✅ Có |

## 🏗️ Source Code

| File | Mô tả | Vai trò |
|------|-------|---------|
| **config.py** | Cấu hình tập trung | Config layer |
| **prompts.py** | LLM prompts | Prompt layer |
| **data_loader.py** | Load & preprocess data | Data layer |
| **llm_client.py** | LLM API wrapper | LLM layer |
| **slide_generators.py** | Logic tạo slides | Business logic |
| **report_generator.py** | Orchestrator chính | Orchestration |

## 🎯 Workflow

```
┌─────────────────────────────────────────────────────────┐
│                    WORKFLOW OVERVIEW                     │
└─────────────────────────────────────────────────────────┘

1. DEMO (Không cần API)
   ├─ Chạy: python test/demo_without_api.py
   ├─ Input: test/sample_data.json
   └─ Output: test/demo_report.html
   
2. FULL PIPELINE (Cần API)
   ├─ Chạy: python test/run_simple.py
   ├─ Input: Excel file + API credentials
   ├─ Process:
   │  ├─ Load data (data_loader.py)
   │  ├─ Generate Slide 1 (slide_generators.py)
   │  ├─ Generate Slide 2 (slide_generators.py)
   │  ├─ Generate Slide 4 (slide_generators.py)
   │  └─ Combine to JSON (report_generator.py)
   ├─ Output: test/report_output.json
   └─ Render: test/final_report.html

3. CUSTOM WORKFLOW
   ├─ Modify config.py
   ├─ Modify prompts.py (optional)
   ├─ Run report_generator.py
   └─ Run template_renderer.py
```

## 🎨 Customization Points

```
┌─────────────────────────────────────────────────────────┐
│                  WHAT CAN YOU CUSTOMIZE?                 │
└─────────────────────────────────────────────────────────┘

1. DATA & DATES
   File: config.py
   - FILE_PATH: Đường dẫn Excel
   - REPORT_DATE: Ngày phân tích
   - COMPARE_DATE: Ngày so sánh
   - BRAND_NAME: Tên thương hiệu

2. ANALYSIS PARAMETERS
   File: config.py
   - TOP_N_TOPICS: Số topics phân tích
   - TOP_N_ATTRIBUTES: Số attributes phân tích
   - LOOKBACK_DAYS: Số ngày nhìn lại

3. LLM PROMPTS
   File: prompts.py
   - get_overview_insight_prompt()
   - get_trendline_insight_prompt()
   - get_sentiment_insight_prompt()

4. BUSINESS LOGIC
   File: slide_generators.py
   - Slide1Generator: Logic tính KPI
   - Slide2Generator: Logic trendline
   - Slide4Generator: Logic sentiment

5. HTML TEMPLATE
   File: template_parameterized.html
   - Layout, styling, charts
```

## 🔍 Quick Reference

### Chạy demo (không cần API)
```bash
python test/demo_without_api.py
```

### Chạy full report (cần API)
```bash
export API_KEY="your_key"
export BASE_URL="your_url"
python test/run_simple.py
```

### Chỉ generate JSON
```bash
python test/report_generator.py
```

### Chỉ render HTML
```python
from test.template_renderer import TemplateRenderer
import json

with open('data.json', 'r') as f:
    data = json.load(f)
    
renderer = TemplateRenderer('test/template_parameterized.html')
renderer.render_to_file(data, 'output.html')
```

## 📦 Dependencies

```bash
pip install pandas openpyxl openai
```

## 🎓 Learning Path

### Beginner
1. Đọc QUICKSTART.md
2. Chạy demo_without_api.py
3. Xem sample_data.json để hiểu cấu trúc
4. Mở demo_report.html trong browser

### Intermediate
1. Đọc SETUP_GUIDE.md
2. Chuẩn bị data Excel
3. Set API credentials
4. Chạy run_simple.py
5. Customize config.py

### Advanced
1. Đọc README_refactored.md
2. Hiểu kiến trúc module
3. Customize prompts.py
4. Modify slide_generators.py
5. Extend với slides mới

## 🐛 Common Issues

| Issue | Solution | File to check |
|-------|----------|---------------|
| Module not found | `pip install pandas openpyxl openai` | requirements.txt |
| API_KEY not set | `export API_KEY="..."` | Environment |
| File not found | Update FILE_PATH | config.py |
| Import error | Run from project root | - |
| Date parsing error | Check Excel date format | data file |
| No output | Check logs and errors | Terminal output |

## 📞 Support Flow

```
Issue?
  ├─ Check QUICKSTART.md
  ├─ Check SETUP_GUIDE.md
  ├─ Run demo_without_api.py to test
  ├─ Verify config.py settings
  ├─ Check API credentials
  └─ Review error messages
```

## 🎯 Next Steps

After getting it working:
1. ✅ Customize prompts for better insights
2. ✅ Add more slides if needed
3. ✅ Modify HTML template styling
4. ✅ Add data validation
5. ✅ Add logging and monitoring
6. ✅ Create scheduled jobs
7. ✅ Add email notifications

---

**Start here:** `QUICKSTART.md` → Run `demo_without_api.py` → Success! 🎉
