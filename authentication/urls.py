from django.urls import path
from django.conf.urls.static import static
from authentication.views import LoginViewSet, RefreshViewSet, RegistrationViewSet
from profile_management import settings

namespace = "authentication"

urlpatterns = [
    path(r"login/", LoginViewSet.as_view({"post": "create"}), name="auth-login"),
    path(r"refresh/", RefreshViewSet.as_view({"post": "create"}), name="auth-refresh"),
    path(r"register/", RegistrationViewSet.as_view({"post": "create"}), name="auth-register"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)