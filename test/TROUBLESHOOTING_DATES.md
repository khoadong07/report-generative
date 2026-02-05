# 🔧 TROUBLESHOOTING: DATE ERRORS

## ❌ LỖI THƯỜNG GẶP

### Lỗi: "single positional indexer is out-of-bounds"

**Nguyên nhân:**
Ngày bạn chọn (`--report-date` hoặc `--compare-date`) không có dữ liệu trong file Excel.

**Ví dụ:**
```bash
python generate_slide_prompt.py \
  --excel "Nestle_Gerber_15h_labeled.xlsx" \
  --brand "Nestlé" \
  --report-date "2026-02-05" \    # ❌ Không có data
  --compare-date "2026-02-04"     # ❌ Không có data
```

**Lỗi xuất hiện:**
```
📡 Analyzing channel distribution...
❌ Error generating report: single positional indexer is out-of-bounds
```

---

## ✅ GIẢI PHÁP

### Bước 1: Kiểm tra ngày có sẵn

Chạy script kiểm tra:
```bash
cd test
python check_available_dates.py --excel "Nestle_Gerber_15h_labeled.xlsx"
```

**Output:**
```
📅 CHECKING AVAILABLE DATES
════════════════════════════════════════════════════════════

[1/3] Loading Excel file: Nestle_Gerber_15h_labeled.xlsx
   ✅ Loaded 2,640 rows

[2/3] Checking for PublishedDay column...
   ✅ Found PublishedDay column

[3/3] Analyzing dates...

📊 DATE STATISTICS
════════════════════════════════════════════════════════════
Total rows: 2,640
Unique dates: 6
Date range: 2026-01-27 to 2026-02-01

📅 AVAILABLE DATES (with row counts)
════════════════════════════════════════════════════════════
2026-01-27 - 2 rows
2026-01-28 - 19 rows
2026-01-29 - 1 rows
2026-01-30 - 46 rows
2026-01-31 - 845 rows
2026-02-01 - 1,727 rows

💡 RECOMMENDATIONS
════════════════════════════════════════════════════════════
📈 Date with most data: 2026-02-01 (1,727 rows)

📆 5 most recent dates:
   - 2026-01-28 (19 rows)
   - 2026-01-29 (1 rows)
   - 2026-01-30 (46 rows)
   - 2026-01-31 (845 rows)
   - 2026-02-01 (1,727 rows)

✅ SUGGESTED DATES FOR REPORT:
   --report-date "2026-02-01"
   --compare-date "2026-01-31"
```

### Bước 2: Sử dụng ngày đúng

```bash
python generate_slide_prompt.py \
  --excel "Nestle_Gerber_15h_labeled.xlsx" \
  --brand "Nestlé" \
  --report-date "2026-02-01" \      # ✅ Có data (1,727 rows)
  --compare-date "2026-01-31"       # ✅ Có data (845 rows)
```

---

## 🎯 QUY TẮC CHỌN NGÀY

### 1. Report Date (Ngày báo cáo)
- Phải có dữ liệu trong Excel
- Thường chọn ngày gần nhất
- Nên chọn ngày có nhiều data (>100 rows)

### 2. Compare Date (Ngày so sánh)
- Phải có dữ liệu trong Excel
- Thường là ngày trước report date 1 ngày
- Cũng nên có đủ data để so sánh

### 3. Khoảng cách giữa 2 ngày
- Khuyến nghị: 1 ngày (so sánh hôm nay vs hôm qua)
- Có thể: 7 ngày (so sánh tuần này vs tuần trước)
- Tránh: Quá xa nhau (>30 ngày)

---

## 📊 KIỂM TRA DATA TRƯỚC KHI CHẠY

### Quick check với pandas:
```python
import pandas as pd

# Load Excel
df = pd.read_excel("Nestle_Gerber_15h_labeled.xlsx")

# Convert to date
df['PublishedDay'] = pd.to_datetime(df['PublishedDay']).dt.date

# Check available dates
print("Available dates:")
print(df.groupby('PublishedDay').size().sort_index())

# Check specific date
report_date = pd.to_datetime("2026-02-05").date()
count = len(df[df['PublishedDay'] == report_date])
print(f"\nData for {report_date}: {count} rows")
```

---

## 🔍 CÁC TRƯỜNG HỢP ĐẶC BIỆT

### Trường hợp 1: Ngày có ít data (<10 rows)
**Vấn đề:** Insight có thể không đủ chất lượng

**Giải pháp:**
- Chọn ngày khác có nhiều data hơn
- Hoặc chấp nhận insight ngắn gọn

### Trường hợp 2: Chỉ có 1 ngày duy nhất
**Vấn đề:** Không thể so sánh

**Giải pháp:**
- Sử dụng cùng ngày cho cả report và compare
- Hoặc thêm data cho ngày khác

### Trường hợp 3: Data không liên tục
**Ví dụ:** Có 01/01, 01/03, 01/05 (thiếu 01/02, 01/04)

