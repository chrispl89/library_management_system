#!/usr/bin/env python
"""
Script to create test users with different roles
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management_project.settings')
django.setup()

from library.models import CustomUser

def create_test_users():
    """Create test users with different roles"""
    
    users_to_create = [
        {
            'username': 'librarian_user',
            'email': 'librarian@test.com',
            'password': 'Test1234',
            'role': 'librarian',
            'is_active': True
        },
        {
            'username': 'reader_user',
            'email': 'reader@test.com',
            'password': 'Test1234',
            'role': 'reader',
            'is_active': True
        },
        {
            'username': 'admin_user',
            'email': 'admin@test.com',
            'password': 'Test1234',
            'role': 'admin',
            'is_active': True
        },
    ]
    
    created_count = 0
    
    for user_data in users_to_create:
        username = user_data['username']
        
        # Check if user already exists
        if CustomUser.objects.filter(username=username).exists():
            print(f"❌ User '{username}' already exists - skipping")
            continue
        
        # Create user
        user = CustomUser.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            role=user_data['role'],
            is_active=user_data['is_active']
        )
        
        created_count += 1
        print(f"✅ Created user: {username} (role: {user_data['role']})")
    
    print(f"\n🎉 Successfully created {created_count} test users!")
    print("\nTest user credentials:")
    print("-" * 50)
    print("Username: librarian_user | Password: Test1234 | Role: librarian")
    print("Username: reader_user    | Password: Test1234 | Role: reader")
    print("Username: admin_user     | Password: Test1234 | Role: admin")
    print("-" * 50)

if __name__ == '__main__':
    create_test_users()
