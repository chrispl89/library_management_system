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

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 14+** and npm
- **Git**

### Installation

#### 1. Clone the repository

```bash
git clone https://github.com/chrispl89/library_management_system.git
cd library_management_system
```

#### 2. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Navigate to Django directory
cd django

# Run database migrations
python manage.py migrate

# Create initial data (test users and book catalog)
cd ..
python setup_test_data.py
python create_book_catalog.py

# Start backend server
cd django
python manage.py runserver
```

Backend will run at: **http://127.0.0.1:8000**

#### 3. Frontend Setup

Open a **new terminal** window:

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start development server
npm start
```

Frontend will run at: **http://localhost:3000**

---

## 🔐 Test Credentials

The system comes with pre-configured test users:

| Username | Password | Role | Permissions |
|----------|----------|------|-------------|
| **admin_user** | AdminPass123! | Admin | Full system access |
| **librarian_user** | LibrarianPass123! | Librarian | Book management, all operations |
| **reader_user** | ReaderPass123! | Reader | Browse, borrow, review books |

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
├── django/                      # Backend (Django REST Framework)
│   ├── library/                 # Main application
│   │   ├── models.py           # Database models
│   │   ├── views.py            # API endpoints
│   │   ├── serializers.py      # Data serialization
│   │   ├── permissions.py      # Access control
│   │   └── urls.py             # URL routing
│   ├── library_management_project/  # Project settings
│   ├── manage.py               # Django management
│   └── db.sqlite3              # Database (SQLite)
│
├── frontend/                    # Frontend (React)
│   ├── public/                 # Static files
│   ├── src/
│   │   ├── components/         # Reusable components
│   │   ├── context/           # React Context (Auth)
│   │   ├── pages/             # Application pages
│   │   ├── services/          # API integration
│   │   └── App.js             # Main application
│   └── package.json           # Node dependencies
│
├── setup_test_data.py          # Create test users
├── create_book_catalog.py      # Populate book catalog
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🛠️ Technology Stack

### Backend
- **Django 5.1.6** - Web framework
- **Django REST Framework 3.15.2** - API development
- **Simple JWT 5.4.0** - Authentication
- **Django CORS Headers** - Cross-origin support
- **SQLite** - Database (development)
- **WhiteNoise** - Static file serving

### Frontend
- **React 19.2.0** - UI framework
- **React Router DOM 7.9.4** - Routing
- **Axios 1.12.2** - HTTP client
- **Lucide React** - Icons
- **Bootstrap 5.3.8** - Styling
- **TailwindCSS** - Utility styling

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

## 📚 Book Catalog

The system includes **319 books** across **15 categories**:

- **Classic Fiction** (30 books) - Austen, Dickens, Brontë, Tolkien
- **Science Fiction** (30 books) - Herbert, Asimov, Gibson, Clarke
- **Fantasy** (30 books) - Tolkien, Rowling, Martin, Sanderson
- **Mystery & Thriller** (30 books) - Christie, Doyle, Larsson, Brown
- **Dystopian Fiction** (20 books) - Orwell, Atwood, Collins
- **Historical Fiction** (20 books) - Doerr, Follett, Hosseini
- **Romance** (20 books) - Sparks, Green, Gabaldon
- **Horror** (20 books) - King, Rice, Blatty
- **Biography & Memoir** (20 books) - Frank, Mandela, Obama
- **Self-Help & Psychology** (20 books) - Kahneman, Clear, Covey
- **Business & Economics** (15 books) - Ries, Thiel, Collins
- **Philosophy** (15 books) - Plato, Nietzsche, Aurelius
- **Poetry** (15 books) - Homer, Shakespeare, Dickinson
- **Young Adult** (15 books) - Chbosky, Green, Yoon
- **Adventure** (15 books) - London, Verne, Dumas

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

### Dashboard
```
GET    /api/dashboard/          # Get user dashboard data
```

---

## 🐛 Troubleshooting

### Backend won't start

**Check Python version:**
```bash
python --version  # Should be 3.8+
```

**Reinstall dependencies:**
```bash
pip install -r requirements.txt
```

**Reset database:**
```bash
cd django
python manage.py migrate
```

### Frontend won't start

**Check Node version:**
```bash
node --version  # Should be 14+
```

**Clear and reinstall:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Clear browser cache:**
- Press `Ctrl + Shift + R` to hard refresh

### Login fails

**Ensure users are activated:**
```bash
python setup_test_data.py
```

**Check credentials:**
- Username: `reader_user`
- Password: `ReaderPass123!`
- Password is case-sensitive and includes special character

### CORS errors

**Verify backend settings:**
- CORS is configured for `http://localhost:3000`
- Check `django/library_management_project/settings.py`

### Books not showing

**Populate catalog:**
```bash
python create_book_catalog.py
```

---

## 🔄 Resetting the System

To start fresh with clean data:

```bash
# Stop both servers (Ctrl+C)

# Reset database
cd django
del db.sqlite3  # Windows
# rm db.sqlite3  # Linux/Mac

# Recreate database
python manage.py migrate

# Recreate test data
cd ..
python setup_test_data.py
python create_book_catalog.py

# Restart servers
```

---

## 📝 Development Notes

### Adding New Books

**Manual addition** (as librarian):
1. Login as `librarian_user`
2. Click "Add Book" button
3. Search Google Books or enter manually

**Bulk addition** (via script):
1. Edit `create_book_catalog.py`
2. Add books to `BOOK_CATALOG` dictionary
3. Run: `python create_book_catalog.py`

### Modifying User Roles

**Via Django Admin:**
1. Navigate to `http://127.0.0.1:8000/admin`
2. Login with admin credentials
3. Edit users under "Library" > "Custom users"

**Via Django Shell:**
```bash
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> user = User.objects.get(username='username')
>>> user.role = 'librarian'  # or 'admin' or 'reader'
>>> user.save()
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
- Review the **API documentation**
- Ensure all dependencies are installed

---

**Version:** 1.0.0  
**Status:** Production Ready  
**Last Updated:** October 2025
