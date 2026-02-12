# Docker Quick Start Guide

Hướng dẫn nhanh để chạy cả Daily và Weekly Report Generator với Docker.

## 🎯 Chọn phiên bản

### Daily Report (12 slides, 24 giờ)
```bash
# Port: 8522
make run
# hoặc
./docker-run.sh
```

### Weekly Report (10 slides, 7 ngày)
```bash
# Port: 8523
make run-weekly
# hoặc
./docker-run-weekly.sh
```

## ⚡ Quick Commands

### Daily Report

| Command | Description |
|---------|-------------|
| `make build` | Build image |
| `make run` | Start container |
| `make stop` | Stop container |
| `make logs-f` | View logs |
| `make restart` | Restart |
| `make clean` | Clean up |

### Weekly Report

| Command | Description |
|---------|-------------|
| `make build-weekly` | Build image |
| `make run-weekly` | Start container |
| `make stop-weekly` | Stop container |
| `make logs-weekly-f` | View logs |
| `make restart-weekly` | Restart |
| `make clean-weekly` | Clean up |

## 🌐 Access URLs

- **Daily Report**: http://localhost:8522
- **Weekly Report**: http://localhost:8523

## 🔧 Cấu hình ban đầu

1. Copy file `.env`:
```bash
cp .env.example .env
```

2. Chỉnh sửa `.env`:
```env
API_KEY=your_api_key_here
BASE_URL=https://api.openai.com/v1
```

3. Chạy:
```bash
# Daily
make run

# Weekly
make run-weekly
```

## 🚀 Chạy cả hai cùng lúc

```bash
# Start Daily (port 8522)
make run

# Start Weekly (port 8523)
make run-weekly

# Kiểm tra
docker ps
```

## 📊 Monitoring

```bash
# Xem logs Daily
make logs-f

# Xem logs Weekly
make logs-weekly-f

# Xem status
docker ps

# Xem resource usage
docker stats
```

## 🛑 Dừng tất cả

```bash
# Stop Daily
make stop

# Stop Weekly
make stop-weekly

# Hoặc dừng tất cả containers
docker stop $(docker ps -q)
```

## 🧹 Clean up

```bash
# Clean Daily
make clean

# Clean Weekly
make clean-weekly

# Clean tất cả (bao gồm volumes)
make clean-all
docker-compose -f docker-compose.weekly.yml down -v
```

## 🔄 Update code

```bash
# Daily
make rebuild

# Weekly
make rebuild-weekly
```

## 📝 Files quan trọng

```
Daily Report:
├── Dockerfile
├── docker-compose.yml
├── docker-compose.prod.yml
├── app.py
└── docker-run.sh

Weekly Report:
├── Dockerfile.weekly
├── docker-compose.weekly.yml
├── docker-compose.prod.weekly.yml
├── app_weekly.py
└── docker-run-weekly.sh
```

## 🐛 Troubleshooting

### Port conflict
```bash
# Kiểm tra port đang dùng
lsof -i :8522
lsof -i :8523

# Hoặc đổi port trong docker-compose.yml
```

### Container không start
```bash
# Xem logs
docker logs slide-prompt-generator
docker logs slide-prompt-generator-weekly

# Hoặc
make logs
make logs-weekly
```

### Rebuild từ đầu
```bash
# Daily
make clean
make build
make run

# Weekly
make clean-weekly
make build-weekly
make run-weekly
```

## 🎓 Best Practices

1. **Development**: Dùng `make run` và `make run-weekly`
2. **Production**: Dùng `make run-prod` và `make run-weekly-prod`
3. **Logs**: Luôn check logs khi có lỗi
4. **Updates**: Dùng `make rebuild` để update code
5. **Cleanup**: Định kỳ clean unused images/containers

## 📞 Help

```bash
# Xem tất cả commands
make help
```
