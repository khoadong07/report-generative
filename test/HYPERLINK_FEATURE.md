# 🔗 TÍNH NĂNG TỰ ĐỘNG CHUYỂN ĐỔI HYPERLINK

## 📋 TỔNG QUAN

Tính năng tự động chuyển đổi URLs trong insight thành markdown hyperlinks để hiển thị đẹp hơn và clickable trong các nền tảng tạo slide.

## 🎯 VẤN ĐỀ

### Trước khi có tính năng:
```
Insight text với URL dạng:
"Lượng thảo luận tăng đột biến. [Nguồn: https://www.tiktok.com/@vtv.times/video/7601896457389591826]"
```

**Vấn đề:**
- URL dài, khó đọc
- Không clickable trong một số platform
- Trông không chuyên nghiệp
- Chiếm nhiều không gian

### Sau khi có tính năng:
```
Insight text với hyperlink:
"Lượng thảo luận tăng đột biến. [Nguồn](https://www.tiktok.com/@vtv.times/video/7601896457389591826)"
```

**Lợi ích:**
- ✅ Hiển thị gọn gàng: chỉ hiện "[Nguồn]"
- ✅ Clickable: Click vào sẽ mở URL
- ✅ Chuyên nghiệp hơn
- ✅ Tiết kiệm không gian

---

## 🔧 CÁCH HOẠT ĐỘNG

### Regex Pattern
```python
pattern = r'\[(?:Nguồn|Source):\s*(https?://[^\]]+)\]'
```

**Giải thích:**
- `\[` - Bắt đầu với dấu `[`
- `(?:Nguồn|Source)` - Match "Nguồn" hoặc "Source"
- `:` - Dấu hai chấm
- `\s*` - Có thể có khoảng trắng
- `(https?://[^\]]+)` - Capture URL (http hoặc https)
- `\]` - Kết thúc với dấu `]`

### Conversion Logic
```python
def format_insight_with_hyperlinks(insight_text):
    """Convert URLs to markdown hyperlinks"""
    pattern = r'\[(?:Nguồn|Source):\s*(https?://[^\]]+)\]'
    
    def replace_link(match):
        url = match.group(1).strip()
        return f'[Nguồn]({url})'
    
    return re.sub(pattern, replace_link, insight_text)
```

---

## 📊 VÍ DỤ CHUYỂN ĐỔI

### Ví dụ 1: Single URL
**Input:**
```
Lượng thảo luận tăng đột biến. [Nguồn: https://www.tiktok.com/@vtv.times/video/7601896457389591826]
```

**Output:**
```
Lượng thảo luận tăng đột biến. [Nguồn](https://www.tiktok.com/@vtv.times/video/7601896457389591826)
```

### Ví dụ 2: Multiple URLs
**Input:**
```
Sự việc xoay quanh thông báo thu hồi. [Nguồn: http://facebook.com/138841156165916_1294284519398922] Nguyên nhân được xác định. [Nguồn: http://facebook.com/419555621494041_1317059697125118]
```

**Output:**
```
Sự việc xoay quanh thông báo thu hồi. [Nguồn](http://facebook.com/138841156165916_1294284519398922) Nguyên nhân được xác định. [Nguồn](http://facebook.com/419555621494041_1317059697125118)
```

### Ví dụ 3: Real Insight
**Input:**
```
Lượng thảo luận về Nestlé tăng đột biến trong ngày 2026-02-01, với 1,727 lượt đề cập, 
tăng hơn 104% so với ngày hôm trước, cho thấy một sự kiện tiêu cực đang thu hút sự chú ý 
lớn từ cộng đồng mạng. [Nguồn: https://www.tiktok.com/@vtv.times/video/7601896457389591826] 
Sự việc xoay quanh thông báo thu hồi tự nguyện 21 lô bánh ăn dặm Gerber® Arrowroot Biscuits 
tại Mỹ do phát hiện khả năng lẫn mảnh nhựa mềm hoặc giấy trong sản phẩm. 
[Nguồn: http://facebook.com/138841156165916_1294284519398922]
```

