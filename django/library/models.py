from django.db import models
from django.contrib.auth.models import User

class BookQuerySet(models.QuerySet):
    def by_category(self, category):
        return self.filter(category__iexact=category)

class BookManager(models.Manager):
    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)
    
    def by_category(self, category):
        return self.get_queryset().by_category(category)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = BookManager()  # Nasz niestandardowy manager

    def __str__(self):
        return f"{self.title} by {self.author}"
