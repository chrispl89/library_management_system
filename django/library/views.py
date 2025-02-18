from rest_framework import viewsets, permissions, generics, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.generic import ListView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Book, Loan
from .serializers import BookSerializer, LoanSerializer, UserRegistrationSerializer
from .permissions import IsOwnerOrReadOnly


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
        book.is_available = False
        book.save()
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def return_book(self, request, pk=None):
        loan = self.get_object()
        if loan.status == "RETURNED":
            return Response({"error": "Book already returned!"}, status=status.HTTP_400_BAD_REQUEST)
        loan.mark_as_returned()
        return Response({"message": "Book returned successfully!"})

@method_decorator(cache_page(60 * 15), name='dispatch')
class BookListView(ListView):
    model = Book
    template_name = "library/book_list.html"  
    context_object_name = "books" 
