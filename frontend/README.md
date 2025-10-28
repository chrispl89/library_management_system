# Library Management System - Frontend

Modern React frontend application for the Library Management System with full Django REST API integration.

## ✨ Features

### Authentication & Authorization
- **JWT-based authentication** with token refresh
- **Role-based access control** (Admin, Librarian, Reader)
- **Secure login and registration**
- **Protected routes** for authenticated users

### Book Catalog
- **Browse 300+ books** across 15 categories
- **Advanced search** by title, author, or category
- **Category filtering** with dropdown selector
- **Real-time availability** tracking
- **One-click borrowing** directly from catalog
- **Google Books integration** for easy book addition

### Book Management (Librarians & Admins)
- **Add new books** manually or via Google Books search
- **Edit book information**
- **Delete books** from catalog
- **View who added each book**

### Loan System
- **Borrow books** with automatic 14-day due date
- **Track active loans** in dedicated page
- **Return books** with one click
- **Fine calculation** for overdue returns ($1/day)
- **Loan status tracking** (ACTIVE/RETURNED/OVERDUE)

### Reservations
- **Reserve unavailable books**
- **3-day reservation period**
- **View active reservations**
- **Cancel reservations**

### Reviews & Ratings
- **5-star rating system**
- **Write detailed reviews**
- **View all book reviews**

### User Dashboard
- **Activity overview** with statistics
- **Active loans summary**
- **Current reservations**
- **Review history**
- **User profile** with activity tracking

## 🛠️ Tech Stack

- **React 19.2.0** - UI framework
- **React Router DOM 7.9.4** - Client-side routing
- **Axios 1.12.2** - HTTP client for API calls
- **Bootstrap 5.3.8** - CSS framework
- **TailwindCSS** - Utility-first styling
- **Lucide React 0.546.0** - Modern icon library
- **JWT Decode 4.0.0** - Token management

## 📋 Prerequisites

- **Node.js** v14 or higher
- **npm** (comes with Node.js)
- **Django backend** running on `http://127.0.0.1:8000`

## 🚀 Installation

### 1. Install dependencies
```bash
cd frontend
npm install
```

### 2. Ensure backend is running
Make sure the Django backend is running on port 8000:
```bash
# In another terminal
cd django
python manage.py runserver
```

### 3. Start development server
```bash
npm start
```

The application will automatically open at **http://localhost:3000**

## 🔐 Test Credentials

Use these credentials to test the application:

| Username | Password | Role |
|----------|----------|------|
| reader_user | ReaderPass123! | Reader |
| librarian_user | LibrarianPass123! | Librarian |
| admin_user | AdminPass123! | Admin |

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Layout.js          # Main layout with navigation
│   ├── context/
│   │   └── AuthContext.js     # Authentication context
│   ├── pages/
│   │   ├── Home.js            # Landing page
│   │   ├── Login.js           # Login page
│   │   ├── Register.js        # Registration page
│   │   ├── Books.js           # Books management
│   │   ├── Loans.js           # Loans management
│   │   ├── Reservations.js    # Reservations management
│   │   ├── Reviews.js         # Reviews management
│   │   └── Dashboard.js       # User dashboard
│   ├── services/
│   │   └── api.js             # API service layer
│   ├── App.js                 # Main app component
│   └── index.js               # Entry point
└── package.json
```

## API Integration

The frontend communicates with the Django backend through the following endpoints:

- **Authentication**: `/api/token/`, `/api/register/`
- **Books**: `/api/books/`
- **Loans**: `/api/loans/`
- **Reservations**: `/api/reservations/`
- **Reviews**: `/api/reviews/`
- **Dashboard**: `/api/dashboard/`
- **Google Books**: `/api/google-books/`

## 👥 User Roles & Permissions

### Reader
- ✅ Browse and search all books
- ✅ Filter by category
- ✅ Borrow available books
- ✅ Return books
- ✅ Create reservations
- ✅ Write reviews and ratings
- ✅ View personal dashboard
- ❌ Cannot add/edit/delete books

### Librarian
- ✅ All Reader permissions
- ✅ Add new books
- ✅ Edit book information
- ✅ Delete books
- ✅ View who added each book
- ❌ Cannot manage users

### Admin
- ✅ All Librarian permissions
- ✅ User management
- ✅ Delete any review
- ✅ Full system access

## 📜 Available Scripts

### `npm start`
Runs the app in development mode at **http://localhost:3000**

### `npm test`
Launches the test runner in interactive watch mode

### `npm run build`
Builds the app for production to the `build` folder

## 🐛 Troubleshooting

### Frontend won't start

**Clear cache and reinstall:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Check Node version:**
```bash
node --version  # Should be v14+
```

### Login not working

**Hard refresh the page:**
- Press `Ctrl + Shift + R` (Windows/Linux)
- Press `Cmd + Shift + R` (Mac)

**Check browser console:**
- Press `F12` to open Developer Tools
- Look for errors in Console tab

**Verify backend is running:**
```bash
curl http://127.0.0.1:8000/api/books/
```

### Books not showing

**Backend needs data:**
```bash
cd ..
python setup_test_data.py
python create_book_catalog.py
```

**Clear browser cache:**
- Settings → Privacy → Clear browsing data
- Select "Cached images and files"

### CORS errors

**Ensure backend CORS is configured:**
- Check `django/library_management_project/settings.py`
- CORS_ALLOWED_ORIGINS should include `http://localhost:3000`

## 🎯 Usage Guide

### Browsing Books
1. Navigate to "Books" page
2. Use search bar to find books
3. Select category from dropdown filter
4. Click book card to see details

### Borrowing Books
1. Login as any user
2. Find an available book
3. Click green "Borrow Book" button
4. Book is loaned for 14 days automatically

### Managing Loans
1. Go to "Loans" page
2. View all active loans
3. Click "Return Book" to return
4. Late returns show fine amount

### Adding Books (Librarian/Admin only)
1. Login as librarian or admin
2. Click "Add Book" button
3. Search Google Books or enter manually
4. Fill in details and save

## 🔗 API Configuration

API base URL is configured in `src/services/api.js`:

```javascript
const API_BASE_URL = 'http://127.0.0.1:8000/api';
```

To change for production, update this constant.

## 📱 Pages

- **/** - Home/Landing page
- **/login** - User login
- **/register** - New user registration
- **/books** - Browse and search books
- **/loans** - Manage loans (protected)
- **/reservations** - Book reservations (protected)
- **/reviews** - Write and view reviews (protected)
- **/dashboard** - User dashboard (protected)

## 🎨 Styling

The app uses a combination of:
- **Bootstrap** for base components
- **TailwindCSS** for utility classes
- **Custom CSS** in component files

## 📦 Build for Production

```bash
npm run build
```

Creates optimized production build in `build/` folder.

## 📄 License

This project is for educational purposes.

---

**Version:** 1.0.0  
**Built with:** Create React App  
**Last Updated:** October 2025
