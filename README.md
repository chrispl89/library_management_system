# Library Management System 📚

This is a Python-based Library Management System that allows users to manage a collection of books. The system supports various operations such as adding, removing, editing, and searching for books. It also includes user management and database functionalities.

## Features ✨

- **Book Management**: Add, remove, edit, and search for books.
- **User Management**: Register and login users, each with their own library.
- **File Operations**: Save and load library data to/from text and JSON files.
- **Database Integration**: Store and manage books using an SQLite database.
- **Logging**: Log actions and handle exceptions with detailed messages.

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
    python library.py
    ```

2. Follow the on-screen menu to register or login as a user.

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


### Classes and Methods 🧩

### Book
- `__init__(self, title, author)`: Initializes a new book.
- `get_info(self)`: Returns information about the book.
- `set_category(self, new_category)`: Sets a new category for the book.

### Library
- `add_book(self, book)`: Adds a book to the library.
- `remove_book(self, book)`: Removes a book from the library.
- `show_books(self)`: Displays all books in the library.
- `edit_book(self, book, new_title=None, new_author=None, new_category=None)`: Edits the details of a book.
- `search_books(self, keyword, field=None)`: Searches for books based on a keyword.
- `sort_books(self, field="title", ascending=True)`: Sorts books by a specified field.

### FileManager
- `write_to_file(self, filename)`: Saves the library contents to a text file.
- `read_from_file(self, filename)`: Reads the contents of a text file.
- `save_to_json(self, filename)`: Saves the library contents to a JSON file.
- `load_from_json(self, filename)`: Loads data from a JSON file.

### UserManager
- `register(self, username)`: Registers a new user.
- `login(self, username)`: Logs in a user.

### DBManager
- `add_book(self, book)`: Adds a book to the database.
- `remove_book(self, title)`: Removes a book from the database.
- `edit_book(self, old_title, new_title=None, new_author=None, new_category=None)`: Updates the details of a book in the database.
- `get_books(self)`: Retrieves all books from the database.

