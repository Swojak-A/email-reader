from django.test import override_settings

import pytest

from modules.email_reader.interface import EmailReader

pytestmark = pytest.mark.django_db


class TestEmailReaderInstantiation:
    @pytest.fixture(autouse=True)
    def setup_method(self, mocker):
        self.mock_imap = mocker.patch("imaplib.IMAP4_SSL")

    @override_settings(
        EMAIL_READER_HOST="example.com",
        EMAIL_READER_USERNAME="testuser",
        EMAIL_READER_PASSWORD="testpass",  # noqa: S106
    )
    def test_instantiation(self):
        reader = EmailReader(
            email_addresses_whitelist=["example@example.com"],
        )

        assert reader
        assert isinstance(reader, EmailReader)

    def test_instantiation_with_email_address_whitelist_as_tuple(self):
        reader = EmailReader(
            host="example.com",
            username="testuser",
            password="testpass",  # noqa: S106
            email_addresses_whitelist=("example@example.com",),
        )

        assert reader
        assert isinstance(reader, EmailReader)

    def test_instantiation_with_email_address_whitelist_as_list(self):
        reader = EmailReader(
            host="example.com",
            username="testuser",
            password="testpass",  # noqa: S106
            email_addresses_whitelist=["example@example.com"],
        )

        assert reader
        assert isinstance(reader, EmailReader)

    @pytest.mark.parametrize(
        "email_address_whitelist",
        [
            "example.com",
            b"example.com",
            [],
            None,
            123,
        ],
    )
    def test_instantiation_with_invalid_email_address_whitelist(
        self, email_address_whitelist
    ):
        with pytest.raises(ValueError):
            EmailReader(
                host="example.com",
                username="testuser",
                password="testpass",  # noqa: S106
                email_addresses_whitelist=email_address_whitelist,
            )