**Output:**
```
Lượng thảo luận về Nestlé tăng đột biến trong ngày 2026-02-01, với 1,727 lượt đề cập, 
tăng hơn 104% so với ngày hôm trước, cho thấy một sự kiện tiêu cực đang thu hút sự chú ý 
lớn từ cộng đồng mạng. [Nguồn](https://www.tiktok.com/@vtv.times/video/7601896457389591826) 
Sự việc xoay quanh thông báo thu hồi tự nguyện 21 lô bánh ăn dặm Gerber® Arrowroot Biscuits 
tại Mỹ do phát hiện khả năng lẫn mảnh nhựa mềm hoặc giấy trong sản phẩm. 
[Nguồn](http://facebook.com/138841156165916_1294284519398922)
```

---

## 🎨 HIỂN THỊ TRONG CÁC PLATFORM

### Manuss / Gamma (Markdown Support)
```
Hiển thị: "... cộng đồng mạng. [Nguồn] Sự việc xoay quanh..."
                                  ↑
                              Clickable link
```

### PowerPoint (sau khi export)
```
Hiển thị: "... cộng đồng mạng. [Nguồn](https://...) Sự việc..."
                                  ↑
                          Có thể click nếu platform hỗ trợ
```

### PDF (sau khi export)
```
Hiển thị: "... cộng đồng mạng. [Nguồn] Sự việc..."
                                  ↑
                          Clickable link (nếu PDF reader hỗ trợ)
```

---

## 🧪 TESTING

### Chạy test suite
```bash
cd test
python test_hyperlink_conversion.py
```

**Output:**
```
🧪 TESTING HYPERLINK CONVERSION
════════════════════════════════════════════════════════════════════════════════

[Test 1] Single URL
────────────────────────────────────────────────────────────────────────────────
✅ PASSED

[Test 2] Multiple URLs
────────────────────────────────────────────────────────────────────────────────
✅ PASSED

[Test 3] URL with spaces
────────────────────────────────────────────────────────────────────────────────
✅ PASSED

[Test 4] Mixed http and https
────────────────────────────────────────────────────────────────────────────────
✅ PASSED

[Test 5] No URLs
────────────────────────────────────────────────────────────────────────────────
✅ PASSED

[Test 6] Real example from report
────────────────────────────────────────────────────────────────────────────────
✅ PASSED

📊 TEST SUMMARY
════════════════════════════════════════════════════════════════════════════════
Total: 6
✅ Passed: 6
❌ Failed: 0
```

---

## 📦 TÍCH HỢP VÀO SCRIPTS

### Script 1: `generate_slide_prompt_simple.py`
```python
def generate_slide1_data(slide_data):
    """Generate formatted data for Slide 1"""
    # ... existing code ...
    
    # Format insight with hyperlinks
    insight = format_insight_with_hyperlinks(slide_data['insight'])
    
    return {
        'title': slide_data['title'],
        'subtitle': slide_data['subtitle'],
        'kpis': kpis,
        'insight': insight  # ← Hyperlinks đã được format
    }
```

### Script 2: `generate_slide_prompt.py`
Tương tự, tất cả 4 slide generators đều sử dụng `format_insight_with_hyperlinks()`

---

## 🎯 USE CASES

### Use Case 1: Tạo slide cho presentation
```bash
# Generate report
python generate_report.py

# Generate prompt (với hyperlinks)
python generate_slide_prompt_simple.py

# Copy prompt vào Manuss
# → Insights có hyperlinks clickable
```

### Use Case 2: Export PDF
```bash
# Sau khi tạo slide trên Manuss/Gamma
# Export to PDF
# → PDF có hyperlinks clickable
```

### Use Case 3: Share online
```bash
# Share link Manuss/Gamma presentation
# → Người xem có thể click vào sources
```

---

## 🔍 SO SÁNH TRƯỚC/SAU

