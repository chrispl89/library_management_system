from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Utwórz użytkownika testowego i wymuś uwierzytelnienie
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)
        
        # Utwórz przykładową książkę
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            category="Fiction",
            added_by=self.user
        )

    def test_get_books(self):
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_book(self):
        data = {"title": "New Book", "author": "New Author", "category": "Non-fiction"}
        response = self.client.post("/api/books/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Book")

    def test_edit_book(self):
        data = {"title": "Updated Title"}
        url = f"/api/books/{self.book.id}/"
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Title")

    def test_delete_book(self):
        url = f"/api/books/{self.book.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
