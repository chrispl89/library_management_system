from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book, Loan, Reservation, Review
from django.utils import timezone

CustomUser = get_user_model()

class BookAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpass", role="librarian")
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
        self.user = CustomUser.objects.create_user(username="loanuser", password="loanpass")
        self.client.force_authenticate(user=self.user)
        self.book = Book.objects.create(
            title="Loan Test Book", 
            author="Loan Author", 
            category="Fiction", 
            added_by=self.user
        )

    def test_create_loan(self):
        data = {"book": self.book.id, "due_date": "2025-12-31"}
        response = self.client.post("/api/loans/", data, format="json")
        print("🔎 Full Response:", response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_return_book(self):
        data = {"book": self.book.id, "due_date": "2025-12-31"}
        response = self.client.post("/api/loans/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        loan_id = response.data["id"]
        response = self.client.post(f"/api/loans/{loan_id}/return_book/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("fine"), "0.00")

class ReservationAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="reservationuser", password="testpass")
        self.client.force_authenticate(user=self.user)
        self.book = Book.objects.create(
            title="Reserved Book", 
            author="Test Author", 
            category="Fiction", 
            added_by=self.user
        )

    def test_create_reservation(self):
        data = {"book": self.book.id}
        response = self.client.post("/api/reservations/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["book_title"], self.book.title)

    def test_cancel_reservation(self):
        reservation = Reservation.objects.create(
            book=self.book, user=self.user, expires_at=timezone.now() + timezone.timedelta(days=3)
        )
        response = self.client.post(f"/api/reservations/{reservation.id}/cancel_reservation/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="reviewuser", password="testpass", role="reader")
        self.client.force_authenticate(user=self.user)
        self.book = Book.objects.create(
            title="Review Test Book", 
            author="Review Author", 
            category="Fiction", 
            added_by=self.user
        )

    def test_create_review(self):
        data = {"book": self.book.id, "rating": 5, "comment": "Excellent book!"}
        response = self.client.post("/api/reviews/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["rating"], 5)
