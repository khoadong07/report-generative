# Masan Weekly Report - Docker Guide

## Chạy với Docker Compose

### 1. Build và Start

```bash
# Từ thư mục deployment
cd deployment

# Build và start cả 2 services (weekly + masan)
docker-compose -f docker-compose.weekly.yml up -d

# Hoặc chỉ start service masan
docker-compose -f docker-compose.weekly.yml up -d streamlit-masan
```

### 2. Truy cập

- **Weekly Report**: http://localhost:8523
- **Masan Report**: http://localhost:8524

### 3. Xem logs

```bash
# Xem logs của masan service
docker-compose -f docker-compose.weekly.yml logs -f streamlit-masan

# Xem logs của cả 2 services
docker-compose -f docker-compose.weekly.yml logs -f
```

### 4. Stop services

```bash
# Stop tất cả services
docker-compose -f docker-compose.weekly.yml down

# Stop chỉ masan service
docker-compose -f docker-compose.weekly.yml stop streamlit-masan
```

### 5. Rebuild sau khi thay đổi code

```bash
# Rebuild và restart
docker-compose -f docker-compose.weekly.yml up -d --build streamlit-masan
```

## Cấu trúc Services

### streamlit-weekly
- Port: 8523
- Container: slide-prompt-generator-weekly
- App: weekly_report/app.py

### streamlit-masan
- Port: 8524
- Container: slide-prompt-generator-masan
- App: weekly_report_masan/app.py

## Environment Variables

Đảm bảo file `.env` trong thư mục `deployment/` có các biến:

```
API_KEY=your_api_key
BASE_URL=your_base_url
MODEL=meta-llama/Meta-Llama-3.1-70B-Instruct
```

## Troubleshooting

### Service không start

```bash
# Kiểm tra logs
docker-compose -f docker-compose.weekly.yml logs streamlit-masan

# Kiểm tra container status
docker ps -a | grep masan
```

### Port đã được sử dụng

Thay đổi port trong `docker-compose.weekly.yml`:

```yaml
ports:
  - "8525:8501"  # Thay 8524 thành port khác
```

### Rebuild từ đầu

```bash
# Xóa container và image cũ
docker-compose -f docker-compose.weekly.yml down
docker rmi slide-prompt-generator-masan

# Build lại
docker-compose -f docker-compose.weekly.yml up -d --build
```

## Health Check

Services có health check tự động:
- Interval: 30s
- Timeout: 10s
- Retries: 3

Kiểm tra health:

```bash
docker inspect --format='{{.State.Health.Status}}' slide-prompt-generator-masan
```

## Volumes

- `../uploads:/app/uploads` - Thư mục upload files
- `.env:/app/.env:ro` - Environment variables (read-only)

## Network

Cả 2 services chạy trên cùng network `app-network` để có thể giao tiếp với nhau nếu cần.
