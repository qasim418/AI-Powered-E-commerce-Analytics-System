# Deployment Guide 🚀

This guide provides comprehensive instructions for deploying the AI-Powered eCommerce Database Assistant to various environments.

## 📋 Deployment Overview

The application consists of:
- **Frontend**: React.js application (static files)
- **Backend**: Flask API server
- **Database**: MySQL database
- **AI Service**: Google Gemini API (external)

## 🏗️ Architecture Options

### 1. Single Server Deployment
- Frontend and backend on same server
- Local MySQL database
- Suitable for: Development, testing, small-scale production

### 2. Multi-Server Deployment
- Separate servers for frontend, backend, and database
- Load balancing and redundancy
- Suitable for: Production, high-traffic scenarios

### 3. Cloud Deployment
- Cloud hosting services (AWS, Azure, Google Cloud)
- Managed database services
- Auto-scaling and high availability
- Suitable for: Enterprise, scalable production

## 🌐 Production Deployment

### Prerequisites
- Ubuntu 20.04+ or CentOS 8+ server
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt recommended)
- 2GB+ RAM, 20GB+ storage

### Step 1: Server Setup

#### Update System
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y nginx mysql-server python3 python3-pip nodejs npm git
```

#### Create Application User
```bash
sudo adduser fyp-app
sudo usermod -aG sudo fyp-app
su - fyp-app
```

#### Clone Repository
```bash
git clone https://github.com/yourusername/ai-ecommerce-assistant.git
cd ai-ecommerce-assistant
```

### Step 2: Database Setup

#### Secure MySQL Installation
```bash
sudo mysql_secure_installation
```

#### Create Database and User
```sql
sudo mysql -u root -p

CREATE DATABASE online_store CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'fyp_user'@'localhost' IDENTIFIED BY 'secure_password_here';
GRANT ALL PRIVILEGES ON online_store.* TO 'fyp_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### Import Schema
```bash
mysql -u fyp_user -p online_store < database_schema.sql
```

### Step 3: Backend Deployment

#### Create Virtual Environment
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Configure Environment
```bash
cp .env.example .env
nano .env
```

```env
GEMINI=your_gemini_api_key_here
DB_HOST=localhost
DB_USER=fyp_user
DB_PASS=secure_password_here
DB_NAME=online_store
FLASK_ENV=production
```

#### Create Systemd Service
```bash
sudo nano /etc/systemd/system/fyp-backend.service
```

```ini
[Unit]
Description=FYP Backend API
After=network.target

[Service]
Type=simple
User=fyp-app
WorkingDirectory=/home/fyp-app/ai-ecommerce-assistant/backend
Environment=PATH=/home/fyp-app/ai-ecommerce-assistant/backend/venv/bin
ExecStart=/home/fyp-app/ai-ecommerce-assistant/backend/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Start Backend Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable fyp-backend
sudo systemctl start fyp-backend
sudo systemctl status fyp-backend
```

### Step 4: Frontend Deployment

#### Build React Application
```bash
cd ../frontend
npm install
npm run build
```

#### Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/fyp-frontend
```

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    root /home/fyp-app/ai-ecommerce-assistant/frontend/build;
    index index.html;
    
    # Frontend static files
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Backend API proxy
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Static assets caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

#### Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/fyp-frontend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 5: SSL Certificate (Production)

#### Install Certbot
```bash
sudo apt install -y certbot python3-certbot-nginx
```

#### Obtain Certificate
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

#### Auto-renewal
```bash
sudo crontab -e
# Add line:
0 12 * * * /usr/bin/certbot renew --quiet
```

## 🐳 Docker Deployment

### Docker Compose Setup

#### Create docker-compose.yml
```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      - REACT_APP_API_URL=http://backend:5000

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    depends_on:
      - database
    environment:
      - DB_HOST=database
      - DB_USER=root
      - DB_PASS=rootpassword
      - DB_NAME=online_store
      - GEMINI=${GEMINI}
    volumes:
      - ./backend:/app

  database:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
      - MYSQL_DATABASE=online_store
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./database_schema.sql:/docker-entrypoint-initdb.d/schema.sql

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./frontend/build:/usr/share/nginx/html
    depends_on:
      - frontend
      - backend

volumes:
  mysql_data:
```

#### Create Dockerfiles

**Frontend Dockerfile:**
```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
```

**Backend Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
```

