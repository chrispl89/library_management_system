# Library Management System - Docker Setup

This guide explains how to run the entire library management system using Docker.

## Prerequisites

- Docker Desktop installed (Windows/Mac) or Docker Engine (Linux)
- Docker Compose v2.0 or higher
- At least 4GB of available RAM
- Ports 80, 3000, 5432, and 8000 available

## Quick Start

### 1. Start All Services

```bash
# From the project root directory
docker-compose up -d
```

This will start:
- PostgreSQL database (port 5432)
- Django backend (port 8000)
- React frontend (port 3000)

### 2. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/

### 3. Stop All Services

```bash
docker-compose down
```

## Detailed Setup

### Environment Variables

The system uses the following default environment variables (configured in `docker-compose.yml`):

#### Database
- `POSTGRES_DB`: library_db
- `POSTGRES_USER`: library_user
- `POSTGRES_PASSWORD`: library_pass123 (⚠️ Change in production!)

#### Django
- `DJANGO_DEBUG`: True (set to False in production)
- `DATABASE_URL`: postgresql://library_user:library_pass123@db:5432/library_db

### Initial Setup

After starting the containers for the first time:

```bash
# Create a superuser for Django admin
docker-compose exec backend python manage.py createsuperuser

# Activate the user (if registration requires activation)
docker-compose exec backend python activate_users.py
```

### Running Tests

#### Django Tests
```bash
# Run all Django tests
docker-compose exec backend python manage.py test

# Run specific test class
docker-compose exec backend python manage.py test library.tests.BookAPITestCase

# Run with coverage
docker-compose exec backend pytest --cov=library
```

#### React Tests
```bash
# Run Jest tests
docker-compose exec frontend npm test

# Run tests in CI mode
docker-compose exec frontend npm test -- --coverage --watchAll=false
```

## Database Management

### Migrations

```bash
# Create new migrations
docker-compose exec backend python manage.py makemigrations

# Apply migrations
docker-compose exec backend python manage.py migrate

# Show migration status
docker-compose exec backend python manage.py showmigrations
```

### Database Backup

```bash
# Backup database
docker-compose exec db pg_dump -U library_user library_db > backup.sql

# Restore database
docker-compose exec -T db psql -U library_user library_db < backup.sql
```

### Access Database Shell

```bash
docker-compose exec db psql -U library_user -d library_db
```

## Development Workflow

### Hot Reload

Both frontend and backend support hot reload in development mode:

- **Django**: Changes to Python files automatically restart the server
- **React**: Changes to JS/JSX files trigger automatic rebuild

### Logs

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Rebuild Containers

```bash
# Rebuild all containers
docker-compose build

# Rebuild specific service
docker-compose build backend

# Rebuild and restart
docker-compose up -d --build
```

## Production Deployment

### With Nginx (Recommended)

```bash
# Start with production profile
docker-compose --profile production up -d
```

This starts nginx on port 80 serving both frontend and backend.

### Environment Variables for Production

Create a `.env` file in the project root:

```env
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=your-secret-key-here
POSTGRES_PASSWORD=strong-password-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### SSL/HTTPS Setup

1. Place SSL certificates in `nginx/certs/`
2. Update `nginx/nginx.conf` to include SSL configuration
3. Restart nginx: `docker-compose restart nginx`

## Troubleshooting

### Port Already in Use

```bash
# Check what's using the port
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000

# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Changed from 8000:8000
```

### Database Connection Issues

```bash
# Check database is healthy
docker-compose ps

# Restart database
docker-compose restart db

# View database logs
docker-compose logs db
```

### Frontend Build Fails

```bash
# Clear node_modules and rebuild
docker-compose exec frontend rm -rf node_modules
docker-compose exec frontend npm install

# Or rebuild the image
docker-compose build --no-cache frontend
```

### Reset Everything

```bash
# Stop and remove all containers, volumes, and images
docker-compose down -v --rmi all

# Remove Docker volumes
docker volume prune

# Start fresh
docker-compose up -d --build
```

## Performance Optimization

### Production Settings

1. **Gunicorn** for Django (replace runserver)
2. **Nginx** for serving static files
3. **PostgreSQL** connection pooling
4. **Redis** for caching (optional)

### Resource Limits

Add to `docker-compose.yml`:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
```

## Monitoring

### Container Stats

```bash
# Real-time resource usage
docker stats

# Container status
docker-compose ps
```

### Application Health

```bash
# Check backend health
curl http://localhost:8000/api/books/

# Check frontend
curl http://localhost:3000/

# Check database
docker-compose exec db pg_isready -U library_user
```

## Additional Commands

### Shell Access

```bash
# Django shell
docker-compose exec backend python manage.py shell

# Database shell
docker-compose exec db psql -U library_user library_db

# Container bash
docker-compose exec backend bash
docker-compose exec frontend sh
```

### Data Population

```bash
# Run data setup scripts
docker-compose exec backend python setup_test_data.py
docker-compose exec backend python create_book_catalog.py
```

## Common Issues

1. **Permission Denied**: Run Docker commands with `sudo` (Linux) or ensure Docker Desktop is running (Windows/Mac)
2. **Network Issues**: Check firewall settings and Docker network: `docker network ls`
3. **Slow Build**: Use `--parallel` flag: `docker-compose build --parallel`

## Support

For issues and questions:
- Check logs: `docker-compose logs -f`
- Restart services: `docker-compose restart`
- Full reset: `docker-compose down -v && docker-compose up -d --build`
