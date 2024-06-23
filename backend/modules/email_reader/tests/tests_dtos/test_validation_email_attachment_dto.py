import pytest
from pydantic import ValidationError

from modules.email_reader.dto import EmailAttachmentDto

pytestmark = pytest.mark.django_db


class TestEmailAttachmentDTO:

    """Test cases for EmailAttachmentDto validation for most common cases"""

    def test_positive_validation(self):
        EmailAttachmentDto(
            filename="test.txt",
            data=b"test file content",
            mime_type="application/octet-stream",
        )

    def test_validation_invalid_filename(self):
        with pytest.raises(ValidationError):
            EmailAttachmentDto(
                filename=1,
                data=b"test file content",
                mime_type="application/octet-stream",
            )

    def test_validation_missing_data(self):
        with pytest.raises(ValidationError):
            EmailAttachmentDto(
                filename="test.txt",
                # data=b"test file content",
                mime_type="application/octet-stream",
            )

    def test_validation_missing_mime_type(self):
        with pytest.raises(ValidationError):
            EmailAttachmentDto(
                filename="test.txt",
                data=b"test file content",
                # mime_type="application/octet-stream",
            )
