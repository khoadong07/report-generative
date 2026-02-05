# ✅ Đã thêm Slide 3: Channel Breakdown

## 🎯 Thứ tự slides đầy đủ:

1. **Slide 1**: Overview (KPI metrics)
2. **Slide 2**: Trendline (Xu hướng theo thời gian)
3. **Slide 3**: Channel Breakdown (Phân bổ theo kênh) ⭐ MỚI
4. **Slide 4**: Sentiment & Brand Attribute

## 📊 Slide 3 - Channel Breakdown

### Chức năng:
- Phân tích phân bổ thảo luận theo từng kênh (Facebook, TikTok, YouTube, etc.)
- Xác định kênh có thảo luận cao nhất
- Trích xuất top buzz posts từ kênh chính
- Generate insight về xu hướng kênh

### Dữ liệu output:
```json
{
  "title": "Phân tích theo kênh thảo luận",
  "subtitle": "Ngày 2026-02-01 (so sánh với 2026-01-31)",
  "top_channel": "Facebook",
  "channel_distribution": [
    {
      "Channel": "Facebook",
      "today_buzz": 1680,
      "yesterday_buzz": 834,
      "change_pct": 101.44
    },
    {
      "Channel": "TikTok",
      "today_buzz": 21,
      "yesterday_buzz": 5,
      "change_pct": 320.0
    }
  ],
  "insight": "Insight text với URLs..."
}
```

## 🔧 Files đã cập nhật:

### 1. `prompts.py`
- ✅ Thêm `get_channel_breakdown_prompt()` function

### 2. `slide_generators.py`
- ✅ Thêm `Slide3Generator` class
- ✅ Phân tích channel distribution
- ✅ Tìm top channel
- ✅ Extract top buzz posts
- ✅ Generate insight với LLM
- ✅ Replace URL placeholders

### 3. `report_generator.py`
- ✅ Import `Slide3Generator`
- ✅ Initialize slide3_gen
- ✅ Generate slide 3 trong workflow
- ✅ Thêm slide_3 vào output JSON

### 4. `generate_report.py`
- ✅ Cập nhật thời gian dự kiến: 3-4 phút (4 LLM calls)

### 5. `LOGGING_INFO.md`
- ✅ Cập nhật documentation với Slide 3

## 📝 Logic xử lý:

```python
# 1. Phân tích channel distribution
channel_today = report_df.groupby("Channel").size()
channel_yesterday = compare_df.groupby("Channel").size()

# 2. Tính % thay đổi
channel_df["change_pct"] = calculate_percentage_change(...)

# 3. Tìm top channel
top_channel = channel_df.iloc[0]["Channel"]

# 4. Extract top buzz từ top channel
df_top_buzz = (
    df_top_channel
    .sort_values("engagement", ascending=False)
    .head(6)
)

# 5. Build URL map
url_map = {f"URL_{i+1}": url for i, url in enumerate(urls)}

# 6. Call LLM với prompt
insight = llm_client.generate_insight(prompt)

# 7. Replace URL_X với real URLs
final_insight = replace_url_placeholders(insight, url_map)
```

## ⏱️ Thời gian xử lý:

- Phân tích channel: <1s
- Extract top buzz: <1s
- LLM call: 30-60s
- Replace URLs: <1s
- **Total**: ~30-60s

## 🎨 Template HTML

Slide 3 sẽ cần template HTML tương ứng trong `template_parameterized.html`:
- Bar chart cho channel distribution
- Insight section
- Navigation

## 🚀 Chạy với Slide 3:

```bash
cd test
python generate_report.py
```

Output sẽ có:
```
[5/8] Generating Slide 3: Channel Breakdown...
      📡 Analyzing channel distribution...
      → Top channel: Facebook
      → Total channels: 5
      🤖 Calling LLM for insights...
      ✅ Slide 3 completed
```

## 📊 Kết quả:

File `report_output.json` sẽ có:
```json
{
  "report_metadata": {...},
  "slide_1": {...},
  "slide_2": {...},
  "slide_3": {...},  ⭐ MỚI
  "slide_4": {...}
}
```

## 💡 Lưu ý:

1. **Channel column**: Đảm bảo Excel file có column "Channel"
2. **Top N**: Mặc định lấy 6 top buzz posts (config trong TOP_N_TOPICS)
3. **URL replacement**: Tự động thay URL_1, URL_2... bằng URLs thật
4. **Logging**: Có log chi tiết cho từng bước

## ✅ Checklist:

- [x] Thêm prompt function
- [x] Thêm Slide3Generator class
- [x] Cập nhật report_generator
- [x] Cập nhật logging
- [x] Cập nhật documentation
- [ ] Cập nhật HTML template (nếu cần render)
- [ ] Test với data thật

---

**Bây giờ hệ thống đã có đầy đủ 4 slides!** 🎉
