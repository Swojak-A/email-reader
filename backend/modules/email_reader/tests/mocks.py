EMAIL_WITHOUT_ATTACHMENT_CONTENT = (
    b"From: sender@example.com\r\n"
    b"To: receiver@example.com\r\n"
    b"Subject: Test Email\r\n"
    b"Date: Mon, 18 Oct 2021 14:30:00 -0400\r\n"
    b"Message-ID: <1234@example.com>\r\n"
    b"Cc: cc@example.com\r\n"
    b'Content-Type: text/plain; charset="us-ascii"\r\n'
    b"MIME-Version: 1.0\r\n"
    b"Content-Transfer-Encoding: 7bit\r\n"
    b"\r\n"
    b"This is the body.\r\n"
)

EMAIL_WITH_ATTACHMENT_CONTENT = (
    b"From: sender@example.com\r\n"
    b"To: receiver@example.com\r\n"
    b"Subject: Test Email\r\n"
    b"Date: Mon, 18 Oct 2021 14:30:00 -0400\r\n"
    b"Message-ID: <1234@example.com>\r\n"
    b"Cc: cc@example.com\r\n"
    b'Content-Type: multipart/mixed; boundary="===============123456789=="\r\n'
    b"--===============123456789==\r\n"
    b'Content-Type: text/plain; charset="us-ascii"\r\n'
    b"MIME-Version: 1.0\r\n"
    b"Content-Transfer-Encoding: 7bit"
    b"\r\n"
    b"This is the body.\r\n"
    b"--===============123456789==\r\n"
    b'Content-Type: application/octet-stream; name="test.txt"\r\n'
    b"MIME-Version: 1.0\r\n"
    b"Content-Transfer-Encoding: base64\r\n"
    b'Content-Disposition: attachment; filename="test.txt"\r\n'
    b"\r\n"
    b"dGVzdCBmaWxlIGNvbnRlbnQ=\r\n"
    b"--===============123456789==--\r\n"
)
