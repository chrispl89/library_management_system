from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Book, Profile
from django.conf import settings

@receiver(post_save, sender=Book)
def book_saved(sender, instance, created, **kwargs):
    """
    Handles post-save events for Book model
    
    Triggers:
    - After creating new book
    - After updating existing book
    
    Actions:
    - Prints creation/update notification to console
    """
    if created:
        print(f"📗 New book added: {instance}")
    else:
        print(f"📘 Book updated: {instance}")

@receiver(post_delete, sender=Book)
def book_deleted(sender, instance, **kwargs):
    """
    Handles post-deletion events for Book model
    
    Triggers:
    - After deleting book record
    
    Actions:
    - Prints deletion notification to console
    """
    print(f"📕 Book deleted: {instance}")


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Maintains profile lifecycle tied to User model
    
    Triggers:
    - After user creation (creates profile)
    - After user updates (saves profile)
    
    Notes:
    - Silently handles missing profile in update cases
    - Uses try/except to prevent crash on profile conflicts
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except Exception:
            pass
        