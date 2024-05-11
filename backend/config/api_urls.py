from django.urls import include, path

app_name = "api"

urlpatterns = [
    path(
        "healthchecks/", include("modules.healthchecks.urls", namespace="healthchecks")
    ),
]
