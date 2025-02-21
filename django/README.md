# Library Management System

A web-based Library Management System built with Django for managing library catalogs, tracking books, members, and borrowing activities.

## Features

- **Book Management**: Add, edit, and delete books with details (title, author, ISBN, genre, etc.).
- **Member Management**: Register and manage library members.
- **Borrowing System**: Track book borrow/return dates and calculate overdue fees.
- **Search Functionality**: Search books by title, author, or genre.
- **Authentication**: Secure login for librarians/admins.
- **Admin Dashboard**: Django admin interface for advanced management.

## Technology Stack

- **Backend**: Django (Python)
- **Database**: SQLite (default; can be configured for PostgreSQL/MySQL)
- **Frontend**: HTML, CSS, Bootstrap
- **Authentication**: Django Auth System
- **Tools**: django-extensions (for `runserver_plus`)

## Installation

1. **Prerequisites**:
   - Python 3.8+ installed
   - Git (optional)

2. **Clone the repository**:
   ```bash
   git clone https://github.com/chrispl89/library_management_system.git
   cd library_management_system/django
3. **Set up a virtual environment**:
    ```bash
    python -m venv venv
    # Linux/macOS:
    source venv/bin/activate
    # Windows:
    .\venv\Scripts\activate
4. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
5. **Run migrations**:
    ```bash
    python manage.py migrate
6. **Create a superuser (admin)**:
    ```bash
    python manage.py createsuperuser
7. **Run development server**:
    ```bash
    # Standard server:
    python manage.py runserver

    # OR with SSL (requires django-extensions):
    python manage.py runserver_plus --cert-file cert.pem
8. **Access the admin panel at http://localhost:8000/admin and log in with your superuser credentials.**

## Usage
- **Admin Panel**: Manage books, members, and borrowing records via the Django admin interface.

### Librarian Access

1. **Log in with admin credentials**
2. **Available actions**:
    - Add/edit books and members.
    - Track borrow/return status.
    - Search for books.
    - Generate reports
### Members
- View personal borrowing history (requires frontend implementation).

## Contributing

1. **[Fork the repository](https://github.com/chrispl89/library_management_system/fork)**.
2. Create a feature branch:  
   `git checkout -b feature/new-feature`.
3. Commit changes:  
   `git commit -m "Add new feature"`.
4. Push to the branch:  
   `git push origin feature/new-feature`.
5. **[Open a Pull Request](https://github.com/chrispl89/library_management_system/compare)**.


## Acknowledgements
- Built with **[Django](https://www.djangoproject.com/)**.
- Frontend styled with **[Bootstrap](https://getbootstrap.com/)**.
- SSL support: **[django-extensions](https://django-extensions.readthedocs.io/)**

---

**Note**: This project is primarily for educational purposes. For production use:

- Configure proper database (PostgreSQL/MySQL)

- Set up HTTPS with trusted certificate

- Implement additional security measures