from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from profiles.views import ProfileView

namespace = "profiles"

urlpatterns = [
    path("", ProfileView.as_view({"get": "list", "post": "create", "put": "update", "delete": "destroy"})),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]