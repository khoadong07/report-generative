# Deployment Guide

## Services

### 1. Weekly Report (Port 8523)
- Container: `slide-prompt-generator-weekly`
- App: `weekly_report/app.py`
- URL: http://localhost:8523

### 2. Masan Report (Port 8524)
- Container: `slide-prompt-generator-masan`
- App: `weekly_report_masan/app.py`
- URL: http://localhost:8524

## Quick Start

### Start All Services

```bash
cd deployment
docker-compose -f docker-compose.weekly.yml up -d
```

### Start Individual Service

```bash
# Start only Weekly Report
docker-compose -f docker-compose.weekly.yml up -d streamlit-weekly

# Start only Masan Report
docker-compose -f docker-compose.weekly.yml up -d streamlit-masan
```

## Using Helper Script

Make the script executable first:

```bash
chmod +x run-masan.sh
```

Then use it:

```bash
# Start Masan service
./run-masan.sh start

# Stop Masan service
./run-masan.sh stop

# View logs
./run-masan.sh logs

# Rebuild and restart
./run-masan.sh rebuild

# Check status
./run-masan.sh status

# Open shell in container
./run-masan.sh shell
```

## Environment Setup

Create `.env` file in `deployment/` directory:

```env
API_KEY=your_api_key_here
BASE_URL=https://your-api-url.com
MODEL=meta-llama/Meta-Llama-3.1-70B-Instruct
```

## Common Commands

### View Logs

```bash
# All services
docker-compose -f docker-compose.weekly.yml logs -f

# Specific service
docker-compose -f docker-compose.weekly.yml logs -f streamlit-masan
```

### Stop Services

```bash
# Stop all
docker-compose -f docker-compose.weekly.yml down

# Stop specific service
docker-compose -f docker-compose.weekly.yml stop streamlit-masan
```

### Rebuild After Code Changes

```bash
# Rebuild specific service
docker-compose -f docker-compose.weekly.yml up -d --build streamlit-masan

# Rebuild all services
docker-compose -f docker-compose.weekly.yml up -d --build
```

### Check Service Health

```bash
# Check container status
docker ps | grep slide-prompt-generator

# Check health status
docker inspect --format='{{.State.Health.Status}}' slide-prompt-generator-masan
```

### Access Container Shell

```bash
# Masan container
docker exec -it slide-prompt-generator-masan /bin/bash

# Weekly container
docker exec -it slide-prompt-generator-weekly /bin/bash
```

## Troubleshooting

### Port Already in Use

Change port in `docker-compose.weekly.yml`:

```yaml
ports:
  - "8525:8501"  # Change 8524 to another port
```

### Service Won't Start

1. Check logs:
```bash
docker-compose -f docker-compose.weekly.yml logs streamlit-masan
```

2. Check if .env file exists:
```bash
ls -la .env
```

3. Verify environment variables:
```bash
docker-compose -f docker-compose.weekly.yml config
```

### Clean Rebuild

```bash
# Stop and remove containers
docker-compose -f docker-compose.weekly.yml down

# Remove images
docker rmi deployment-streamlit-masan
docker rmi deployment-streamlit-weekly

# Rebuild
docker-compose -f docker-compose.weekly.yml up -d --build
```

### Check Container Resources

```bash
# CPU and memory usage
docker stats slide-prompt-generator-masan

# Disk usage
docker system df
```

## File Structure

```
deployment/
├── docker/
│   ├── Dockerfile.weekly    # Weekly report Dockerfile
│   └── Dockerfile.masan     # Masan report Dockerfile
├── docker-compose.weekly.yml # Compose file for both services
├── run-masan.sh             # Helper script for Masan service
├── .env                     # Environment variables (create this)
└── README.md                # This file
```

## Network

Both services run on the same Docker network `app-network` for potential inter-service communication.

## Volumes

- `../uploads:/app/uploads` - Shared upload directory
- `.env:/app/.env:ro` - Environment variables (read-only)

## Health Checks

Both services have automatic health checks:
- Interval: 30 seconds
- Timeout: 10 seconds
- Retries: 3
- Start period: 10 seconds

## Production Considerations

1. **Security**:
   - Use secrets management instead of .env files
   - Run containers as non-root user
   - Enable TLS/SSL

2. **Performance**:
   - Adjust resource limits in docker-compose.yml
   - Use production-grade WSGI server
   - Enable caching

3. **Monitoring**:
   - Add logging aggregation
   - Set up monitoring (Prometheus, Grafana)
   - Configure alerts

4. **Backup**:
   - Regular backup of uploads directory
   - Database backups if applicable
   - Configuration backups

## Support

For issues or questions:
1. Check logs first
2. Verify environment variables
3. Check Docker and Docker Compose versions
4. Review service health status
