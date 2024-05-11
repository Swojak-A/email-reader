import factory

from modules.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    class Meta:
        model = User

    @factory.lazy_attribute
    def email(self):
        return f"{self.first_name}.{self.last_name}@example.com".lower()