**Giải pháp:**
- Chọn 2 ngày liên tiếp có data
- Ví dụ: report=01/03, compare=01/01

---

## 🛠️ SCRIPT HELPER

### check_available_dates.py

**Chức năng:**
- Kiểm tra tất cả ngày có trong Excel
- Đếm số rows cho mỗi ngày
- Gợi ý ngày tốt nhất để chọn

**Cách dùng:**
```bash
# Basic
python check_available_dates.py

# With custom Excel file
python check_available_dates.py --excel "path/to/your/file.xlsx"
```

**Output:**
- Danh sách tất cả ngày có data
- Số lượng rows cho mỗi ngày
- Gợi ý report_date và compare_date
- Example command sẵn sàng copy

---

## 📝 CHECKLIST TRƯỚC KHI CHẠY

- [ ] Đã chạy `check_available_dates.py`
- [ ] Report date có trong danh sách available dates
- [ ] Compare date có trong danh sách available dates
- [ ] Report date có đủ data (>50 rows khuyến nghị)
- [ ] Compare date có đủ data (>50 rows khuyến nghị)
- [ ] Format ngày đúng: YYYY-MM-DD
- [ ] File Excel tồn tại và đúng path

---

## 🎓 VÍ DỤ THỰC TẾ

### Ví dụ 1: Kiểm tra và chạy đúng

```bash
# Bước 1: Kiểm tra dates
cd test
python check_available_dates.py

# Output cho thấy:
# Available: 2026-01-31 (845 rows), 2026-02-01 (1,727 rows)

# Bước 2: Chạy với dates đúng
python generate_slide_prompt.py \
  --excel "Nestle_Gerber_15h_labeled.xlsx" \
  --brand "Nestlé" \
  --report-date "2026-02-01" \
  --compare-date "2026-01-31"

# ✅ Success!
```

### Ví dụ 2: Sửa lỗi date không tồn tại

```bash
# Lỗi ban đầu
python generate_slide_prompt.py \
  --report-date "2026-02-05" \    # ❌ Không có data
  --compare-date "2026-02-04"     # ❌ Không có data

# Error: single positional indexer is out-of-bounds

# Kiểm tra dates
python check_available_dates.py
# → Thấy chỉ có data đến 2026-02-01

# Sửa lại
python generate_slide_prompt.py \
  --report-date "2026-02-01" \    # ✅ Có data
  --compare-date "2026-01-31"     # ✅ Có data

# ✅ Success!
```

---

## 🚨 ERROR MESSAGES & SOLUTIONS

### Error 1: "No data available for report date"
```
⚠️  WARNING: No data found for report date 2026-02-05
Available dates in dataset:
   - 2026-01-27
   - 2026-01-28
   ...
```

**Solution:** Chọn ngày từ danh sách available dates

### Error 2: "single positional indexer is out-of-bounds"
```
📡 Analyzing channel distribution...
❌ Error: single positional indexer is out-of-bounds
```

**Solution:** 
1. Chạy `check_available_dates.py`
2. Chọn ngày có data
3. Chạy lại với ngày đúng

### Error 3: "File not found"
```
❌ Excel file not found: Nestle_Gerber_15h_labeled.xlsx
```

**Solution:**
1. Kiểm tra file có tồn tại: `ls -la *.xlsx`
2. Kiểm tra đúng thư mục: `pwd`
3. Sử dụng đường dẫn đầy đủ nếu cần

---

## 💡 BEST PRACTICES

### 1. Luôn kiểm tra dates trước
```bash
python check_available_dates.py
```

### 2. Chọn ngày có nhiều data
- Tối thiểu: 50 rows
- Khuyến nghị: 100+ rows
- Tốt nhất: 500+ rows

### 3. Chọn ngày liên tiếp
- Report: 2026-02-01
- Compare: 2026-01-31
- ✅ Liên tiếp, dễ so sánh

### 4. Lưu lại dates đã dùng
```bash
# Tạo file note
echo "Last successful run:" > last_run.txt
echo "Report: 2026-02-01" >> last_run.txt
echo "Compare: 2026-01-31" >> last_run.txt
```

### 5. Automation với script
```bash
#!/bin/bash
# auto_generate.sh

# Get latest 2 dates
DATES=$(python check_available_dates.py | grep "SUGGESTED DATES" -A 2)
REPORT_DATE=$(echo "$DATES" | grep "report-date" | cut -d'"' -f2)
COMPARE_DATE=$(echo "$DATES" | grep "compare-date" | cut -d'"' -f2)

# Run with auto-detected dates
python generate_slide_prompt.py \
  --excel "data.xlsx" \
  --brand "Brand" \
  --report-date "$REPORT_DATE" \
  --compare-date "$COMPARE_DATE"
```

---

**Luôn kiểm tra dates trước khi chạy để tránh lỗi! 📅**
