from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, UserRegistrationView, BookListView

router = DefaultRouter()
router.register(r"books-api", BookViewSet, basename="book")

urlpatterns = [
    # Endpoint rejestracji użytkownika
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    # Widok HTML wyświetlający książki
    path("list/", BookListView.as_view(), name="book-list"),
    # Endpointy API (dla CRUD na książkach)
    path("", include(router.urls)),
]
