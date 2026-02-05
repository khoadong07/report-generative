# ⚡ QUICKSTART: TẠO PROMPT CHO SLIDE

## 🎯 Cách nhanh nhất (2 bước)

### Bước 1: Generate report
```bash
cd test
python generate_report.py
```
**Output:** `report_output.json`

### Bước 2: Generate prompt
```bash
python generate_slide_prompt_simple.py
```
**Output:** `slide_prompt.txt`

### Bước 3: Sử dụng prompt
1. Mở file `slide_prompt.txt`
2. Copy toàn bộ nội dung (Cmd+A, Cmd+C)
3. Paste vào Manuss/Gamma: https://manuss.com hoặc https://gamma.app
4. Click "Generate"
5. Đợi 30-60 giây → Xong!

---

## 📝 Chi tiết

### Script 1: `generate_report.py`
**Chức năng:** Tạo report JSON từ Excel với LLM insights

**Cách dùng:**
```bash
cd test
python generate_report.py
```

**Yêu cầu:**
- File `.env` có `API_KEY` và `BASE_URL`
- File `config.py` đã cấu hình đúng:
  - `FILE_PATH`: Đường dẫn Excel
  - `BRAND_NAME`: Tên thương hiệu
  - `REPORT_DATE`: Ngày báo cáo
  - `COMPARE_DATE`: Ngày so sánh

**Output:** `report_output.json`

**Thời gian:** 3-4 phút (gọi LLM 4 lần)

---

### Script 2: `generate_slide_prompt_simple.py`
**Chức năng:** Chuyển đổi JSON thành prompt hoàn chỉnh

**Cách dùng cơ bản:**
```bash
python generate_slide_prompt_simple.py
```

**Cách dùng với tham số:**
```bash
python generate_slide_prompt_simple.py \
  --json "report_output.json" \
  --output "my_prompt.txt"
```

**Tham số:**
- `--json`: File JSON input (mặc định: `report_output.json`)
- `--output`: File prompt output (mặc định: `slide_prompt.txt`)

**Output:** `slide_prompt.txt`

**Thời gian:** < 1 giây

---

## 🔧 Cấu hình trước khi chạy

### 1. Cài đặt dependencies
```bash
pip install pandas openpyxl python-dotenv openai
```

### 2. Tạo file `.env`
```bash
cd test
cat > .env << EOF
API_KEY=sk-proj-your-openai-key-here
BASE_URL=https://api.openai.com/v1
EOF
```

### 3. Cập nhật `config.py`
```python
# File path
FILE_PATH = "Nestle_Gerber_15h_labeled.xlsx"

# Brand and dates
BRAND_NAME = "Nestlé"
REPORT_DATE = "2026-02-01"
COMPARE_DATE = "2026-01-31"
```

---

## 📊 Workflow hoàn chỉnh

```
Excel File
    ↓
[config.py] → generate_report.py → report_output.json
                                          ↓
                        generate_slide_prompt_simple.py
                                          ↓
                                  slide_prompt.txt
                                          ↓
                                Copy & Paste vào Manuss
                                          ↓
                                    Click Generate
                                          ↓
                                  4 Slides đẹp! 🎉
```

---

## 💡 Tips

### Tip 1: Tạo alias
```bash
# Thêm vào ~/.bashrc hoặc ~/.zshrc
alias gen-report='cd ~/path/to/test && python generate_report.py'
alias gen-prompt='cd ~/path/to/test && python generate_slide_prompt_simple.py'

# Sử dụng
gen-report
gen-prompt
```

### Tip 2: One-liner
```bash
cd test && python generate_report.py && python generate_slide_prompt_simple.py && cat slide_prompt.txt | pbcopy
```
Lệnh này sẽ:
1. Generate report
2. Generate prompt
3. Copy prompt vào clipboard (macOS)

### Tip 3: Kiểm tra output
```bash
# Xem metadata
cat report_output.json | jq '.report_metadata'

# Đếm số dòng prompt
wc -l slide_prompt.txt

# Xem preview
head -50 slide_prompt.txt
```

---

## 🐛 Troubleshooting

### Lỗi: "API credentials not found"
```bash
# Kiểm tra .env
cat test/.env

# Nếu không có, tạo mới
cd test
echo 'API_KEY=your-key' > .env
echo 'BASE_URL=https://api.openai.com/v1' >> .env
```

### Lỗi: "JSON file not found"
```bash
# Chạy generate_report.py trước
cd test
python generate_report.py

# Kiểm tra file đã tạo
ls -la report_output.json
```

### Lỗi: "Module not found"
```bash
# Cài đặt dependencies
pip install pandas openpyxl python-dotenv openai

# Hoặc từ requirements.txt
pip install -r requirements.txt
```

### Prompt quá dài
- Prompt thường ~500-800 dòng
- Manuss/Gamma có thể xử lý được
- Nếu quá dài, có thể chia nhỏ thành từng slide

---

## 📚 Tài liệu liên quan

- `HUONG_DAN_GENERATE_PROMPT.md` - Hướng dẫn chi tiết
- `PROMPT_FOR_SLIDE_PLATFORMS.md` - Spec của prompt
- `HUONG_DAN_SU_DUNG_PROMPT.md` - Cách dùng prompt

---

## ✅ Checklist

Trước khi chạy:
- [ ] Đã cài đặt Python 3.8+
- [ ] Đã cài đặt dependencies
- [ ] File `.env` có API key
- [ ] File `config.py` đã cấu hình
- [ ] File Excel tồn tại và đúng format

Sau khi chạy:
- [ ] File `report_output.json` được tạo
- [ ] File `slide_prompt.txt` được tạo
- [ ] Prompt có đầy đủ 4 slides
- [ ] Insight có URLs nguồn

---

**Happy slide making! 🎉**
