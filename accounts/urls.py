from django.urls import path, include
from accounts.views import AccountView


urlpatterns = [
    path("", include("allauth.urls" ), name="socialaccount_signup"),
    path("", AccountView.as_view({"get": "list", "post": "create", "put": "update", "delete": "destroy"})),
    path("<int:pk>", AccountView.as_view({"get": "retrieve", "delete": "destroy"})),
]