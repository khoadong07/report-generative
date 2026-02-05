# PROMPT CHI TIẾT: XÂY DỰNG 4 SLIDE TỪ DỮ LIỆU REPORT

## 📋 TỔNG QUAN HỆ THỐNG

### Mục đích
Hệ thống này tự động tạo báo cáo phân tích thương hiệu gồm 4 slide từ dữ liệu social listening, sử dụng LLM để sinh insight thông minh cho từng slide.

### Quy trình tổng thể
```
Dữ liệu Excel → generate_report.py → report_output.json → render_html.py → HTML Report
```

---

## 🎯 CẤU TRÚC 4 SLIDE

### **SLIDE 1: TỔNG QUAN THƯƠNG HIỆU (Overview)**
**Mục đích:** Cung cấp cái nhìn tổng quan về tình hình thảo luận thương hiệu trong ngày

**Dữ liệu hiển thị:**
- 7 KPI cards so sánh với ngày hôm trước:
  1. Tổng thảo luận (Total Buzz)
  2. Tổng bài đăng (Posts)
  3. Tổng tương tác (Engagement = Reactions + Shares + Comments)
  4. Lượt reactions
  5. Lượt chia sẻ (Shares)
  6. Bình luận (Comments)
  7. Lượt xem (Views)

**Insight được sinh:**
- Phân tích 5-6 câu văn xuôi
- Mô tả quy mô & mức độ chú ý
- Diễn biến sự vụ và phản ứng cộng đồng
- Dựa trên top 6 bài viết NEGATIVE có engagement cao nhất
- Mỗi câu gắn 1 URL nguồn duy nhất

**Cách tính toán:**
```python
# Engagement
engagement = reactions + shares + comments

# Percentage change
change_pct = ((today - yesterday) / yesterday) * 100

# Top negative topics
df_neg = report_df[
    (Sentiment == "negative") & 
    (Type in ["Post", "Video", "Article"])
]
df_top = df_neg.sort_by(engagement).head(6)
```

---

### **SLIDE 2: TRENDLINE - DIỄN BIẾN THẢO LUẬN**
**Mục đích:** Phân tích xu hướng thảo luận trong 7 ngày gần nhất

**Dữ liệu hiển thị:**
- Biểu đồ đường (line chart) thể hiện buzz theo ngày
- Khoảng thời gian: 7 ngày (report_date - 6 ngày)
- Xác định ngày có buzz cao nhất (peak day)
- Đánh giá ngày hiện tại có còn "hot" không (>= 50% peak)

**Insight được sinh:**
- Phân tích 3-4 câu
- Tóm tắt sự vụ chính xảy ra trong peak day
- Đánh giá mức độ quan tâm hiện tại
- Dựa trên top 3 bài viết NEGATIVE trong peak day
- Mỗi insight gắn 1 URL

**Cách tính toán:**
```python
# Trendline window
start_day = report_date - timedelta(days=6)
df_window = df[(PublishedDay >= start_day) & (PublishedDay <= report_date)]

# Peak detection
peak_day = df_window.groupby('PublishedDay').size().idxmax()
peak_buzz = df_window[df_window['PublishedDay'] == peak_day].shape[0]

# Still hot?
is_still_hot = current_buzz >= 0.5 * peak_buzz
```

---

### **SLIDE 3: PHÂN TÍCH THEO KÊNH (Channel Breakdown)**
**Mục đích:** Phân tích phân bổ thảo luận theo các kênh truyền thông

**Dữ liệu hiển thị:**
- Biểu đồ cột (bar chart) thể hiện buzz theo channel
- So sánh với ngày hôm trước
- Các channel: Facebook, TikTok, YouTube, News, Threads, etc.
- Xác định top channel (kênh có buzz cao nhất)

**Insight được sinh:**
- Phân tích 6-7 câu văn xuôi
- Chỉ ra kênh chính và xu hướng
- Giải thích nguyên nhân và tác động
- Dựa trên top 6 bài viết có engagement cao nhất trong top channel
- Mỗi câu gắn 1 URL placeholder (URL_1, URL_2, ...) sau đó thay thế bằng URL thật

