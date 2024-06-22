import pytest

from modules.email_reader.utils import extract_email_address


class TestExtractEmailAddress:
    @pytest.mark.parametrize(
        "email_str, expected",
        [
            ("John Doe <john.doe@example.com>", "john.doe@example.com"),
            ("<john.doe@example.com>, jane.doe@example.com", "john.doe@example.com"),
            ("<john.doe@example.com>", "john.doe@example.com"),
            ("john.doe@example.com", "john.doe@example.com"),
            ("john.doe@example.com", "john.doe@example.com"),
            ("No email here", None),
            ("", None),
        ],
    )
    def test_extract_email_address(self, email_str, expected):
        assert extract_email_address(email_str) == expected
