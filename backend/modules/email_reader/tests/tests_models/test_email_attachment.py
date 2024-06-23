import pytest

from modules.email_reader.models import Email, EmailAttachment
from modules.email_reader.tests.factories import EmailAttachmentFactory

pytestmark = pytest.mark.django_db


class TestEmailAttachmentModel:
    def test_model_creation(self):
        email_attachment = EmailAttachmentFactory()

        assert EmailAttachment.objects.count() == 1
        assert Email.objects.count() == 1
        assert (
            str(email_attachment)
            == f"{email_attachment.filename} ({email_attachment.mime_type})"
        )
