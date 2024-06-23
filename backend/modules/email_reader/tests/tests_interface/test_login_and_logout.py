import pytest

from modules.email_reader.interface import EmailReader


class TestEmailReaderLoginAndLogout:
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_imap = mocker.patch("imaplib.IMAP4_SSL")

    def test_successful_login(self, mocker):
        imap_mock = mocker.patch("modules.email_reader.interface.imaplib.IMAP4_SSL")
        mock_instance = imap_mock.return_value
        mock_instance.login.return_value = ("OK", "Logged in")

        reader = EmailReader(
            host="example.com",
            username="testuser",
            password="testpass",  # noqa: S106
            email_addresses_whitelist=["sender@example.com"],
        )  # noqa: S106
        reader.login()

        assert imap_mock.called

    def test_successful_logout(self, mocker):
        imap_mock = mocker.patch("modules.email_reader.interface.imaplib.IMAP4_SSL")
        mock_instance = imap_mock.return_value
        mock_instance.logout.return_value = ("OK", "Logged out")

        reader = EmailReader(
            host="example.com",
            username="testuser",
            password="testpass",  # noqa: S106
            email_addresses_whitelist=["sender@example.com"],
        )
        reader.logout()

        assert imap_mock.called
