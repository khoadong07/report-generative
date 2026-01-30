# Deployment Guide

## Quick Start - Development

### Using Docker Compose (Development)

```bash
# Build and start containers
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop containers
docker-compose down
```

Access app at: `http://localhost:8501`

## Production Deployment

### Prerequisites

- Docker & Docker Compose installed
- SSL certificates (for HTTPS)
- Domain name (optional)
- 2GB+ RAM, 10GB+ disk space

### Step 1: Prepare Environment

```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

### Step 2: Setup SSL Certificates

#### Option A: Using Let's Encrypt (Recommended)

```bash
# Create SSL directory
mkdir -p ssl

# Generate self-signed certificate (temporary)
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes

# Later, replace with Let's Encrypt certificates
# certbot certonly --standalone -d yourdomain.com
```

#### Option B: Using Existing Certificates

```bash
# Copy your certificates
cp /path/to/cert.pem ssl/cert.pem
cp /path/to/key.pem ssl/key.pem

# Set permissions
chmod 600 ssl/key.pem
chmod 644 ssl/cert.pem
```

### Step 3: Build and Deploy

```bash
# Build images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Verify services are running
docker-compose -f docker-compose.prod.yml ps

# Check health
docker-compose -f docker-compose.prod.yml exec app curl http://localhost:8501/_stcore/health
```

### Step 4: Verify Deployment

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs -f app

# Test application
curl https://localhost/

# Check Nginx
docker-compose -f docker-compose.prod.yml logs -f nginx
```

## Configuration

### Environment Variables

Create `.env` file:

```env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_LOGGER_LEVEL=warning
STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=false
```

### Nginx Configuration

Edit `nginx.conf` to customize:
- Server name
- SSL certificates path
- Rate limiting
- Proxy settings
- Cache settings

### Streamlit Configuration

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[client]
showErrorDetails = false
toolbarMode = "minimal"

[server]
maxUploadSize = 200
enableXsrfProtection = true
enableCORS = false
```

## Monitoring

### View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f app
docker-compose -f docker-compose.prod.yml logs -f nginx

# Last 100 lines
docker-compose -f docker-compose.prod.yml logs --tail=100 app
```

### Health Check

```bash
# Check container health
docker-compose -f docker-compose.prod.yml ps

# Manual health check
docker-compose -f docker-compose.prod.yml exec app curl http://localhost:8501/_stcore/health
```

### Resource Usage

```bash
# Monitor resource usage
docker stats

# Specific container
docker stats social-listening-app
```

## Maintenance

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild images
docker-compose -f docker-compose.prod.yml build --no-cache

# Restart services
docker-compose -f docker-compose.prod.yml up -d
```

### Backup Data

```bash
# Backup reports
tar -czf reports_backup_$(date +%Y%m%d).tar.gz reports/

# Backup data
tar -czf data_backup_$(date +%Y%m%d).tar.gz data/

# Backup uploads
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz uploads/
```

### Clean Up

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Full cleanup
docker system prune -a
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs app

# Rebuild image
docker-compose -f docker-compose.prod.yml build --no-cache app

# Restart
docker-compose -f docker-compose.prod.yml restart app
```

### Port Already in Use

```bash
# Find process using port
lsof -i :8501
lsof -i :80
lsof -i :443

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
```

### SSL Certificate Issues

```bash
# Check certificate validity
openssl x509 -in ssl/cert.pem -text -noout

# Verify certificate and key match
openssl x509 -noout -modulus -in ssl/cert.pem | openssl md5
openssl rsa -noout -modulus -in ssl/key.pem | openssl md5
```

### Nginx Not Proxying

```bash
# Check Nginx configuration
docker-compose -f docker-compose.prod.yml exec nginx nginx -t

# Reload Nginx
docker-compose -f docker-compose.prod.yml exec nginx nginx -s reload

# Check logs
docker-compose -f docker-compose.prod.yml logs nginx
```

### High Memory Usage

```bash
# Check memory usage
docker stats

# Reduce Streamlit cache
# Edit .streamlit/config.toml:
# [client]
# caching = false

# Restart with memory limit
docker-compose -f docker-compose.prod.yml down
# Edit docker-compose.prod.yml to add memory limits
docker-compose -f docker-compose.prod.yml up -d
```

## Performance Tuning

### Nginx Optimization

```nginx
# In nginx.conf
worker_processes auto;
worker_connections 2048;
keepalive_timeout 65;

# Enable gzip
gzip on;
gzip_comp_level 6;
```

### Streamlit Optimization

```toml
# In .streamlit/config.toml
[client]
caching = true
showErrorDetails = false

[logger]
level = "warning"

[server]
maxUploadSize = 200
enableXsrfProtection = true
```

### Docker Optimization

```yaml
# In docker-compose.prod.yml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

## Security

### SSL/TLS

```bash
# Generate strong certificate
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes

# Set proper permissions
chmod 600 ssl/key.pem
chmod 644 ssl/cert.pem
```

### Firewall

```bash
# Allow only necessary ports
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

### Rate Limiting

Configured in `nginx.conf`:
- General: 10 requests/second
- Upload: 5 requests/minute

### Security Headers

Configured in `nginx.conf`:
- HSTS (HTTP Strict Transport Security)
- X-Frame-Options
- X-Content-Type-Options
- X-XSS-Protection
- Referrer-Policy

## Scaling

### Horizontal Scaling

```yaml
# docker-compose.prod.yml
services:
  app:
    deploy:
      replicas: 3
```

### Load Balancing

Nginx automatically load balances across multiple app instances:

```nginx
upstream streamlit_app {
    server app:8501;
    server app:8502;
    server app:8503;
}
```

## Backup & Recovery

### Automated Backup

```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup reports
tar -czf $BACKUP_DIR/reports_$DATE.tar.gz reports/

# Backup data
tar -czf $BACKUP_DIR/data_$DATE.tar.gz data/

# Keep only last 7 days
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

Add to crontab:
```bash
0 2 * * * /path/to/backup.sh
```

### Recovery

```bash
# Restore reports
tar -xzf reports_backup.tar.gz

# Restore data
tar -xzf data_backup.tar.gz

# Restart services
docker-compose -f docker-compose.prod.yml restart
```

## Monitoring & Alerts

### Using Prometheus (Optional)

```yaml
# docker-compose.prod.yml
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
```

### Using ELK Stack (Optional)

```yaml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.0.0
  
  kibana:
    image: docker.elastic.co/kibana/kibana:8.0.0
```

## Support

For issues:
1. Check logs: `docker-compose logs -f`
2. Verify configuration
3. Check system resources
4. Review troubleshooting section above
