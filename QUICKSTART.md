# 🚀 Library Management System - Quick Start Guide

## ⚡ Super Fast Start (Docker - Recommended)

### Prerequisites
- Docker Desktop installed and running
- Ports 3000, 8000, and 5432 available

### Start in 3 Steps

1. **Clone/Navigate to the project:**
```bash
cd library_management_system
```

2. **Start everything with one command:**
```bash
docker-compose up -d
```

3. **Open your browser:**
- Frontend: http://localhost:3000
- Admin: http://localhost:8000/admin/

That's it! The system is running! 🎉

---

## 📋 What's Running?

After `docker-compose up -d`, you have:
- ✅ PostgreSQL database (port 5432)
- ✅ Django backend API (port 8000)
- ✅ React frontend (port 3000)

---

## 🔧 First Time Setup

### Create Admin User
```bash
docker-compose exec backend python manage.py createsuperuser
```
Follow the prompts to create your admin account.

### Verify Everything Works
```bash
# Check all services are running
docker-compose ps

# View logs
docker-compose logs -f
```

---

## 🎯 Common Tasks

### Start the System
```powershell
# Windows (PowerShell)
./start.ps1

# Or use Docker Compose directly
docker-compose up -d
```

### Stop the System
```powershell
# Windows (PowerShell)
./stop.ps1

# Or use Docker Compose directly
docker-compose down
```

### Run Tests
```powershell
# Windows (PowerShell) - Runs all tests
./test.ps1

# Or run individually
docker-compose exec backend python manage.py test
docker-compose exec frontend npm test -- --watchAll=false
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Access Database
```bash
docker-compose exec db psql -U library_user library_db
```

---

## 📱 Using the Application

### Register a New User
1. Go to http://localhost:3000
2. Click "Register"
3. Fill in the form
4. Check Django console for activation link (or activate manually)

### Browse Books
1. Go to "Books" page
2. Use search, filters, and sorting
3. Click "Borrow Book" if logged in

### View Statistics
1. Login to the system
2. Navigate to "Statistics" page
3. See analytics dashboard

### Manage Books (Librarian/Admin)
1. Login as librarian or admin
2. Go to Books page
3. Click "Add Book" button
4. Or edit/delete existing books

---

## 🔑 Default Roles

The system has three roles:
- **Admin** - Full access to everything
- **Librarian** - Can manage books, view all data
- **Reader** - Can borrow books, write reviews

---

## 🐛 Troubleshooting

### Services Won't Start
```bash
# Check Docker is running
docker info

# Check ports are available
# Windows
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Restart everything
docker-compose down
docker-compose up -d --build
```

### Database Issues
```bash
# Reset database (WARNING: Deletes all data!)
docker-compose down -v
docker-compose up -d

# View database logs
docker-compose logs db
```

### Frontend Won't Load
```bash
# Rebuild frontend
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

### Backend Errors
```bash
# Check backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend

# Run migrations
docker-compose exec backend python manage.py migrate
```

---

## 📊 Test Data

### Load Sample Data
```bash
# Create sample books and users
docker-compose exec backend python setup_test_data.py
docker-compose exec backend python create_book_catalog.py
```

---

## 🔒 Security Notes

### For Development
- Default credentials are in `docker-compose.yml`
- Debug mode is enabled
- CORS allows localhost

### For Production
1. Create `.env` file from `.env.example`
2. Change all passwords
3. Set `DJANGO_DEBUG=False`
4. Update `ALLOWED_HOSTS`
5. Use proper SMTP for emails
6. Enable SSL/HTTPS

---

## 🎓 Learn More

- **DOCKER_README.md** - Detailed Docker documentation
- **FEATURES.md** - Complete feature list
- **README.md** - Full project documentation

---

## ⭐ Features Overview

- ✅ User authentication & authorization
- ✅ Book management (CRUD)
- ✅ Loan tracking with due dates
- ✅ Reservations system
- ✅ Book reviews & ratings
- ✅ Google Books API integration
- ✅ Statistics dashboard
- ✅ User profiles
- ✅ Activity history
- ✅ Search, filter, and sort
- ✅ Responsive design
- ✅ Form validation
- ✅ Loading states

---

## 🆘 Need Help?

1. Check logs: `docker-compose logs -f`
2. Restart services: `docker-compose restart`
3. Full reset: `docker-compose down -v && docker-compose up -d --build`
4. Read DOCKER_README.md for detailed troubleshooting

---

## ✨ Next Steps

After getting the system running:

1. **Create an admin account** - `docker-compose exec backend python manage.py createsuperuser`
2. **Load test data** - `docker-compose exec backend python setup_test_data.py`
3. **Explore the Statistics page** - Login and go to /statistics
4. **Try the search and filtering** - Go to Books page
5. **Borrow a book** - Create a loan
6. **Write a review** - Rate a book

---

## 🎉 You're Ready!

The system is production-ready with:
- Docker containerization
- PostgreSQL database
- Nginx reverse proxy
- 27+ passing tests
- Complete API documentation
- Beautiful React UI

**Enjoy your Library Management System!** 📚

---

**Quick Commands Cheat Sheet:**
```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Logs
docker-compose logs -f

# Tests
docker-compose exec backend python manage.py test

# Admin
docker-compose exec backend python manage.py createsuperuser

# Database
docker-compose exec db psql -U library_user library_db
```
