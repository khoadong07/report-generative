# 🔧 Docker Troubleshooting Guide

## ❌ Error: requirements.txt not found

### Problem
```
failed to solve: failed to compute cache key: "/requirements.txt": not found
```

### Solutions

#### 1. Check .dockerignore
File `.dockerignore` có thể đang loại trừ `requirements.txt`.

**Fix:**
```bash
# Edit .dockerignore
nano .dockerignore

# Ensure this line exists:
!requirements.txt
```

#### 2. Verify file exists
```bash
# Check if requirements.txt exists
ls -la requirements.txt

# If not, create it
cat > requirements.txt << EOF
streamlit>=1.28.0
pandas>=2.0.0
openpyxl>=3.1.0
python-dotenv>=1.0.0
requests>=2.31.0
numpy>=1.24.0
EOF
```

#### 3. Clear Docker cache
```bash
# Clear build cache
docker builder prune -a

# Rebuild
docker-compose build --no-cache
```

#### 4. Use simple Dockerfile
```bash
# Try with simplified Dockerfile
docker build -f Dockerfile.simple -t slide-prompt-generator .
```

## ❌ Error: .env file not found

### Problem
App starts but API credentials missing.

### Solution
```bash
# Create .env from example
cp .env.example .env

# Edit with your credentials
nano .env
```

## ❌ Error: Port 8501 already in use

### Problem
```
Error starting userland proxy: listen tcp4 0.0.0.0:8501: bind: address already in use
```

### Solutions

#### 1. Find and stop the process
```bash
# Find process using port 8501
lsof -i :8501

# Kill the process
kill -9 <PID>
```

#### 2. Use different port
```bash
# Edit docker-compose.yml
ports:
  - "8502:8501"  # Use 8502 instead

# Access at http://localhost:8502
```

## ❌ Error: Cannot connect to Docker daemon

### Problem
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

### Solution
```bash
# Start Docker
# On Mac: Open Docker Desktop
# On Linux:
sudo systemctl start docker

# Verify
docker info
```

## ❌ Error: Out of memory

### Problem
Container crashes or becomes unresponsive.

### Solution

#### 1. Increase Docker memory
```bash
# Docker Desktop: Settings > Resources > Memory
# Increase to at least 4GB
```

#### 2. Limit container memory
```yaml
# Edit docker-compose.yml
services:
  streamlit-app:
    deploy:
      resources:
        limits:
          memory: 2G
```

## ❌ Error: Module not found

### Problem
```
ModuleNotFoundError: No module named 'xxx'
```

### Solution

#### 1. Update requirements.txt
```bash
# Add missing module
echo "missing-module>=1.0.0" >> requirements.txt

# Rebuild
docker-compose build
```

#### 2. Install in running container
```bash
# Shell into container
docker-compose exec streamlit-app bash

# Install module
pip install missing-module

# Exit and commit changes
exit
docker commit slide-prompt-generator slide-prompt-generator:latest
```

## ❌ Error: Permission denied

### Problem
```
Permission denied: '/app/uploads'
```

### Solution
```bash
# Create uploads directory with correct permissions
mkdir -p uploads
chmod 777 uploads

# Or in Dockerfile
RUN mkdir -p /app/uploads && chmod 777 /app/uploads
```

## ❌ Error: Build takes too long

### Problem
Docker build is very slow.

### Solutions

#### 1. Use BuildKit
```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Build
docker-compose build
```

#### 2. Use cache
```bash
# Build with cache
docker-compose build --build-arg BUILDKIT_INLINE_CACHE=1
```

#### 3. Reduce image size
```bash
# Use multi-stage build
# See Dockerfile.optimized
```

## 🧪 Testing Commands

### Test Docker setup
```bash
# Run test script
bash docker-test.sh
```

### Test build
```bash
# Build only
docker-compose build

# Build without cache
docker-compose build --no-cache
```

### Test run
```bash
# Run in foreground (see logs)
docker-compose up

# Run in background
docker-compose up -d
```

### Test app
```bash
# Check if app is running
curl http://localhost:8501/_stcore/health

# Expected: {"status": "ok"}
```

## 📊 Debugging Commands

### View logs
```bash
# All logs
docker-compose logs

# Follow logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100
```

### Shell access
```bash
# Open bash in container
docker-compose exec streamlit-app bash

# Or if container is not running
docker run -it --rm slide-prompt-generator bash
```

### Inspect container
```bash
# Container details
docker inspect slide-prompt-generator

# Environment variables
docker exec slide-prompt-generator env

# File system
docker exec slide-prompt-generator ls -la /app
```

### Check resources
```bash
# Container stats
docker stats slide-prompt-generator

# Disk usage
docker system df

# Clean up
docker system prune -a
```

## 🔍 Common Issues

### Issue: App loads but shows errors

**Check:**
1. API credentials in .env
2. Excel file format
3. Python dependencies
4. Container logs

**Debug:**
```bash
# Check environment variables
docker-compose exec streamlit-app env | grep API

# Test Python imports
docker-compose exec streamlit-app python -c "import streamlit; print(streamlit.__version__)"

# Check file permissions
docker-compose exec streamlit-app ls -la /app
```

### Issue: Upload fails

**Check:**
1. Upload directory exists
2. Permissions are correct
3. File size limits

**Fix:**
```bash
# Create uploads directory
docker-compose exec streamlit-app mkdir -p /app/uploads

# Fix permissions
docker-compose exec streamlit-app chmod 777 /app/uploads
```

### Issue: Slow performance

**Optimize:**
1. Increase Docker resources
2. Use SSD for Docker storage
3. Limit concurrent requests
4. Enable caching

## 📞 Getting Help

If issues persist:

1. **Check logs**: `docker-compose logs -f`
2. **Verify setup**: `bash docker-test.sh`
3. **Clean rebuild**: `make clean && make build && make run`
4. **Check Docker version**: `docker --version` (need 20.10+)
5. **Check system resources**: RAM, CPU, disk space

## 🔗 Useful Links

- [Docker Documentation](https://docs.docker.com/)
- [Streamlit Docker Guide](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker)
- [Docker Compose Troubleshooting](https://docs.docker.com/compose/troubleshooting/)
