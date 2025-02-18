from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 

class BookQuerySet(models.QuerySet):
    def by_category(self, category):
        return self.filter(category__iexact=category)

    def available_books(self):
        return self.filter(is_available=True)

class BookManager(models.Manager):
    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)
    
    def by_category(self, category):
        return self.get_queryset().by_category(category)

    def available_books(self):
        return self.get_queryset().available_books()

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)

    objects = BookManager()  

    def __str__(self):
        return f"{self.title} by {self.author}"

class Loan(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("RETURNED", "Returned"),
        ("OVERDUE", "Overdue"),
    ]

    book = models.ForeignKey(Book, on_delete=models.PROTECT) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    returned_at = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ACTIVE")

    def mark_as_returned(self):
        """Mark the loan as returned and update status"""
        self.status = "RETURNED"
        self.returned_at = timezone.now().date()  
        self.book.is_available = True
        self.book.save()
        self.save()

    def __str__(self):
        return f"{self.book.title} - {self.user.username} ({self.status})"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("EXPIRED", "Expired"),
        ("CANCELLED", "Cancelled"),
    ]

    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ACTIVE")

    def is_expired(self):
        return self.expires_at < timezone.now()

    def expire_reservation(self):
        """Mark the reservation as expired and free the book."""
        self.status = "EXPIRED"
        self.save()

    def cancel_reservation(self):
        """Cancel the reservation manually."""
        self.status = "CANCELLED"
        self.save()

    def __str__(self):
        return f"Reservation: {self.book.title} by {self.user.username} ({self.status})"