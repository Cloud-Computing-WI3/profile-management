from django.urls import path
from accounts.views import AccountView


urlpatterns = [
    path("", AccountView.as_view({"get": "list", "post": "create", "put": "update", "delete": "destroy"})),
    path("<int:pk>", AccountView.as_view({"get": "retrieve", "delete": "destroy"})),
]