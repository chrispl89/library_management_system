from rest_framework import viewsets, permissions, generics, status, serializers, views
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.generic import ListView
from rest_framework.views import APIView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Book, Loan, Reservation, Review, Profile
from .serializers import (BookSerializer, LoanSerializer, UserRegistrationSerializer, ReservationSerializer, ReviewSerializer, 
                          ProfileSerializer, UserSerializer)
from .permissions import IsLibrarianOrReadOnly, IsAdmin, IsOwnerOrAdmin
from django.utils import timezone
import requests
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail



User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """
    Handles user registration with email activation workflow
    
    Features:
    - Creates inactive user accounts
    - Sends activation emails with secure tokens
    - Uses AllowAny permissions for open registration
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        """Create user and send activation email with unique token"""
        user = serializer.save(is_active=False) 
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        activation_link = f"http://127.0.0.1:8000/api/activate/{uid}/{token}/"
        send_mail(
            "Activate your account",
            f"Click the link to activate your account: {activation_link}",
            "noreply@library.com",
            [user.email],
            fail_silently=False,
        )


class BookViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for book management
    
    Permissions:
    - Librarians: Full access
    - Others: Read-only
    - Auto-sets added_by to current user on creation
    """
    queryset = Book.objects.all().select_related('added_by')
    serializer_class = BookSerializer
    permission_classes = [IsLibrarianOrReadOnly]

    def perform_create(self, serializer):
        """Automatically assign current user as book creator"""
        serializer.save(added_by=self.request.user)


class LoanViewSet(viewsets.ModelViewSet):
    """
    Manages book loan lifecycle
    
    Features:
    - Updates book availability status
    - Tracks loan history in user profile
    - Provides return_book custom action
    """
    queryset = Loan.objects.all().select_related("book", "user")
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Handle book availability and user activity tracking"""
        book = serializer.validated_data["book"]
        serializer.save(user=self.request.user)
        book.is_available = False
        book.save()
        profile = self.request.user.profile
        current_history = profile.activity_history or ""
        new_history_line = f"Loan created for '{book.title}' on {timezone.now()}\n"
        profile.activity_history = current_history + new_history_line
        profile.save()

    @action(detail=True, methods=["post"])
    def return_book(self, request, pk=None):
        """Process book returns and calculate overdue fines"""
        loan = self.get_object()
        if loan.status == "RETURNED":
            return Response({"error": "Book already returned!"}, status=status.HTTP_400_BAD_REQUEST)
        loan.mark_as_returned()
        return Response({"message": "Book returned successfully!", "fine": f"{loan.fine:.2f}"})


@method_decorator(cache_page(60 * 15), name='dispatch')
class BookListView(ListView):
    """
    Cached book listing for public access
    
    Features:
    - 15-minute response caching
    - Traditional Django template rendering
    """
    model = Book
    template_name = "library/book_list.html"
    context_object_name = "books"


class ReservationViewSet(viewsets.ModelViewSet):
    """
    Manages book reservations with expiration
    
    Features:
    - Automatic 3-day expiration
    - User-specific reservation tracking
    - Cancelation endpoint
    """
    queryset = Reservation.objects.all().select_related("book", "user")
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        expires_at = timezone.now() + timezone.timedelta(days=3)
        reservation = serializer.save(user=self.request.user, expires_at=expires_at)
        profile = self.request.user.profile
        current_history = profile.activity_history or ""
        new_history_line = f"Reservation created for '{reservation.book.title}' on {timezone.now()}\n"
        profile.activity_history = current_history + new_history_line
        profile.save()

    @action(detail=True, methods=["post"])
    def cancel_reservation(self, request, pk=None):
        reservation = self.get_object()
        if reservation.user != request.user:
            return Response({"error": "You can only cancel your own reservations."}, status=status.HTTP_403_FORBIDDEN)
        reservation.cancel_reservation()
        return Response({"message": "Reservation cancelled successfully."})

    @action(detail=False, methods=["get"])
    def my_reservations(self, request):
        reservations = Reservation.objects.filter(user=request.user, status="ACTIVE")
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Handles book reviews and ratings
    
    Permissions:
    - Authenticated users: Create/read
    - Admins only: Delete
    """
    queryset = Review.objects.all().select_related("book", "user")
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == "destroy":
            self.permission_classes = [IsAdmin]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GoogleBooksSearchView(APIView):
    """
    Proxy for Google Books API search
    
    Parameters:
    - q (required): Search query string
    
    Returns:
    - Raw Google Books API response
    """
    permission_classes = [permissions.AllowAny] 
    def get(self, request):
        """Handle external API requests with error wrapping"""
        query = request.query_params.get("q", "").strip()
        if not query:
            return Response({"error": "Query parameter 'q' is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # URL Google Books API
        google_api_url = "https://www.googleapis.com/books/v1/volumes"
        params = {
            "q": query,
            "maxResults": 5  # max results, is editable
        }
        try:
            response = requests.get(google_api_url, params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            return Response({"error": "Failed to fetch data from Google Books API.", "details": str(e)},
                            status=status.HTTP_502_BAD_GATEWAY)
        
        data = response.json()
        return Response(data, status=status.HTTP_200_OK)
    

class ProfileViewSet(viewsets.ModelViewSet):
    """
    Manages user profile data
    
    Security:
    - Users can only access their own profile
    - Admins can view all profiles
    """
    queryset = Profile.objects.select_related("user").all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Profile.objects.all()
        return Profile.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        

class UserViewSet(viewsets.ModelViewSet):
    """
    User management endpoint
    
    Permissions:
    - Admins: Full access
    - Users: Self-service only
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        return [permissions.IsAdminUser()]  
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff: 
            return User.objects.all()
        return User.objects.filter(id=user.id)


class ActivateAccountView(views.APIView):
    """
    Handles account activation via email tokens
    
    Parameters:
    - uidb64: Base64 encoded user ID
    - token: Time-limited activation token
    """
    permission_classes = [permissions.AllowAny]
    
    def activate_view(request, uidb64, token):
        print(f"UID: {uidb64}, Token: {token}") 
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
    
    def get(self, request, uidb64, token):
        """Validate activation token and activate user"""
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, id=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({"message": "Account activated successfully!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid token!"}, status=status.HTTP_400_BAD_REQUEST)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid request!"}, status=status.HTTP_400_BAD_REQUEST)
        

class UserDashboardView(APIView):
    """
    Aggregated user activity dashboard
    
    Returns:
    - Profile data
    - Active loans
    - Current reservations
    - Review history
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Compile dashboard data from multiple models"""
        user = request.user
        profile_data = ProfileSerializer(user.profile).data
        
        active_loans = Loan.objects.filter(user=user, status="ACTIVE")
        loans_data = LoanSerializer(active_loans, many=True).data

        active_reservations = Reservation.objects.filter(user=user, status="ACTIVE")
        reservations_data = ReservationSerializer(active_reservations, many=True).data

        user_reviews = Review.objects.filter(user=user)
        reviews_data = ReviewSerializer(user_reviews, many=True).data

        return Response({
            "profile": profile_data,
            "active_loans": loans_data,
            "active_reservations": reservations_data,
            "reviews": reviews_data
        })
    