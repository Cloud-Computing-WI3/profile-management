from django.urls import path
from categories.views import CategoryView

urlpatterns = [
    path("", CategoryView.as_view({"get": "list", "post": "create", "put": "update", "delete": "destroy"})),
]