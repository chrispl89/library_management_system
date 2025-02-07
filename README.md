# Library Management System 📚

This is a Python-based Library Management System with a GUI built using tkinter. It allows users to manage a collection of books, supporting various operations such as adding, removing, editing, and searching for books.

The system also includes user management and a database backend (SQLite), where books are stored persistently, along with information about who added or last modified them.

## ✨ Features

### ✅ Graphical User Interface (GUI):
- User-friendly Tkinter interface with tabbed navigation (`ttk.Notebook`).
- Two main views:
  - **My Library** – Displays all books in the database.
  - **Database** – Provides an advanced global view with filtering & sorting.

### ✅ Database Integration (SQLite):
- Persistent book storage in an SQLite database (`library.db`).
- Column `last_modified_by` tracks the user who added or modified each book.
- Filtering & sorting options (including sorting by user who modified a book).

### ✅ User Management:
- Users can register and log in, maintaining their session.
- Each user can add, edit, and remove books (affecting a shared database).

### ✅ Book Management:
- Add books with title, author, category.
- Remove and edit books (with username tracking).
- Search books by title, author, category, or last modified by.

### ✅ Logging & Exception Handling:
- Logs user actions such as adding/removing/editing books.
- Handles database errors and incorrect user inputs.

## Installation 🛠️

1. Clone the repository:
    ```sh
    git clone https://github.com/chrispl89/library_management_system.git
    cd library-management-system
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage 🚀

1. Run the main script:
    ```sh
    python library_management_system.py
    ```

2. Use the Graphical Interface to manage books:
- View all books in the My Library tab.
- Add, remove, and edit books (all actions are stored in the database).
- Filter & sort books in the Database tab (by title, author, category, or last modified by).

3. After logging in, you can perform various library operations such as showing books, adding books, removing books, and editing books.

## Example 📖

```python
# Example of adding a book
library = Library()
book = Book("The Great Gatsby", "F. Scott Fitzgerald")
library.add_book(book)

# Example of saving library to a JSON file
file_manager = FileManager()
file_manager.save_to_json("library.json")

# Example of loading library from a JSON file
file_manager.load_from_json("library.json")
```

### Classes and Methods 🧩

### Book
- `__init__(self, title, author)`: Initializes a new book.
- `get_info(self)`: Returns information about the book.
- `set_category(self, new_category)`: Sets a new category for the book.

### Library
- `add_book(self, book)`: Adds a book to the library.
- `remove_book(self, book)`: Removes a book from the library.
- `edit_book(self, book, new_title=None, new_author=None, new_category=None)`: Edits the details of a book.
- `search_books(self, keyword, field=None)`: Searches for books based on a keyword.

### FileManager
- `save_to_json(self, filename)`: Saves the library contents to a JSON file.
- `load_from_json(self, filename)`: Loads data from a JSON file.

### UserManager
- `register(self, username)`: Registers a new user.
- `login(self, username)`: Logs in a user.

### DBManager
- `add_book(self, book, username)` – Adds a book to the database and tracks who added it.
- `edit_book(self, old_title, new_title=None, new_author=None, new_category=None, username=None)` – Updates a book and records the last modifier.
- `get_books(self, filter_field=None, filter_value=None, sort_field=None, ascending=True)` – Retrieves books with filtering and sorting.

### 💾 Database Schema (SQLite)
| Column            | Type    | Description                          |
|-------------------|---------|--------------------------------------|
| id                | INTEGER | Unique book ID (Primary Key)         |
| title             | TEXT    | Book title                           |
| author            | TEXT    | Book author                          |
| category          | TEXT    | Book category                        |
| last_modified_by  | TEXT    | User who last modified the book      |
