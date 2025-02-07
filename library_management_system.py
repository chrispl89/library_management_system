import json
import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# ================================
# Decorator for logging function calls
# ================================
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

# ================================
# Exception definitions
# ================================
class InvalidBookError(Exception):
    """Exception raised when trying to add an invalid Book object."""
    pass

class BookNotFoundError(Exception):
    """Exception raised when a book is not found in the library."""
    pass

# ================================
# Book class
# ================================
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

# ================================
# Library class (in-memory, not used for persistence now)
# ================================
class Library:
    """
    Class managing a collection of books.
    """
    total_books = 0

    def __init__(self):
        self.books = []

    @staticmethod
    def is_valid_book(book):
        return isinstance(book, Book)

    @log_action
    def add_book(self, book):
        if not isinstance(book, Book):
            raise InvalidBookError(f'{book} is not a valid book')
        self.books.append(book)
        Library.total_books += 1

    @log_action
    def remove_book(self, book):
        if book not in self.books:
            raise BookNotFoundError(f"{book.title} not found in Library.")
        self.books.remove(book)
        Library.total_books -= 1

    def show_books(self):
        if self.books:
            for book in self.books:
                print(f"📚 {book.get_info()}")
        else:
            print("📭 The library is empty.")

    def edit_book(self, book, new_title=None, new_author=None, new_category=None):
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

    def remove_book_by_title(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                self.books.remove(book)
                print(f"📕 Book '{title}' has been removed.")
                return True
        print(f"❌ Book '{title}' not found.")
        return False

# ================================
# FileManager class (extends Library)
# ================================
class FileManager(Library):
    """
    Class extending Library with file save and load functionalities.
    """
    def write_to_file(self, filename):
        try:
            with open(filename, "w") as file:
                for book in self.books:
                    file.write(book.get_info() + "\n")
            print(f"💾 Library contents saved to {filename}.")
        except Exception as e:
            print(f"⚠️ An error occurred: {e}")

    def read_from_file(self, filename):
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
        try:
            with open(filename, "w") as file:
                books_data = [
                    {"title": book.title, "author": book.author, "category": book.category}
                    for book in self.books
                ]
                json.dump(books_data, file, indent=4)
            print(f"💾 Library contents saved to {filename} in JSON format.")
        except Exception as e:
            print(f"⚠️ An error occurred: {e}")

    def load_from_json(self, filename):
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

# ================================
# UserManager class
# ================================
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
        user_file = os.path.join(self.users_dir, f"{username}.json")
        if os.path.exists(user_file):
            print("❌ User already exists!")
            return False
        with open(user_file, "w") as f:
            json.dump([], f)
        print(f"✅ User '{username}' registered!")
        return True

    def login(self, username):
        user_file = os.path.join(self.users_dir, f"{username}.json")
        if not os.path.exists(user_file):
            print("❌ User does not exist!")
            return False
        self.current_user = FileManager()
        self.current_user.load_from_json(user_file)
        print(f"🔑 Logged in as '{username}'!")
        return True

# ================================
# DBManager class (with last_modified_by field)
# ================================
class DBManager:
    """
    Class managing an SQLite database storing books.
    """
    def __init__(self, db_file="library.db"):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.create_table()
        self.update_table()  # Ensure the column exists

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            last_modified_by TEXT NOT NULL DEFAULT 'unknown'
        );
        '''
        self.conn.execute(query)
        self.conn.commit()

    def update_table(self):
        cursor = self.conn.execute("PRAGMA table_info(books)")
        columns = [row[1] for row in cursor.fetchall()]
        if "last_modified_by" not in columns:
            self.conn.execute("ALTER TABLE books ADD COLUMN last_modified_by TEXT NOT NULL DEFAULT 'unknown'")
            self.conn.commit()
            print("Column 'last_modified_by' added to the 'books' table.")

    def add_book(self, book, username):
        query = "INSERT INTO books (title, author, category, last_modified_by) VALUES (?, ?, ?, ?);"
        self.conn.execute(query, (book.title, book.author, book.category, username))
        self.conn.commit()
        print(f"📕 Book '{book.title}' added to the database by {username}.")

    def remove_book(self, title):
        query = "DELETE FROM books WHERE lower(title)=?;"
        cur = self.conn.execute(query, (title.lower(),))
        self.conn.commit()
        if cur.rowcount > 0:
            print(f"📕 Book '{title}' has been removed from the database.")
            return True
        else:
            print(f"❌ Book '{title}' not found in the database.")
            return False

    def edit_book(self, old_title, new_title=None, new_author=None, new_category=None, username=None):
        cur = self.conn.execute("SELECT * FROM books WHERE lower(title)=?;", (old_title.lower(),))
        row = cur.fetchone()
        if row is None:
            print(f"❌ Book '{old_title}' not found in the database.")
            return False
        current_title, current_author, current_category = row[1], row[2], row[3]
        updated_title = new_title if new_title else current_title
        updated_author = new_author if new_author else current_author
        updated_category = new_category if new_category else current_category
        query = "UPDATE books SET title=?, author=?, category=?, last_modified_by=? WHERE id=?;"
        self.conn.execute(query, (updated_title, updated_author, updated_category, username if username else row[4], row[0]))
        self.conn.commit()
        print(f"✏️ Book '{old_title}' updated to '{updated_title}' in the database by {username}.")
        return True

    def get_books(self, user=None, filter_field=None, filter_value=None, sort_field=None, ascending=True):
        query = "SELECT title, author, category, last_modified_by FROM books"
        params = []
        conditions = []
        if user:
            conditions.append("last_modified_by = ?")
            params.append(user)
        if filter_field and filter_value:
            conditions.append(f"lower({filter_field}) LIKE ?")
            params.append(f"%{filter_value.lower()}%")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        if sort_field:
            query += f" ORDER BY {sort_field} {'ASC' if ascending else 'DESC'}"
        cur = self.conn.execute(query, params)
        rows = cur.fetchall()
        return rows

    def close(self):
        self.conn.close()

# ================================
# GUI - Login Frame
# ================================
class LoginFrame(tk.Frame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app  # reference to the main application
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Login / Register", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self, width=30)
        self.username_entry.pack(pady=5)
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Login", command=self.login).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Register", command=self.register).grid(row=0, column=1, padx=5)

    def login(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username!")
            return
        if self.app.user_manager.login(username):
            self.app.current_username = username
            # For DB operations, use DBManager as persistent storage
            self.app.current_library = self.app.db_manager
            self.app.show_notebook()
        else:
            messagebox.showerror("Error", "User does not exist!")

    def register(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username!")
            return
        if self.app.user_manager.register(username):
            messagebox.showinfo("Success", f"User '{username}' registered!")
        else:
            messagebox.showerror("Error", "User already exists!")

# ================================
# GUI - Library Frame (My Library: global view, showing ALL books)
# ================================
class LibraryFrame(tk.Frame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app  # reference to the main application
        self.create_widgets()

    def create_widgets(self):
        # Search Bar Frame
        search_frame = tk.Frame(self)
        search_frame.pack(pady=5, fill=tk.X)
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(search_frame, text=" in ").pack(side=tk.LEFT)
        self.search_field = ttk.Combobox(search_frame, values=["All", "Title", "Author", "Category", "Last Modified By"], width=15)
        self.search_field.current(0)
        self.search_field.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_books).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Reset", command=self.refresh_tree).pack(side=tk.LEFT, padx=5)

        # Book form
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)
        tk.Label(form_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = tk.Entry(form_frame, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Author:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.author_entry = tk.Entry(form_frame, width=40)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Category:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.category_entry = tk.Entry(form_frame, width=40)
        self.category_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Button(form_frame, text="Add Book", command=self.add_book).grid(row=3, column=0, columnspan=2, pady=10)

        # Treeview for showing books (with Last Modified By column)
        self.tree = ttk.Treeview(self, columns=("Title", "Author", "Category", "Last Modified By"), show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Last Modified By", text="Last Modified By")
        self.tree.column("Title", width=200)
        self.tree.column("Author", width=150)
        self.tree.column("Category", width=150)
        self.tree.column("Last Modified By", width=150)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Operation buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Remove Book", command=self.remove_book).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Edit Book", command=self.edit_book).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_tree).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Logout", command=self.logout).grid(row=0, column=3, padx=5)

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        category = self.category_entry.get().strip()
        if not title or not author:
            messagebox.showerror("Error", "Title and Author cannot be empty!")
            return
        new_book = Book(title, author)
        if category:
            new_book.set_category(category)
        self.app.current_library.add_book(new_book, self.app.current_username)
        messagebox.showinfo("Success", f"Book '{title}' has been added!")
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.refresh_tree()

    def remove_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to remove!")
            return
        item = selected[0]
        values = self.tree.item(item, "values")
        title = values[0]
        if self.app.current_library.remove_book(title):
            messagebox.showinfo("Success", f"Book '{title}' has been removed!")
        else:
            messagebox.showerror("Error", f"Book '{title}' not found!")
        self.refresh_tree()

    def edit_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to edit!")
            return
        item = selected[0]
        values = self.tree.item(item, "values")
        old_title, old_author, old_category, _ = values
        new_title = simpledialog.askstring("Edit Book", "New Title:", initialvalue=old_title)
        if new_title is None or new_title.strip() == "":
            return
        new_author = simpledialog.askstring("Edit Book", "New Author:", initialvalue=old_author)
        if new_author is None or new_author.strip() == "":
            return
        new_category = simpledialog.askstring("Edit Book", "New Category:", initialvalue=old_category)
        if new_category is None or new_category.strip() == "":
            return
        if self.app.current_library.edit_book(old_title, new_title.strip(), new_author.strip(), new_category.strip(), username=self.app.current_username):
            messagebox.showinfo("Success", "Book updated successfully!")
        else:
            messagebox.showerror("Error", "Failed to update book!")
        self.refresh_tree()

    def search_books(self):
        keyword = self.search_entry.get().strip()
        field = self.search_field.get().lower()
        if not keyword:
            messagebox.showwarning("Warning", "Please enter a search keyword!")
            return
        search_field = None if field == "all" else field.replace(" ", "_")
        results = self.app.current_library.get_books(filter_field=search_field, filter_value=keyword)
        for item in self.tree.get_children():
            self.tree.delete(item)
        for book in results:
            self.tree.insert("", tk.END, values=book)
            
    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Now show all books from the database (global view)
        for book in self.app.current_library.get_books():
            self.tree.insert("", tk.END, values=book)

    def logout(self):
        self.app.logout()

# ================================
# GUI - Database Frame (global DB view with filtering/sorting)
# ================================
class DBFrame(tk.Frame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        # Search Bar Frame for DB operations
        search_frame = tk.Frame(self)
        search_frame.pack(pady=5, fill=tk.X)
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(search_frame, text=" in ").pack(side=tk.LEFT)
        self.search_field = ttk.Combobox(search_frame, values=["All", "Title", "Author", "Category", "Last Modified By"], width=15)
        self.search_field.current(0)
        self.search_field.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_books).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Reset", command=self.refresh_tree).pack(side=tk.LEFT, padx=5)

        # Book form for database operations
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)
        tk.Label(form_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = tk.Entry(form_frame, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Author:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.author_entry = tk.Entry(form_frame, width=40)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Category:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.category_entry = tk.Entry(form_frame, width=40)
        self.category_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Button(form_frame, text="Add Book", command=self.add_book).grid(row=3, column=0, columnspan=2, pady=10)

        # Treeview for database books (global view)
        self.tree = ttk.Treeview(self, columns=("Title", "Author", "Category", "Last Modified By"), show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Last Modified By", text="Last Modified By")
        self.tree.column("Title", width=200)
        self.tree.column("Author", width=150)
        self.tree.column("Category", width=150)
        self.tree.column("Last Modified By", width=150)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Buttons for DB operations
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Remove Book", command=self.remove_book).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Edit Book", command=self.edit_book).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_tree).grid(row=0, column=2, padx=5)

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        category = self.category_entry.get().strip()
        if not title or not author:
            messagebox.showerror("Error", "Title and Author cannot be empty!")
            return
        new_book = Book(title, author)
        if category:
            new_book.set_category(category)
        self.app.db_manager.add_book(new_book, self.app.current_username)
        messagebox.showinfo("Success", f"Book '{title}' added to the database!")
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.refresh_tree()

    def remove_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to remove!")
            return
        item = selected[0]
        title = self.tree.item(item, "values")[0]
        if self.app.db_manager.remove_book(title):
            messagebox.showinfo("Success", f"Book '{title}' removed from the database!")
        else:
            messagebox.showerror("Error", f"Book '{title}' not found in the database!")
        self.refresh_tree()

    def edit_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to edit!")
            return
        item = selected[0]
        old_title, old_author, old_category, _ = self.tree.item(item, "values")
        new_title = simpledialog.askstring("Edit Book", "New Title:", initialvalue=old_title)
        if new_title is None or new_title.strip() == "":
            return
        new_author = simpledialog.askstring("Edit Book", "New Author:", initialvalue=old_author)
        if new_author is None or new_author.strip() == "":
            return
        new_category = simpledialog.askstring("Edit Book", "New Category:", initialvalue=old_category)
        if new_category is None or new_category.strip() == "":
            return
        if self.app.db_manager.edit_book(old_title, new_title.strip(), new_author.strip(), new_category.strip(), username=self.app.current_username):
            messagebox.showinfo("Success", "Book updated successfully in the database!")
        else:
            messagebox.showerror("Error", "Failed to update book in the database!")
        self.refresh_tree()

    def search_books(self):
        keyword = self.search_entry.get().strip()
        field = self.search_field.get().lower()
        if not keyword:
            messagebox.showwarning("Warning", "Please enter a search keyword!")
            return
        filter_field = None if field == "all" else field.replace(" ", "_")
        results = self.app.db_manager.get_books(filter_field=filter_field, filter_value=keyword)
        for item in self.tree.get_children():
            self.tree.delete(item)
        for book in results:
            self.tree.insert("", tk.END, values=book)

    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for book in self.app.db_manager.get_books():
            self.tree.insert("", tk.END, values=book)

# ================================
# Main Application class
# ================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("850x650")
        # Initialize managers
        self.user_manager = UserManager()
        self.db_manager = DBManager()
        self.current_library = None  # Will be set to DBManager upon login
        self.current_username = None  # To track the logged-in user for DB operations

        # Create frames
        self.login_frame = LoginFrame(self, self)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        # Notebook for Library and Database operations (shown after login)
        self.notebook = ttk.Notebook(self)
        self.library_frame = LibraryFrame(self.notebook, self)
        self.db_frame = DBFrame(self.notebook, self)
        self.notebook.add(self.library_frame, text="My Library")
        self.notebook.add(self.db_frame, text="Database")

    def show_notebook(self):
        self.login_frame.pack_forget()
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.library_frame.refresh_tree()
        self.db_frame.refresh_tree()

    def logout(self):
        self.notebook.pack_forget()
        self.current_library = None
        self.current_username = None
        self.login_frame.username_entry.delete(0, tk.END)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

# ================================
# Run the application
# ================================
if __name__ == "__main__":
    app = App()
    app.mainloop()
