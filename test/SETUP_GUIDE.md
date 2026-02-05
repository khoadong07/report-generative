# Hướng dẫn Setup và Chạy Report Generation System

## Bước 1: Cài đặt Dependencies

### 1.1. Kiểm tra Python version
```bash
python --version
# Yêu cầu: Python 3.8+
```

### 1.2. Cài đặt các thư viện cần thiết
```bash
pip install pandas openpyxl openai
```

Hoặc nếu có file requirements:
```bash
pip install -r requirements.txt
```

## Bước 2: Chuẩn bị Dữ liệu

### 2.1. File Excel
Đảm bảo file Excel có các columns sau:
- `PublishedDate` - Ngày đăng (datetime)
- `Type` - Loại bài đăng
- `Sentiment` - Cảm xúc (Positive/Negative/Neutral)
- `Labels` - Nhãn phân loại (cách nhau bởi dấu phẩy)
- `UrlTopic` - URL của bài đăng
- `Title` - Tiêu đề
- `Content` - Nội dung
- `Description` - Mô tả
- `Reactions` - Số lượt reaction
- `Shares` - Số lượt share
- `Comments` - Số bình luận
- `Views` - Số lượt xem

### 2.2. Cập nhật đường dẫn file
Mở file `test/config.py` và cập nhật:
```python
FILE_PATH = "path/to/your/data.xlsx"  # Đường dẫn đến file Excel của bạn
```

## Bước 3: Cấu hình API

### 3.1. Lấy API credentials
Bạn cần có:
- `API_KEY` - API key cho LLM service
- `BASE_URL` - Base URL của LLM API endpoint

### 3.2. Set environment variables

**Trên macOS/Linux:**
```bash
export API_KEY="your_api_key_here"
export BASE_URL="your_base_url_here"
```

**Hoặc tạo file `.env` trong thư mục test:**
```bash
# test/.env
API_KEY=your_api_key_here
BASE_URL=your_base_url_here
```

Nếu dùng file `.env`, cần cài thêm:
```bash
pip install python-dotenv
```

Và thêm vào đầu file `report_generator.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Bước 4: Cấu hình Report

Mở file `test/config.py` và điều chỉnh:

```python
# Ngày báo cáo
REPORT_DATE = "2026-02-01"  # Ngày bạn muốn phân tích
COMPARE_DATE = "2026-01-31"  # Ngày để so sánh

# Tên thương hiệu
BRAND_NAME = "Nestlé"  # Thay bằng tên thương hiệu của bạn

# Số lượng phân tích
TOP_N_TOPICS = 6  # Số lượng topics để phân tích
TOP_N_ATTRIBUTES = 6  # Số lượng attributes để phân tích
LOOKBACK_DAYS = 6  # Số ngày nhìn lại cho trendline
```

## Bước 5: Chạy Report Generation

### 5.1. Chạy full report
```bash
cd /path/to/your/project
python test/report_generator.py
```

Output sẽ được lưu vào `test/report_output.json`

### 5.2. Chạy với custom output path
```python
from test.report_generator import ReportGenerator
import os

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")

generator = ReportGenerator(api_key, base_url)
report = generator.generate_and_save("my_custom_report.json")
```

### 5.3. Chạy từng slide riêng lẻ
```python
from test.report_generator import ReportGenerator
import os

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")

generator = ReportGenerator(api_key, base_url)

# Load data
df = generator.data_loader.preprocess()
report_df = generator.data_loader.filter_by_date("2026-02-01")
compare_df = generator.data_loader.filter_by_date("2026-01-31")

# Generate only Slide 1
slide1 = generator.slide1_gen.generate(
    report_df, compare_df,
    "Nestlé", "2026-02-01", "2026-01-31"
)
print(slide1)
```

## Bước 6: Render HTML Report

### 6.1. Từ JSON đã generate
```bash
python -c "
from test.template_renderer import TemplateRenderer
import json

# Load report data
with open('test/report_output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Render
renderer = TemplateRenderer('test/template_parameterized.html')
renderer.render_to_file(data, 'test/final_report.html')
print('HTML rendered successfully!')
"
```

### 6.2. Xem kết quả
Mở file `test/final_report.html` trong trình duyệt:
```bash
open test/final_report.html  # macOS
# hoặc
xdg-open test/final_report.html  # Linux
# hoặc mở trực tiếp trong browser
```

## Bước 7: Chạy Examples

```bash
python test/example_usage.py
```

## Troubleshooting

### Lỗi: ModuleNotFoundError
```bash
# Cài đặt lại dependencies
pip install pandas openpyxl openai
```

### Lỗi: API_KEY not found
```bash
# Kiểm tra environment variables
echo $API_KEY
echo $BASE_URL

# Nếu rỗng, set lại
export API_KEY="your_key"
export BASE_URL="your_url"
```

### Lỗi: File not found
```bash
# Kiểm tra đường dẫn file trong config.py
# Đảm bảo file Excel tồn tại
ls -la /path/to/your/data.xlsx
```

### Lỗi: Import error
```bash
# Đảm bảo bạn đang ở đúng thư mục
cd /path/to/project/root

# Hoặc thêm project root vào PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/project/root"
```

### Lỗi: Date parsing
Đảm bảo format ngày trong Excel là datetime hợp lệ. Nếu không, có thể cần convert:
```python
# Trong Excel, format cột PublishedDate thành datetime
# Hoặc trong code, thêm format parameter:
df["PublishedDate"] = pd.to_datetime(df["PublishedDate"], format="%Y-%m-%d %H:%M:%S")
```

## Quick Start Script

Tạo file `test/run_report.sh`:
```bash
#!/bin/bash

# Set API credentials
export API_KEY="your_api_key_here"
export BASE_URL="your_base_url_here"

# Run report generation
echo "Generating report..."
python test/report_generator.py

# Render HTML
echo "Rendering HTML..."
python -c "
from test.template_renderer import TemplateRenderer
import json

with open('test/report_output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

renderer = TemplateRenderer('test/template_parameterized.html')
renderer.render_to_file(data, 'test/final_report.html')
"

echo "Done! Open test/final_report.html in your browser"
```

Chạy:
```bash
chmod +x test/run_report.sh
./test/run_report.sh
```

## Workflow Tổng Quát

```
1. Chuẩn bị dữ liệu Excel
   ↓
2. Cấu hình config.py (dates, brand, file path)
   ↓
3. Set API credentials (API_KEY, BASE_URL)
   ↓
4. Chạy report_generator.py → tạo JSON
   ↓
5. Chạy template_renderer.py → tạo HTML
   ↓
6. Mở HTML trong browser để xem kết quả
```

## Cấu trúc Output

```
test/
├── report_output.json      # JSON data từ report generator
├── final_report.html        # HTML report đã render
└── logs/                    # Logs (nếu có)
```

## Tips

1. **Test với dữ liệu nhỏ trước**: Thử với 1-2 ngày dữ liệu để kiểm tra
2. **Check prompts**: Xem file `prompts.py` để hiểu LLM đang được hỏi gì
3. **Debug mode**: Thêm print statements để theo dõi quá trình
4. **Cache results**: Lưu intermediate results để không phải chạy lại từ đầu
5. **Monitor API usage**: Theo dõi số lượng API calls để tránh vượt quota

## Support

Nếu gặp vấn đề, kiểm tra:
1. Python version (>= 3.8)
2. Dependencies đã cài đủ chưa
3. API credentials đúng chưa
4. File path trong config.py đúng chưa
5. Format dữ liệu Excel đúng chưa
