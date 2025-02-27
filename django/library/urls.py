from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookViewSet, LoanViewSet, ReservationViewSet, ReviewViewSet,
    UserRegistrationView, ProfileViewSet, UserViewSet,
    ActivateAccountView, DashboardTemplateView, GoogleBooksSearchView
)

router = DefaultRouter()
router.register(r"books", BookViewSet, basename="book")
router.register(r"loans", LoanViewSet, basename="loan")
router.register(r"reservations", ReservationViewSet)
router.register(r"reviews", ReviewViewSet, basename="review")
router.register(r"profiles", ProfileViewSet, basename="profile")
router.register(r"users", UserViewSet)

urlpatterns = [
    # Activation and registration endpoints
    path("activate/<uidb64>/<token>/", ActivateAccountView.as_view(), name="activate"),
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("google-books/", GoogleBooksSearchView.as_view(), name="google-books-search"),
    
    # Dashboard endpoint for frontend (renders HTML)
    path("dashboard/", DashboardTemplateView.as_view(), name="dashboard"),
    
    # API endpoints (returning JSON) – these will be available under /api/
    path("api/", include(router.urls)),
]
