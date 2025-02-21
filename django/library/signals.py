from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Book, Profile
from django.conf import settings

@receiver(post_save, sender=Book)
def book_saved(sender, instance, created, **kwargs):
    if created:
        print(f"📗 New book added: {instance}")
    else:
        print(f"📘 Book updated: {instance}")

@receiver(post_delete, sender=Book)
def book_deleted(sender, instance, **kwargs):
    print(f"📕 Book deleted: {instance}")


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except Exception:
            pass
