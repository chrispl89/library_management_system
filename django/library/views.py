from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer
from .models import Book
from rest_framework import viewsets, permissions
from .serializers import BookSerializer
from .permissions import IsOwnerOrReadOnly
from django.views.generic import ListView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().select_related('added_by')
    serializer_class = BookSerializer
    # Użytkownik musi być uwierzytelniony, a operacje zapisu mogą wykonywać tylko właściciele
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)

@method_decorator(cache_page(60 * 15), name='dispatch')
class BookListView(ListView):
    model = Book
    template_name = "library/book_list.html"  # Ścieżka do szablonu
    context_object_name = "books" 
