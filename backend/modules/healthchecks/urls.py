from django.urls import path

from .views import HealthCheckApiView

app_name = "healthchecks"

urlpatterns = [
    path("status", HealthCheckApiView.as_view(), name="status"),
]
