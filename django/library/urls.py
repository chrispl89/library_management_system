from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, UserRegistrationView, BookListView

router = DefaultRouter()
router.register(r"books", BookViewSet, basename="book")

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("", include(router.urls)),
    path("list/", BookListView.as_view(), name="book-list"),
]
