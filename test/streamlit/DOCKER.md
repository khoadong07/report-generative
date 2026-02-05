# 🐳 Docker Deployment Guide

Complete guide để deploy Streamlit app với Docker.

## 📋 Prerequisites

- Docker installed (version 20.10+)
- Docker Compose installed (version 2.0+)
- `.env` file với API credentials

## 🚀 Quick Start

### 1. Chuẩn bị môi trường

```bash
cd test/streamlit

# Copy .env.example và điền API credentials
cp .env.example .env
nano .env  # hoặc vim, code, etc.
```

### 2. Build và chạy

```bash
# Build image
make build

# Run container
make run

# Hoặc dùng docker-compose trực tiếp
docker-compose up -d
```

### 3. Truy cập app

Mở browser: **http://localhost:8501**

## 📦 Docker Commands

### Using Makefile (Recommended)

```bash
# Build image
make build

# Run development
make run

# Run production (with nginx)
make run-prod

# Stop container
make stop

# Restart
make restart

# View logs
make logs
make logs-f  # follow logs

# Shell access
make shell

# Clean up
make clean
make clean-all  # including volumes
```

### Using Docker Compose

```bash
# Build and run
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Shell access
docker-compose exec streamlit-app bash
```

### Using Docker directly

```bash
# Build
docker build -t slide-prompt-generator .

# Run
docker run -d \
  --name slide-prompt-generator \
  -p 8501:8501 \
  --env-file .env \
  -v $(pwd)/uploads:/app/uploads \
  slide-prompt-generator

# Stop
docker stop slide-prompt-generator

# Remove
docker rm slide-prompt-generator
```

## 🏗️ Architecture

### Development Setup

```
┌─────────────────┐
│   Browser       │
│  localhost:8501 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Streamlit App  │
│   Container     │
│   Port 8501     │
└─────────────────┘
```

### Production Setup (with Nginx)

```
┌─────────────────┐
│   Browser       │
│  localhost:80   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Nginx Proxy    │
│   Container     │
│   Port 80/443   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Streamlit App  │
│   Container     │
│   Port 8501     │
└─────────────────┘
```

## 📁 File Structure

```
test/streamlit/
├── Dockerfile              # Main Docker image
├── docker-compose.yml      # Development setup
├── docker-compose.prod.yml # Production setup
├── .dockerignore          # Files to exclude
├── nginx.conf             # Nginx configuration
├── Makefile               # Convenient commands
├── .env                   # Environment variables (create this)
├── .env.example           # Template
├── requirements.txt       # Python dependencies
├── app.py                 # Main Streamlit app
└── uploads/               # Uploaded files (created at runtime)
```

## 🔧 Configuration

### Environment Variables

Create `.env` file:

```bash
# API Configuration
API_KEY=your_api_key_here
BASE_URL=your_base_url_here

# Streamlit Configuration (optional)
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
```

### Docker Compose Variables

Edit `docker-compose.yml` to customize:

```yaml
ports:
  - "8501:8501"  # Change external port if needed

volumes:
  - ./uploads:/app/uploads  # Persist uploaded files

environment:
  - API_KEY=${API_KEY}
  - BASE_URL=${BASE_URL}
```

## 🔒 Production Deployment

### 1. Use Production Compose File

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 2. Enable HTTPS (Optional)

Generate SSL certificates:

```bash
# Create ssl directory
mkdir -p ssl

# Generate self-signed certificate (for testing)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/key.pem -out ssl/cert.pem

# For production, use Let's Encrypt
# certbot certonly --standalone -d yourdomain.com
```

Uncomment HTTPS section in `nginx.conf`.

### 3. Resource Limits

Edit `docker-compose.prod.yml`:

```yaml
deploy:
  resources:
    limits:
      cpus: '2'      # Max 2 CPUs
      memory: 2G     # Max 2GB RAM
    reservations:
      cpus: '1'      # Min 1 CPU
      memory: 1G     # Min 1GB RAM
```

## 📊 Monitoring

### View Logs

```bash
# All logs
docker-compose logs

# Follow logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Specific service
docker-compose logs streamlit-app
```

### Resource Usage

```bash
# Container stats
docker stats slide-prompt-generator

# Using make
make stats
```

### Health Check

```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' slide-prompt-generator

# Manual health check
curl http://localhost:8501/_stcore/health
```

## 🐛 Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs

# Check if port is in use
lsof -i :8501

# Remove old container
docker-compose down
docker-compose up -d
```

### API credentials not working

```bash
# Verify .env file exists
ls -la .env

# Check environment variables in container
docker-compose exec streamlit-app env | grep API
```

### Upload fails

```bash
# Check uploads directory permissions
ls -la uploads/

# Fix permissions
chmod 777 uploads/
```

### Out of memory

```bash
# Increase memory limit in docker-compose.prod.yml
deploy:
  resources:
    limits:
      memory: 4G  # Increase to 4GB
```

## 🔄 Updates and Maintenance

### Update Application

```bash
# Pull latest code
git pull

# Rebuild and restart
make rebuild

# Or manually
docker-compose down
docker-compose build
docker-compose up -d
```

### Update Dependencies

```bash
# Edit requirements.txt
nano requirements.txt

# Rebuild image
make build

# Restart
make restart
```

### Backup Data

```bash
# Backup uploads directory
tar -czf uploads-backup-$(date +%Y%m%d).tar.gz uploads/

# Backup .env
cp .env .env.backup
```

## 🧪 Testing

### Test Container

```bash
# Run tests inside container
docker-compose exec streamlit-app python -m pytest

# Or using make
make test
```

### Test API Connection

```bash
# Shell into container
make shell

# Test API
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('API_KEY:', os.getenv('API_KEY')[:10] + '...')
print('BASE_URL:', os.getenv('BASE_URL'))
"
```

## 📈 Performance Optimization

### 1. Multi-stage Build (Optional)

Create `Dockerfile.optimized`:

```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["streamlit", "run", "app.py"]
```

### 2. Use Docker BuildKit

```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Build with cache
docker-compose build --build-arg BUILDKIT_INLINE_CACHE=1
```

### 3. Optimize Image Size

```bash
# Check image size
docker images slide-prompt-generator

# Remove unused layers
docker image prune -a
```

## 🌐 Cloud Deployment

### AWS ECS

```bash
# Build for ARM (if using Graviton)
docker buildx build --platform linux/arm64 -t slide-prompt-generator .

# Push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <ecr-url>
docker tag slide-prompt-generator:latest <ecr-url>/slide-prompt-generator:latest
docker push <ecr-url>/slide-prompt-generator:latest
```

### Google Cloud Run

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT-ID/slide-prompt-generator

# Deploy
gcloud run deploy slide-prompt-generator \
  --image gcr.io/PROJECT-ID/slide-prompt-generator \
  --platform managed \
  --port 8501
```

### DigitalOcean App Platform

```bash
# Use docker-compose.yml
# Deploy via DigitalOcean dashboard or doctl CLI
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Streamlit Docker Guide](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker)
- [Nginx Documentation](https://nginx.org/en/docs/)

## 🆘 Support

Nếu gặp vấn đề:

1. Check logs: `make logs-f`
2. Verify .env file
3. Check port availability
4. Review Docker/Compose versions
5. Check system resources (RAM, CPU, disk)
