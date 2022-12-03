from django.urls import path, include
from accounts.views import AccountView, RegistrationViewSet


urlpatterns = [
    path("", include("allauth.urls" ), name="socialaccount_signup"),
    path("", AccountView.as_view({"get": "list", "post": "create", "put": "update", "delete": "destroy"})),
    path("registration/", RegistrationViewSet.as_view({"post": "create"}), name="registration"),
    path("<int:pk>", AccountView.as_view({"get": "retrieve", "delete": "destroy"})),
]