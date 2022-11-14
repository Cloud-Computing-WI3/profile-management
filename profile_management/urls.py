from django.contrib import admin
from django.urls import path, include
from profile_management import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("profiles/", include("profiles.urls")),
    path("auth/", include("authentication.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
