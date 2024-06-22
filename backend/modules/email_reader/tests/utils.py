# flake8: noqa: S101


def assert_correct_email_data(email_data):
    """Asserts the correctness of the extracted data
    in relation to EMAIL_... mock."""
    assert "email_id" in email_data
    assert email_data["email_id"] == "1"
    assert "sender" in email_data
    assert email_data["sender"] == "sender@example.com"
    assert "receiver" in email_data
    assert email_data["receiver"] == "receiver@example.com"
    assert "subject" in email_data
    assert email_data["subject"] == "Test Email"
    assert "body" in email_data
    # we strip body to ignore the \r\n characters in the body since
    #  they are processed differently due to different type of content_type
    #  in the email
    assert email_data["body"].strip() == "This is the body."
    assert "sent_at" in email_data
    assert email_data["sent_at"] == "Mon, 18 Oct 2021 14:30:00 -0400"
    assert "message_id" in email_data
    assert email_data["message_id"] == "<1234@example.com>"
    assert "has_attachments" in email_data


def assert_correct_email_attachments_data(email_data):
    """Asserts the correctness of the extracted data
    in relation to EMAIL_WITH_ATTACHMENT_CONTENT mock."""
    assert email_data["has_attachments"] is True
    assert "attachments" in email_data
    assert email_data["attachments"]
    assert "filename" in email_data["attachments"][0]
    assert email_data["attachments"][0]["filename"] == "test.txt"
    assert "data" in email_data["attachments"][0]
    assert email_data["attachments"][0]["data"] == b"test file content"
    assert "mime_type" in email_data["attachments"][0]
    assert email_data["attachments"][0]["mime_type"] == "application/octet-stream"
