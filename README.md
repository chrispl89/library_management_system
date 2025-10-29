# Library Management System

[![Status](https://img.shields.io/badge/status-production--ready-green)](https://github.com/chrispl89/library_management_system)
[![Django](https://img.shields.io/badge/Django-5.1.6-green)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-19.2.0-blue)](https://reactjs.org/)

A modern, full-stack library management system with Django REST Framework backend and React frontend. Features include user management with role-based access, book cataloging, loan tracking, reservations, and review system.

---

## ✨ Key Features

### User Management
- **Multi-role authentication** (Admin, Librarian, Reader)
- **JWT-based security** with token refresh
- **Role-based permissions** and access control
- **User profiles** with activity tracking

### Book Management
- **Comprehensive catalog** (300+ books across 15 categories)
- **CRUD operations** for librarians and admins
- **Google Books API integration** for easy book addition
- **Advanced search and filtering** by title, author, or category
- **Category-based filtering** for easy browsing
- **Availability tracking** in real-time

### Loan System
- **Easy borrowing** directly from book catalog
- **Automatic due date calculation** (14 days)
- **Return processing** with overdue tracking
- **Fine calculation** ($1/day for overdue books)
- **Loan history** and status tracking

### Reservations
- **Book reservation system** with 3-day expiration
- **Active reservation management**
- **Cancellation support**

### Reviews & Ratings
- **5-star rating system**
- **User comments and feedback**
- **Review management**

### Dashboard
- **User activity overview**
- **Active loans and reservations**
- **Personal review history**
- **Profile management**

---

## 🚀 Quick Start with Docker (Recommended)

### Prerequisites

- **Docker Desktop** installed and running
- **Git**

### Installation

#### 1. Clone the repository

```bash
git clone https://github.com/chrispl89/library_management_system.git
cd library_management_system
```

#### 2. Start all services with Docker

**Windows (PowerShell):**
```powershell
.\start.ps1
```

**Or use Docker Compose directly:**
```bash
docker-compose up -d
```

This will start:
- **PostgreSQL** database (port 5432)
- **Django** backend (port 8000)
- **React** frontend (port 3000)

#### 3. Create test users and sample data

```bash
# Create test users (librarian, reader, admin)
docker-compose exec backend python create_test_users.py

# Add 15 sample books
docker-compose exec backend python create_sample_books.py

# (Optional) Create superuser for admin panel
docker-compose exec backend python manage.py createsuperuser
```

#### 4. Access the application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/api/
- **Admin Panel:** http://localhost:8000/admin/

#### 5. Stop the system

**Windows (PowerShell):**
```powershell
.\stop.ps1
```

**Or:**
```bash
docker-compose down
```

---

## 🛠️ Alternative: Manual Setup (Without Docker)

### Prerequisites

- **Python 3.8+**
- **Node.js 14+** and npm

### Backend Setup

```bash
# Install Python dependencies
pip install -r django/requirements.txt

# Navigate to Django directory
cd django

# Run database migrations
python manage.py migrate

# Create test users
python create_test_users.py

# Start backend server
python manage.py runserver
```

Backend runs at: **http://127.0.0.1:8000**

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend runs at: **http://localhost:3000**

---

## 🔐 Test Credentials

After running `create_test_users.py`, you can login with:

| Username | Password | Role | Permissions |
|----------|----------|------|-------------|
| **admin_user** | Test1234 | Admin | Full system access |
| **librarian_user** | Test1234 | Librarian | Book management, all operations |
| **reader_user** | Test1234 | Reader | Browse, borrow, review books |

---

## 📖 Using the Application

### For Readers

1. **Browse Books**
   - Navigate to "Books" page
   - Use search bar to find books by title, author, or category
   - Filter by category using the dropdown menu
   - View availability status (Available/Unavailable)

2. **Borrow Books**
   - Click "Borrow Book" button on any available book
   - Book is automatically loaned for 14 days
   - View your loans in the "Loans" section

3. **Return Books**
   - Go to "Loans" page
   - Click "Return Book" on active loans
   - Late returns incur fines ($1/day)

4. **Reserve Books**
   - Navigate to "Reservations"
   - Create reservations for books
   - Reservations expire after 3 days

5. **Write Reviews**
   - Go to "Reviews" section
   - Rate books (1-5 stars)
   - Add comments

6. **Check Dashboard**
   - View all active loans and reservations
   - See your review history
   - Track your activity

### For Librarians

All reader features, plus:

- **Add New Books**
  - Click "Add Book" button
  - Search Google Books or enter manually
  - Books are added to catalog

- **Edit Books**
  - Update book information
  - Modify categories and details

- **Delete Books**
  - Remove books from catalog
  - System prevents deletion of books with active loans

### For Admins

All features plus:
- User management
- System configuration
- Full administrative access

---

## 🗂️ Project Structure

```
library_management_system/
├── django/                          # Backend (Django REST Framework)
│   ├── library/                     # Main application
│   │   ├── models.py               # Database models
│   │   ├── views.py                # API endpoints
│   │   ├── serializers.py          # Data serialization
│   │   ├── permissions.py          # Access control
│   │   ├── urls.py                 # URL routing
│   │   └── tests.py                # Unit tests (27 tests)
│   ├── library_management_project/ # Project settings
│   ├── create_test_users.py        # Create test users script
│   ├── create_sample_books.py      # Add sample books script
│   ├── activate_users.py           # Activate all users script
│   ├── Dockerfile                  # Docker configuration
│   ├── requirements.txt            # Python dependencies
│   └── manage.py                   # Django management
│
├── frontend/                        # Frontend (React)
│   ├── public/                     # Static files
│   ├── src/
│   │   ├── components/             # Reusable components
│   │   │   ├── Layout.js          # Navigation & layout
│   │   │   └── LoadingSpinner.js  # Loading component
│   │   ├── context/               # React Context (Auth)
│   │   ├── pages/                 # Application pages
│   │   │   ├── Books.js           # Book catalog with sorting
│   │   │   ├── Dashboard.js       # User dashboard
│   │   │   ├── Statistics.js      # Analytics page
│   │   │   └── ...
│   │   ├── services/              # API integration
│   │   ├── utils/                 # Utilities
│   │   │   └── validation.js      # Form validation
│   │   └── App.js                 # Main application
│   ├── Dockerfile                  # Docker configuration
│   ├── nginx.conf                  # Nginx configuration
│   └── package.json               # Node dependencies
│
├── docker-compose.yml              # Docker services orchestration
├── start.ps1                       # Windows startup script
├── stop.ps1                        # Windows stop script
├── test.ps1                        # Test runner script
├── DOCKER_README.md                # Docker documentation
├── QUICKSTART.md                   # Quick start guide
├── FEATURES.md                     # Features documentation
└── README.md                       # This file
```

---

## 🛠️ Technology Stack

### Backend
- **Django 5.1.6** - Web framework
- **Django REST Framework 3.15.2** - API development
- **Simple JWT 5.3.1** - Authentication
- **Django CORS Headers 4.6.0** - Cross-origin support
- **PostgreSQL 15** - Production database (Docker)
- **SQLite** - Development database (fallback)
- **Gunicorn 23.0.0** - Production WSGI server
- **WhiteNoise 6.8.2** - Static file serving
- **psycopg2-binary 2.9.9** - PostgreSQL adapter

### Frontend
- **React 19.2.0** - UI framework
- **React Router DOM 7.9.4** - Routing
- **Axios 1.12.2** - HTTP client
- **Lucide React** - Icons
- **Bootstrap 5.3.8** - Styling
- **TailwindCSS** - Utility styling

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **Nginx** - Reverse proxy & static file serving
- **PostgreSQL 15 Alpine** - Database container

---

## 📊 Database Schema

### Models

**CustomUser**
- username, email, password
- role (admin/librarian/reader)
- is_active status

**Book**
- title, author, category
- is_available (availability status)
- added_by (user reference)
- created_at timestamp

**Loan**
- book, user references
- loan_date, due_date, returned_at
- status (ACTIVE/RETURNED/OVERDUE)
- fine (calculated penalty)

**Reservation**
- book, user references
- created_at, expires_at
- status (ACTIVE/EXPIRED/CANCELLED)

**Review**
- book, user references
- rating (1-5 stars)
- comment
- created_at timestamp

**Profile**
- user (one-to-one)
- phone_number, address
- activity_history (auto-tracked)

---

## 📚 Sample Book Catalog

The `create_sample_books.py` script adds **15 classic books** across multiple categories:

- **Fiction** - The Great Gatsby, To Kill a Mockingbird, The Catcher in the Rye
- **Science Fiction** - 1984, Brave New World
- **Fantasy** - The Hobbit, Harry Potter, The Lord of the Rings, The Chronicles of Narnia
- **Romance** - Pride and Prejudice
- **Classic** - Crime and Punishment
- **Epic Poetry** - The Odyssey
- **Adventure** - Moby-Dick
- **Drama** - Hamlet
- **Political Fiction** - Animal Farm

**Add more books:**
- As librarian through the web interface
- Via Google Books API integration
- By modifying `create_sample_books.py` script

---

## 🔧 API Endpoints

### Authentication
```
POST   /api/token/              # Login (get JWT tokens)
POST   /api/token/refresh/      # Refresh access token
POST   /api/register/           # User registration
```

### Books
```
GET    /api/books/              # List all books
POST   /api/books/              # Create book (librarian only)
GET    /api/books/{id}/         # Get book details
PUT    /api/books/{id}/         # Update book (librarian only)
DELETE /api/books/{id}/         # Delete book (librarian only)
GET    /api/google-books/?q=    # Search Google Books
```

### Loans
```
GET    /api/loans/              # List user's loans
POST   /api/loans/              # Create new loan
POST   /api/loans/{id}/return_book/  # Return book
```

### Reservations
```
GET    /api/reservations/                      # List reservations
POST   /api/reservations/                      # Create reservation
GET    /api/reservations/my_reservations/      # Get user's reservations
POST   /api/reservations/{id}/cancel_reservation/  # Cancel
```

### Reviews
```
GET    /api/reviews/            # List reviews
POST   /api/reviews/            # Create review
DELETE /api/reviews/{id}/       # Delete review (admin only)
```

### Dashboard & Statistics
```
GET    /api/dashboard/          # Get user dashboard data
GET    /api/statistics/         # Get library analytics & statistics
```

### User Management
```
GET    /api/profiles/           # List profiles
GET    /api/profiles/{id}/      # Get profile details
PATCH  /api/profiles/{id}/      # Update profile
GET    /api/activate/{uid}/{token}/  # Activate user account
```

---

## 🐛 Troubleshooting

### Docker Issues

**Docker Desktop not running:**
```powershell
# Ensure Docker Desktop is running
docker info
```

**Services won't start:**
```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Full rebuild
docker-compose down
docker-compose up -d --build
```

**Port conflicts:**
```bash
# Check what's using the ports
netstat -ano | findstr :3000
netstat -ano | findstr :8000
netstat -ano | findstr :5432
```

**Reset everything:**
```bash
# Stop and remove all containers, volumes
docker-compose down -v
docker-compose up -d --build
```

### Database Issues

**Reset database (Docker):**
```bash
docker-compose down -v  # Removes volumes
docker-compose up -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python create_test_users.py
```

### Application Issues

**No users exist:**
```bash
docker-compose exec backend python create_test_users.py
```

**No books showing:**
```bash
docker-compose exec backend python create_sample_books.py
```

**Login fails:**
- Ensure test credentials: `reader_user` / `Test1234`
- Passwords are case-sensitive

### Manual Setup Issues

**Backend won't start:**
```bash
pip install -r django/requirements.txt
cd django
python manage.py migrate
```

**Frontend won't start:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 🔄 Resetting the System

### Docker Reset

```bash
# Stop and remove everything (including database)
docker-compose down -v

# Rebuild and start
docker-compose up -d --build

# Create fresh data
docker-compose exec backend python create_test_users.py
docker-compose exec backend python create_sample_books.py
```

### Manual Setup Reset

```bash
# Stop servers (Ctrl+C)

# Reset database
cd django
rm db.sqlite3  # Linux/Mac
# del db.sqlite3  # Windows

# Recreate database
python manage.py migrate

# Recreate test data
python create_test_users.py
python create_sample_books.py

# Restart servers
```

---

## 📝 Development Notes

### Adding New Books

**Manual addition** (as librarian):
1. Login as `librarian_user` / `Test1234`
2. Click "Add Book" button
3. Search Google Books or enter manually

**Bulk addition** (via script):
1. Edit `django/create_sample_books.py`
2. Add books to `sample_books` list
3. Run: `docker-compose exec backend python create_sample_books.py`

### Managing Users

**Create additional users:**
```bash
# Docker
docker-compose exec backend python manage.py createsuperuser

# Manual
python manage.py createsuperuser
```

**Modify user roles (Django Shell):**
```bash
# Docker
docker-compose exec backend python manage.py shell

# Manual
python manage.py shell

# Then in shell:
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> user = User.objects.get(username='username')
>>> user.role = 'librarian'  # or 'admin' or 'reader'
>>> user.save()
```

### Running Tests

**Django tests:**
```bash
# Docker
docker-compose exec backend python manage.py test

# Or use test script
.\test.ps1

# Manual
cd django
python manage.py test
```

**React tests:**
```bash
# Docker
docker-compose exec frontend npm test

# Manual
cd frontend
npm test
```

---

## 🎯 Features in Detail

### Role-Based Access Control

**Admin:**
- Full system access
- User management
- Delete any review
- All librarian and reader permissions

**Librarian:**
- Add, edit, delete books
- View who added each book
- All reader permissions

**Reader:**
- Browse and search books
- Borrow and return books
- Create reservations
- Write reviews
- View personal dashboard

### Fine Calculation

- **Rate:** $1.00 per day overdue
- **Calculation:** Automatic on book return
- **Display:** Shows in loans table and dashboard
- **Example:** 5 days late = $5.00 fine

### Reservation System

- **Duration:** 3 days from creation
- **Status Tracking:** ACTIVE, EXPIRED, CANCELLED
- **User Actions:** Create, view, cancel
- **Auto-expiration:** Handled by system

### Search & Filtering

- **Text Search:** Title, author, category
- **Category Filter:** Dropdown with all 15 categories
- **Combined Filtering:** Search + category filter work together
- **Results Counter:** Shows "X of Y books"
- **Clear Filters:** One-click reset

---

## 📄 License

This project is for educational purposes.

---

## 🙏 Acknowledgments

- Built with **Django** and **React**
- Icons by **Lucide React**
- Book data from **Google Books API**

---

## 📞 Support

For issues or questions:
- Check the **Troubleshooting** section
- Review **DOCKER_README.md** for detailed Docker documentation
- See **QUICKSTART.md** for quick start guide
- Check **FEATURES.md** for complete feature list

---

## 📖 Additional Documentation

- **[DOCKER_README.md](DOCKER_README.md)** - Comprehensive Docker guide
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
- **[FEATURES.md](FEATURES.md)** - Complete feature documentation
- **[django/tests.py](django/library/tests.py)** - 27 unit tests for API

---

**Version:** 2.0.0  
**Status:** Production Ready (Docker + PostgreSQL)  
**Last Updated:** October 2025  
**Tests:** 27 passing Django tests + React component tests
