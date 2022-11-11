from django.urls import path
from authentication.views import LoginViewSet, RefreshViewSet

namespace = "authentication"

urlpatterns = [
    path(r"login/", LoginViewSet.as_view({"post": "create"}), name="auth-login"),
    path(r"refresh/", RefreshViewSet.as_view({"post": "create"}), name="auth-refresh"),
]