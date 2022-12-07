from django.urls import path
from keywords.views import KeywordView

urlpatterns = [
    path("", KeywordView.as_view({"get": "list", "post": "create", "put": "update", "delete": "destroy"})),
]