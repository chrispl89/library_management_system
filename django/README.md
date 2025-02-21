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
    source venv/bin/activate  # On Windows: venv\Scripts\activate
4. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
5. **Run migrations**:
    ```bash
    python manage.py migrate
6. **Create a superuser (admin)**:
    ```bash
    python manage.py createsuperuser
7. **Run the server**:
    ```bash
    python manage.py runserver_plus --cert-file cert.pem --key-file key.pem 
    # using SSL. In production use trusted certificate
8. **Access the admin panel at http://localhost:8000/admin and log in with your superuser credentials.**

## Usage
- **Admin Panel**: Manage books, members, and borrowing records via the Django admin interface.
- **Librarian Access**: Log in to the system to:

    - Add/edit books and members.

    - Track borrow/return status.

    - Search for books.
- **Members**: Members can view their borrowing history (if frontend is implemented).

## Contributing

1. **[Fork the repository](https://github.com/chrispl89/library_management_system/fork)**.
2. Create a feature branch:  
   `git checkout -b feature/new-feature`.
3. Commit changes:  
   `git commit -m "Add new feature"`.
4. Push to the branch:  
   `git push origin feature/new-feature`.
5. **[Open a Pull Request](https://github.com/chrispl89/library_management_system/compare)**.

## License
Distributed under the **[MIT License](https://choosealicense.com/licenses/mit/)**. See **[LICENSE](https://github.com/chrispl89/library_management_system/blob/main/LICENSE)** for details.

## Acknowledgements
- Built with **[Django](https://www.djangoproject.com/)**.
- Frontend styled with **[Bootstrap](https://getbootstrap.com/)**.

---

**Note**: This project is intended for educational purposes. Customize the database and settings for production use.