from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone 
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class BookQuerySet(models.QuerySet):
    """Custom queryset providing additional book filtering methods"""
    
    def by_category(self, category):
        """Filter books by case-insensitive category match"""
        return self.filter(category__iexact=category)

    def available_books(self):
        """Return only books marked as available"""
        return self.filter(is_available=True)


class BookManager(models.Manager):
    """Custom manager implementing book-related query methods"""
    
    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)
        
    def by_category(self, category):
        """Public access to category filtering"""
        return self.get_queryset().by_category(category)
        
    def available_books(self):
        """Public access to availability filtering"""
        return self.get_queryset().available_books()

class Book(models.Model):
    """
    Represents a physical or digital book in the library system
    
    Attributes:
        title (CharField): Book title (max 255 chars)
        author (CharField): Author name (max 255 chars)
        category (CharField): Classification category (max 100 chars)
        added_by (ForeignKey): User who added the book
        created_at (DateTimeField): Date/time of record creation
        is_available (BooleanField): Availability status
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        """String representation combining title and author"""
        return f"{self.title} by {self.author}"


class Loan(models.Model):
    """
    Tracks book lending operations and return status
    
    Attributes:
        book (ForeignKey): Borrowed book reference
        user (ForeignKey): User who borrowed the book
        loan_date (DateTimeField): Date/time of borrowing
        due_date (DateField): Expected return date
        returned_at (DateField): Actual return date (nullable)
        status (CharField): Current loan state (ACTIVE/RETURNED/OVERDUE)
        fine (DecimalField): Calculated overdue penalty
    """
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("RETURNED", "Returned"),
        ("OVERDUE", "Overdue"),
    ]

    book = models.ForeignKey(Book, on_delete=models.PROTECT) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    returned_at = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ACTIVE")
    fine = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def mark_as_returned(self):
        """Update loan status to returned and calculate potential fines"""
        self.status = "RETURNED"
        self.returned_at = timezone.now().date()
        if self.returned_at > self.due_date:
            days_overdue = (self.returned_at - self.due_date).days
            self.fine = days_overdue * 1.00 
        else:
            self.fine = 0.00
        self.book.is_available = True
        self.book.save()
        self.save()

    def __str__(self):
        return f"{self.book.title} - {self.user.username} ({self.status})"


class Reservation(models.Model):
    """
    Manages book reservation lifecycle
    
    Attributes:
        book (ForeignKey): Reserved book reference
        user (ForeignKey): User making reservation
        created_at (DateTimeField): Reservation timestamp
        expires_at (DateTimeField): Reservation expiration time
        status (CharField): Current reservation state
    """
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("EXPIRED", "Expired"),
        ("CANCELLED", "Cancelled"),
    ]

    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ACTIVE")

    def is_expired(self):
        """Check if reservation has passed expiration time"""
        return self.expires_at < timezone.now()

    def expire_reservation(self):
        """Automatically mark reservation as expired"""
        self.status = "EXPIRED"
        self.save()

    def cancel_reservation(self):
        """Manually cancel active reservation"""
        self.status = "CANCELLED"
        self.save()

    def __str__(self):
        return f"Reservation: {self.book.title} by {self.user.username} ({self.status})"

class Review(models.Model):
    """
    Stores user ratings and comments for books
    
    Attributes:
        book (ForeignKey): Reviewed book reference
        user (ForeignKey): Review author
        rating (IntegerField): 1-5 star rating
        comment (TextField): Optional review text
        created_at (DateTimeField): Review timestamp
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review of {self.book.title} by {self.user.username} ({self.rating})"
    

class CustomUser(AbstractUser):
    """
    Extended user model with role-based access control
    
    Attributes:
        role (CharField): System access level (admin/librarian/reader)
        is_active (BooleanField): Account activation status
    """
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("librarian", "Librarian"),
        ("reader", "Reader"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="reader")
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"
    

class Profile(models.Model):
    """
    Stores additional user profile information
    
    Attributes:
        user (OneToOneField): Associated user account
        phone_number (CharField): Contact number
        address (TextField): Physical address
        activity_history (TextField): User action log
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    activity_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
    