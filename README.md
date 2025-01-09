# Library Management System

This is a simple Library Management System written in Python. It allows you to manage books and magazines in a library, borrow and return them, and keep track of availability. The system demonstrates the use of object-oriented programming (OOP) principles like inheritance, encapsulation, and polymorphism.

## Features

- **Add books and magazines**: You can add books and magazines to the library.
- **Borrow and return books**: Users can borrow books if they are available and return them once they are done.
- **Track availability**: The system tracks whether each book or magazine is available or borrowed.
- **Book and magazine details**: Detailed information about each book or magazine, including title, author, and issue number (for magazines), is displayed.

## Classes

### Book
The `Book` class represents a general book in the library.

- **Attributes**:
  - `title`: The title of the book.
  - `author`: The author of the book.
  - `available`: A boolean indicating whether the book is available for borrowing.
  
- **Methods**:
  - `get_info()`: Returns the information about the book, including its availability.
  - `borrow()`: Marks the book as borrowed.
  - `return_book()`: Marks the book as available.

### Magazine (Inherits from `Book`)
The `Magazine` class represents a magazine in the library, inheriting from the `Book` class.

- **Attributes**:
  - `issue_number`: The issue number of the magazine.
  
- **Methods**:
  - `get_info()`: Returns the information about the magazine, including its issue number and availability.

### Library
The `Library` class manages a collection of books and magazines.

- **Attributes**:
  - `books`: A list of books and magazines in the library.
  
- **Methods**:
  - `add_book()`: Adds a book or magazine to the library.
  - `list_books()`: Lists all the books and magazines in the library.
  - `borrow_book()`: Allows a user to borrow a book if it is available.
  - `return_book()`: Allows a user to return a borrowed book.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/library-management-system.git
