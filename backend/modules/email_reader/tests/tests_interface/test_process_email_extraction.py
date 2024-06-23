import pytest

from modules.email_reader.interface import EmailReader
from modules.email_reader.tests.mocks import (
    EMAIL_WITH_ATTACHMENT_CONTENT,
    EMAIL_WITHOUT_ATTACHMENT_CONTENT,
)
from modules.email_reader.tests.utils import assert_correct_email_data


class TestProcessEmailExtraction:
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_imap = mocker.patch("imaplib.IMAP4_SSL")

    def test_email_with_attachments(self, mocker):
        imap_mock = mocker.patch("modules.email_reader.interface.imaplib.IMAP4_SSL")
        mock_instance = imap_mock.return_value
        mock_instance.login.return_value = ("OK", "Logged in")
        mock_instance.select.return_value = ("OK", b"")
        mock_instance.search.return_value = ("OK", [b"1"])
        mock_instance.fetch.return_value = (
            "OK",
            [(b"1", EMAIL_WITH_ATTACHMENT_CONTENT)],
        )
        mock_instance.logout.return_value = ("OK", "Logged out")

        reader = EmailReader(
            host="example.com",
            username="testuser",
            password="testpass",  # noqa: S106
            email_addresses_whitelist=["sender@example.com"],
        )
        emails = reader.process_emails_extraction()

        assert isinstance(emails, list)
        assert_correct_email_data(emails[0].to_dict())
        assert mock_instance.login.called
        assert mock_instance.select.called
        assert mock_instance.search.called
        assert mock_instance.fetch.called
        assert mock_instance.logout.called

    def test_email_without_attachments(self, mocker):
        imap_mock = mocker.patch("modules.email_reader.interface.imaplib.IMAP4_SSL")
        mock_instance = imap_mock.return_value
        mock_instance.login.return_value = ("OK", "Logged in")
        mock_instance.select.return_value = ("OK", b"")
        mock_instance.search.return_value = ("OK", [b"1"])
        mock_instance.fetch.return_value = (
            "OK",
            [(b"1", EMAIL_WITHOUT_ATTACHMENT_CONTENT)],
        )
        mock_instance.logout.return_value = ("OK", "Logged out")

        reader = EmailReader(
            host="example.com",
            username="testuser",
            password="testpass",  # noqa: S106
            email_addresses_whitelist=["sender@example.com"],
        )
        emails = reader.process_emails_extraction()

        assert isinstance(emails, list)
        assert_correct_email_data(emails[0].to_dict())
        assert not emails[0].has_attachments
        assert mock_instance.login.called
        assert mock_instance.select.called
        assert mock_instance.search.called
        assert mock_instance.fetch.called
        assert mock_instance.logout.called
