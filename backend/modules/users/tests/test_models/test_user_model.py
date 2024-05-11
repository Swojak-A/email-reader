import pytest

from modules.users.models import User
from modules.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestUserModel:
    def test_create_user(self):
        UserFactory()

        assert User.objects.count() == 1
