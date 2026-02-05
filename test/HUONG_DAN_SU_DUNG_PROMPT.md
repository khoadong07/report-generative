# 📖 HƯỚNG DẪN SỬ DỤNG PROMPT TẠO SLIDE

## 🎯 TỔNG QUAN

File `PROMPT_FOR_SLIDE_PLATFORMS.md` chứa prompt chi tiết để tạo slide chuyên nghiệp trên các nền tảng AI như Manuss, Gamma, Beautiful.ai. Hướng dẫn này sẽ chỉ bạn cách sử dụng từng bước.

---

## 📋 BƯỚC 1: CHUẨN BỊ DỮ LIỆU

### 1.1. Chạy generate_report.py
```bash
cd test
python generate_report.py
```

**Output:** File `report_output.json` chứa dữ liệu cho 4 slide

### 1.2. Kiểm tra dữ liệu
Mở file `report_output.json` và xác nhận có đầy đủ:
- ✅ `report_metadata` (brand, dates)
- ✅ `slide_1` (KPIs + insight)
- ✅ `slide_2` (trendline + insight)
- ✅ `slide_3` (channels + insight)
- ✅ `slide_4` (sentiment + insight)

---

## 🚀 BƯỚC 2: CHỌN PLATFORM VÀ CHUẨN BỊ PROMPT

### Option A: Sử dụng Manuss (Khuyến nghị)

#### Bước 2.1: Truy cập Manuss
- Website: https://manuss.com (hoặc app tương tự)
- Đăng nhập/Đăng ký tài khoản
- Chọn "Create New Presentation" hoặc "New from AI"

#### Bước 2.2: Copy prompt cơ bản
Mở file `PROMPT_FOR_SLIDE_PLATFORMS.md`, kéo xuống phần **"INSTRUCTIONS FOR AI SLIDE PLATFORMS"**, copy đoạn prompt này:

```
Create a professional 4-slide presentation for Brand Health Analysis with the following specifications:

SLIDE 1 - BRAND OVERVIEW:
- Title: "Tổng quan về thương hiệu [Brand]"
- Layout: 7 KPI cards in grid (4 top row, 3 bottom row)
- Each card shows: metric name, large number, percentage change with up/down arrow
- Bottom section: Insight box with light blue background and analysis text
- Style: Corporate, clean, data-focused

SLIDE 2 - TRENDLINE:
- Title: "Trendline | Diễn biến thảo luận"
- Layout: Line chart showing 7-day trend
- Highlight peak day with red marker
- Show current status indicator (hot/cool)
- Bottom section: Trend analysis insight
- Chart style: Blue line, smooth curve, markers on data points

SLIDE 3 - CHANNEL BREAKDOWN:
- Title: "Phân tích theo kênh thảo luận"
- Layout: Horizontal bar chart
- Bars colored by channel (Facebook blue, TikTok black, etc.)
- Show value and percentage change on each bar
- Highlight top channel with trophy icon
- Bottom section: Channel analysis insight

SLIDE 4 - SENTIMENT ANALYSIS:
- Title: "Sentiment & Brand Attribute"
- Layout: Two-column (Pie chart left, Stacked bar right)
- Pie chart: 3 segments (Negative red, Neutral gray, Positive green)
- Stacked bar: Top 6 brand attributes with sentiment breakdown
- Bottom section: Sentiment analysis insight
- Style: Professional, easy to read

DESIGN THEME:
- Colors: Blue (#1e40af), Gray (#6b7280), Red (#dc2626), Green (#16a34a)
- Font: Modern sans-serif
- Style: Corporate, professional, data-driven
- Layout: Clean, spacious, well-organized
```

#### Bước 2.3: Thêm dữ liệu thực tế
Thêm vào cuối prompt:

