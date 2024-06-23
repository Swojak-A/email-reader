import pytest

from modules.email_reader.exceptions import (
    EmailReaderInvalidStatusException,
    NoEmailsFoundException,
)
from modules.email_reader.interface import EmailReader


class TestEmailReaderFetchEmailIds:
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_imap = mocker.patch("imaplib.IMAP4_SSL")

    def test_successful_fetching_email_ids(self, mocker):
        imap_mock = mocker.patch("modules.email_reader.interface.imaplib.IMAP4_SSL")
        mock_instance = imap_mock.return_value
        mock_instance.login.return_value = ("OK", "Logged in")
        mock_instance.select.return_value = ("OK", b"")
        mock_instance.search.return_value = ("OK", [b"1 2 3"])

        reader = EmailReader(
            host="example.com",
            username="testuser",
            password="testpass",  # noqa: S106
            email_addresses_whitelist=["sender@example.com"],
        )
        reader.login()
        email_ids = reader.fetch_email_ids()

        assert email_ids == ["1", "2", "3"]

    def test_single_email_id(self, mocker):
        imap_mock = mocker.patch("modules.email_reader.interface.imaplib.IMAP4_SSL")
        mock_instance = imap_mock.return_value
        mock_instance.login.return_value = ("OK", "Logged in")
        mock_instance.select.return_value = ("OK", b"")
        mock_instance.search.return_value = ("OK", [b"1"])

        reader = EmailReader(
            host="example.com",
            username="testuser",
            password="testpass",  # noqa: S106
            email_addresses_whitelist=["sender@example.com"],
        )
        reader.login()
        email_ids = reader.fetch_email_ids()

        assert email_ids == ["1"]

    def test_search_failure(self, mocker):
        imap_mock = mocker.patch("modules.email_reader.interface.imaplib.IMAP4_SSL")
        mock_instance = imap_mock.return_value
        mock_instance.login.return_value = ("OK", "Logged in")
        mock_instance.select.return_value = ("OK", b"")
        mock_instance.search.return_value = ("NO", [])

        reader = EmailReader(
            host="example.com",
            username="testuser",
            password="testpass",  # noqa: S106
            email_addresses_whitelist=["sender@example.com"],
        )
        reader.login()

        with pytest.raises(EmailReaderInvalidStatusException):
            reader.fetch_email_ids()

    def test_no_emails_found(self, mocker):
        imap_mock = mocker.patch("modules.email_reader.interface.imaplib.IMAP4_SSL")
        mock_instance = imap_mock.return_value
        mock_instance.login.return_value = ("OK", "Logged in")
        mock_instance.select.return_value = ("OK", b"")
        mock_instance.search.return_value = ("OK", [b""])

        reader = EmailReader(
            host="example.com",
            username="testuser",
            password="testpass",  # noqa: S106
            email_addresses_whitelist=["sender@example.com"],
        )
        reader.login()

        with pytest.raises(NoEmailsFoundException):
            reader.fetch_email_ids()
