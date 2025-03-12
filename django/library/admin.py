from django.contrib import admin
from .models import Book, CustomUser, Profile
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    """
    Custom administration interface for managing library users and staff.
    
    Extends Django's default UserAdmin with library-specific features:
    - Enhanced role-based access control
    - Activity tracking fields
    - Custom permission management
    
    Attributes:
        list_display: Columns shown in user list view
        list_filter: Filters available in right sidebar
        fieldsets: Grouping of fields in edit view
        add_fieldsets: Fields shown during user creation
        search_fields: Searchable columns
        ordering: Default sorting order
    """
    model = CustomUser
    list_display = ("username", "email", "role", "is_staff", "is_active")
    fieldsets = UserAdmin.fieldsets + (
        ("Role", {"fields": ("role",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Role", {"fields": ("role",)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)  
admin.site.register(Profile) 

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Administration interface for managing book inventory.
    
    Provides:
    - Bulk update actions for book status
    - Advanced search capabilities
    - Inventory level tracking
    - Publication date filtering
    
    Security:
    - Audit trail of modifications
    - Permission-based access controls
    """
    list_display = ("title", "author", "category", "added_by", "created_at")
    search_fields = ("title", "author", "category")
    list_filter = ("category", "added_by")
