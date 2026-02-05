# 📖 HƯỚNG DẪN SỬ DỤNG GENERATE_SLIDE_PROMPT.PY

## 🎯 MỤC ĐÍCH

Script `generate_slide_prompt.py` tự động tạo prompt hoàn chỉnh cho các nền tảng tạo slide (Manuss, Gamma, Beautiful.ai) từ file Excel.

**Input:**
- File Excel chứa dữ liệu social listening
- Tên thương hiệu
- Ngày báo cáo
- Ngày so sánh

**Output:**
- File `.txt` chứa prompt hoàn chỉnh (sẵn sàng copy-paste)
- File `.json` chứa dữ liệu báo cáo

---

## 🚀 CÁCH SỬ DỤNG

### Cách 1: Sử dụng cơ bản

```bash
cd test

python generate_slide_prompt.py \
  --excel "Nestle_Gerber_15h_labeled.xlsx" \
  --brand "Nestlé" \
  --report-date "2026-02-01" \
  --compare-date "2026-01-31"
```

**Output:**
- `slide_prompt.txt` - Prompt hoàn chỉnh
- `report_data.json` - Dữ liệu JSON

### Cách 2: Tùy chỉnh tên file output

```bash
python generate_slide_prompt.py \
  --excel "data/brand_data.xlsx" \
  --brand "Vinamilk" \
  --report-date "2026-02-05" \
  --compare-date "2026-02-04" \
  --output "vinamilk_prompt.txt" \
  --json-output "vinamilk_data.json"
```

### Cách 3: Sử dụng đường dẫn tuyệt đối

```bash
python generate_slide_prompt.py \
  --excel "/Users/username/data/brand_analysis.xlsx" \
  --brand "TH True Milk" \
  --report-date "2026-02-01" \
  --compare-date "2026-01-31" \
  --output "/Users/username/output/prompt.txt"
```

---

## 📝 THAM SỐ CHI TIẾT

### `--excel` (Bắt buộc)
Đường dẫn đến file Excel chứa dữ liệu

**Format Excel yêu cầu:**
- Các cột: `Title`, `Description`, `Content`, `Sentiment`, `Type`, `Channel`, `Labels`, `Reactions`, `Shares`, `Views`, `UrlTopic`, `PublishedDay`
- `PublishedDay`: Định dạng date (YYYY-MM-DD)
- `Labels`: Chuỗi phân tách bởi dấu phẩy

**Ví dụ:**
```bash
--excel "Nestle_Gerber_15h_labeled.xlsx"
--excel "../data/brand_data.xlsx"
--excel "/full/path/to/data.xlsx"
```

### `--brand` (Bắt buộc)
Tên thương hiệu cần phân tích

**Ví dụ:**
```bash
--brand "Nestlé"
--brand "Vinamilk"
--brand "TH True Milk"
```

### `--report-date` (Bắt buộc)
Ngày báo cáo (ngày chính cần phân tích)

**Format:** `YYYY-MM-DD`

**Ví dụ:**
```bash
--report-date "2026-02-01"
--report-date "2026-01-15"
```

### `--compare-date` (Bắt buộc)
Ngày so sánh (thường là ngày hôm trước)

**Format:** `YYYY-MM-DD`

**Ví dụ:**
```bash
--compare-date "2026-01-31"
--compare-date "2026-01-14"
```

### `--output` (Tùy chọn)
Tên file output cho prompt

**Mặc định:** `slide_prompt.txt`

**Ví dụ:**
```bash
--output "nestle_prompt.txt"
--output "output/brand_prompt_20260201.txt"
```

### `--json-output` (Tùy chọn)
Tên file output cho dữ liệu JSON

**Mặc định:** `report_data.json`

**Ví dụ:**
```bash
--json-output "nestle_data.json"
--json-output "output/brand_data_20260201.json"
```

---

## 📊 QUY TRÌNH HOẠT ĐỘNG

```
┌─────────────────┐
│  Excel File     │
│  + Parameters   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Load & Validate │
│     Data        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Generate Report │
│ (Call LLM 4x)   │ ← 3-4 phút
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Format Data    │
│  for Slides     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Build Complete  │
│     Prompt      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Save Outputs:   │
│ - prompt.txt    │
│ - data.json     │
└─────────────────┘
```

---

## 📄 OUTPUT FORMAT

### File 1: `slide_prompt.txt`

Prompt hoàn chỉnh với cấu trúc:

