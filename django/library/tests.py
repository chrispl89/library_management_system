from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book, Loan

class BookAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)
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

class LoanAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="loanuser", password="loanpass")
        self.client.force_authenticate(user=self.user)
        self.book = Book.objects.create(
            title="Loan Test Book", 
            author="Loan Author", 
            category="Fiction", 
            added_by=self.user
        )

    def test_create_loan(self):
        data = {"book": self.book.id, "due_date": "2025-12-31"}
        response = self.client.post("/api/loans/", data)
        print("🔎 Full Response:", response.json())
          
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_return_book(self):
        data = {"book": self.book.id, "due_date": "2025-12-31"}
        response = self.client.post("/api/loans/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        loan_id = response.data["id"]
        response = self.client.post(f"/api/loans/{loan_id}/return_book/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
