# 🎨 DEMO: KẾT QUẢ CHUYỂN ĐỔI HYPERLINK

## 📝 VÍ DỤ THỰC TẾ

### INPUT (từ report_output.json):
```
Lượng thảo luận về Nestlé tăng đột biến trong ngày 2026-02-01, với 1,727 lượt đề cập, tăng hơn 104% so với ngày hôm trước, cho thấy một sự kiện tiêu cực đang thu hút sự chú ý lớn từ cộng đồng mạng. [Nguồn: https://www.tiktok.com/@vtv.times/video/7601896457389591826] Sự việc xoay quanh thông báo thu hồi tự nguyện 21 lô bánh ăn dặm Gerber® Arrowroot Biscuits tại Mỹ do phát hiện khả năng lẫn mảnh nhựa mềm hoặc giấy trong sản phẩm. [Nguồn: http://facebook.com/138841156165916_1294284519398922] Nguyên nhân được xác định là do nguyên liệu bột dong riềng từ một nhà cung cấp, và Nestlé đã ngừng hợp tác với đơn vị này để đảm bảo chất lượng. [Nguồn: http://facebook.com/419555621494041_1317059697125118]
```

### OUTPUT (trong slide_prompt.txt):
```
Lượng thảo luận về Nestlé tăng đột biến trong ngày 2026-02-01, với 1,727 lượt đề cập, tăng hơn 104% so với ngày hôm trước, cho thấy một sự kiện tiêu cực đang thu hút sự chú ý lớn từ cộng đồng mạng. [Nguồn](https://www.tiktok.com/@vtv.times/video/7601896457389591826) Sự việc xoay quanh thông báo thu hồi tự nguyện 21 lô bánh ăn dặm Gerber® Arrowroot Biscuits tại Mỹ do phát hiện khả năng lẫn mảnh nhựa mềm hoặc giấy trong sản phẩm. [Nguồn](http://facebook.com/138841156165916_1294284519398922) Nguyên nhân được xác định là do nguyên liệu bột dong riềng từ một nhà cung cấp, và Nestlé đã ngừng hợp tác với đơn vị này để đảm bảo chất lượng. [Nguồn](http://facebook.com/419555621494041_1317059697125118)
```

---

## 🔍 SO SÁNH CHI TIẾT

### Câu 1:
**Trước:**
```
... cộng đồng mạng. [Nguồn: https://www.tiktok.com/@vtv.times/video/7601896457389591826] Sự việc...
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                     URL dài 70 ký tự, khó đọc
```

**Sau:**
```
... cộng đồng mạng. [Nguồn](https://www.tiktok.com/@vtv.times/video/7601896457389591826) Sự việc...
                     ^^^^^^
                     Hiển thị gọn, clickable
```

### Câu 2:
**Trước:**
```
... trong sản phẩm. [Nguồn: http://facebook.com/138841156165916_1294284519398922] Nguyên nhân...
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                     URL dài 60 ký tự
```

**Sau:**
```
... trong sản phẩm. [Nguồn](http://facebook.com/138841156165916_1294284519398922) Nguyên nhân...
                     ^^^^^^
                     Gọn gàng hơn
```

---

## 📊 THỐNG KÊ

### Độ dài text:
- **Input:** ~850 ký tự (bao gồm URLs đầy đủ)
- **Output:** ~850 ký tự (giữ nguyên URLs trong markdown)
- **Hiển thị:** ~650 ký tự (URLs ẩn sau hyperlinks)

### Số lượng URLs:
- **Slide 1:** 6 URLs → 6 hyperlinks
- **Slide 2:** 3 URLs → 3 hyperlinks
- **Slide 3:** 6 URLs → 6 hyperlinks
- **Slide 4:** 5 URLs → 5 hyperlinks
- **Tổng:** 20 URLs → 20 hyperlinks

---

## 🎯 HIỂN THỊ TRÊN CÁC PLATFORM

### Manuss:
```
Insight text hiển thị với [Nguồn] là clickable links màu xanh
Click vào sẽ mở URL trong tab mới
```

### Gamma:
```
Tương tự Manuss, hỗ trợ markdown hyperlinks
Có thể customize màu sắc của links
```

### PowerPoint (export):
```
Hyperlinks được giữ nguyên
Có thể click trong presentation mode
```

### PDF (export):
```
Links clickable nếu PDF reader hỗ trợ
Thường hiển thị màu xanh và underline
```

---

## ✅ CHECKLIST KIỂM TRA

Sau khi generate prompt, kiểm tra:

- [ ] Tất cả `[Nguồn: URL]` đã được convert thành `[Nguồn](URL)`
- [ ] Không còn URLs dạng `[Nguồn: http...]` trong prompt
- [ ] Format markdown đúng: `[text](url)` không có khoảng trắng
- [ ] URLs giữ nguyên (http/https)
- [ ] Không bị mất URLs nào

### Lệnh kiểm tra:
```bash
# Đếm số hyperlinks đã convert
grep -o '\[Nguồn\](http' slide_prompt.txt | wc -l

# Kiểm tra còn URLs chưa convert không (nên là 0)
grep -o '\[Nguồn: http' slide_prompt.txt | wc -l

# Xem preview
grep '\[Nguồn\]' slide_prompt.txt | head -5
```

---

## 🚀 CÁCH SỬ DỤNG

### Bước 1: Generate report
```bash
cd test
python generate_report.py
```

### Bước 2: Generate prompt với hyperlinks
```bash
python generate_slide_prompt_simple.py
```

### Bước 3: Kiểm tra output
```bash
# Xem có hyperlinks không
cat slide_prompt.txt | grep '\[Nguồn\](' | head -3
```

### Bước 4: Copy vào Manuss/Gamma
```bash
# macOS
cat slide_prompt.txt | pbcopy

# Linux
cat slide_prompt.txt | xclip -selection clipboard

# Windows
type slide_prompt.txt | clip
```

### Bước 5: Paste và Generate
- Paste vào Manuss/Gamma
- Click "Generate"
- Kiểm tra insights có hyperlinks clickable

---

## 💡 TIPS

### Tip 1: Preview hyperlinks
Sử dụng markdown viewer để preview:
```bash
# Install markdown viewer
npm install -g markdown-preview

# Preview
markdown-preview slide_prompt.txt
```

### Tip 2: Validate URLs
```bash
# Extract all URLs
grep -oP '\[Nguồn\]\(\K[^)]+' slide_prompt.txt > urls.txt

# Check URLs (optional)
while read url; do
    curl -I "$url" 2>/dev/null | head -1
done < urls.txt
```

### Tip 3: Custom link text
Nếu muốn custom text thay vì "Nguồn":
```python
# Trong format_insight_with_hyperlinks()
return f'[Xem chi tiết]({url})'  # Thay vì [Nguồn]
```

---

**Tính năng này giúp slides trông chuyên nghiệp và dễ sử dụng hơn! 🎉**
