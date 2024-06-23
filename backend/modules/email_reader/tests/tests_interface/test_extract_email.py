import pytest

from modules.email_reader.dto import EmailDto
from modules.email_reader.interface import EmailReader
from modules.email_reader.tests.mocks import (
    EMAIL_WITH_ATTACHMENT_CONTENT,
    EMAIL_WITHOUT_ATTACHMENT_CONTENT,
)
from modules.email_reader.tests.utils import (
    assert_correct_email_attachments_data,
    assert_correct_email_data,
)


class TestEmailReaderExtractEmail:
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_imap = mocker.patch("imaplib.IMAP4_SSL")

    def test_email_without_attachments(self, mocker):
        imap_mock = mocker.patch("modules.email_reader.interface.imaplib.IMAP4_SSL")
        mock_instance = imap_mock.return_value
        mock_instance.login.return_value = ("OK", "Logged in")
        mock_instance.fetch.return_value = (
            "OK",
            [(b"1", EMAIL_WITHOUT_ATTACHMENT_CONTENT)],
        )

        reader = EmailReader(
            host="example.com",
            username="testuser",
            password="testpass",  # noqa: S106
            email_addresses_whitelist=["sender@example.com"],
        )
        reader.login()
        email_data = reader.extract_email("1")

        assert isinstance(email_data, EmailDto)
        assert_correct_email_data(email_data.to_dict())

    def test_email_with_attachments(self, mocker):
        imap_mock = mocker.patch("modules.email_reader.interface.imaplib.IMAP4_SSL")
        mock_instance = imap_mock.return_value
        mock_instance.login.return_value = ("OK", "Logged in")
        mock_instance.fetch.return_value = (
            "OK",
            [(b"1", EMAIL_WITH_ATTACHMENT_CONTENT)],
        )

        reader = EmailReader(
            host="example.com",
            username="testuser",
            password="testpass",  # noqa: S106
            email_addresses_whitelist=["sender@example.com"],
        )
        reader.login()
        email_data = reader.extract_email("1")

        assert isinstance(email_data, EmailDto)
        assert_correct_email_data(email_data.to_dict())
        assert_correct_email_attachments_data(email_data.to_dict())

    def test_assertion_for_bytes_instance_passed_as_arg(self, mocker):
        imap_mock = mocker.patch("modules.email_reader.interface.imaplib.IMAP4_SSL")
        mock_instance = imap_mock.return_value
        mock_instance.login.return_value = ("OK", "Logged in")
        mock_instance.fetch.return_value = (
            "OK",
            [(b"1", EMAIL_WITH_ATTACHMENT_CONTENT)],
        )

        reader = EmailReader(
            host="example.com",
            username="testuser",
            password="testpass",  # noqa: S106
            email_addresses_whitelist=("sender@example.com",),
        )
        reader.login()

        with pytest.raises(TypeError):
            reader.extract_email(b"1")
