from django.urls import reverse

from rest_framework.test import APIClient


def test_healthcheck_endpoint():
    client = APIClient()
    response = client.get(reverse("api:healthchecks:status"))
    assert response.status_code == 200
    assert response.json() == {"message": "email-reader app works!"}
