from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book, Loan, Reservation, Review, Profile
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

CustomUser = get_user_model()


class BookAPITestCase(APITestCase):
    """Tests CRUD operations for Book API endpoints with librarian privileges"""
    
    def setUp(self):
        """Create test user and sample book for authentication and testing"""
        self.user = CustomUser.objects.create_user(username="testuser", password="testpass", role="librarian")
        self.client.force_authenticate(user=self.user)
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            category="Fiction",
            added_by=self.user
        )

    def test_get_books(self):
        """Verify book listing returns at least the created test book"""
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_book(self):
        """Test successful book creation with valid data"""
        data = {"title": "New Book", "author": "New Author", "category": "Non-fiction"}
        response = self.client.post("/api/books/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Book")

    def test_edit_book(self):
        """Verify partial updates to book details"""
        data = {"title": "Updated Title"}
        url = f"/api/books/{self.book.id}/"
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Title")

    def test_delete_book(self):
        """Test book deletion workflow"""
        url = f"/api/books/{self.book.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_book_invalid_data(self):
        """Test book creation with missing required fields"""
        data = {"title": "Incomplete Book"}
        response = self.client.post("/api/books/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_non_librarian_access(self):
        """Verify regular users can't modify books"""
        regular_user = CustomUser.objects.create_user(username="regular", password="pass", role="reader")
        self.client.force_authenticate(user=regular_user)
        
        # Test create
        response = self.client.post("/api/books/", {"title": "New Book"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test delete
        url = f"/api/books/{self.book.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LoanAPITestCase(APITestCase):
    """Tests book loan lifecycle including creation and return"""
    
    def setUp(self):
        """Create user and book for loan testing"""
        self.user = CustomUser.objects.create_user(username="loanuser", password="loanpass")
        self.client.force_authenticate(user=self.user)
        self.book = Book.objects.create(
            title="Loan Test Book", 
            author="Loan Author", 
            category="Fiction", 
            added_by=self.user
        )

    def test_create_loan(self):
        """Verify successful loan creation with future due date"""
        data = {"book": self.book.id, "due_date": "2025-12-31"}
        response = self.client.post("/api/loans/", data, format="json")
        print("🔎 Full Response:", response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_return_book(self):
        """Test complete loan lifecycle with on-time return"""
        data = {"book": self.book.id, "due_date": "2025-12-31"}
        response = self.client.post("/api/loans/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        loan_id = response.data["id"]
        response = self.client.post(f"/api/loans/{loan_id}/return_book/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("fine"), "0.00")

    def test_loan_unavailable_book(self):
        """Test loaning already borrowed book"""
        # First loan
        self.test_create_loan()
        
        # Second loan attempt
        data = {"book": self.book.id, "due_date": "2025-12-31"}
        response = self.client.post("/api/loans/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_overdue_fine_calculation(self):
        """Verify correct fine calculation for overdue returns"""
        data = {"book": self.book.id, "due_date": "2020-01-01"}  # Past date
        response = self.client.post("/api/loans/", data, format="json")
        loan_id = response.data["id"]
        
        response = self.client.post(f"/api/loans/{loan_id}/return_book/")
        self.assertGreater(float(response.data["fine"]), 0.00)


class ReservationAPITestCase(APITestCase):
    """Tests reservation management including creation and cancellation"""
    
    def setUp(self):
        """Initialize user and book for reservation tests"""
        self.user = CustomUser.objects.create_user(username="reservationuser", password="testpass")
        self.client.force_authenticate(user=self.user)
        self.book = Book.objects.create(
            title="Reserved Book", 
            author="Test Author", 
            category="Fiction", 
            added_by=self.user
        )

    def test_create_reservation(self):
        """Verify successful reservation creation"""
        data = {"book": self.book.id}
        response = self.client.post("/api/reservations/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["book_title"], self.book.title)

    def test_cancel_reservation(self):
        """Test manual reservation cancellation workflow"""
        reservation = Reservation.objects.create(
            book=self.book, user=self.user, expires_at=timezone.now() + timezone.timedelta(days=3)
        )
        response = self.client.post(f"/api/reservations/{reservation.id}/cancel_reservation/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reserve_unavailable_book(self):
        """Test reserving a book that's currently loaned"""
        # Loan book first
        loan_data = {"book": self.book.id, "due_date": "2025-12-31"}
        self.client.post("/api/loans/", loan_data, format="json")
        
        # Try to reserve
        data = {"book": self.book.id}
        response = self.client.post("/api/reservations/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_auto_expire_reservation(self):
        """Verify reservation expiration after time passes"""
        reservation = Reservation.objects.create(
            book=self.book, 
            user=self.user, 
            expires_at=timezone.now() - timezone.timedelta(days=1)  # Past date
        )
        self.assertTrue(reservation.is_expired())


class ReviewAPITestCase(APITestCase):
    """Tests review submission and validation"""
    
    def setUp(self):
        """Create test user and book for review testing"""
        self.user = CustomUser.objects.create_user(username="reviewuser", password="testpass", role="reader")
        self.client.force_authenticate(user=self.user)
        self.book = Book.objects.create(
            title="Review Test Book", 
            author="Review Author", 
            category="Fiction", 
            added_by=self.user
        )

    def test_create_review(self):
        """Verify valid review submission with rating and comment"""
        data = {"book": self.book.id, "rating": 5, "comment": "Excellent book!"}
        response = self.client.post("/api/reviews/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["rating"], 5)

    def test_invalid_rating_values(self):
        """Test boundary values for ratings (1-5)"""
        data = {"book": self.book.id, "rating": 0}
        response = self.client.post("/api/reviews/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data["rating"] = 6
        response = self.client.post("/api/reviews/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  
class AccountActivationTestCase(APITestCase):
    """Tests user account activation workflow with token validation"""
    
    def setUp(self):
        """Create inactive user and generate activation tokens"""
        self.user = CustomUser.objects.create_user(username="activateuser", password="Pass1234", email="activate@example.com", role="reader")
        self.user.is_active = False
        self.user.save()
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)

    def test_activate_account_valid(self):
        """Test successful activation with valid token"""
        url = f"/api/activate/{self.uid}/{self.token}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Account activated successfully!")
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_activate_account_invalid_token(self):
        """Verify error handling for invalid activation tokens"""
        url = f"/api/activate/{self.uid}/invalidtoken/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserDashboardTestCase(APITestCase):
    """Tests user dashboard data aggregation"""
    
    def setUp(self):
        """Create user and ensure profile exists"""
        self.user = CustomUser.objects.create_user(username="dashboarduser", password="Pass1234", role="reader")
        self.client.force_authenticate(user=self.user)
        # Ensure profile is created
        from .models import Profile
        Profile.objects.get_or_create(user=self.user)

    def test_dashboard_empty(self):
        """Verify dashboard structure with no active records"""
        url = "/api/dashboard/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertIn("profile", data)
        self.assertEqual(data["active_loans"], [])
        self.assertEqual(data["active_reservations"], [])
        self.assertEqual(data["reviews"], [])