**Cách tính toán:**
```python
# Channel distribution
channel_today = report_df.groupby('Channel').size()
channel_yesterday = compare_df.groupby('Channel').size()
channel_df = merge(channel_today, channel_yesterday)
channel_df['change_pct'] = calculate_percentage_change(today, yesterday)

# Top channel
top_channel = channel_df.sort_values('today_buzz', ascending=False).iloc[0]['Channel']

# Top buzz in top channel
df_top_channel = report_df[report_df['Channel'] == top_channel]
df_top_buzz = df_top_channel.sort_by(engagement).head(6)
```

---

### **SLIDE 4: SENTIMENT & BRAND ATTRIBUTE**
**Mục đích:** Phân tích cảm xúc và thuộc tính thương hiệu

**Dữ liệu hiển thị:**
- Biểu đồ tròn (pie chart): Phân bổ Sentiment (Negative, Neutral, Positive)
- Biểu đồ cột nhóm (stacked bar chart): Sentiment theo Brand Attribute
- Top 6 brand attributes có lượng đề cập cao nhất

**Insight được sinh:**
- Phân tích 4-5 câu văn xuôi
- So sánh Negative / Neutral / Positive
- Nêu rõ brand attribute nổi bật theo từng sentiment
- Dựa trên top 5 bài viết có engagement cao nhất
- Mỗi câu gắn 1 URL placeholder (URL_1, URL_2, ...) sau đó thay thế

**Cách tính toán:**
```python
# Sentiment distribution
sentiment_dist = report_df['Sentiment'].value_counts()

# Explode labels
df_exploded = report_df.explode('Label_List')

# Attribute x Sentiment
attr_sentiment = df_exploded.groupby(['Label_List', 'Sentiment']).size()

# Top 6 attributes
top_attrs = attr_sentiment.groupby('Label_List').sum().sort_values().head(6)

# Pivot table
pivot_df = attr_sentiment.pivot(
    index='Label_List',
    columns='Sentiment',
    values='Count'
)
```

---

## 🤖 CÁCH LLM SINH INSIGHT

### Nguyên tắc chung
1. **Văn phong:** Chuyên nghiệp, trung lập, không cảm tính
2. **Độ dài:** Ngắn gọn, súc tích (3-7 câu tùy slide)
3. **Dẫn chứng:** Mỗi câu phải có 1 URL nguồn
4. **Không lặp URL:** Mỗi URL chỉ xuất hiện 1 lần
5. **Format:** Văn xuôi, KHÔNG gạch đầu dòng, KHÔNG tiêu đề

### Quy trình sinh insight

#### Bước 1: Chuẩn bị context
```python
# Lấy top posts theo tiêu chí
df_top = filter_and_sort(
    df=report_df,
    criteria=sentiment/channel/attribute,
    sort_by='engagement',
    limit=top_n
)

# Build context text
context = []
for row in df_top:
    context.append(f"""
Tiêu đề: {row['Title']}
Mô tả: {row['Description']}
Nội dung: {row['Content']}
Engagement: {row['engagement']}
URL: {row['UrlTopic']}
""")
```

#### Bước 2: Tạo prompt
```python
prompt = f"""
Bạn là chuyên gia phân tích khủng hoảng truyền thông.

BỐI CẢNH:
- Thương hiệu: {brand}
- Ngày phân tích: {report_date}
- [Thông tin cụ thể theo slide]

DỮ LIỆU:
{context_text}

NHIỆM VỤ:
[Yêu cầu cụ thể theo slide]

YÊU CẦU BẮT BUỘC:
- Viết X-Y câu, văn xuôi
- Mỗi câu kết thúc bằng [Nguồn: URL]
- Mỗi URL chỉ dùng 1 lần
- KHÔNG gạch đầu dòng
- KHÔNG tiêu đề
"""
```

#### Bước 3: Gọi LLM API
```python
response = llm_client.generate_insight(prompt)
```

#### Bước 4: Post-processing (chỉ Slide 3 & 4)
```python
# Thay thế URL placeholder bằng URL thật
for key, real_url in url_map.items():
    insight = insight.replace(f"[Nguồn: {key}]", f"[Nguồn: {real_url}]")
```

---

## 📊 ĐỊNH DẠNG OUTPUT

