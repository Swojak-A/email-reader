import pytest

from modules.email_reader.dto import EmailAttachmentDto
from modules.email_reader.models import EmailAttachment
from modules.email_reader.tests.factories import EmailFactory

pytestmark = pytest.mark.django_db


class TestEmailAttachmentDTO:
    def setup_method(self):
        self.email_attachment_dto = EmailAttachmentDto(
            filename="test.txt",
            data=b"test file content",
            mime_type="application/octet-stream",
        )

    def test_creation(self):
        assert self.email_attachment_dto
        assert isinstance(self.email_attachment_dto, EmailAttachmentDto)
        assert self.email_attachment_dto.filename == "test.txt"
        assert self.email_attachment_dto.data == b"test file content"
        assert self.email_attachment_dto.mime_type == "application/octet-stream"

    def test_to_model(self):
        self.email_attachment_dto.to_model(email=EmailFactory(attachments=[]))

        assert EmailAttachment.objects.count() == 1
        email_attachment = EmailAttachment.objects.first()
        assert email_attachment.filename == self.email_attachment_dto.filename
        assert email_attachment.file.read() == self.email_attachment_dto.data
        assert email_attachment.mime_type == self.email_attachment_dto.mime_type
        assert email_attachment.email

    def test_to_dict(self):
        email_attachment_dict = self.email_attachment_dto.to_dict()

        assert email_attachment_dict
        assert isinstance(email_attachment_dict, dict)
        assert email_attachment_dict["filename"] == "test.txt"
        assert email_attachment_dict["data"] == b"test file content"
        assert email_attachment_dict["mime_type"] == "application/octet-stream"
