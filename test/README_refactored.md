# Refactored Report Generation System

Hệ thống tạo báo cáo phân tích thương hiệu được refactor với cấu trúc module hóa, tách biệt logic và prompt.

## Cấu trúc Project

```
test/
├── config.py                 # Cấu hình chung (dates, brand, thresholds)
├── prompts.py               # Template prompts cho LLM
├── data_loader.py           # Load và preprocess dữ liệu
├── llm_client.py            # Wrapper cho LLM API
├── slide_generators.py      # Logic tạo từng slide
├── report_generator.py      # Orchestrator chính
├── template_parameterized.html  # HTML template
├── template_renderer.py     # Render HTML từ JSON
└── sample_data.json         # Dữ liệu mẫu
```

## Kiến trúc

### 1. Config Layer (`config.py`)
Chứa tất cả cấu hình:
- Đường dẫn file dữ liệu
- Ngày báo cáo và so sánh
- Tên thương hiệu
- Các ngưỡng phân tích (TOP_N, LOOKBACK_DAYS)
- Cấu hình LLM (model, temperature)
- Danh sách topic types và columns

### 2. Prompt Layer (`prompts.py`)
Tách riêng tất cả prompts thành functions:
- `get_overview_insight_prompt()` - Prompt cho slide 1
- `get_trendline_insight_prompt()` - Prompt cho slide 2
- `get_channel_insight_prompt()` - Prompt cho slide 3
- `get_sentiment_insight_prompt()` - Prompt cho slide 4

**Lợi ích:**
- Dễ chỉnh sửa prompts mà không động vào code logic
- Có thể version control prompts riêng
- Dễ A/B test các prompt khác nhau

### 3. Data Layer (`data_loader.py`)
Class `DataLoader` xử lý:
- Load dữ liệu từ Excel
- Clean text columns
- Normalize dates
- Ensure numeric columns
- Filter by date/date range

Helper functions:
- `calculate_percentage_change()` - Tính % thay đổi
- `calculate_engagement()` - Tính engagement score

### 4. LLM Layer (`llm_client.py`)
Class `LLMClient` wrapper cho OpenAI API:
- Khởi tạo client với config
- Method `generate_insight()` để gọi LLM
- Hỗ trợ custom system prompt

### 5. Business Logic Layer (`slide_generators.py`)
Các class generator cho từng slide:

#### `Slide1Generator`
- Tính toán các KPI metrics
- Lấy top negative topics
- Generate insight qua LLM
- Return structured data

#### `Slide2Generator`
- Tính trendline theo ngày
- Detect peak day
- Phân tích peak day topics
- Generate insight về xu hướng

#### `Slide4Generator`
- Phân tích sentiment distribution
- Phân tích brand attributes
- Build evidence với URL mapping
- Generate insight và replace URL keys

### 6. Orchestration Layer (`report_generator.py`)
Class `ReportGenerator`:
- Khởi tạo tất cả components
- Orchestrate việc tạo từng slide
- Combine thành report hoàn chỉnh
- Save to JSON

## Cách sử dụng

### 1. Cấu hình

Chỉnh sửa `config.py`:
```python
FILE_PATH = "path/to/your/data.xlsx"
REPORT_DATE = "2026-02-01"
COMPARE_DATE = "2026-01-31"
BRAND_NAME = "Your Brand"
```

### 2. Set API credentials

```bash
export API_KEY="your_api_key"
export BASE_URL="your_base_url"
```

### 3. Chạy report generation

```python
from test.report_generator import ReportGenerator

# Initialize
generator = ReportGenerator(api_key="...", base_url="...")

# Generate report
report = generator.generate_and_save("output.json")
```

Hoặc chạy trực tiếp:
```bash
python test/report_generator.py
```

### 4. Render HTML

```python
from test.template_renderer import TemplateRenderer
import json

# Load report data
with open('output.json', 'r') as f:
    data = json.load(f)

# Render template
renderer = TemplateRenderer('test/template_parameterized.html')
renderer.render_to_file(data, 'final_report.html')
```

## Cấu trúc Output JSON

```json
{
  "report_metadata": {
    "brand": "Brand Name",
    "report_date": "2026-02-01",
    "compare_date": "2026-01-31",
    "generated_at": "2026-02-05T..."
  },
  "slide_1": {
    "title": "...",
    "subtitle": "...",
    "data": [...],
    "insight": "..."
  },
  "slide_2": {
    "title": "...",
    "trendline": [...],
    "peak_day": {...},
    "insight": "..."
  },
  "slide_4": {
    "title": "...",
    "sentiment_distribution": [...],
    "attribute_sentiment": [...],
    "insight": "..."
  }
}
```

## Tùy chỉnh

### Thay đổi prompts
Chỉnh sửa functions trong `prompts.py`

### Thay đổi logic tính toán
Chỉnh sửa methods trong các Generator classes trong `slide_generators.py`

### Thêm slide mới
1. Tạo prompt function trong `prompts.py`
2. Tạo Generator class trong `slide_generators.py`
3. Thêm vào `ReportGenerator.generate_report()`

### Thay đổi cấu hình
Chỉnh sửa constants trong `config.py`

## Ưu điểm của kiến trúc mới

1. **Separation of Concerns**: Mỗi module có trách nhiệm rõ ràng
2. **Maintainability**: Dễ maintain và debug
3. **Testability**: Dễ viết unit tests cho từng component
4. **Reusability**: Có thể reuse các components
5. **Flexibility**: Dễ thay đổi và mở rộng
6. **Prompt Management**: Prompts được quản lý tập trung
7. **Configuration**: Config tập trung, dễ thay đổi

## Dependencies

```
pandas
openpyxl
openai
```

Install:
```bash
pip install pandas openpyxl openai
```

## Lưu ý

- File dữ liệu Excel cần có các columns: PublishedDate, Type, Sentiment, Labels, UrlTopic, Title, Content, Description, Reactions, Shares, Comments, Views
- API_KEY và BASE_URL cần được set trong environment variables
- Prompts được viết bằng tiếng Việt, có thể customize trong `prompts.py`