### File: `report_output.json`

```json
{
  "report_metadata": {
    "brand": "Tên thương hiệu",
    "report_date": "YYYY-MM-DD",
    "compare_date": "YYYY-MM-DD",
    "generated_at": "ISO timestamp"
  },
  "slide_1": {
    "title": "Tổng quan về thương hiệu {brand}",
    "subtitle": "Ngày {report_date} (so sánh với {compare_date})",
    "data": [
      {
        "type": "buzz",
        "label": "Tổng thảo luận",
        "today": 1727,
        "yesterday": 845,
        "change_pct": 104.38
      },
      // ... 6 KPIs khác
    ],
    "insight": "Văn bản insight 5-6 câu với [Nguồn: URL]..."
  },
  "slide_2": {
    "title": "Trendline | Diễn biến thảo luận",
    "subtitle": "Khoảng thời gian: {start_date} → {end_date}",
    "window": {
      "start_date": "YYYY-MM-DD",
      "end_date": "YYYY-MM-DD"
    },
    "trendline": [
      {"date": "YYYY-MM-DD", "buzz": 123},
      // ... 7 ngày
    ],
    "peak_day": {
      "date": "YYYY-MM-DD",
      "buzz": 1727,
      "links": ["url1", "url2", "url3"]
    },
    "current_day": {
      "date": "YYYY-MM-DD",
      "buzz": 1727,
      "is_still_hot": true
    },
    "insight": "Văn bản insight 3-4 câu..."
  },
  "slide_3": {
    "title": "Phân tích theo kênh thảo luận",
    "subtitle": "Ngày {report_date} (so sánh với {compare_date})",
    "top_channel": "Facebook",
    "channel_distribution": [
      {
        "Channel": "Facebook",
        "today_buzz": 1680,
        "yesterday_buzz": 834,
        "change_pct": 101.44
      },
      // ... các channel khác
    ],
    "insight": "Văn bản insight 6-7 câu..."
  },
  "slide_4": {
    "title": "Sentiment & Brand Attribute",
    "subtitle": "Ngày {report_date}",
    "sentiment_distribution": [
      {"Sentiment": "Neutral", "Count": 1029},
      {"Sentiment": "Negative", "Count": 583},
      {"Sentiment": "Positive", "Count": 115}
    ],
    "attribute_sentiment": [
      {
        "Label_List": "Chất lượng Sản phẩm",
        "Negative": 461,
        "Neutral": 724,
        "Positive": 76
      },
      // ... top 6 attributes
    ],
    "insight": "Văn bản insight 4-5 câu..."
  }
}
```

---

## 🔧 CÁC THAM SỐ CẤU HÌNH

### Trong `report_generator.py`:
```python
TOPIC_TYPES = ["Post", "Video", "Article"]  # Loại bỏ Comment
TOP_N_OVERVIEW = 6        # Số topic phân tích cho Slide 1
TOP_N_PEAK = 3            # Số topic phân tích cho Slide 2 (peak day)
TOP_N_BUZZ = 6            # Số topic phân tích cho Slide 3 (channel)
TOP_N_ATTR = 6            # Số attributes hiển thị cho Slide 4
LOOKBACK_DAYS = 6         # Số ngày lookback cho trendline (7 ngày total)
```

### Trong LLM Client:
```python
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.3         # Thấp để đảm bảo output ổn định
MAX_TOKENS = 1000         # Đủ cho insight 3-7 câu
```

---

## 🎨 RENDER HTML

### Quy trình render
```
report_output.json → convert_report_format.py → report_converted.json → render_html.py → final_report.html
```

### Template HTML sử dụng:
- `template_landing.html`: Landing page với 4 slide
- Chart.js: Vẽ biểu đồ (line, bar, pie, stacked bar)
- Tailwind CSS: Styling responsive

### Các biểu đồ:
1. **Slide 1:** KPI cards (không có chart)
2. **Slide 2:** Line chart (trendline)
3. **Slide 3:** Bar chart (channel distribution)
4. **Slide 4:** Pie chart (sentiment) + Stacked bar chart (attribute x sentiment)

---

## ⚡ CÁCH CHẠY HỆ THỐNG

