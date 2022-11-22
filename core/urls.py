from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.views import GoogleLogin, LoginViewSet

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/login", LoginViewSet.as_view({"post": "create"}), name="login"),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/google/", GoogleLogin.as_view(), name="google_login"),
]
