"""
Setup script to create and activate test users
Run from django directory: python setup_test_data.py
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'django'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from library.models import Profile

User = get_user_model()

def create_test_users():
    """Create test users if they don't exist"""
    users_data = [
        {"username": "admin_user", "email": "admin@test.com", "password": "AdminPass123!", "role": "admin"},
        {"username": "librarian_user", "email": "librarian@test.com", "password": "LibrarianPass123!", "role": "librarian"},
        {"username": "reader_user", "email": "reader@test.com", "password": "ReaderPass123!", "role": "reader"},
    ]
    
    for user_data in users_data:
        username = user_data['username']
        
        # Check if user exists
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.is_active = True
            user.save()
            print(f"✓ Activated existing user: {username} ({user.role})")
        else:
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                role=user_data['role'],
                is_active=True
            )
            # Create profile
            Profile.objects.get_or_create(user=user)
            print(f"✓ Created new user: {username} ({user.role})")

def activate_all_users():
    """Activate all existing users"""
    count = User.objects.filter(is_active=False).update(is_active=True)
    if count > 0:
        print(f"\n✓ Activated {count} previously inactive users")

def list_users():
    """List all users"""
    print("\n" + "="*60)
    print("All Users in Database:")
    print("="*60)
    for user in User.objects.all():
        print(f"  • {user.username:<20} | Role: {user.role:<12} | Active: {user.is_active}")
    print("="*60 + "\n")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  SETTING UP TEST DATA")
    print("="*60 + "\n")
    
    create_test_users()
    activate_all_users()
    list_users()
    
    print("✓ Setup completed!\n")
