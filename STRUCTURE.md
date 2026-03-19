# Cấu trúc dự án sau khi refactor

## Tổng quan
Dự án đã được tổ chức lại thành cấu trúc thư mục logic để dễ bảo trì và phát triển.

## Cấu trúc thư mục

```
/
├── core/                          # Các module cốt lõi được chia sẻ
│   ├── __init__.py
│   ├── config.py                  # Cấu hình chung
│   ├── data_loader.py             # Xử lý dữ liệu Excel
│   └── llm_client.py              # Client LLM API
│
├── generators/                    # Logic tạo báo cáo
│   ├── __init__.py
│   ├── daily/                     # Báo cáo hàng ngày (6 slides)
│   │   ├── __init__.py
│   │   ├── report_generator.py    # Orchestrator báo cáo daily
│   │   ├── slide_generators.py    # 6 slide generators
│   │   ├── generate_slide_prompt.py # Tạo prompt từ dữ liệu
│   │   └── prompts.py             # Template prompts cho LLM
│   │
│   └── weekly/                    # Báo cáo hàng tuần (12 slides)
│       ├── __init__.py
│       ├── report_generator_weekly.py # Orchestrator báo cáo weekly
│       ├── slide_generators_weekly.py # 12 slide generators
│       ├── generate_slide_prompt_weekly.py # Tạo prompt từ dữ liệu
│       └── prompts_weekly.py      # Template prompts cho LLM
│
├── interfaces/                    # Giao diện người dùng
│   ├── __init__.py
│   ├── app.py                     # Streamlit app daily
│   ├── app_weekly.py              # Streamlit app weekly
│   └── api_server.py              # FastAPI REST server
│
├── deployment/                    # Cấu hình triển khai
│   ├── __init__.py
│   ├── docker/                    # Docker files
│   │   ├── __init__.py
│   │   ├── Dockerfile             # Daily Streamlit
│   │   ├── Dockerfile.api         # FastAPI server
│   │   └── Dockerfile.weekly      # Weekly Streamlit
│   ├── docker-compose.yml         # Daily + API services
│   ├── docker-compose.weekly.yml  # Weekly service
│   ├── docker-compose.api.yml     # API only service
│   ├── nginx.conf                 # Nginx config
│   └── nginx.api.conf             # Nginx API config
│
├── uploads/                       # Thư mục upload files
├── logs/                          # Thư mục logs
├── .kiro/                         # Kiro IDE config
├── requirements.txt               # Dependencies cho Streamlit
├── requirements_api.txt           # Dependencies cho API
├── Makefile                       # Build commands
├── run.sh                         # Quick start script
├── README.md                      # Hướng dẫn sử dụng
├── STRUCTURE.md                   # Tài liệu này
├── .env                           # Environment variables (ở thư mục gốc)
├── .env.example                   # Template env file (ở thư mục gốc)
└── .dockerignore                  # Docker ignore rules
```

## Lợi ích của cấu trúc mới

### 1. **Tách biệt rõ ràng các concerns**
- **core/**: Logic chung được chia sẻ
- **generators/**: Logic tạo báo cáo (daily vs weekly)
- **interfaces/**: Giao diện người dùng (Streamlit, API)
- **deployment/**: Cấu hình triển khai

### 2. **Giảm code duplication**
- Các module core được chia sẻ giữa daily và weekly
- Import paths rõ ràng và nhất quán

### 3. **Dễ bảo trì**
- Mỗi thư mục có trách nhiệm cụ thể
- Dễ tìm và sửa lỗi
- Dễ thêm tính năng mới

### 4. **Scalable**
- Dễ thêm loại báo cáo mới (monthly, quarterly)
- Dễ thêm interface mới (CLI, web dashboard)
- Dễ thêm deployment target mới

## Thay đổi chính

### Import statements
Tất cả import đã được cập nhật để sử dụng đường dẫn mới:
```python
# Trước
from config import *
from data_loader import DataLoader

# Sau  
from core.config import *
from core.data_loader import DataLoader
```

### Docker configuration
- Dockerfile được di chuyển vào `deployment/docker/`
- Docker-compose files được di chuyển vào `deployment/`
- Build context được cập nhật để trỏ đúng thư mục

### Makefile commands
Tất cả lệnh docker-compose đã được cập nhật:
```bash
# Trước
docker-compose up --build

# Sau
docker-compose -f deployment/docker-compose.yml up --build
```

## Cách sử dụng

### Quick start
```bash
# Chạy daily service
make run

# Chạy weekly service  
make run-weekly

# Hoặc sử dụng script
./run.sh
```

### Development
```bash
# Build images
make build
make build-weekly

# View logs
make logs
make logs-weekly

# Clean up
make clean
make clean-weekly
```

## Backward compatibility

Cấu trúc mới vẫn giữ nguyên:
- Tất cả logic và prompt templates
- API endpoints và responses
- Environment variables
- Docker port mappings
- Streamlit interfaces

Chỉ thay đổi cách tổ chức file và import paths.

## Lưu ý quan trọng

### Vị trí file cấu hình
- File `.env` và `.env.example` vẫn ở **thư mục gốc** của dự án
- Các file docker-compose trong `deployment/` sẽ tham chiếu đến `../.env`
- Điều này đảm bảo cấu hình environment được chia sẻ giữa tất cả services

### Chạy docker-compose
Khi chạy từ thư mục gốc:
```bash
# Đúng - từ thư mục gốc
docker-compose -f deployment/docker-compose.yml up

# Sai - từ thư mục deployment (sẽ không tìm thấy .env)
cd deployment && docker-compose up
```

### Sử dụng Makefile
Makefile đã được cập nhật để chạy từ thư mục gốc:
```bash
make run      # Chạy daily service
make run-weekly  # Chạy weekly service
```

### Xử lý file .env
Do cấu trúc thư mục mới, file `.env` được xử lý như sau:

1. **File gốc**: `.env` ở thư mục root chứa cấu hình chính
2. **File copy**: `deployment/.env` được tự động copy từ file gốc khi chạy
3. **Makefile và run.sh** tự động copy `.env` sang `deployment/.env` trước khi chạy docker-compose
4. **Gitignore**: Cả hai file `.env` và `deployment/.env` đều được ignore

**Lưu ý**: Chỉ cần chỉnh sửa file `.env` ở thư mục gốc, file trong deployment sẽ được tự động cập nhật.