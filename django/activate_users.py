#!/usr/bin/env python
"""
Script to activate all users in the database
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Activate all users
users = User.objects.all()
count = users.update(is_active=True)

print(f"✅ Activated {count} users")

# List all users
print("\n📋 Users in database:")
for user in User.objects.all():
    print(f"  - {user.username} (role: {user.role}) - Active: {user.is_active}")
