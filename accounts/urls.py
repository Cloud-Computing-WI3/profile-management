from django.urls import path, include
from accounts.views import AccountView, RegistrationViewSet, get_user_categories, get_user_keywords


urlpatterns = [
    path("", include("allauth.urls" ), name="socialaccount_signup"),
    path("", AccountView.as_view({"get": "list", "post": "create"})),
    path("<int:pk>", AccountView.as_view({"get": "retrieve", "post": "create", "put": "update", "delete": "destroy"})),
    path("registration/", RegistrationViewSet.as_view({"post": "create"}), name="registration"),
    path("<int:pk>/categories", get_user_categories, name="get_user_categories"),
    path("<int:pk>/keywords", get_user_keywords, name="get_user_keywords"),
]