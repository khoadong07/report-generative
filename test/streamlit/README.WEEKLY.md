# Weekly Report Generator - Docker Setup

Hướng dẫn chạy Weekly Report Generator với Docker Compose.

## 📋 Yêu cầu

- Docker (version 20.10+)
- Docker Compose (version 2.0+)
- File `.env` với API credentials

## 🚀 Cách sử dụng

### 1. Chuẩn bị môi trường

Tạo file `.env` từ template (nếu chưa có):

```bash
cp .env.example .env
```

Chỉnh sửa file `.env` với thông tin API của bạn:

```env
API_KEY=your_api_key_here
BASE_URL=https://api.openai.com/v1
```

### 2. Chạy với Docker Compose

#### Cách 1: Sử dụng script (Khuyến nghị)

```bash
# Cấp quyền thực thi
chmod +x docker-run-weekly.sh

# Chạy script
./docker-run-weekly.sh
```

#### Cách 2: Sử dụng Makefile

```bash
# Build và chạy
make build-weekly
make run-weekly

# Hoặc rebuild toàn bộ
make rebuild-weekly
```

#### Cách 3: Sử dụng Docker Compose trực tiếp

```bash
# Development mode
docker-compose -f docker-compose.weekly.yml up -d

# Production mode
docker-compose -f docker-compose.prod.weekly.yml up -d
```

### 3. Truy cập ứng dụng

Mở trình duyệt và truy cập:

```
http://localhost:8523
```

## 📊 Quản lý container

### Xem logs

```bash
# Xem logs
make logs-weekly

# Theo dõi logs real-time
make logs-weekly-f

# Hoặc dùng docker-compose
docker-compose -f docker-compose.weekly.yml logs -f
```

### Kiểm tra trạng thái

```bash
make status-weekly

# Hoặc
docker-compose -f docker-compose.weekly.yml ps
```

### Restart container

```bash
make restart-weekly

# Hoặc
docker-compose -f docker-compose.weekly.yml restart
```

### Dừng container

```bash
make stop-weekly

# Hoặc
docker-compose -f docker-compose.weekly.yml down
```

### Truy cập shell trong container

```bash
make shell-weekly

# Hoặc
docker-compose -f docker-compose.weekly.yml exec streamlit-weekly /bin/bash
```

## 🔧 Cấu hình

### Ports

- **Development**: `8523:8501`
- **Production**: `8523:8501`

### Volumes

- `./uploads:/app/uploads` - Lưu trữ file upload
- `./.env:/app/.env:ro` - Mount file .env (read-only)

### Environment Variables

Các biến môi trường được load từ file `.env`:

- `API_KEY` - API key cho LLM
- `BASE_URL` - Base URL cho LLM API

## 🏗️ Cấu trúc files

```
.
├── Dockerfile.weekly              # Dockerfile cho weekly app
├── docker-compose.weekly.yml      # Docker compose (development)
├── docker-compose.prod.weekly.yml # Docker compose (production)
├── docker-run-weekly.sh           # Script chạy nhanh
├── app_weekly.py                  # Streamlit app chính
├── report_generator_weekly.py     # Report generator
├── slide_generators_weekly.py     # Slide generators
├── prompts_weekly.py              # Prompt templates
└── generate_slide_prompt_weekly.py # Prompt generator
```

## 🐛 Troubleshooting

### Container không start

```bash
# Xem logs để debug
docker-compose -f docker-compose.weekly.yml logs

# Kiểm tra .env file
cat .env
```

### Port đã được sử dụng

Nếu port 8523 đã được sử dụng, chỉnh sửa trong `docker-compose.weekly.yml`:

```yaml
ports:
  - "8524:8501"  # Đổi sang port khác
```

### Rebuild từ đầu

```bash
# Xóa container và image cũ
make clean-weekly

# Build lại
make build-weekly

# Chạy lại
make run-weekly
```

### Xóa toàn bộ (bao gồm volumes)

```bash
docker-compose -f docker-compose.weekly.yml down -v
docker rmi streamlit_streamlit-weekly:latest
```

## 📝 So sánh Daily vs Weekly

| Feature | Daily Report | Weekly Report |
|---------|-------------|---------------|
| Port | 8522 | 8523 |
| App File | `app.py` | `app_weekly.py` |
| Dockerfile | `Dockerfile` | `Dockerfile.weekly` |
| Compose File | `docker-compose.yml` | `docker-compose.weekly.yml` |
| Slides | 12 slides | 10 slides |
| Time Range | 24 hours | 7 days |

## 🔐 Production Deployment

Để deploy production:

1. Sử dụng file production compose:
```bash
docker-compose -f docker-compose.prod.weekly.yml up -d
```

2. Cấu hình resource limits đã được set:
   - CPU: 1-2 cores
   - Memory: 1-2GB

3. Logging được cấu hình với rotation:
   - Max size: 10MB
   - Max files: 3

4. Health check tự động mỗi 30s

## 📞 Support

Nếu gặp vấn đề, kiểm tra:

1. Docker và Docker Compose đã cài đặt đúng
2. File `.env` có đầy đủ thông tin
3. Port 8523 không bị chiếm dụng
4. Có đủ dung lượng disk cho Docker images

## 🎯 Quick Commands Reference

```bash
# Start
make run-weekly

# Stop
make stop-weekly

# Logs
make logs-weekly-f

# Restart
make restart-weekly

# Clean
make clean-weekly

# Rebuild
make rebuild-weekly
```
