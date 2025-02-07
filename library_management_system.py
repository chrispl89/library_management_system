import json
import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


def log_action(func):
    """
    Decorator for logging function calls.

    Logs the function name and arguments, and also handles any exceptions.
    """
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            args_info = ", ".join(
                str(arg.title) if isinstance(arg, Book) else str(arg)
                for arg in args[1:]
            )
            print(f"📋 Action logged: {func.__name__} was called with {args_info}.")
            return result
        except Exception as e:
            print(f"⚠️ Exception occurred during {func.__name__}: {e}")
            raise
    return wrapper

class InvalidBookError(Exception):
    """Exception raised when trying to add an invalid Book object."""
    pass

class BookNotFoundError(Exception):
    """Exception raised when a book is not found in the library."""
    pass

class Book:
    """
    Class representing a book.
    
    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        category (str): The category of the book (default is "Literature").
    """
    category = "Literature"

    def __init__(self, title, author):
        """
        Initializes a new instance of the Book class.
        
        Args:
            title (str): The title of the book.
            author (str): The author of the book.
        """
        self.title = title
        self.author = author

    def get_info(self):
        """
        Returns a formatted string with information about the book.

        Returns:
            str: Information about the book (title, author, category).
        """
        return f"Title: {self.title}, Author: {self.author}, Category: {self.category}"

    def set_category(self, new_category):
        """
        Sets a new category for the book.
        
        Args:
            new_category (str): The new category.
        """
        self.category = new_category

class Library:
    """
    Class managing a collection of books.

    Attributes:
        books (list): List of books in the library.
        total_books (int): Total number of books in all libraries.
    """
    total_books = 0

    def __init__(self):
        """Initializes an empty library."""
        self.books = []

    @staticmethod
    def is_valid_book(book):
        """
        Checks if the given object is an instance of the Book class.

        Args:
            book: The object to check.

        Returns:
            bool: True if the object is an instance of Book, otherwise False.
        """
        return isinstance(book, Book)

    @log_action
    def add_book(self, book):
        """
        Adds a book to the library.

        Args:
            book (Book): The book object to add.

        Raises:
            InvalidBookError: If the object is not an instance of the Book class.
        """
        if not isinstance(book, Book):
            raise InvalidBookError(f'{book} is not a valid book')
        self.books.append(book)
        Library.total_books += 1

    @log_action
    def remove_book(self, book):
        """
        Removes a book from the library.

        Args:
            book (Book): The book to remove.

        Raises:
            BookNotFoundError: If the book is not found in the library.
        """
        if book not in self.books:
            raise BookNotFoundError(f"{book.title} not found in Library.")
        self.books.remove(book)
        Library.total_books -= 1

    def show_books(self):
        """
        Displays information about all books in the library.
        """
        if self.books:
            for book in self.books:
                print(f"📚 {book.get_info()}")
        else:
            print("📭 The library is empty.")

    @classmethod
    def from_book_list(cls, book_list):
        """
        Creates a library from a list of books.

        Args:
            book_list (list): List of Book objects.

        Returns:
            Library: A new instance of the Library class with the added books.
        """
        library = cls()
        for book in book_list:
            if cls.is_valid_book(book):
                library.add_book(book)
            else:
                print(f"{book} is not a valid book.")
        return library

    def edit_book(self, book, new_title=None, new_author=None, new_category=None):
        """
        Edits the details of a book in the library.

        Args:
            book (Book): The book to edit.
            new_title (str, optional): The new title.
            new_author (str, optional): The new author.
            new_category (str, optional): The new category.

        Raises:
            BookNotFoundError: If the book is not found in the library.
        """
        if book not in self.books:
            raise BookNotFoundError(f"❌ {book.title} not found in Library.")
        if new_title:
            book.title = new_title
        if new_author:
            book.author = new_author
        if new_category:
            book.set_category(new_category)
        print(f"✏️ Book updated: {book.get_info()}")

    def search_books(self, keyword, field=None):
        """
        Searches for books in the library based on the given keyword.

        Args:
            keyword (str): The word or string to search for.
            field (str, optional): The field to search in.
                Can be "title", "author", or "category". 
                If not provided, all fields are searched.

        Returns:
            list: List of books that match the search criteria.
        """
        keyword_lower = keyword.lower()
        results = []
        for book in self.books:
            if field == "title":
                if keyword_lower in book.title.lower():
                    results.append(book)
            elif field == "author":
                if keyword_lower in book.author.lower():
                    results.append(book)
            elif field == "category":
                if keyword_lower in book.category.lower():
                    results.append(book)
            else:
                if (keyword_lower in book.title.lower() or 
                    keyword_lower in book.author.lower() or 
                    keyword_lower in book.category.lower()):
                    results.append(book)
        return results

    def sort_books(self, field="title", ascending=True):
        """
        Sorts books by the given criterion.

        Args:
            field (str): The field to sort books by. Possible values: "title", "author", "category".
            ascending (bool): Whether to sort in ascending (True) or descending (False) order.

        Returns:
            list: Sorted list of books.
        """
        valid_fields = ["title", "author", "category"]
        if field not in valid_fields:
            raise ValueError(f"Invalid sorting field. Choose from: {valid_fields}")

        sorted_books = sorted(self.books, key=lambda book: getattr(book, field).lower(), reverse=not ascending)
        return sorted_books

    def remove_book_by_title(self, title):
        """
        Removes a book from the library based on the title.

        Args:
            title (str): The title of the book to remove.

        Returns:
            bool: True if the book was removed, False if not found.
        """
        for book in self.books:
            if book.title.lower() == title.lower():
                self.books.remove(book)
                print(f"📕 Book '{title}' has been removed.")
                return True
        print(f"❌ Book '{title}' not found.")
        return False

