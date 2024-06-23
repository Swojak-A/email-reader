from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config import api_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urls, namespace="api")),
]

if settings.ENVIRONMENT == "local":
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