### Bước 1: Chuẩn bị môi trường
```bash
cd test
cp .env.example .env
# Điền API_KEY và BASE_URL vào .env
```

### Bước 2: Generate report
```bash
python generate_report.py
```
**Output:** `report_output.json` (4 slides với insight)

**Thời gian:** 3-4 phút (gọi LLM 4 lần)

### Bước 3: Convert format (optional)
```bash
python convert_report_format.py
```
**Output:** `report_converted.json` (format cho HTML)

### Bước 4: Render HTML
```bash
python render_html.py
```
**Output:** `final_report.html` (báo cáo hoàn chỉnh)

---

## 📝 LƯU Ý QUAN TRỌNG

### 1. Về dữ liệu đầu vào
- File Excel phải có các cột: `Title`, `Description`, `Content`, `Sentiment`, `Type`, `Channel`, `Labels`, `Reactions`, `Shares`, `Views`, `UrlTopic`, `PublishedDay`
- `PublishedDay` phải là định dạng date
- `Labels` là chuỗi phân tách bởi dấu phẩy: "Label1, Label2, Label3"

### 2. Về LLM API
- Hệ thống gọi LLM 4 lần (1 lần/slide)
- Mỗi lần gọi mất ~30-60 giây
- Cần API key hợp lệ và đủ quota
- Model khuyến nghị: GPT-4o-mini hoặc tương đương

### 3. Về insight quality
- Chất lượng insight phụ thuộc vào:
  - Chất lượng dữ liệu đầu vào
  - Prompt engineering
  - Model LLM sử dụng
- Nên review và điều chỉnh prompt nếu output không đạt yêu cầu

### 4. Về URL trong insight
- Slide 1 & 2: URL thật được gắn trực tiếp
- Slide 3 & 4: Dùng placeholder (URL_1, URL_2, ...) rồi thay thế sau
- Lý do: Tránh LLM tự tạo URL giả

### 5. Về performance
- Có thể song song hóa 4 lần gọi LLM để giảm thời gian
- Hiện tại chạy tuần tự để dễ debug và theo dõi

---

## 🚀 MỞ RỘNG & TÙY CHỈNH

### Thêm slide mới
1. Tạo class `SlideXGenerator` trong `slide_generators.py`
2. Implement method `generate()` và `_generate_insight()`
3. Tạo prompt template trong `prompts.py`
4. Thêm vào `ReportGenerator.generate_and_save()`

### Thay đổi số lượng top items
- Điều chỉnh `TOP_N_*` trong constructor của các Generator class
- Ví dụ: `Slide1Generator(llm_client, topic_types, top_n=10)`

### Thay đổi lookback window
- Điều chỉnh `LOOKBACK_DAYS` trong `Slide2Generator`
- Ví dụ: `Slide2Generator(llm_client, topic_types, lookback_days=14)`

### Custom prompt
- Chỉnh sửa các function trong `prompts.py`
- Test kỹ để đảm bảo output format đúng

---

## 🐛 TROUBLESHOOTING

### Lỗi: "API credentials not found"
→ Kiểm tra file `.env` có đúng format và nằm trong thư mục `test/`

### Lỗi: "LLM API timeout"
→ Tăng timeout trong `llm_client.py` hoặc kiểm tra kết nối mạng

### Insight không có URL
→ Kiểm tra dữ liệu có cột `UrlTopic` và không null

### Insight bị lặp URL
→ Điều chỉnh prompt để nhấn mạnh "Mỗi URL chỉ dùng 1 lần"

### Chart không hiển thị
→ Kiểm tra format JSON trong `report_converted.json` có đúng schema

---

## 📚 TÀI LIỆU THAM KHẢO

- `test/FINAL_INSTRUCTIONS.md`: Hướng dẫn chi tiết cách chạy
- `test/FINAL_SUMMARY.md`: Tóm tắt kiến trúc hệ thống
- `test/slide_generators.py`: Source code các generator
- `test/prompts.py`: Các prompt template
- `test/report_output.json`: Ví dụ output thực tế

---

**Tác giả:** AI Report Generation System  
**Phiên bản:** 1.0  
**Ngày cập nhật:** 2026-02-05
