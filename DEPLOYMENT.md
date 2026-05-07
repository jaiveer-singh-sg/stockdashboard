# Stock Dashboard - Deployment Guide

## Quick Start (Development)

### On Windows

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
playwright install

# 3. Setup environment
copy .env.example .env

# 4. Run application
python run.py
```

### On Linux/Mac

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt
playwright install

# 3. Setup environment
cp .env.example .env

# 4. Run application
python run.py
```

The application will be available at `http://localhost:5000`

## Production Deployment

### Using Gunicorn

```bash
# Install gunicorn (already in requirements.txt)
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
```

### Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]
```

Build and run:

```bash
docker build -t stock-dashboard .
docker run -p 5000:8000 stock-dashboard
```

### Using Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: production
      FLASK_HOST: 0.0.0.0
      FLASK_PORT: 5000
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    restart: unless-stopped
```

Run:

```bash
docker-compose up -d
```

### Using Heroku

1. Create `Procfile`:
```
web: gunicorn app:create_app()
```

2. Create `runtime.txt`:
```
python-3.9.16
```

3. Deploy:
```bash
heroku create stock-dashboard
git push heroku main
```

### Using AWS EC2

1. Launch EC2 instance (Ubuntu 20.04)

2. SSH into instance:
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. Install dependencies:
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv nginx

# Install system deps for Playwright
sudo apt-get install -y libglib2.0-0 libpangocairo-1.0-0
```

4. Clone repository and setup:
```bash
git clone <repo-url>
cd StocksDashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
```

5. Configure Nginx as reverse proxy:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

6. Setup Systemd service:
Create `/etc/systemd/system/stock-dashboard.service`:
```ini
[Unit]
Description=Stock Dashboard Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/StocksDashboard
Environment="PATH=/home/ubuntu/StocksDashboard/venv/bin"
ExecStart=/home/ubuntu/StocksDashboard/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:create_app()
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable stock-dashboard
sudo systemctl start stock-dashboard
```

## Environment Variables

Key environment variables for production:

```env
# Flask
FLASK_ENV=production
SECRET_KEY=your-very-secure-secret-key
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Data Sources
YAHOO_FINANCE_ENABLED=true
TRADINGVIEW_HEADLESS_BROWSER=true

# Caching
CACHE_TIMEOUT=3600

# Security
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_HTTPONLY=true
SESSION_COOKIE_SAMESITE=Lax
```

## Performance Optimization

### Caching Strategy
- Implement Redis for distributed caching
- Cache market data for configurable duration
- Cache technical indicators

### Database
- Consider SQLite for local data storage
- Implement PostgreSQL for production
- Cache NASDAQ ticker list

### Frontend
- Minify CSS and JavaScript
- Implement lazy loading
- Use CDN for static assets

### API Rate Limiting
- Implement rate limiting per IP
- Cache API responses
- Implement request throttling

## Security Considerations

1. **Secret Key**: Generate strong secret key
```python
import secrets
print(secrets.token_hex(32))
```

2. **HTTPS**: Use SSL/TLS certificate
3. **CORS**: Configure allowed origins
4. **Input Validation**: Sanitize all inputs
5. **Dependency Updates**: Keep packages updated

## Monitoring & Logging

### Setup Logging

```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

### Metrics to Monitor
- API response times
- Error rates
- Cache hit/miss ratio
- Data freshness
- User activity

## Backup & Recovery

1. Regular database backups
2. Configuration backups
3. Log archiving
4. Disaster recovery plan

## Troubleshooting

### High Memory Usage
- Reduce Playwright browser pool size
- Implement connection pooling
- Profile code for memory leaks

### Slow API Responses
- Enable caching
- Optimize database queries
- Use CDN for assets

### Data Accuracy Issues
- Validate data sources
- Implement data reconciliation
- Add error handling and retry logic

## Testing Deployment

```bash
# Test development server
python run.py

# Test with gunicorn locally
gunicorn -w 4 -b 127.0.0.1:8000 "app:create_app()"

# Test environment variables
python -c "from app import create_app; app = create_app('production'); print('App loaded successfully')"
```

## CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install
      - name: Run tests
        run: pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to production
        run: |
          # Add deployment script here
          echo "Deploying..."
```

## Support

For deployment issues:
1. Check logs: `tail -f logs/app.log`
2. Verify environment variables
3. Test data source connectivity
4. Check system resources
