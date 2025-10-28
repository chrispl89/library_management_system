"""
Generate a comprehensive book catalog with 300+ books across multiple categories
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'django'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from library.models import Book

User = get_user_model()

# Get librarian user to add books
try:
    librarian = User.objects.get(username='librarian_user')
except User.DoesNotExist:
    print("Error: librarian_user not found. Run setup_test_data.py first.")
    sys.exit(1)

# Comprehensive book catalog organized by category
BOOK_CATALOG = {
    "Classic Fiction": [
        ("Pride and Prejudice", "Jane Austen"),
        ("Wuthering Heights", "Emily Brontë"),
        ("Jane Eyre", "Charlotte Brontë"),
        ("Sense and Sensibility", "Jane Austen"),
        ("Emma", "Jane Austen"),
        ("Great Expectations", "Charles Dickens"),
        ("Oliver Twist", "Charles Dickens"),
        ("A Tale of Two Cities", "Charles Dickens"),
        ("David Copperfield", "Charles Dickens"),
        ("The Picture of Dorian Gray", "Oscar Wilde"),
        ("The Importance of Being Earnest", "Oscar Wilde"),
        ("Frankenstein", "Mary Shelley"),
        ("Dracula", "Bram Stoker"),
        ("The Strange Case of Dr Jekyll and Mr Hyde", "Robert Louis Stevenson"),
        ("Treasure Island", "Robert Louis Stevenson"),
        ("Moby-Dick", "Herman Melville"),
        ("The Scarlet Letter", "Nathaniel Hawthorne"),
        ("The Adventures of Huckleberry Finn", "Mark Twain"),
        ("The Adventures of Tom Sawyer", "Mark Twain"),
        ("Little Women", "Louisa May Alcott"),
        ("The Count of Monte Cristo", "Alexandre Dumas"),
        ("The Three Musketeers", "Alexandre Dumas"),
        ("Les Misérables", "Victor Hugo"),
        ("The Hunchback of Notre-Dame", "Victor Hugo"),
        ("Crime and Punishment", "Fyodor Dostoevsky"),
        ("The Brothers Karamazov", "Fyodor Dostoevsky"),
        ("War and Peace", "Leo Tolstoy"),
        ("Anna Karenina", "Leo Tolstoy"),
        ("The Idiot", "Fyodor Dostoevsky"),
        ("Dead Souls", "Nikolai Gogol"),
    ],
    
    "Science Fiction": [
        ("Dune", "Frank Herbert"),
        ("Foundation", "Isaac Asimov"),
        ("I, Robot", "Isaac Asimov"),
        ("The Caves of Steel", "Isaac Asimov"),
        ("Neuromancer", "William Gibson"),
        ("Snow Crash", "Neal Stephenson"),
        ("Ender's Game", "Orson Scott Card"),
        ("Speaker for the Dead", "Orson Scott Card"),
        ("The Hitchhiker's Guide to the Galaxy", "Douglas Adams"),
        ("Brave New World", "Aldous Huxley"),
        ("Fahrenheit 451", "Ray Bradbury"),
        ("The Martian Chronicles", "Ray Bradbury"),
        ("Do Androids Dream of Electric Sheep?", "Philip K. Dick"),
        ("Ubik", "Philip K. Dick"),
        ("The Man in the High Castle", "Philip K. Dick"),
        ("Slaughterhouse-Five", "Kurt Vonnegut"),
        ("Cat's Cradle", "Kurt Vonnegut"),
        ("Stranger in a Strange Land", "Robert A. Heinlein"),
        ("Starship Troopers", "Robert A. Heinlein"),
        ("The Moon is a Harsh Mistress", "Robert A. Heinlein"),
        ("2001: A Space Odyssey", "Arthur C. Clarke"),
        ("Rendezvous with Rama", "Arthur C. Clarke"),
        ("Childhood's End", "Arthur C. Clarke"),
        ("The Left Hand of Darkness", "Ursula K. Le Guin"),
        ("The Dispossessed", "Ursula K. Le Guin"),
        ("Hyperion", "Dan Simmons"),
        ("The Fall of Hyperion", "Dan Simmons"),
        ("Ready Player One", "Ernest Cline"),
        ("The Expanse: Leviathan Wakes", "James S.A. Corey"),
        ("Old Man's War", "John Scalzi"),
    ],
    
    "Fantasy": [
        ("The Hobbit", "J.R.R. Tolkien"),
        ("The Fellowship of the Ring", "J.R.R. Tolkien"),
        ("The Two Towers", "J.R.R. Tolkien"),
        ("The Return of the King", "J.R.R. Tolkien"),
        ("The Silmarillion", "J.R.R. Tolkien"),
        ("Harry Potter and the Philosopher's Stone", "J.K. Rowling"),
        ("Harry Potter and the Chamber of Secrets", "J.K. Rowling"),
        ("Harry Potter and the Prisoner of Azkaban", "J.K. Rowling"),
        ("Harry Potter and the Goblet of Fire", "J.K. Rowling"),
        ("Harry Potter and the Order of the Phoenix", "J.K. Rowling"),
        ("Harry Potter and the Half-Blood Prince", "J.K. Rowling"),
        ("Harry Potter and the Deathly Hallows", "J.K. Rowling"),
        ("A Game of Thrones", "George R.R. Martin"),
        ("A Clash of Kings", "George R.R. Martin"),
        ("A Storm of Swords", "George R.R. Martin"),
        ("A Feast for Crows", "George R.R. Martin"),
        ("A Dance with Dragons", "George R.R. Martin"),
        ("The Name of the Wind", "Patrick Rothfuss"),
        ("The Wise Man's Fear", "Patrick Rothfuss"),
        ("The Way of Kings", "Brandon Sanderson"),
        ("Words of Radiance", "Brandon Sanderson"),
        ("Oathbringer", "Brandon Sanderson"),
        ("Mistborn: The Final Empire", "Brandon Sanderson"),
        ("The Well of Ascension", "Brandon Sanderson"),
        ("The Hero of Ages", "Brandon Sanderson"),
        ("The Chronicles of Narnia: The Lion, the Witch and the Wardrobe", "C.S. Lewis"),
        ("Prince Caspian", "C.S. Lewis"),
        ("The Voyage of the Dawn Treader", "C.S. Lewis"),
        ("The Magician's Nephew", "C.S. Lewis"),
        ("The Last Battle", "C.S. Lewis"),
    ],
    
    "Mystery & Thriller": [
        ("The Adventures of Sherlock Holmes", "Arthur Conan Doyle"),
        ("The Hound of the Baskervilles", "Arthur Conan Doyle"),
        ("A Study in Scarlet", "Arthur Conan Doyle"),
        ("The Sign of Four", "Arthur Conan Doyle"),
        ("And Then There Were None", "Agatha Christie"),
        ("Murder on the Orient Express", "Agatha Christie"),
        ("The Murder of Roger Ackroyd", "Agatha Christie"),
        ("Death on the Nile", "Agatha Christie"),
        ("The ABC Murders", "Agatha Christie"),
        ("The Girl with the Dragon Tattoo", "Stieg Larsson"),
        ("The Girl Who Played with Fire", "Stieg Larsson"),
        ("The Girl Who Kicked the Hornet's Nest", "Stieg Larsson"),
        ("Gone Girl", "Gillian Flynn"),
        ("Sharp Objects", "Gillian Flynn"),
        ("Dark Places", "Gillian Flynn"),
        ("The Da Vinci Code", "Dan Brown"),
        ("Angels & Demons", "Dan Brown"),
        ("The Lost Symbol", "Dan Brown"),
        ("Inferno", "Dan Brown"),
        ("Digital Fortress", "Dan Brown"),
        ("The Silence of the Lambs", "Thomas Harris"),
        ("Red Dragon", "Thomas Harris"),
        ("Hannibal", "Thomas Harris"),
        ("The Maltese Falcon", "Dashiell Hammett"),
        ("The Big Sleep", "Raymond Chandler"),
        ("The Long Goodbye", "Raymond Chandler"),
        ("In Cold Blood", "Truman Capote"),
        ("The Talented Mr. Ripley", "Patricia Highsmith"),
        ("Strangers on a Train", "Patricia Highsmith"),
        ("Rebecca", "Daphne du Maurier"),
    ],
    
    "Dystopian Fiction": [
        ("1984", "George Orwell"),
        ("Animal Farm", "George Orwell"),
        ("The Handmaid's Tale", "Margaret Atwood"),
        ("The Testaments", "Margaret Atwood"),
        ("Lord of the Flies", "William Golding"),
        ("A Clockwork Orange", "Anthony Burgess"),
        ("The Road", "Cormac McCarthy"),
        ("Never Let Me Go", "Kazuo Ishiguro"),
        ("The Giver", "Lois Lowry"),
        ("Divergent", "Veronica Roth"),
        ("Insurgent", "Veronica Roth"),
        ("Allegiant", "Veronica Roth"),
        ("The Hunger Games", "Suzanne Collins"),
        ("Catching Fire", "Suzanne Collins"),
        ("Mockingjay", "Suzanne Collins"),
        ("The Maze Runner", "James Dashner"),
        ("The Scorch Trials", "James Dashner"),
        ("The Death Cure", "James Dashner"),
        ("Station Eleven", "Emily St. John Mandel"),
        ("The Passage", "Justin Cronin"),
    ],
    
    "Historical Fiction": [
        ("All the Light We Cannot See", "Anthony Doerr"),
        ("The Book Thief", "Markus Zusak"),
        ("The Pillars of the Earth", "Ken Follett"),
        ("World Without End", "Ken Follett"),
        ("A Column of Fire", "Ken Follett"),
        ("The Nightingale", "Kristin Hannah"),
        ("The Tattooist of Auschwitz", "Heather Morris"),
        ("The Help", "Kathryn Stockett"),
        ("The Kite Runner", "Khaled Hosseini"),
        ("A Thousand Splendid Suns", "Khaled Hosseini"),
        ("And the Mountains Echoed", "Khaled Hosseini"),
        ("The Other Boleyn Girl", "Philippa Gregory"),
        ("Wolf Hall", "Hilary Mantel"),
        ("Bring Up the Bodies", "Hilary Mantel"),
        ("The Mirror & the Light", "Hilary Mantel"),
        ("Memoirs of a Geisha", "Arthur Golden"),
        ("The Name of the Rose", "Umberto Eco"),
        ("I, Claudius", "Robert Graves"),
        ("The Last Kingdom", "Bernard Cornwell"),
        ("Shogun", "James Clavell"),
    ],
    
    "Romance": [
        ("Outlander", "Diana Gabaldon"),
        ("Dragonfly in Amber", "Diana Gabaldon"),
        ("Voyager", "Diana Gabaldon"),
        ("Me Before You", "Jojo Moyes"),
        ("After You", "Jojo Moyes"),
        ("The Notebook", "Nicholas Sparks"),
        ("A Walk to Remember", "Nicholas Sparks"),
        ("The Lucky One", "Nicholas Sparks"),
        ("Safe Haven", "Nicholas Sparks"),
        ("Dear John", "Nicholas Sparks"),
        ("The Fault in Our Stars", "John Green"),
        ("Looking for Alaska", "John Green"),
        ("Paper Towns", "John Green"),
        ("Eleanor & Park", "Rainbow Rowell"),
        ("Attachments", "Rainbow Rowell"),
        ("Normal People", "Sally Rooney"),
        ("Conversations with Friends", "Sally Rooney"),
        ("The Time Traveler's Wife", "Audrey Niffenegger"),
        ("One Day", "David Nicholls"),
        ("Call Me by Your Name", "André Aciman"),
    ],
    
    "Horror": [
        ("The Shining", "Stephen King"),
        ("It", "Stephen King"),
        ("Pet Sematary", "Stephen King"),
        ("Carrie", "Stephen King"),
        ("Misery", "Stephen King"),
        ("The Stand", "Stephen King"),
        ("Salem's Lot", "Stephen King"),
        ("The Dead Zone", "Stephen King"),
        ("Christine", "Stephen King"),
        ("Cujo", "Stephen King"),
        ("The Exorcist", "William Peter Blatty"),
        ("Rosemary's Baby", "Ira Levin"),
        ("Interview with the Vampire", "Anne Rice"),
        ("The Vampire Lestat", "Anne Rice"),
        ("Queen of the Damned", "Anne Rice"),
        ("The Haunting of Hill House", "Shirley Jackson"),
        ("We Have Always Lived in the Castle", "Shirley Jackson"),
        ("The Turn of the Screw", "Henry James"),
        ("House of Leaves", "Mark Z. Danielewski"),
        ("Bird Box", "Josh Malerman"),
    ],
    
    "Biography & Memoir": [
        ("The Diary of a Young Girl", "Anne Frank"),
        ("Long Walk to Freedom", "Nelson Mandela"),
        ("I Am Malala", "Malala Yousafzai"),
        ("Educated", "Tara Westover"),
        ("Becoming", "Michelle Obama"),
        ("Steve Jobs", "Walter Isaacson"),
        ("Leonardo da Vinci", "Walter Isaacson"),
        ("Einstein: His Life and Universe", "Walter Isaacson"),
        ("The Autobiography of Benjamin Franklin", "Benjamin Franklin"),
        ("Dreams from My Father", "Barack Obama"),
        ("The Glass Castle", "Jeannette Walls"),
        ("Wild", "Cheryl Strayed"),
        ("Eat, Pray, Love", "Elizabeth Gilbert"),
        ("Born a Crime", "Trevor Noah"),
        ("When Breath Becomes Air", "Paul Kalanithi"),
        ("The Immortal Life of Henrietta Lacks", "Rebecca Skloot"),
        ("Hillbilly Elegy", "J.D. Vance"),
        ("Man's Search for Meaning", "Viktor E. Frankl"),
        ("Night", "Elie Wiesel"),
        ("The Year of Magical Thinking", "Joan Didion"),
    ],
    
    "Self-Help & Psychology": [
        ("Thinking, Fast and Slow", "Daniel Kahneman"),
        ("Atomic Habits", "James Clear"),
        ("The 7 Habits of Highly Effective People", "Stephen R. Covey"),
        ("How to Win Friends and Influence People", "Dale Carnegie"),
        ("The Power of Habit", "Charles Duhigg"),
        ("Mindset: The New Psychology of Success", "Carol S. Dweck"),
        ("Grit", "Angela Duckworth"),
        ("Quiet: The Power of Introverts", "Susan Cain"),
        ("The Subtle Art of Not Giving a F*ck", "Mark Manson"),
        ("12 Rules for Life", "Jordan B. Peterson"),
        ("Sapiens: A Brief History of Humankind", "Yuval Noah Harari"),
        ("Homo Deus: A Brief History of Tomorrow", "Yuval Noah Harari"),
        ("21 Lessons for the 21st Century", "Yuval Noah Harari"),
        ("Influence: The Psychology of Persuasion", "Robert B. Cialdini"),
        ("The Four Agreements", "Don Miguel Ruiz"),
        ("Daring Greatly", "Brené Brown"),
        ("The Gifts of Imperfection", "Brené Brown"),
        ("Can't Hurt Me", "David Goggins"),
        ("The Alchemist", "Paulo Coelho"),
        ("The Monk Who Sold His Ferrari", "Robin Sharma"),
    ],
}

def create_books():
    """Create all books in the catalog"""
    
    print("\n" + "="*70)
    print("  CREATING COMPREHENSIVE BOOK CATALOG")
    print("="*70 + "\n")
    
    existing_count = Book.objects.count()
    print(f"Existing books in database: {existing_count}")
    print("Adding new books to catalog...\n")
    
    total_books = 0
    category_counts = {}
    
    for category, books_list in BOOK_CATALOG.items():
        print(f"Adding {len(books_list)} books to category: {category}")
        count = 0
        
        for title, author in books_list:
            try:
                Book.objects.create(
                    title=title,
                    author=author,
                    category=category,
                    added_by=librarian,
                    is_available=True
                )
                count += 1
                total_books += 1
            except Exception as e:
                print(f"  ⚠ Error adding '{title}': {e}")
        
        category_counts[category] = count
        print(f"  ✅ Added {count} books\n")
    
    print("="*70)
    print(f"  CATALOG CREATION COMPLETE")
    print("="*70 + "\n")
    
    print(f"Total books created: {total_books}\n")
    
    print("Books by category:")
    for category, count in sorted(category_counts.items()):
        print(f"  • {category:<35} {count:>3} books")
    
    print("\n" + "="*70)
    print(f"  ✅ Successfully created {total_books} books across {len(category_counts)} categories")
    print("="*70 + "\n")

if __name__ == "__main__":
    create_books()
