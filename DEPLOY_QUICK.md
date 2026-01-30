# Quick Deployment Guide

## Development (5 minutes)

### Start

```bash
docker-compose up -d
```

Access: `http://localhost:8501`

### Stop

```bash
docker-compose down
```

### View Logs

```bash
docker-compose logs -f app
```

## Production (15 minutes)

### 1. Prepare

```bash
# Copy environment
cp .env.example .env

# Generate SSL certificate
make ssl-generate
# or
./deploy.sh ssl-generate
```

### 2. Build & Deploy

```bash
# Build images
make build
# or
./deploy.sh build

# Start services
make up
# or
./deploy.sh up
```

### 3. Verify

```bash
# Check status
make status

# Check health
make health
```

Access: `https://localhost` (or your domain)

## Common Commands

### Using Make

```bash
make help              # Show all commands
make dev-up           # Start development
make up               # Start production
make down             # Stop services
make restart          # Restart services
make logs             # View logs
make status           # Show status
make health           # Check health
make backup           # Backup data
make clean            # Clean up
make ssl-generate     # Generate SSL
```

### Using Deploy Script

```bash
./deploy.sh help              # Show all commands
./deploy.sh build             # Build images
./deploy.sh up                # Start services
./deploy.sh down              # Stop services
./deploy.sh restart           # Restart services
./deploy.sh logs              # View logs
./deploy.sh status            # Show status
./deploy.sh health            # Check health
./deploy.sh backup            # Backup data
./deploy.sh ssl-generate      # Generate SSL
```

### Using Docker Compose

```bash
# Development
docker-compose up -d
docker-compose down
docker-compose logs -f

# Production
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml logs -f
```

## Troubleshooting

### Port in Use

```bash
# Find process
lsof -i :8501

# Kill process
kill -9 <PID>
```

### Container Won't Start

```bash
# Check logs
docker-compose logs app

# Rebuild
docker-compose build --no-cache

# Restart
docker-compose restart
```

### SSL Issues

```bash
# Check certificate
make ssl-check

# Regenerate
make ssl-generate
```

### High Memory

```bash
# Check usage
docker stats

# Restart services
make restart
```

## Backup & Restore

### Backup

```bash
make backup
# Creates: backups/reports_TIMESTAMP.tar.gz
#          backups/data_TIMESTAMP.tar.gz
#          backups/uploads_TIMESTAMP.tar.gz
```

### Restore

```bash
./deploy.sh restore backups/reports_TIMESTAMP.tar.gz
```

## Monitoring

### Logs

```bash
# All services
make logs

# Specific service
docker-compose -f docker-compose.prod.yml logs app
docker-compose -f docker-compose.prod.yml logs nginx

# Last 100 lines
docker-compose -f docker-compose.prod.yml logs --tail=100 app
```

### Resource Usage

```bash
docker stats
```

### Health Check

```bash
make health
```

## Update

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
make update
```

## Security

### SSL Certificate

```bash
# Generate self-signed (development)
make ssl-generate

# For production, use Let's Encrypt:
# 1. Get certificate from Let's Encrypt
# 2. Copy to ssl/cert.pem and ssl/key.pem
# 3. Restart Nginx
```

### Firewall

```bash
# Allow ports
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

## Performance

### Optimize Nginx

Edit `nginx.conf`:
- Increase `worker_processes`
- Increase `worker_connections`
- Enable gzip compression

### Optimize Streamlit

Edit `.streamlit/config.toml`:
- Disable error details
- Set logger level to warning
- Enable caching

## Scaling

### Multiple Instances

Edit `docker-compose.prod.yml`:

```yaml
services:
  app:
    deploy:
      replicas: 3
```

Nginx will load balance automatically.

## Cleanup

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

## Next Steps

1. Read `DEPLOYMENT.md` for detailed guide
2. Check `README.md` for application info
3. Review `nginx.conf` for customization
4. Setup monitoring (optional)
5. Configure backups (recommended)

## Support

For issues:
1. Check logs: `make logs`
2. Verify status: `make status`
3. Check health: `make health`
4. Review DEPLOYMENT.md troubleshooting section