```
DATA FOR SLIDE 1:
Brand: Nestlé
Date: 2026-02-01
Compare Date: 2026-01-31

KPIs:
1. Tổng thảo luận: 1,727 (+104.38%)
2. Tổng bài đăng: 481 (+314.66%)
3. Tổng tương tác: 23,259 (-23.22%)
4. Lượt reactions: 17,639 (+10.78%)
5. Lượt chia sẻ: 4,374 (-67.94%)
6. Bình luận: 1,246 (+70.92%)
7. Lượt xem: 635,491 (-45.71%)

Insight: [Copy insight từ report_output.json slide_1.insight]

DATA FOR SLIDE 2:
Trendline (7 days):
- 27/01: 2
- 28/01: 19
- 29/01: 1
- 30/01: 46
- 31/01: 845
- 01/02: 1,727 (PEAK)

Peak Day: 01/02 - 1,727 lượt
Current: 01/02 - Vẫn đang HOT

Insight: [Copy insight từ report_output.json slide_2.insight]

DATA FOR SLIDE 3:
Channels:
- Facebook: 1,680 (+101.44%)
- TikTok: 21 (+250%)
- YouTube: 16 (+100%)
- News: 8 (+300%)
- Threads: 2 (-33.33%)

Top Channel: Facebook (97%)

Insight: [Copy insight từ report_output.json slide_3.insight]

DATA FOR SLIDE 4:
Sentiment Distribution:
- Neutral: 1,029 (60%)
- Negative: 583 (34%)
- Positive: 115 (6%)

Top Brand Attributes:
1. Chất lượng Sản phẩm: Neg 461, Neu 724, Pos 76
2. Giá cả & Khuyến mãi: Neg 86, Neu 192, Pos 24
3. Hương vị: Neg 8, Neu 36, Pos 1
4. Nguồn gốc & Thành phần: Neg 8, Neu 24, Pos 5
5. Thương hiệu & Quảng cáo: Neg 6, Neu 15, Pos 4
6. Khác: Neg 10, Neu 13, Pos 0

Insight: [Copy insight từ report_output.json slide_4.insight]
```

#### Bước 2.4: Paste vào Manuss
- Paste toàn bộ prompt (cơ bản + data) vào ô input của Manuss
- Click "Generate" hoặc "Create"
- Đợi 30-60 giây để AI tạo slide

---

### Option B: Sử dụng Gamma.app

#### Bước 2.1: Truy cập Gamma
- Website: https://gamma.app
- Đăng nhập
- Chọn "Create new" → "Generate with AI"

#### Bước 2.2: Sử dụng prompt ngắn gọn hơn
Gamma thích prompt ngắn gọn, sử dụng format này:

```
Create a 4-slide brand analysis presentation:

Slide 1: Overview with 7 KPI cards showing metrics and % changes
Slide 2: Line chart showing 7-day trend with peak day highlighted
Slide 3: Horizontal bar chart of channels (Facebook, TikTok, YouTube, News)
Slide 4: Pie chart (sentiment) + stacked bar chart (attributes)

Theme: Corporate blue, professional, data-driven

Data: [Paste dữ liệu từ report_output.json]
```

#### Bước 2.3: Refine từng slide
- Gamma sẽ tạo draft đầu tiên
- Click vào từng slide để edit
- Sử dụng AI commands: "/chart", "/layout", "/style"
- Paste dữ liệu chi tiết cho từng slide

---

### Option C: Sử dụng Beautiful.ai

#### Bước 2.1: Truy cập Beautiful.ai
- Website: https://beautiful.ai
- Đăng nhập
- Chọn "New Presentation" → "Start with AI"

#### Bước 2.2: Chọn template
- Tìm template "Analytics Dashboard" hoặc "Data Report"
- Click "Use this template"

#### Bước 2.3: Customize từng slide
Beautiful.ai ít hỗ trợ prompt dài, nên làm thủ công:

**Slide 1:**
- Chọn layout "Metrics Grid"
- Add 7 metric cards
- Paste data từ `slide_1.data`
- Add text box cho insight

**Slide 2:**
- Chọn layout "Chart + Text"
- Add line chart
- Input data từ `slide_2.trendline`
- Add insight text

**Slide 3:**
- Chọn layout "Horizontal Bar Chart"
- Input data từ `slide_3.channel_distribution`
- Customize colors theo channel

