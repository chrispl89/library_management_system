"""
Script to activate all users in the database
Run this with: python manage.py shell < activate_users.py
"""

from django.contrib.auth import get_user_model

User = get_user_model()

# Activate all users
users = User.objects.all()
count = users.update(is_active=True)

print(f"Activated {count} users")

# List all users
print("\nUsers in database:")
for user in User.objects.all():
    print(f"  - {user.username} ({user.role}) - Active: {user.is_active}")