class FileManager(Library):
    """
    Class extending Library with file save and load functionalities.
    """
    def write_to_file(self, filename):
        """
        Saves the library contents to a text file.

        Args:
            filename (str): The name of the file to save data to.
        """
        try:
            with open(filename, "w") as file:
                for book in self.books:
                    file.write(book.get_info() + "\n")
            print(f"💾 Library contents saved to {filename}.")
        except Exception as e:
            print(f"⚠️ An error occurred: {e}")

    def read_from_file(self, filename):
        """
        Reads the contents of a text file and displays it.

        Args:
            filename (str): The name of the file to read from.
        """
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
                print(f"📄 Contents of {filename}:")
                for line in lines:
                    print(line.strip())
        except FileNotFoundError:
            print(f"❌ File {filename} not found.")
        except Exception as e:
            print(f"⚠️ An error occurred: {e}")

    def save_to_json(self, filename):
        """
        Saves the library contents to a JSON file.

        Args:
            filename (str): The name of the JSON file to save data to.
        """
        try:
            with open(filename, "w") as file:
                books_data = [
                    {
                        "title": book.title,
                        "author": book.author,
                        "category": book.category
                    }
                    for book in self.books
                ]
                json.dump(books_data, file, indent=4)
            print(f"💾 Library contents saved to {filename} in JSON format.")
        except Exception as e:
            print(f"⚠️ An error occurred: {e}")

    def load_from_json(self, filename):
        """
        Loads data from a JSON file and adds books to the library.

        Args:
            filename (str): The name of the JSON file to read from.
        """
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                for book_data in data:
                    if "title" not in book_data or "author" not in book_data or "category" not in book_data:
                        print(f"⚠️ Skipping invalid book data: {book_data}")
                        continue
                    book = Book(book_data["title"], book_data["author"])
                    book.set_category(book_data["category"])
                    self.add_book(book)
            print(f"📄 Library contents loaded from {filename}.")
        except FileNotFoundError:
            print(f"❌ File {filename} not found.")
        except json.JSONDecodeError:
            print(f"⚠️ Invalid JSON format in {filename}.")
        except Exception as e:
            print(f"⚠️ An error occurred: {e}")

    # Remove the edit_book method from FileManager to use the inherited one from Library

