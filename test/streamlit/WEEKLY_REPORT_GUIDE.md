# Weekly Report - Hướng dẫn chi tiết

## 📋 Tổng quan

Weekly Report là báo cáo tuần với **12 slides** phân tích toàn diện về brand health trong 7 ngày.

### Đặc điểm chính:
- **Cửa sổ thời gian**: 7 ngày (1 tuần)
- **So sánh**: 4 tuần (tuần hiện tại + 3 tuần trước)
- **Số lượng slides**: 12 slides
- **Thời gian generate**: ~2 phút (parallel processing)
- **Input**: Brand name + Excel file + End date + Time

---

## 🎯 Cấu trúc 12 Slides

### **SLIDE 1: Tổng quan về Brand**
**Mục đích**: Cung cấp cái nhìn tổng quan về brand trong tuần

**Nội dung**:
- 6 KPI cards:
  - Tổng đề cập
  - Tổng tương tác
  - Tổng lượt xem
  - Lượt reaction
  - Lượt chia sẻ
  - Lượt bình luận
- Chart cột đứng so sánh 4 tuần:
  - 3 tuần trước
  - 2 tuần trước
  - Tuần trước
  - Tuần hiện tại
- Insight (LLM-generated)

**Logic**:
- Lấy data trong cửa sổ 7 ngày của tuần hiện tại
- Tính tổng các metrics
- So sánh với 3 tuần trước đó
- LLM phân tích xu hướng và các chủ đề nổi bật

---

### **SLIDE 2: Đường biểu diễn xu hướng đề cập**
**Mục đích**: Hiển thị xu hướng đề cập theo từng ngày trong tuần

**Nội dung**:
- Line chart 7 điểm (7 ngày)
- Insight (LLM-generated)

**Logic**:
- Group by PublishedDay trong tuần
- Đếm số lượng đề cập mỗi ngày
- LLM phân tích ngày có lượng thảo luận cao nhất và lý do

---

### **SLIDE 3: Phân bố lượt đề cập theo kênh**
**Mục đích**: Phân tích phân bố thảo luận trên các kênh truyền thông

**Nội dung**:
- Pie chart: Phân bố theo Channel (Facebook, TikTok, YouTube, News, etc.)
- Horizontal bar chart: Top 10 nguồn (SiteName) có lượng đề cập cao nhất
- Insight (LLM-generated)

**Logic**:
- Group by Channel → count
- Group by SiteName → count → top 10
- LLM phân tích kênh chính và nguồn nổi bật

---

### **SLIDE 4: Top nguồn có lượng tương tác cao nhất**
**Mục đích**: Liệt kê các nguồn có engagement cao nhất

**Nội dung**:
- Bảng 10 dòng
- Columns: STT, Nguồn, Tổng tương tác, Reactions, Shares, Comments
- **KHÔNG có insight**

**Logic**:
- Filter Type in TOPIC_TYPES
- Calculate engagement = Reactions + Shares + Comments
- Group by SiteName → sum engagement
- Sort descending → top 10

---

### **SLIDE 5: Top bài đăng có tương tác cao nhất**
**Mục đích**: Liệt kê các bài đăng có số lượng comments cao nhất

**Nội dung**:
- Bảng 10 dòng
- Columns: STT, Nội dung, Ngày đăng, Kênh, Nguồn, Comments, Link
- **KHÔNG có insight**

**Logic**:
- Filter Type in TOPIC_TYPES
- Sort by Comments descending → top 10
- Hiển thị content (hoặc title nếu content rỗng)

---

### **SLIDE 6: Sắc thái và cụm chủ đề đề cập nổi bật**
**Mục đích**: Phân tích sentiment và các chủ đề chính

**Nội dung**:
- 2 Pie charts (side-by-side):
  - Left: Sentiment tuần trước
  - Right: Sentiment tuần hiện tại
- Horizontal bar chart: Top 10 chủ đề (Labels1) với sentiment breakdown
  - Mỗi bar có 3 màu: Negative (đỏ), Neutral (xám), Positive (xanh)
- Insight (LLM-generated)

**Logic**:
- Group by Sentiment → count (cho cả 2 tuần)
- Group by Labels1 + Sentiment → count
- Top 10 Labels1 theo tổng count
- LLM phân tích sentiment tổng quan và top chủ đề

---

### **SLIDE 7: Các chủ đề đề cập tích cực về Brand**
**Mục đích**: Phân tích các chủ đề positive

**Nội dung**:
- Horizontal bar chart: Top 10 chủ đề positive (Labels1)
- Insight (LLM-generated) với dẫn chứng cụ thể + link

**Logic**:
- Filter Sentiment = "Positive"
- Group by Labels1 → count → top 10
- LLM phân tích top chủ đề và dẫn chứng từ bài đăng

---

### **SLIDE 8: Top các đề cập tích cực về Brand**
**Mục đích**: Đếm số lượng đề cập positive theo chủ đề

**Nội dung**:
- Bảng 10 dòng
- Columns: STT, Chủ đề (Labels1), Số lượng
- **KHÔNG có insight**

**Logic**:
- Filter Sentiment = "Positive"
- Group by Labels1 → count → top 10

---

### **SLIDE 9: Top các bài đăng tích cực về Brand**
**Mục đích**: Liệt kê bài đăng positive có comments cao nhất