**Slide 4:**
- Chọn layout "Two Charts"
- Left: Pie chart (sentiment)
- Right: Stacked bar (attributes)
- Add insight text

---

## 🎨 BƯỚC 3: TINH CHỈNH DESIGN

### 3.1. Kiểm tra màu sắc
Đảm bảo sử dụng đúng color palette:
```
Primary Blue:    #1e40af
Secondary Gray:  #6b7280
Success Green:   #16a34a
Danger Red:      #dc2626
Warning Yellow:  #f59e0b
```

### 3.2. Điều chỉnh typography
- Slide title: 32px, Bold
- Section title: 24px, Bold
- Body text: 14px, Regular
- Line height: 1.6

### 3.3. Kiểm tra spacing
- Slide padding: 48px
- Section margin: 32px
- Element spacing: 16px

### 3.4. Format numbers
- Thêm dấu phẩy: 1,727 (không phải 1727)
- Làm tròn %: 104.38% (2 chữ số thập phân)
- Format dates: DD/MM/YYYY

---

## 📊 BƯỚC 4: THÊM BIỂU ĐỒ

### 4.1. Line Chart (Slide 2)
```
Type: Line chart
X-axis: 27/01, 28/01, 29/01, 30/01, 31/01, 01/02
Y-axis: 2, 19, 1, 46, 845, 1727
Style: Blue line, smooth curve, markers
Highlight: Peak at 01/02 with red marker
```

**Cách thêm:**
- Click "Add Chart" → "Line Chart"
- Paste data vào data editor
- Customize: Line color = Blue, Line width = 3px
- Add marker at peak point

### 4.2. Bar Chart (Slide 3)
```
Type: Horizontal bar chart
Labels: Facebook, TikTok, YouTube, News, Threads
Values: 1680, 21, 16, 8, 2
Colors: #1877f2, #000000, #ff0000, #f59e0b, #6b7280
```

**Cách thêm:**
- Click "Add Chart" → "Bar Chart" → "Horizontal"
- Paste data
- Customize colors cho từng bar
- Add data labels (values + %)

### 4.3. Pie Chart (Slide 4 - Left)
```
Type: Donut chart
Segments:
- Neutral: 1029 (60%) - Gray #6b7280
- Negative: 583 (34%) - Red #dc2626
- Positive: 115 (6%) - Green #16a34a
```

**Cách thêm:**
- Click "Add Chart" → "Pie Chart" → "Donut"
- Input 3 segments
- Set colors
- Show percentages

### 4.4. Stacked Bar Chart (Slide 4 - Right)
```
Type: Horizontal stacked bar
Categories: 6 brand attributes
Stacks: Negative (red), Neutral (gray), Positive (green)
Data: [From slide_4.attribute_sentiment]
```

**Cách thêm:**
- Click "Add Chart" → "Stacked Bar" → "Horizontal"
- Input data for each attribute
- Set 3 series (Neg, Neu, Pos)
- Customize colors

---

## ✅ BƯỚC 5: KIỂM TRA CHẤT LƯỢNG

### Quality Checklist:
- [ ] **Dữ liệu chính xác:** Tất cả số liệu khớp với `report_output.json`
- [ ] **Biểu đồ rõ ràng:** Labels, legends, colors đúng
- [ ] **Insight đầy đủ:** Tất cả 4 slide đều có insight
- [ ] **Màu sắc nhất quán:** Sử dụng đúng color palette
- [ ] **Typography chuẩn:** Font size, weight, spacing đúng
- [ ] **Layout cân đối:** Không bị chật chội hoặc thừa space
- [ ] **Links hoạt động:** URLs trong insight clickable
- [ ] **Responsive:** Hiển thị tốt ở nhiều kích thước màn hình

### Test Presentation Mode:
- Click "Present" hoặc "Slideshow"
- Kiểm tra từng slide
- Đảm bảo text đọc được từ xa
- Charts hiển thị đầy đủ

---

## 💾 BƯỚC 6: EXPORT VÀ CHIA SẺ

### 6.1. Export PDF
- Click "Export" → "PDF"
- Chọn quality: High (300 DPI)
- Download file

