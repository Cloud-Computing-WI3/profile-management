from django.urls import path
from profiles.views import ProfileView

namespace = "profiles"

urlpatterns = [
    path("", ProfileView.as_view({"get": "list", "post": "create", "put": "update", "delete": "destroy"})),
    path("<int:pk>", ProfileView.as_view({"get": "retrieve", "delete": "destroy"})),
]