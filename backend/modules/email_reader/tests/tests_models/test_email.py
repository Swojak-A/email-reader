from django.core.exceptions import ValidationError

import pytest

from modules.email_reader.models import Email
from modules.email_reader.tests.factories import EmailFactory

pytestmark = pytest.mark.django_db


class TestEmailModel:
    def test_model_creation(self):
        email = EmailFactory()

        assert Email.objects.count() == 1
        assert str(email) == f"{email.sender}: {email.subject}"
        # asserting the fields
        assert email.email_id
        assert email.subject
        assert email.body
        assert email.sender
        assert "@" in email.sender
        assert email.receiver
        assert "@" in email.receiver
        assert email.sent_at
        assert email.message_id
        assert email.message_id.startswith("<")
        assert email.message_id.endswith(">")
        # checking on the attachments
        assert email.has_attachments
        assert email.attachments.count() == 1
        attachment = email.attachments.first()
        assert attachment.filename
        assert attachment.file
        assert attachment.mime_type

    def test_model_creation_without_attachments(self):
        email = EmailFactory(attachments=[])

        assert Email.objects.count() == 1
        assert str(email) == f"{email.sender}: {email.subject}"
        # checking on the attachments
        assert not email.has_attachments
        assert email.attachments.count() == 0

    def test_email_fields_validation(self):
        with pytest.raises(ValidationError):
            EmailFactory(sender="invalid_email_address")