**Nội dung**:
- Bảng 10 dòng
- Columns: STT, Nội dung, Ngày đăng, Kênh, Nguồn, Comments, Link
- **KHÔNG có insight**

**Logic**:
- Filter Sentiment = "Positive" AND Type in TOPIC_TYPES
- Sort by Comments descending → top 10

---

### **SLIDE 10: Các chủ đề đề cập tiêu cực về Brand**
**Mục đích**: Phân tích các chủ đề negative

**Nội dung**:
- Horizontal bar chart: Top 10 chủ đề negative (Labels1)
- Insight (LLM-generated) với dẫn chứng cụ thể + link

**Logic**:
- Filter Sentiment = "Negative"
- Group by Labels1 → count → top 10
- LLM phân tích top chủ đề và dẫn chứng từ bài đăng

---

### **SLIDE 11: Top các đề cập tiêu cực về Brand**
**Mục đích**: Đếm số lượng đề cập negative theo chủ đề

**Nội dung**:
- Bảng 10 dòng
- Columns: STT, Chủ đề (Labels1), Số lượng
- **KHÔNG có insight**

**Logic**:
- Filter Sentiment = "Negative"
- Group by Labels1 → count → top 10

---

### **SLIDE 12: Top các bài đăng tiêu cực về Brand**
**Mục đích**: Liệt kê bài đăng negative có comments cao nhất

**Nội dung**:
- Bảng 10 dòng
- Columns: STT, Nội dung, Ngày đăng, Kênh, Nguồn, Comments, Link
- **KHÔNG có insight**

**Logic**:
- Filter Sentiment = "Negative" AND Type in TOPIC_TYPES
- Sort by Comments descending → top 10

---

## 🔧 Cách sử dụng

### 1. Chạy ứng dụng
```bash
streamlit run app_weekly.py
```

### 2. Upload file Excel
- File phải có các columns: PublishedDate, Type, Channel, SiteName, Sentiment, Labels1, Title, Content, Reactions, Shares, Comments, Views, UrlTopic

### 3. Nhập thông tin
- **Brand name**: Tên thương hiệu (ví dụ: Vinamilk)
- **End date**: Ngày kết thúc tuần hiện tại (ví dụ: 10/02/2026)
- **Time**: Giờ cắt data (mặc định: 15:00)

### 4. Hệ thống tự động tính
- **Week 1** (current): End date - 7 days → End date
- **Week 2**: End date - 14 days → End date - 7 days
- **Week 3**: End date - 21 days → End date - 14 days
- **Week 4**: End date - 28 days → End date - 21 days

### 5. Generate
- Click "Generate weekly report"
- Đợi ~2 phút
- Download prompt hoặc JSON

---

## 📊 Data Requirements

### Required Columns:
- `PublishedDate` (datetime): Ngày giờ đăng bài
- `Type` (string): Loại bài đăng (fbUserTopic, fbPageTopic, etc.)
- `Channel` (string): Kênh (Facebook, TikTok, YouTube, News)
- `SiteName` (string): Tên nguồn
- `Sentiment` (string): Sắc thái (Positive, Neutral, Negative)
- `Labels1` (string): Chủ đề chính
- `Title` (string): Tiêu đề
- `Content` (string): Nội dung
- `Reactions` (numeric): Số lượt reaction
- `Shares` (numeric): Số lượt share
- `Comments` (numeric): Số lượt comment
- `Views` (numeric): Số lượt xem
- `UrlTopic` (string): Link bài đăng

---

## 🎨 Design Guidelines

### Color Scheme:
- **Primary Blue**: #1e40af (headers, charts)
- **Success Green**: #16a34a (positive sentiment)
- **Danger Red**: #dc2626 (negative sentiment)
- **Neutral Gray**: #6b7280 (neutral sentiment)
- **Background**: #ffffff

### Chart Types:
- **Pie Chart**: Sentiment distribution, Channel distribution
- **Column Chart**: Weekly comparison (4 weeks)
- **Line Chart**: Daily trend (7 days)
- **Horizontal Bar Chart**: Top topics, Top sources
- **Table**: Top posts, Top mentions

---

## 🚀 Performance

### Parallel Processing:
- **6 slides with LLM** (Slides 1, 2, 3, 6, 7, 10) → Generated in parallel (~2 minutes)
- **6 slides without LLM** (Slides 4, 5, 8, 9, 11, 12) → Generated sequentially (~10 seconds)

### Total Time:
- **~2 minutes** for complete 12-slide report

---

## 💡 Tips

1. **Chọn end date phù hợp**: Đảm bảo có đủ data cho 4 tuần
2. **Kiểm tra data quality**: Đảm bảo Sentiment và Labels1 được gán đúng
3. **Review insight**: LLM-generated insights có thể cần chỉnh sửa nhỏ
4. **Save JSON**: Để reuse hoặc debug
5. **Test với data nhỏ**: Trước khi chạy full report

---

## 🐛 Troubleshooting

### Error: No data for current week
**Solution**: Chọn end date có data trong Excel file

### Error: Missing Labels1 column
**Solution**: Đảm bảo Excel file có column Labels1

### LLM timeout
**Solution**: Kiểm tra API credentials và network connection

### Insight không có URL
**Solution**: Đảm bảo UrlTopic column không rỗng

---

## 📞 Support

Nếu gặp vấn đề, kiểm tra:
1. Console logs trong terminal
2. Error details trong Streamlit UI
3. Excel file format
4. API credentials trong .env
