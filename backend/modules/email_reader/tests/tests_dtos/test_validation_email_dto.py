import pytest
from pydantic import ValidationError

from modules.email_reader.dto import EmailDto

pytestmark = pytest.mark.django_db


class TestEmailDTO:

    """Test cases for EmailDto validation for most common cases"""

    def test_positive_validation(self):
        EmailDto(
            email_id="1",
            sender="sender@example.com",
            receiver="receiver@example.com",
            cc="cc@example.com",
            subject="Test Email",
            body="This is the body.",
            sent_at="Mon, 18 Oct 2021 14:30:00 -0400",
            message_id="<1234@example.com>",
            has_attachments=True,
            attachments=[],
        )

    def test_validation_invalid_email_id(self):
        """Test where the email_id is an integer instead of a string"""
        with pytest.raises(ValidationError):
            EmailDto(
                email_id=1,
                sender="sender@example.com",
                receiver="receiver@example.com",
                cc="cc@example.com",
                subject="Test Email",
                body="This is the body.",
                sent_at="Mon, 18 Oct 2021 14:30:00 -0400",
                message_id="<1234@example.com>",
                has_attachments=True,
                attachments=[],
            )

    def test_validation_missing_body(self):
        with pytest.raises(ValidationError):
            EmailDto(
                email_id="1",
                sender="sender@example.com",
                receiver="receiver@example.com",
                cc="cc@example.com",
                subject="Test Email",
                # body="This is the body.",
                sent_at="Mon, 18 Oct 2021 14:30:00 -0400",
                message_id="<1234@example.com>",
                has_attachments=True,
                attachments=[],
            )

    def test_bytes_to_string_casting(self):
        """Test where the body is bytestring instead of string"""
        email_dto = EmailDto(
            email_id=b"1",
            sender="sender@example.com",
            receiver="receiver@example.com",
            cc="cc@example.com",
            subject="Test Email",
            body=b"This is the body.",
            sent_at="Mon, 18 Oct 2021 14:30:00 -0400",
            message_id="<1234@example.com>",
            has_attachments=True,
            attachments=[],
        )
        email = email_dto.to_model()
        assert email.email_id == "1"
        assert email.body == "This is the body."
