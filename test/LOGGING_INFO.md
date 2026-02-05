# 📊 Logging Information

## Đã thêm logging chi tiết vào tất cả các bước

### 🎯 Khi chạy `python generate_report.py`, bạn sẽ thấy:

```
============================================================
📊 REPORT GENERATION SYSTEM
============================================================

[Step 1/5] Checking API credentials...
   ✅ API_KEY: 5LbzDSzGPb...
   ✅ BASE_URL: https://api.deepinfra.com/v1/

[Step 2/5] Loading modules...
   ✅ Modules loaded successfully

[Step 3/5] Initializing report generator...
   ✅ Generator initialized

[Step 4/5] Generating report...
   ⏱️  This will take 3-4 minutes (calling LLM 4 times)
   ☕ Please wait...

============================================================
📊 STARTING REPORT GENERATION
============================================================

[1/8] Loading data from Excel...
      → Loading Excel file...
      → Loaded 2640 rows
      → Cleaning text columns...
      → Normalizing dates...
      → Valid dates: 2640 rows
      → Converting numeric columns...
      ✅ Loaded 2640 rows

[2/8] Filtering data by dates...
      ✅ Report date (2026-02-01): 1727 rows
      ✅ Compare date (2026-01-31): 845 rows

[3/8] Generating Slide 1: Overview...
      📝 Calculating KPIs...
      🤖 Calling LLM for insights (this may take 30-60 seconds)...
         → Extracting top negative topics...
         → Found 6 top negative topics
         → Building prompt...
         → Calling LLM API...
         → API call completed in 12.3s
         → LLM response received
      ✅ Slide 1 completed

[4/8] Generating Slide 2: Trendline...
      📈 Calculating trendline data...
      🤖 Calling LLM for insights (this may take 30-60 seconds)...
         → Analyzing peak day topics...
         → Found 3 peak day topics
         → Building prompt...
         → Calling LLM API...
         → API call completed in 15.7s
         → LLM response received
      ✅ Slide 2 completed

[5/8] Generating Slide 3: Channel Breakdown...
      📡 Analyzing channel distribution...
      🤖 Calling LLM for insights (this may take 30-60 seconds)...
         → Top channel: Facebook
         → Total channels: 5
         → Extracting top buzz from top channel...
         → Found 6 top buzz posts
         → Building prompt...
         → Calling LLM API...
         → API call completed in 14.5s
         → LLM response received
         → Replacing URL placeholders...
      ✅ Slide 3 completed

[6/8] Generating Slide 4: Sentiment & Brand Attribute...
      💭 Analyzing sentiment distribution...
      🤖 Calling LLM for insights (this may take 30-60 seconds)...
         → Building evidence from top posts...
         → Found 5 evidence posts
         → Building prompt...
         → Calling LLM API...
         → API call completed in 18.2s
         → LLM response received
         → Replacing URL placeholders...
      ✅ Slide 4 completed

[7/8] Combining all slides...
      ✅ Report structure created

[8/8] Report generation completed!

[Step 5/5] Report completed!

============================================================
✅ SUCCESS!
============================================================
⏱️  Total time: 3m 15s
📄 Output: report_output.json
📊 Slides generated: 4

📌 Next step:
   python render_html.py
============================================================
```

## 📝 Chi tiết từng bước

### Step 1: API Credentials
- Kiểm tra API_KEY và BASE_URL từ file .env
- Hiển thị 10 ký tự đầu của API key

### Step 2: Module Loading
- Import các modules cần thiết
- Báo lỗi nếu có vấn đề với imports

### Step 3: Initialization
- Khởi tạo ReportGenerator
- Setup LLM client và data loader

### Step 4-5: Report Generation
Gồm 8 bước con:

1. **Load Data**: 
   - Load Excel file
   - Clean text
   - Normalize dates
   - Convert numeric columns

2. **Filter Data**:
   - Filter theo report date
   - Filter theo compare date

3. **Slide 1 (Overview)**:
   - Calculate KPIs
   - Extract top negative topics
   - Call LLM (30-60s)
   - Show API response time

4. **Slide 2 (Trendline)**:
   - Calculate trendline
   - Analyze peak day
   - Call LLM (30-60s)
   - Show API response time

5. **Slide 3 (Channel Breakdown)** ⭐ MỚI:
   - Analyze channel distribution
   - Find top channel
   - Extract top buzz posts
   - Call LLM (30-60s)
   - Replace URL placeholders
   - Show API response time

6. **Slide 4 (Sentiment)**:
   - Analyze sentiment distribution
   - Build evidence
   - Call LLM (30-60s)
   - Replace URL placeholders
   - Show API response time

7. **Combine Slides**:
   - Merge all slides into report structure

8. **Complete**:
   - Show total time
   - Show output file
   - Show number of slides

## ⏱️ Thời gian dự kiến

| Bước | Thời gian | Mô tả |
|------|-----------|-------|
| Load data | 2-5s | Đọc Excel và preprocess |
| Slide 1 | 30-60s | LLM call cho overview |
| Slide 2 | 30-60s | LLM call cho trendline |
| Slide 3 | 30-60s | LLM call cho channel breakdown ⭐ |
| Slide 4 | 30-60s | LLM call cho sentiment |
| Combine | <1s | Merge slides |
| **Total** | **3-4 phút** | Tổng thời gian |

## 🔍 Monitoring

### Nếu script chạy lâu hơn bình thường:

1. **Kiểm tra network**: LLM API cần internet tốt
2. **Kiểm tra API quota**: Có thể hết quota
3. **Kiểm tra data size**: File Excel quá lớn

### Nếu bị stuck:

- Xem log cuối cùng để biết đang ở bước nào
- Nếu stuck ở "Calling LLM API", đợi thêm (có thể API chậm)
- Nếu quá 5 phút, Ctrl+C và chạy lại

## 💡 Tips

1. **Theo dõi progress**: Mỗi bước có emoji và số thứ tự rõ ràng
2. **API timing**: Mỗi LLM call hiển thị thời gian thực tế
3. **Error messages**: Nếu lỗi, sẽ hiển thị thời gian đã chạy và stack trace
4. **Success summary**: Cuối cùng hiển thị tổng thời gian và số slides

## 🐛 Debug

Nếu cần debug chi tiết hơn, có thể thêm:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Vào đầu file `generate_report.py`