### 6.2. Export PowerPoint
- Click "Export" → "PowerPoint"
- Download file .pptx
- Có thể edit thêm trong PowerPoint

### 6.3. Share Link
- Click "Share"
- Set permissions: View only / Can edit
- Copy link và gửi cho team

### 6.4. Embed
- Click "Share" → "Embed"
- Copy embed code
- Paste vào website/dashboard

---

## 🔄 BƯỚC 7: CẬP NHẬT ĐỊNH KỲ

### Khi có dữ liệu mới:

#### 7.1. Generate report mới
```bash
cd test
python generate_report.py
```

#### 7.2. Extract dữ liệu mới
```bash
python -c "
import json
with open('report_output.json') as f:
    data = json.load(f)
    print('Brand:', data['report_metadata']['brand'])
    print('Date:', data['report_metadata']['report_date'])
    # ... print các metrics cần thiết
"
```

#### 7.3. Update slides
- Mở presentation đã tạo
- Click vào từng chart/metric
- Update data
- Refresh charts
- Update insight text

#### 7.4. Version control
- Save as new version: "Brand Report - [Date]"
- Hoặc duplicate presentation
- Giữ lại các version cũ để so sánh

---

## 🎓 TIPS & TRICKS

### Tip 1: Sử dụng Template
Sau khi tạo slide đầu tiên thành công:
- Save as template
- Lần sau chỉ cần update data
- Tiết kiệm thời gian

### Tip 2: Batch Processing
Nếu có nhiều brands:
```python
# Script tự động tạo prompt cho nhiều brands
brands = ['Nestlé', 'Vinamilk', 'TH True Milk']
for brand in brands:
    # Generate report
    # Extract data
    # Create prompt
    # Save to file
```

### Tip 3: Custom Branding
- Upload logo công ty
- Set brand colors
- Customize footer với company info

### Tip 4: Animation
- Add subtle animations cho charts
- Entrance: Fade in
- Chart: Grow from zero
- Không overuse animation

### Tip 5: Speaker Notes
- Add notes cho từng slide
- Giải thích insight chi tiết
- Hướng dẫn present

---

## 🆘 TROUBLESHOOTING

### Vấn đề 1: AI không hiểu prompt
**Giải pháp:**
- Chia nhỏ prompt thành từng slide
- Tạo từng slide một
- Sử dụng prompt ngắn gọn hơn

### Vấn đề 2: Charts không đúng format
**Giải pháp:**
- Tạo chart thủ công
- Paste data từ Excel/CSV
- Customize từng element

### Vấn đề 3: Màu sắc không đúng
**Giải pháp:**
- Set custom color palette trong settings
- Manually change colors cho từng element
- Use color picker với hex codes

### Vấn đề 4: Insight quá dài
**Giải pháp:**
- Rút gọn insight (giữ 3-4 câu chính)
- Tăng font size của insight box
- Chia thành 2 columns

### Vấn đề 5: Export bị lỗi font
**Giải pháp:**
- Sử dụng web-safe fonts
- Embed fonts khi export
- Convert text to outlines (PDF)

---

## 📚 TÀI LIỆU THAM KHẢO

### Files liên quan:
- `PROMPT_FOR_SLIDE_PLATFORMS.md` - Prompt chi tiết
- `PROMPT_BUILD_4_SLIDES.md` - Kiến trúc hệ thống
- `report_output.json` - Dữ liệu mẫu
- `report_converted.json` - Format cho HTML

### External Resources:
- Manuss Documentation: https://manuss.com/docs
- Gamma Guide: https://gamma.app/docs
- Beautiful.ai Help: https://support.beautiful.ai
- Chart.js Docs: https://chartjs.org/docs

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề:
1. Kiểm tra lại file `report_output.json` có đúng format
2. Đọc lại hướng dẫn từng bước
3. Thử với platform khác (Manuss → Gamma → Beautiful.ai)
4. Tạo slide thủ công với data có sẵn

---

**Chúc bạn tạo slide thành công! 🎉**

**Version:** 1.0  
**Last Updated:** 2026-02-05