```
Create a professional 4-slide presentation...

═══════════════════════════════════════════
BRAND: Nestlé
REPORT DATE: 01/02/2026
COMPARE DATE: 31/01/2026
═══════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 1 - BRAND OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYOUT: ...
KPI DATA:
1. Tổng thảo luận: 1,727 (+104.38%)
2. Tổng bài đăng: 481 (+314.66%)
...

INSIGHT:
[Full insight text with sources]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE 2 - TRENDLINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
...

[Tương tự cho Slide 3 và 4]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OVERALL DESIGN THEME
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
...

INSTRUCTIONS:
1. Create all 4 slides...
```

### File 2: `report_data.json`

Dữ liệu JSON đầy đủ:

```json
{
  "report_metadata": {
    "brand": "Nestlé",
    "report_date": "2026-02-01",
    "compare_date": "2026-01-31",
    "generated_at": "2026-02-05T..."
  },
  "slide_1": { ... },
  "slide_2": { ... },
  "slide_3": { ... },
  "slide_4": { ... }
}
```

---

## 🎯 CÁCH SỬ DỤNG OUTPUT

### Bước 1: Mở file prompt
```bash
cat slide_prompt.txt
# hoặc
open slide_prompt.txt
# hoặc
code slide_prompt.txt
```

### Bước 2: Copy toàn bộ nội dung
- Mở file trong text editor
- Select All (Cmd+A / Ctrl+A)
- Copy (Cmd+C / Ctrl+C)

### Bước 3: Paste vào platform

#### Manuss:
1. Truy cập https://manuss.com
2. Click "New Presentation" → "Generate with AI"
3. Paste prompt
4. Click "Generate"
5. Đợi 30-60 giây

#### Gamma:
1. Truy cập https://gamma.app
2. Click "Create new" → "Generate with AI"
3. Paste prompt
4. Click "Generate"
5. Refine từng slide nếu cần

#### Beautiful.ai:
1. Truy cập https://beautiful.ai
2. Click "New Presentation"
3. Paste prompt vào AI assistant
4. Hoặc tạo thủ công từ data trong prompt

---

## ⚙️ CẤU HÌNH

### File `.env` cần có:
```bash
API_KEY=your_openai_api_key_here
BASE_URL=https://api.openai.com/v1
```

### Dependencies:
```bash
pip install pandas openpyxl python-dotenv openai
```

---

## 💡 VÍ DỤ THỰC TÊ

### Ví dụ 1: Phân tích Nestlé
```bash
python generate_slide_prompt.py \
  --excel "Nestle_Gerber_15h_labeled.xlsx" \
  --brand "Nestlé" \
  --report-date "2026-02-01" \
  --compare-date "2026-01-31" \
  --output "nestle_prompt_20260201.txt"
```

**Output:**
```
📊 SLIDE PROMPT GENERATOR
═══════════════════════════════════════

[Step 1/5] Validating inputs...
   ✅ Excel: Nestle_Gerber_15h_labeled.xlsx
   ✅ Brand: Nestlé
   ✅ Report Date: 2026-02-01
   ✅ Compare Date: 2026-01-31

[Step 2/5] Checking API credentials...
   ✅ API_KEY: sk-proj-...
   ✅ BASE_URL: https://api.openai.com/v1

[Step 3/5] Generating report data...
   ⏱️  This will take 3-4 minutes...
   
   📊 Slide 1: Overview
      → Extracting top negative topics...
      → Found 6 top negative topics
      → Building prompt...
      → Calling LLM API...
      → LLM response received
      ✅ Slide 1 completed
   
   [Similar for Slides 2, 3, 4]

[Step 4/5] Saving JSON data...
   ✅ JSON saved: report_data.json

[Step 5/5] Generating slide prompt...
   ✅ Prompt saved: nestle_prompt_20260201.txt

✅ SUCCESS!
═══════════════════════════════════════
📄 JSON Data: report_data.json
📝 Slide Prompt: nestle_prompt_20260201.txt
📊 Brand: Nestlé
📅 Report Date: 2026-02-01

📌 Next steps:
   1. Open nestle_prompt_20260201.txt
   2. Copy the entire content
   3. Paste into Manuss/Gamma/Beautiful.ai
   4. Click 'Generate' and wait 30-60 seconds
```