### TRƯỚC (không có hyperlink conversion):

**Prompt:**
```
INSIGHT:
Lượng thảo luận về Nestlé tăng đột biến trong ngày 2026-02-01, với 1,727 lượt đề cập, 
tăng hơn 104% so với ngày hôm trước. [Nguồn: https://www.tiktok.com/@vtv.times/video/7601896457389591826] 
Sự việc xoay quanh thông báo thu hồi. [Nguồn: http://facebook.com/138841156165916_1294284519398922]
```

**Hiển thị trên slide:**
```
Lượng thảo luận về Nestlé tăng đột biến trong ngày 2026-02-01, với 1,727 lượt đề cập, 
tăng hơn 104% so với ngày hôm trước. [Nguồn: https://www.tiktok.com/@vtv.times/video/7601896457389591826] 
Sự việc xoay quanh thông báo thu hồi. [Nguồn: http://facebook.com/138841156165916_1294284519398922]
```
❌ URL dài, khó đọc, không clickable

---

### SAU (có hyperlink conversion):

**Prompt:**
```
INSIGHT:
Lượng thảo luận về Nestlé tăng đột biến trong ngày 2026-02-01, với 1,727 lượt đề cập, 
tăng hơn 104% so với ngày hôm trước. [Nguồn](https://www.tiktok.com/@vtv.times/video/7601896457389591826) 
Sự việc xoay quanh thông báo thu hồi. [Nguồn](http://facebook.com/138841156165916_1294284519398922)
```

**Hiển thị trên slide:**
```
Lượng thảo luận về Nestlé tăng đột biến trong ngày 2026-02-01, với 1,727 lượt đề cập, 
tăng hơn 104% so với ngày hôm trước. [Nguồn] Sự việc xoay quanh thông báo thu hồi. [Nguồn]
                                              ↑ clickable                              ↑ clickable
```
✅ Gọn gàng, chuyên nghiệp, clickable

---

## 💡 BEST PRACTICES

### 1. Luôn sử dụng format chuẩn trong LLM prompts
```python
# Trong prompts.py
"""
YÊU CẦU BẮT BUỘC:
- Mỗi câu kết thúc bằng [Nguồn: URL]
- Format: [Nguồn: https://...]
- KHÔNG format khác: (Nguồn: ...) hoặc Nguồn: ...
"""
```

### 2. Test conversion trước khi deploy
```bash
python test_hyperlink_conversion.py
```

### 3. Kiểm tra output prompt
```bash
# Xem có hyperlinks không
grep -o '\[Nguồn\](http' slide_prompt.txt | wc -l

# Xem có URLs chưa convert không
grep -o '\[Nguồn: http' slide_prompt.txt | wc -l
# → Nên là 0
```

### 4. Verify trên platform
- Paste prompt vào Manuss/Gamma
- Kiểm tra insights có clickable không
- Test click vào links

---

## 🚀 FUTURE ENHANCEMENTS

### 1. Support thêm formats
```python
# Hiện tại: [Nguồn: URL]
# Tương lai: 
# - (Source: URL)
# - [Link: URL]
# - [Xem thêm: URL]
```

### 2. Shorten URLs
```python
# Convert URL dài thành short link
# https://www.tiktok.com/... → [Nguồn](https://tiktok.com/...)
```

### 3. Custom link text
```python
# Thay vì "Nguồn", có thể custom
# [TikTok](url), [Facebook](url), [News](url)
```

### 4. Validate URLs
```python
# Kiểm tra URL có valid không trước khi convert
# Báo warning nếu URL broken
```

---

## 📚 TÀI LIỆU LIÊN QUAN

- `generate_slide_prompt_simple.py` - Script chính
- `generate_slide_prompt.py` - Script với config
- `test_hyperlink_conversion.py` - Test suite
- `QUICKSTART_PROMPT.md` - Hướng dẫn nhanh

---

**Version:** 1.0  
**Last Updated:** 2026-02-05  
**Feature Status:** ✅ Production Ready
