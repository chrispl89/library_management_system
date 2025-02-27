from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (BookViewSet, UserRegistrationView, BookListView, LoanViewSet, ReservationViewSet, 
                    ReviewViewSet, GoogleBooksSearchView, UserRegistrationView, ProfileViewSet,UserViewSet, 
                    ActivateAccountView, UserViewSet, ActivateAccountView, UserDashboardView)

router = DefaultRouter()
router.register(r"books", BookViewSet, basename="book")
router.register(r"loans", LoanViewSet, basename="loan")
router.register(r"reservations", ReservationViewSet)
router.register(r"reviews", ReviewViewSet, basename="review")
router.register(r"profiles", ProfileViewSet, basename="profile")
router.register(r'users', UserViewSet)

urlpatterns = [
    path("activate/<uidb64>/<token>/", ActivateAccountView.as_view(), name="activate"),
    path("dashboard/", UserDashboardView.as_view(), name="dashboard"),
    path("api/", include(router.urls)),
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("", include(router.urls)),
    path("list/", BookListView.as_view(), name="book-list"),
    path("google-books/", GoogleBooksSearchView.as_view(), name="google-books-search"),
]