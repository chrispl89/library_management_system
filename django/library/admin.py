from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "added_by", "created_at")
    search_fields = ("title", "author", "category")
    list_filter = ("category", "added_by")
