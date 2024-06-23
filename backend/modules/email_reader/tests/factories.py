import factory
from faker import Faker

from modules.email_reader.models import Email, EmailAttachment

fake = Faker("en_US")


class EmailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Email

    # email_id is in the format of stringified integer. e.g.: "123"
    email_id = str(fake.random_int(1, 1000))
    subject = factory.Faker("sentence", nb_words=6, variable_nb_words=True)
    body = factory.Faker("text", max_nb_chars=200)
    sender = factory.Faker("email")
    receiver = factory.Faker("email")
    sent_at = factory.Faker("date_time")
    # message_id is non standard format. e.g.:
    #  "<CAL9_rtonmgAUbSBMJnuhHOEtYrSQFCSwpcLgyRGsmzYKVaBmKo@mail.gmail.com>"
    message_id = f"<CAL9_{fake.pystr(min_chars=46, max_chars=46)}@mail.gmail.com>"

    @factory.post_generation
    def attachments(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted or extracted == []:
            # A list of attachments were passed in, use them
            for attachment in extracted:
                EmailAttachmentFactory(email=self, **attachment)
        else:
            # Create a default attachment
            EmailAttachmentFactory(email=self)


class EmailAttachmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmailAttachment

    email = factory.SubFactory(EmailFactory, attachments=[])
    filename = factory.Faker("file_name")
    file = factory.django.FileField(filename="test.txt")
    mime_type = factory.Faker("mime_type")
