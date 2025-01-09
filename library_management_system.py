class Book:
    borrow_count = 0

    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True

    def get_info(self):
        status = "Available" if self.available else "Borrowed"
        return f"Title: {self.title}\nAuthor: {self.author}\nAvailable: {status}"

    def borrow(self):
        self.available = False

    def return_book(self):
        self.available = True

class Magazine(Book):
    def __init__(self, title, author, issue_number):
        super().__init__(title, author)
        self.issue_number = issue_number

    def get_info(self):
        status = "Available" if self.available else "Borrowed"
        return (f"Title: {self.title}\nAuthor: {self.author}\n"
                f"Issue: {self.issue_number}\nAvailable: {status}")

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def list_books(self):
        if not self.books:
            return "No books in the library."
        books_info = [book.get_info() for book in self.books]
        return f"Books list:\n"+"\n".join(books_info)

    def borrow_book(self, title):
        for book in self.books:
            if book.title == title:
                if book.available:
                    book.available = False
                    Book.borrow_count += 1
                    return f"You have borrowed '{title}'."
                else:
                    return f"Sorry, '{title}' is already borrowed."
        return f"Book '{title}' not found in the library."

    def return_book(self, title):
        for book in self.books:
            if book.title == title:
                if not book.available:
                    book.available = True
                    return f"You have returned '{title}'."
                else:
                    return f"'{title}' was not borrowed."
        return f"Book '{title}' not found in the library."

my_library = Library()

book1 = Book("Hobbit", "Tolkien")
book2 = Book("Harry Potter","Rowling")
book3 = Book("Eragon", "Paolini")
magazine1=Magazine("National Geographic", "Editors Team", "01/24")

my_library.add_book(book1)
my_library.add_book(book2)
my_library.add_book(book3)
my_library.add_book(magazine1)

print(my_library.list_books())

print('======Borrow book=====')
print(my_library.borrow_book("Hobbit"))

print(my_library.list_books())

print("=====Return Book=====")
print(my_library.return_book("Hobbit"))
