from rest_framework import viewsets, permissions, generics, status, serializers
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


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().select_related('added_by')
    serializer_class = BookSerializer
    permission_classes = [IsLibrarianOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all().select_related("book", "user")
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        book = serializer.validated_data["book"]
        serializer.save(user=self.request.user)
        book.is_available = False
        book.save()

    @action(detail=True, methods=["post"])
    def return_book(self, request, pk=None):
        loan = self.get_object()
        if loan.status == "RETURNED":
            return Response({"error": "Book already returned!"}, status=status.HTTP_400_BAD_REQUEST)
        loan.mark_as_returned()
        return Response({"message": "Book returned successfully!", "fine": f"{loan.fine:.2f}"})


@method_decorator(cache_page(60 * 15), name='dispatch')
class BookListView(ListView):
    model = Book
    template_name = "library/book_list.html"
    context_object_name = "books"


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().select_related("book", "user")
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        expires_at = timezone.now() + timezone.timedelta(days=3)
        serializer.save(user=self.request.user, expires_at=expires_at)

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
    permission_classes = [permissions.AllowAny] 
    def get(self, request):
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
        

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
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
