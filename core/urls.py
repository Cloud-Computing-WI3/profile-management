from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.views import GoogleLogin, LoginViewSet
from core import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/login/", LoginViewSet.as_view({"post": "create"}), name="login"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("accounts/", include("accounts.urls")),
    path("categories/", include("categories.urls")),
    path("keywords/", include("keywords.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)