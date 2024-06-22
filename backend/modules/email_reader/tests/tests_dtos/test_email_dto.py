import pytest

from modules.email_reader.dto import EmailAttachmentDto, EmailDto
from modules.email_reader.models import Email, EmailAttachment

pytestmark = pytest.mark.django_db


class TestEmailDTO:
    def setup_method(self):
        self.email_dto = EmailDto(
            email_id="1",
            sender="sender@example.com",
            receiver="receiver@example.com",
            cc="cc@example.com",
            subject="Test Email",
            body="This is the body.",
            sent_at="Mon, 18 Oct 2021 14:30:00 -0400",
            message_id="<1234@example.com>",
            has_attachments=True,
            attachments=[
                EmailAttachmentDto(
                    filename="test.txt",
                    data=b"test file content",
                    mime_type="application/octet-stream",
                )
            ],
        )

    def test_creation(self):
        assert self.email_dto
        assert isinstance(self.email_dto, EmailDto)
        assert self.email_dto.email_id == "1"
        assert self.email_dto.sender == "sender@example.com"
        assert self.email_dto.receiver == "receiver@example.com"
        assert self.email_dto.cc == "cc@example.com"
        assert self.email_dto.subject == "Test Email"
        assert self.email_dto.body == "This is the body."
        assert self.email_dto.sent_at == "Mon, 18 Oct 2021 14:30:00 -0400"
        assert self.email_dto.message_id == "<1234@example.com>"
        assert self.email_dto.has_attachments is True

    def test_to_model(self):
        email = self.email_dto.to_model()

        assert isinstance(email, Email)
        assert email.email_id == self.email_dto.email_id
        assert email.sender == self.email_dto.sender
        assert email.receiver == self.email_dto.receiver
        assert email.subject == self.email_dto.subject
        assert email.body == self.email_dto.body
        assert email.message_id == self.email_dto.message_id
        assert email.has_attachments == self.email_dto.has_attachments
        assert len(email.attachments.all()) == len(self.email_dto.attachments)
        attachment = email.attachments.first()
        assert isinstance(attachment, EmailAttachment)
        assert attachment.filename == self.email_dto.attachments[0].filename
        assert attachment.file.read() == self.email_dto.attachments[0].data
        assert attachment.mime_type == self.email_dto.attachments[0].mime_type

    def test_to_dict(self):
        email_dict = self.email_dto.to_dict()

        assert email_dict
        assert isinstance(email_dict, dict)
        assert email_dict["email_id"] == self.email_dto.email_id
        assert email_dict["sender"] == self.email_dto.sender
        assert email_dict["receiver"] == self.email_dto.receiver
        assert email_dict["subject"] == self.email_dto.subject
        assert email_dict["body"] == self.email_dto.body
        assert email_dict["sent_at"] == self.email_dto.sent_at
        assert email_dict["message_id"] == self.email_dto.message_id
        assert email_dict["has_attachments"] == self.email_dto.has_attachments
        assert email_dict["attachments"]
        assert len(email_dict["attachments"]) == len(self.email_dto.attachments)
        attachment_dict = email_dict["attachments"][0]
        assert attachment_dict
        assert isinstance(attachment_dict, dict)
        assert attachment_dict["filename"] == self.email_dto.attachments[0].filename
        assert attachment_dict["data"] == self.email_dto.attachments[0].data
        assert attachment_dict["mime_type"] == self.email_dto.attachments[0].mime_type
