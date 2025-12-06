# 🚀 AdvocaDabra Deployment Guide

## Production Deployment Checklist

### 🔧 Backend Deployment

1. **Environment Setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   pip install -r requirements.txt
   ```

2. **Production Configuration**:
   ```bash
   # Create .env file
   echo "FLASK_SECRET_KEY=$(openssl rand -hex 32)" > .env
   echo "FLASK_ENV=production" >> .env
   echo "DATABASE_URL=sqlite:///production.db" >> .env
   ```

3. **Production Server** (using Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 backend_server:app
   ```

### 🎨 Frontend Deployment

1. **Build for Production**:
   ```bash
   cd frontend/legal-ai-client
   npm install
   npm run build
   ```

2. **Serve Static Files** (using serve):
   ```bash
   npm install -g serve
   serve -s dist -l 3000
   ```

3. **Environment Configuration**:
   ```javascript
   // Update API URL in production
   const API_BASE_URL = process.env.NODE_ENV === 'production' 
     ? 'https://your-backend-domain.com/api'
     : 'http://localhost:8000/api';
   ```

### 🔒 Security Considerations

- [ ] Change default JWT secret key
- [ ] Enable HTTPS for production
- [ ] Set up proper CORS origins
- [ ] Configure rate limiting
- [ ] Set up file upload size limits
- [ ] Enable request logging
- [ ] Set up database backups

### 📊 Performance Optimization

- [ ] Enable gzip compression
- [ ] Set up CDN for static assets  
- [ ] Configure database connection pooling
- [ ] Enable Redis caching for embeddings
- [ ] Set up load balancing for multiple instances

### 🔍 Monitoring & Logging

- [ ] Set up application logging
- [ ] Configure error tracking (e.g., Sentry)
- [ ] Monitor API response times
- [ ] Track file upload metrics
- [ ] Monitor embedding generation progress

## Docker Deployment (Recommended)

### Backend Dockerfile:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "backend_server:app"]
```

### Frontend Dockerfile:
```dockerfile
FROM node:18-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./backend/uploads:/app/uploads
      - ./backend/di_prime_embeddings:/app/di_prime_embeddings

  frontend:
    build: ./frontend/legal-ai-client
    ports:
      - "3000:80"
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - frontend
      - backend
```

## Cloud Deployment Options

### AWS
- **Backend**: Elastic Beanstalk or ECS
- **Frontend**: S3 + CloudFront
- **Database**: RDS (PostgreSQL) for production
- **Files**: S3 for uploads and embeddings

### Google Cloud
- **Backend**: Cloud Run or App Engine
- **Frontend**: Firebase Hosting
- **Database**: Cloud SQL
- **Files**: Cloud Storage

### Azure
- **Backend**: App Service or Container Instances
- **Frontend**: Static Web Apps
- **Database**: Azure SQL
- **Files**: Blob Storage

## Local Production Testing

```bash
# Test production build locally
cd frontend/legal-ai-client
npm run build
npm run preview

# Test backend with production settings
cd backend
export FLASK_ENV=production
python backend_server.py
```

## Backup Strategy

1. **Database**: Daily SQLite backups
2. **Embeddings**: Weekly backup of di_prime_embeddings/
3. **Uploads**: Daily backup of user files
4. **Configuration**: Version control all config files

## Scaling Considerations

- **Horizontal Scaling**: Multiple backend instances behind load balancer
- **Database**: Migrate to PostgreSQL for better concurrent access
- **Caching**: Redis for API responses and embedding cache
- **CDN**: Serve static files from CDN
- **Queue System**: Celery for background embedding processing