class UserManager:
    """
    Class managing users.
    Each user has their own library saved in the 'users' directory.
    """
    def __init__(self):
        self.users_dir = "users"
        os.makedirs(self.users_dir, exist_ok=True)
        self.current_user = None

    def register(self, username):
        """
        Registers a new user by creating an empty library for them.

        Args:
            username (str): The username.

        Returns:
            bool: True if registration was successful, False if the user already exists.
        """
        user_file = os.path.join(self.users_dir, f"{username}.json")
        if os.path.exists(user_file):
            print("❌ User already exists!")
            return False

        with open(user_file, "w") as f:
            json.dump([], f)
        print(f"✅ User '{username}' registered!")
        return True

    def login(self, username):
        """
        Logs in a user by loading their library from a file.

        Args:
            username (str): The username.

        Returns:
            bool: True if login was successful, False otherwise.
        """
        user_file = os.path.join(self.users_dir, f"{username}.json")
        if not os.path.exists(user_file):
            print("❌ User does not exist!")
            return False

        self.current_user = FileManager()
        self.current_user.load_from_json(user_file)
        print(f"🔑 Logged in as '{username}'!")
        return True

class DBManager:
    """
    Class managing an SQLite database storing books.
    """
    def __init__(self, db_file="library.db"):
        """
        Initializes a connection to the SQLite database.
        
        Args:
            db_file (str): The name of the database file.
        """
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.create_table()

    def create_table(self):
        """
        Creates the 'books' table in the database if it does not already exist.
        """
        query = '''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL
        );
        '''
        self.conn.execute(query)
        self.conn.commit()

    def add_book(self, book):
        """
        Adds a book to the database.
        
        Args:
            book (Book): The Book object whose data will be saved.
        """
        query = "INSERT INTO books (title, author, category) VALUES (?, ?, ?);"
        self.conn.execute(query, (book.title, book.author, book.category))
        self.conn.commit()
        print(f"📕 Book '{book.title}' added to the database.")

    def remove_book(self, title):
        """
        Removes a book from the database based on the title.
        
        Args:
            title (str): The title of the book to remove.
            
        Returns:
            bool: True if the book was removed, False otherwise.
        """
        query = "DELETE FROM books WHERE lower(title)=?;"
        cur = self.conn.execute(query, (title.lower(),))
        self.conn.commit()
        if cur.rowcount > 0:
            print(f"📕 Book '{title}' has been removed from the database.")
            return True
        else:
            print(f"❌ Book '{title}' not found in the database.")
            return False

    def edit_book(self, old_title, new_title=None, new_author=None, new_category=None):
        """
        Updates the details of a book in the database.
        
        Args:
            old_title (str): The title of the book to update.
            new_title (str, optional): The new title.
            new_author (str, optional): The new author.
            new_category (str, optional): The new category.
            
        Returns:
            bool: True if the update was successful, False if the book was not found.
        """
        cur = self.conn.execute("SELECT * FROM books WHERE lower(title)=?;", (old_title.lower(),))
        row = cur.fetchone()
        if row is None:
            print(f"❌ Book '{old_title}' not found in the database.")
            return False
        current_title, current_author, current_category = row[1], row[2], row[3]
        updated_title = new_title if new_title else current_title
        updated_author = new_author if new_author else current_author
        updated_category = new_category if new_category else current_category
        query = "UPDATE books SET title=?, author=?, category=? WHERE id=?;"
        self.conn.execute(query, (updated_title, updated_author, updated_category, row[0]))
        self.conn.commit()
        print(f"✏️ Book '{old_title}' updated to '{updated_title}' in the database.")
        return True

    def get_books(self):
        """
        Retrieves all books from the database.
        
        Returns:
            list: List of tuples containing (title, author, category) of each book.
        """
        query = "SELECT title, author, category FROM books;"
        cur = self.conn.execute(query)
        rows = cur.fetchall()
        return rows

    def close(self):
        """
        Closes the connection to the database.
        """
        self.conn.close()