### Ví dụ 2: Batch processing nhiều brands
```bash
#!/bin/bash
# batch_generate.sh

brands=("Nestlé" "Vinamilk" "TH True Milk")
date="2026-02-01"
compare="2026-01-31"

for brand in "${brands[@]}"; do
    echo "Processing $brand..."
    python generate_slide_prompt.py \
        --excel "data/${brand}_data.xlsx" \
        --brand "$brand" \
        --report-date "$date" \
        --compare-date "$compare" \
        --output "output/${brand}_prompt.txt" \
        --json-output "output/${brand}_data.json"
done
```

---

## 🐛 TROUBLESHOOTING

### Lỗi: "Excel file not found"
**Nguyên nhân:** Đường dẫn file không đúng

**Giải pháp:**
```bash
# Kiểm tra file có tồn tại
ls -la Nestle_Gerber_15h_labeled.xlsx

# Sử dụng đường dẫn tuyệt đối
python generate_slide_prompt.py \
  --excel "$(pwd)/Nestle_Gerber_15h_labeled.xlsx" \
  ...
```

### Lỗi: "Invalid date format"
**Nguyên nhân:** Format ngày không đúng

**Giải pháp:**
```bash
# Đúng: YYYY-MM-DD
--report-date "2026-02-01"

# Sai:
--report-date "01/02/2026"  # ❌
--report-date "2026-2-1"    # ❌
--report-date "01-02-2026"  # ❌
```

### Lỗi: "API credentials not found"
**Nguyên nhân:** File `.env` không có hoặc thiếu thông tin

**Giải pháp:**
```bash
# Tạo file .env
cat > .env << EOF
API_KEY=sk-proj-your-key-here
BASE_URL=https://api.openai.com/v1
EOF

# Kiểm tra
cat .env
```

### Lỗi: "LLM API timeout"
**Nguyên nhân:** Kết nối mạng chậm hoặc API quá tải

**Giải pháp:**
- Kiểm tra kết nối internet
- Thử lại sau vài phút
- Kiểm tra API key còn quota

### Lỗi: "Missing columns in Excel"
**Nguyên nhân:** File Excel thiếu cột bắt buộc

**Giải pháp:**
```python
# Kiểm tra columns
import pandas as pd
df = pd.read_excel("your_file.xlsx")
print(df.columns.tolist())

# Cần có:
# ['Title', 'Description', 'Content', 'Sentiment', 
#  'Type', 'Channel', 'Labels', 'Reactions', 
#  'Shares', 'Views', 'UrlTopic', 'PublishedDay']
```

---

## 📊 TIPS & BEST PRACTICES

### Tip 1: Đặt tên file có ý nghĩa
```bash
# Tốt
--output "nestle_prompt_20260201.txt"
--output "vinamilk_weekly_report.txt"

# Không tốt
--output "prompt.txt"
--output "output1.txt"
```

### Tip 2: Tổ chức thư mục
```bash
mkdir -p output/{prompts,data}

python generate_slide_prompt.py \
  --excel "input/brand.xlsx" \
  --brand "Brand" \
  --report-date "2026-02-01" \
  --compare-date "2026-01-31" \
  --output "output/prompts/brand_20260201.txt" \
  --json-output "output/data/brand_20260201.json"
```

### Tip 3: Tạo alias
```bash
# Thêm vào ~/.bashrc hoặc ~/.zshrc
alias gen-prompt='python ~/path/to/generate_slide_prompt.py'

# Sử dụng
gen-prompt --excel "data.xlsx" --brand "Brand" ...
```

### Tip 4: Logging
```bash
# Lưu log
python generate_slide_prompt.py \
  --excel "data.xlsx" \
  --brand "Brand" \
  --report-date "2026-02-01" \
  --compare-date "2026-01-31" \
  2>&1 | tee generation.log
```

### Tip 5: Automation với cron
```bash
# Chạy tự động mỗi ngày lúc 9h sáng
0 9 * * * cd /path/to/test && python generate_slide_prompt.py --excel "daily_data.xlsx" --brand "Brand" --report-date "$(date +\%Y-\%m-\%d)" --compare-date "$(date -d '1 day ago' +\%Y-\%m-\%d)"
```

---

## 📚 TÀI LIỆU LIÊN QUAN

- `PROMPT_FOR_SLIDE_PLATFORMS.md` - Chi tiết về prompt format
- `HUONG_DAN_SU_DUNG_PROMPT.md` - Hướng dẫn sử dụng prompt
- `PROMPT_BUILD_4_SLIDES.md` - Kiến trúc hệ thống
- `generate_report.py` - Script generate report gốc

---

**Version:** 1.0  
**Last Updated:** 2026-02-05  
**Author:** AI Report Generation System
