from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from library.views import FrontendAppView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("library.urls")), 
    path("api-auth/", include("rest_framework.urls")), 
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    re_path(r'^(?!api/)(?!admin/).*$', FrontendAppView.as_view(), name='home'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