if __name__ == "__main__":
    # USER MENU – login/registration
    user_manager = UserManager()
    
    while True:
        print("\n🔹 Menu:")
        print("1️⃣ Register")
        print("2️⃣ Login")
        print("3️⃣ Exit")
        choice = input("➡️ Choose an option: ")

        if choice == "1":
            username = input("🆕 Enter username: ")
            user_manager.register(username)
        elif choice == "2":
            username = input("🔑 Enter username: ")
            if user_manager.login(username):
                break  # Successfully logged in – exit the loop
        elif choice == "3":
            print("👋 Goodbye!")
            exit()
        else:
            print("❌ Unknown option! Try again.")

    # After logging in, operate on the logged-in user's library:
    current_library = user_manager.current_user
    print("\n📚 Your library (after login):")
    current_library.show_books()

    # LIBRARY OPERATIONS MENU
    while True:
        print("\n📚 Library Menu:")
        print("1️⃣ Show books")
        print("2️⃣ Add book")
        print("3️⃣ Remove book")
        print("4️⃣ Edit book")
        print("5️⃣ Logout")
        lib_choice = input("➡️ Choose an option: ")

        if lib_choice == "1":
            current_library.show_books()
        elif lib_choice == "2":
            title = input("📖 Enter book title: ")
            author = input("✍️ Enter book author: ")
            new_book = Book(title, author)
            current_library.add_book(new_book)
        elif lib_choice == "3":
            title = input("🗑️ Enter book title to remove: ")
            current_library.remove_book_by_title(title)
        elif lib_choice == "4":
            old_title = input("📖 Enter book title to edit: ")
            new_title = input("✏️ Enter new title (or press Enter to keep current): ")
            new_author = input("✏️ Enter new author (or press Enter to keep current): ")
            new_title = new_title if new_title.strip() else None
            new_author = new_author if new_author.strip() else None
            # Find the book object based on the title
            book_to_edit = next((b for b in current_library.books if b.title.lower() == old_title.lower()), None)
            if book_to_edit:
                current_library.edit_book(book_to_edit, new_title, new_author)
            else:
                print("❌ Book not found for editing.")
        elif lib_choice == "5":
            print("👋 Logged out!")
            break
        else:
            print("❌ Unknown option, try again.")

    # After finishing library operations, display its state:
    print("\n📚 Your library:")
    current_library.show_books()

    # ADDITIONAL OPERATIONS ON THE DATABASE (SQLite)
    print("\n=== SQLite Database Operations ===")
    db_manager = DBManager()

    # Create some books
    book1 = Book("Hobbit", "Tolkien")
    book2 = Book("Harry Potter", "Rowling")
    book3 = Book("Eragon", "Paolini")

    # Add books to the database
    db_manager.add_book(book1)
    db_manager.add_book(book2)
    db_manager.add_book(book3)

    # Display books from the database
    print("\n📚 Books in the database:")
    books = db_manager.get_books()
    for b in books:
        print(f"📖 Title: {b[0]}, ✍️ Author: {b[1]}, 📚 Category: {b[2]}")

    # Edit a book
    if db_manager.edit_book("Hobbit", new_title="The Hobbit", new_author="J.R.R. Tolkien", new_category="Fantasy"):
        print("\n✅ Book updated.")
    else:
        print("\n❌ Book not found for editing.")

    # Remove a book
    if db_manager.remove_book("Harry Potter"):
        print("\n✅ Book 'Harry Potter' has been removed from the database.")
    else:
        print("\n❌ Book 'Harry Potter' not found.")

    # Display books from the database after modifications
    print("\n📚 Current database contents:")
    books = db_manager.get_books()
    for b in books:
        print(f"📖 Title: {b[0]}, ✍️ Author: {b[1]}, 📚 Category: {b[2]}")

    # Close the database connection
    db_manager.close()
