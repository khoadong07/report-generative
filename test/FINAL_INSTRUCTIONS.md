# ✅ Hướng dẫn chạy source code - FINAL

## 🎯 TÓM TẮT

Bạn đã có:
- ✅ File `.env` với API credentials
- ✅ File data `Nestle_Gerber_15h_labeled.xlsx`
- ✅ Tất cả dependencies đã cài

## 🚀 CHẠY NGAY

### Cách 1: Chạy từng bước (Recommended)

```bash
# Bước 1: Vào thư mục test
cd test

# Bước 2: Kiểm tra setup
python test_setup.py

# Bước 3: Generate report (mất 1-2 phút)
python generate_report.py

# Bước 4: Render HTML
python render_html.py

# Bước 5: Mở kết quả
open final_report.html
```

### Cách 2: Demo nhanh (Không cần API)

```bash
cd test
python demo_without_api.py
# Chọn option 1
# Mở test/demo_report.html
```

---

## ⚠️ LƯU Ý QUAN TRỌNG

### 1. Chạy từ thư mục `test/`
```bash
cd test  # QUAN TRỌNG!
python generate_report.py
```

### 2. Script sẽ mất thời gian
- Generate report: 1-2 phút (gọi LLM 3 lần)
- Render HTML: vài giây

### 3. Nếu bị lỗi "Module not found"
```bash
# Đảm bảo chạy từ thư mục test
cd test
python generate_report.py
```

---

## 📁 Output Files

Sau khi chạy xong, bạn sẽ có:

```
test/
├── report_output.json    # JSON data từ LLM
└── final_report.html     # HTML report đẹp
```

---

## 🔍 Kiểm tra tiến trình

Nếu script đang chạy lâu, đó là bình thường vì:
1. Đang load data từ Excel (vài giây)
2. Đang gọi LLM cho Slide 1 (30-60 giây)
3. Đang gọi LLM cho Slide 2 (30-60 giây)
4. Đang gọi LLM cho Slide 4 (30-60 giây)

Tổng: khoảng 2-3 phút

---

## 🐛 Troubleshooting

### Lỗi: "name 'API_KEY' is not defined"
✅ ĐÃ SỬA: File `test.py` cũ đã được đổi tên thành `test_old_backup.py`

### Lỗi: "Module not found"
```bash
# Chạy từ thư mục test
cd test
python generate_report.py
```

### Lỗi: "File not found"
```bash
# Kiểm tra file data có tồn tại không
ls -lh Nestle_Gerber_15h_labeled.xlsx
```

### Script chạy quá lâu
- Bình thường! LLM cần 1-2 phút
- Kiểm tra kết nối internet
- Kiểm tra API key còn quota không

---

## 📊 Kết quả mong đợi

File `final_report.html` sẽ có:
- **Slide 1**: KPI Overview với 6-7 metrics
- **Slide 2**: Trendline chart 6 ngày
- **Slide 4**: Sentiment analysis với charts

---

## 💡 Tips

1. **Lần đầu chạy**: Dùng `demo_without_api.py` để xem output trông như thế nào
2. **Customize**: Sửa `config.py` để thay đổi dates, brand name
3. **Prompts**: Sửa `prompts.py` để thay đổi cách LLM generate insights
4. **Template**: Sửa `template_parameterized.html` để thay đổi giao diện

---

## ✅ Checklist

Trước khi chạy, đảm bảo:
- [ ] Đã `cd test`
- [ ] File `.env` có API_KEY và BASE_URL
- [ ] File `Nestle_Gerber_15h_labeled.xlsx` tồn tại
- [ ] Đã cài `pip install pandas openpyxl openai python-dotenv`
- [ ] Đã chạy `python test_setup.py` và tất cả ✅

---

## 🎉 Success!

Khi thấy:
```
✅ SUCCESS!
Report saved to: report_output.json
```

Thì đã xong! Tiếp tục render HTML:
```bash
python render_html.py
open final_report.html
```

---

**Bắt đầu ngay:** `cd test && python generate_report.py`
