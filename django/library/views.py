from rest_framework import viewsets, permissions, generics, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.generic import ListView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Book, Loan, Reservation, Review
from .serializers import BookSerializer, LoanSerializer, UserRegistrationSerializer, ReservationSerializer, ReviewSerializer
from .permissions import IsOwnerOrReadOnly
from django.utils import timezone



class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().select_related('added_by')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

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
        return Response({
            "message": "Book returned successfully!",
            "fine": f"{loan.fine:.2f}"
        })


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
        book = serializer.validated_data["book"]
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
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
