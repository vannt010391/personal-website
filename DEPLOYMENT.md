# Hướng Dẫn Deploy Production

## 1. Chuẩn Bị Server

### Yêu cầu hệ thống
- Ubuntu 20.04/22.04 LTS hoặc CentOS 7/8
- Python 3.10+
- PostgreSQL 13+ hoặc MySQL 8+
- Nginx
- 1GB RAM minimum (2GB khuyến nghị)

### Cài đặt dependencies

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib

# CentOS/RHEL
sudo yum install python3-pip python3-venv nginx postgresql-server postgresql-contrib
```

## 2. Cấu Hình Database

### PostgreSQL

```bash
# Đăng nhập PostgreSQL
sudo -u postgres psql

# Tạo database và user
CREATE DATABASE personalwebsite;
CREATE USER webuser WITH PASSWORD 'your_strong_password';
ALTER ROLE webuser SET client_encoding TO 'utf8';
ALTER ROLE webuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE webuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE personalwebsite TO webuser;
\q
```

## 3. Setup Dự Án

```bash
# Clone dự án
git clone <your-repo-url> /var/www/personal-website
cd /var/www/personal-website

# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

## 4. Cấu Hình Settings

Tạo file `mywebsite/production_settings.py`:

```python
from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'your-server-ip']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'personalwebsite',
        'USER': 'webuser',
        'PASSWORD': 'your_strong_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Security
SECRET_KEY = 'your-new-super-secret-key-change-this'
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files
STATIC_ROOT = '/var/www/personal-website/staticfiles'
MEDIA_ROOT = '/var/www/personal-website/media'

# Email (optional)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 5. Migrate Database

```bash
export DJANGO_SETTINGS_MODULE=mywebsite.production_settings

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## 6. Cấu Hình Gunicorn

Tạo file `/etc/systemd/system/personalwebsite.service`:

```ini
[Unit]
Description=Personal Website Gunicorn Daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/personal-website
Environment="DJANGO_SETTINGS_MODULE=mywebsite.production_settings"
ExecStart=/var/www/personal-website/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/personal-website/gunicorn.sock \
    --timeout 60 \
    --access-logfile /var/log/gunicorn/access.log \
    --error-logfile /var/log/gunicorn/error.log \
    mywebsite.wsgi:application

[Install]
WantedBy=multi-user.target
```

Tạo thư mục log:
```bash
sudo mkdir -p /var/log/gunicorn
sudo chown -R www-data:www-data /var/www/personal-website
sudo chown -R www-data:www-data /var/log/gunicorn
```

Start Gunicorn:
```bash
sudo systemctl start personalwebsite
sudo systemctl enable personalwebsite
sudo systemctl status personalwebsite
```

## 7. Cấu Hình Nginx

Tạo file `/etc/nginx/sites-available/personalwebsite`:

```nginx
upstream personalwebsite {
    server unix:/var/www/personal-website/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL certificates (get from Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';

    client_max_body_size 10M;

    access_log /var/log/nginx/personalwebsite_access.log;
    error_log /var/log/nginx/personalwebsite_error.log;

    location /static/ {
        alias /var/www/personal-website/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/personal-website/media/;
        expires 7d;
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://personalwebsite;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/personalwebsite /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 8. SSL với Let's Encrypt

```bash
# Cài đặt certbot
sudo apt install certbot python3-certbot-nginx

# Tạo SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

## 9. Firewall

```bash
# UFW (Ubuntu)
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable

# Firewalld (CentOS)
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

## 10. Monitoring & Maintenance

### Logs
```bash
# Gunicorn logs
sudo tail -f /var/log/gunicorn/error.log
sudo tail -f /var/log/gunicorn/access.log

# Nginx logs
sudo tail -f /var/log/nginx/personalwebsite_error.log
sudo tail -f /var/log/nginx/personalwebsite_access.log

# Systemd logs
sudo journalctl -u personalwebsite -f
```

### Restart Services
```bash
# Sau khi update code
cd /var/www/personal-website
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart personalwebsite
sudo systemctl restart nginx
```

### Backup Database
```bash
# PostgreSQL
pg_dump -U webuser personalwebsite > backup_$(date +%Y%m%d).sql

# Restore
psql -U webuser personalwebsite < backup_20260204.sql
```

### Automated Backups (Crontab)
```bash
crontab -e

# Backup daily at 2 AM
0 2 * * * /usr/bin/pg_dump -U webuser personalwebsite > /backups/db_$(date +\%Y\%m\%d).sql
```

## 11. Performance Optimization

### Redis Cache
```bash
pip install django-redis redis

# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### Database Indexing
```python
# models.py - thêm db_index=True cho các fields thường query
class Post(models.Model):
    slug = models.SlugField(unique=True, db_index=True)
    status = models.CharField(max_length=10, db_index=True)
```

## 12. Security Checklist

- [ ] DEBUG = False
- [ ] SECRET_KEY mới và an toàn
- [ ] ALLOWED_HOSTS cấu hình đúng
- [ ] SSL/HTTPS enabled
- [ ] Firewall configured
- [ ] Regular backups
- [ ] Strong database passwords
- [ ] CSRF & XSS protection enabled
- [ ] User permissions properly set
- [ ] Regular security updates

## Docker Deployment (Optional)

### Dockerfile
```dockerfile
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mywebsite.wsgi:application"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: personalwebsite
      POSTGRES_USER: webuser
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: gunicorn mywebsite.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    environment:
      - DJANGO_SETTINGS_MODULE=mywebsite.production_settings
    depends_on:
      - db

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/static
      - media_volume:/media
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

---

**Lưu ý:** Thay thế tất cả `yourdomain.com`, passwords và các thông tin cụ thể với giá trị thực tế của bạn.
