#!/usr/bin/env python
"""
Script to create sample books for testing
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management_project.settings')
django.setup()

from library.models import CustomUser, Book

def create_sample_books():
    """Create sample books"""
    
    # Get or create a librarian to add books
    librarian = CustomUser.objects.filter(role='librarian').first()
    if not librarian:
        librarian = CustomUser.objects.filter(is_superuser=True).first()
    
    if not librarian:
        print("❌ No librarian or admin user found. Create users first!")
        return
    
    sample_books = [
        {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'category': 'Fiction'},
        {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'category': 'Fiction'},
        {'title': '1984', 'author': 'George Orwell', 'category': 'Science Fiction'},
        {'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'category': 'Romance'},
        {'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'category': 'Fantasy'},
        {'title': 'Harry Potter and the Philosopher\'s Stone', 'author': 'J.K. Rowling', 'category': 'Fantasy'},
        {'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger', 'category': 'Fiction'},
        {'title': 'Animal Farm', 'author': 'George Orwell', 'category': 'Political Fiction'},
        {'title': 'The Lord of the Rings', 'author': 'J.R.R. Tolkien', 'category': 'Fantasy'},
        {'title': 'Brave New World', 'author': 'Aldous Huxley', 'category': 'Science Fiction'},
        {'title': 'The Chronicles of Narnia', 'author': 'C.S. Lewis', 'category': 'Fantasy'},
        {'title': 'Crime and Punishment', 'author': 'Fyodor Dostoevsky', 'category': 'Classic'},
        {'title': 'The Odyssey', 'author': 'Homer', 'category': 'Epic Poetry'},
        {'title': 'Moby-Dick', 'author': 'Herman Melville', 'category': 'Adventure'},
        {'title': 'Hamlet', 'author': 'William Shakespeare', 'category': 'Drama'},
    ]
    
    created_count = 0
    
    for book_data in sample_books:
        title = book_data['title']
        
        # Check if book already exists
        if Book.objects.filter(title=title).exists():
            print(f"⏭️  Book '{title}' already exists - skipping")
            continue
        
        # Create book
        book = Book.objects.create(
            title=book_data['title'],
            author=book_data['author'],
            category=book_data['category'],
            added_by=librarian,
            is_available=True
        )
        
        created_count += 1
        print(f"📗 Created book: {title} by {book_data['author']}")
    
    print(f"\n🎉 Successfully created {created_count} sample books!")
    print(f"📚 Total books in library: {Book.objects.count()}")

if __name__ == '__main__':
    create_sample_books()