#### Deploy with Docker
```bash
docker-compose up -d
```

## ☁️ Cloud Deployment

### AWS Deployment

#### EC2 Instance Setup
1. Launch EC2 instance (t3.medium or larger)
2. Configure security groups (ports 80, 443, 22)
3. Connect via SSH
4. Follow production deployment steps

#### RDS Database
1. Create RDS MySQL instance
2. Configure security groups
3. Update backend configuration with RDS endpoint

#### S3 for Static Assets
1. Create S3 bucket
2. Enable static website hosting
3. Upload frontend build files
4. Configure CloudFront distribution

### Heroku Deployment

#### Backend on Heroku
```bash
cd backend
heroku create fyp-backend-api
heroku addons:create cleardb:ignite
heroku config:set GEMINI=your_api_key
git push heroku main
```

#### Frontend on Netlify
1. Connect GitHub repository to Netlify
2. Set build command: `npm run build`
3. Set publish directory: `build`
4. Configure environment variables

### Digital Ocean Deployment

#### Droplet Setup
1. Create Ubuntu droplet
2. Add SSH keys
3. Follow production deployment steps
4. Configure firewall rules

#### Managed Database
1. Create managed MySQL database
2. Configure connection settings
3. Import schema

## 🔧 Configuration Management

### Environment Variables

#### Production Backend (.env)
```env
FLASK_ENV=production
FLASK_DEBUG=False
GEMINI=your_production_api_key
DB_HOST=your_db_host
DB_USER=your_db_user
DB_PASS=your_secure_password
DB_NAME=online_store
SECRET_KEY=your_secret_key_here
```

#### Production Frontend
```env
REACT_APP_API_URL=https://your-api-domain.com
REACT_APP_ENV=production
```

### Security Configuration

#### Firewall Setup
```bash
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```

#### Database Security
```sql
-- Remove anonymous users
DELETE FROM mysql.user WHERE User='';

-- Remove remote root access
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');

-- Drop test database
DROP DATABASE IF EXISTS test;

-- Reload privileges
FLUSH PRIVILEGES;
```

## 📊 Monitoring and Maintenance

### Log Management

#### Application Logs
```bash
# View backend logs
sudo journalctl -u fyp-backend -f

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

#### Log Rotation
```bash
sudo nano /etc/logrotate.d/fyp-app
```

```
/var/log/fyp/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    sharedscripts
}
```

### Backup Strategy

#### Database Backup
```bash
#!/bin/bash
# backup-db.sh
mysqldump -u fyp_user -p online_store > backup_$(date +%Y%m%d_%H%M%S).sql
```

#### Application Backup
```bash
#!/bin/bash
# backup-app.sh
tar -czf app_backup_$(date +%Y%m%d).tar.gz /home/fyp-app/ai-ecommerce-assistant
```

### Performance Monitoring

#### System Monitoring
```bash
# Install monitoring tools
sudo apt install -y htop iotop nethogs
```

#### Application Monitoring
- Set up health check endpoints
- Monitor API response times
- Track database performance
- Monitor disk space and memory usage

## 🔄 Continuous Deployment

### GitHub Actions Workflow
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.2
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /home/fyp-app/ai-ecommerce-assistant
          git pull origin main
          cd backend && source venv/bin/activate && pip install -r requirements.txt
          cd ../frontend && npm install && npm run build
          sudo systemctl restart fyp-backend
          sudo systemctl reload nginx
```

### Rollback Strategy
```bash
#!/bin/bash
# rollback.sh
git checkout HEAD~1
# Rebuild and restart services
```

## 🆘 Troubleshooting

### Common Issues

#### Backend Not Starting
```bash
# Check logs
sudo journalctl -u fyp-backend --no-pager

# Check port availability
sudo netstat -tulpn | grep :5000

# Restart service
sudo systemctl restart fyp-backend
```

#### Database Connection Issues
```bash
# Test connection
mysql -u fyp_user -p -h localhost online_store

# Check MySQL status
sudo systemctl status mysql
```

#### Frontend Not Loading
```bash
# Check nginx configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx

# Check file permissions
ls -la /home/fyp-app/ai-ecommerce-assistant/frontend/build
```

---

*This deployment guide covers various deployment scenarios for the AI-Powered eCommerce Database Assistant. Choose the deployment method that best fits your needs and infrastructure requirements.*
