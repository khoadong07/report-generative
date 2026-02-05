# Template HTML Report System

Hệ thống template HTML được tham số hóa để tạo báo cáo phân tích thương hiệu với 4 slide chính.

## Cấu trúc Files

- `template_parameterized.html` - Template HTML chính với các biến được tham số hóa
- `sample_data.json` - File JSON mẫu chứa dữ liệu để render template
- `template_renderer.py` - Script Python để render template với dữ liệu JSON
- `rendered_report.html` - File HTML được render (sẽ được tạo sau khi chạy script)

## Cấu trúc Template

Template bao gồm 4 slide:

### Slide 1: KPI Overview
- Tiêu đề và phụ đề
- 6 thẻ KPI với giá trị, thay đổi và màu sắc
- Phần insight chính

### Slide 2: Trendline
- Biểu đồ đường thể hiện xu hướng theo thời gian
- Phần phân tích xu hướng

### Slide 3: Channel Breakdown  
- Biểu đồ cột thể hiện phân bổ theo kênh
- Phần insight theo kênh

### Slide 4: Sentiment & Brand Attribute
- Biểu đồ tròn cho sentiment
- Biểu đồ cột xếp chồng cho thuộc tính thương hiệu
- Phần phân tích sentiment

## Cấu trúc Dữ liệu JSON

```json
{
  "report_title": "Tiêu đề báo cáo",
  "slide1": {
    "title": "Tiêu đề slide 1",
    "subtitle": "Phụ đề slide 1", 
    "kpi_cards": [
      {
        "label": "Tên KPI",
        "value": "Giá trị",
        "change": "% thay đổi",
        "change_positive": true/false
      }
    ],
    "insight": {
      "title": "Tiêu đề insight",
      "content": "Nội dung insight"
    }
  },
  "slide2": {
    "title": "Tiêu đề slide 2",
    "subtitle": "Phụ đề slide 2",
    "chart": {
      "title": "Tiêu đề biểu đồ",
      "labels": ["Nhãn 1", "Nhãn 2", ...],
      "dataset": {
        "label": "Tên dataset",
        "data": [giá trị 1, giá trị 2, ...]
      }
    },
    "insight": {
      "title": "Tiêu đề insight",
      "content": "Nội dung insight"
    }
  },
  "slide3": {
    "title": "Tiêu đề slide 3",
    "subtitle": "Phụ đề slide 3",
    "chart": {
      "title": "Tiêu đề biểu đồ",
      "labels": ["Kênh 1", "Kênh 2", ...],
      "data": [giá trị 1, giá trị 2, ...],
      "colors": ["#màu1", "#màu2", ...]
    },
    "insight": {
      "title": "Tiêu đề insight", 
      "content": "Nội dung insight"
    }
  },
  "slide4": {
    "title": "Tiêu đề slide 4",
    "subtitle": "Phụ đề slide 4",
    "pie_chart": {
      "title": "Tiêu đề biểu đồ tròn",
      "labels": ["Nhãn 1", "Nhãn 2", "Nhãn 3"],
      "data": [giá trị 1, giá trị 2, giá trị 3]
    },
    "bar_chart": {
      "title": "Tiêu đề biểu đồ cột",
      "labels": ["Thuộc tính 1", "Thuộc tính 2", ...],
      "datasets": {
        "negative": [giá trị negative cho mỗi thuộc tính],
        "neutral": [giá trị neutral cho mỗi thuộc tính], 
        "positive": [giá trị positive cho mỗi thuộc tính]
      }
    },
    "insight": {
      "title": "Tiêu đề insight",
      "content": "Nội dung insight"
    }
  }
}
```

## Cách sử dụng

### 1. Chuẩn bị dữ liệu JSON
Tạo file JSON theo cấu trúc mẫu trong `sample_data.json`

### 2. Render template
```bash
python test/template_renderer.py
```

### 3. Xem kết quả
Mở file `test/rendered_report.html` trong trình duyệt

## Tính năng Template

- **Navigation**: Có nút điều hướng giữa các slide
- **Responsive Charts**: Sử dụng Chart.js cho biểu đồ tương tác
- **Styling**: Sử dụng Tailwind CSS và Inter font
- **Conditional Rendering**: Hỗ trợ hiển thị có điều kiện (màu sắc thay đổi KPI)
- **Loop Rendering**: Hỗ trợ vòng lặp cho danh sách KPI cards

## Tùy chỉnh

### Thay đổi màu sắc
Chỉnh sửa các class CSS trong phần `<style>` của template

### Thêm slide mới
1. Thêm HTML structure cho slide mới
2. Thêm navigation button
3. Thêm chart initialization function nếu cần
4. Cập nhật cấu trúc JSON data

### Thay đổi biểu đồ
Chỉnh sửa các function `initBuzzChart()`, `initChannelChart()`, `initSentimentCharts()` để tùy chỉnh biểu đồ

## Dependencies

- Chart.js (loaded via CDN)
- Tailwind CSS (loaded via CDN)  
- Font Awesome (loaded via CDN)
- Google Fonts - Inter (loaded via CDN)

Tất cả dependencies được load qua CDN nên không cần cài đặt thêm gì.