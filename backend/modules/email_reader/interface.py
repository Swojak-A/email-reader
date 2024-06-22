import email
import imaplib
from collections.abc import Iterable

from django.conf import settings

from modules.email_reader.dto import EmailAttachmentDto, EmailDto
from modules.email_reader.exceptions import (
    EmailReaderInvalidStatusException,
    NoEmailsFoundException,
)
from modules.email_reader.models import EmailAddress


class EmailReader:
    def __init__(
        self,
        host=settings.EMAIL_READER_HOST,
        username=settings.EMAIL_READER_USERNAME,
        password=settings.EMAIL_READER_PASSWORD,
        email_addresses_whitelist=None,
    ):
        self.host = host
        self.username = username
        self.password = password
        self.mail = imaplib.IMAP4_SSL(self.host)
        self.email_addresses_whitelist = self._set_email_addresses_whitelist(
            email_addresses_whitelist
        )
        self.criteria = self._construct_criteria()

    def _assert_correct_email_addresses_whitelist(self, email_addresses_whitelist):
        if not email_addresses_whitelist:
            raise ValueError("Email addresses whitelist cannot be empty")
        if not isinstance(email_addresses_whitelist, Iterable):
            raise ValueError("Email addresses whitelist must be an iterable")
        if isinstance(email_addresses_whitelist, (str, bytes)):
            raise ValueError("Email addresses whitelist cannot be a string")
        if not all(isinstance(email, str) for email in email_addresses_whitelist):
            raise ValueError("All email addresses must be strings")

    def _get_default_email_addresses_whitelist(self):
        email_addresses_whitelist = EmailAddress.objects.filter(
            is_whitelisted=True
        ).values_list("email", flat=True)
        return email_addresses_whitelist

    def _set_email_addresses_whitelist(self, email_addresses_whitelist):
        if email_addresses_whitelist is None:
            email_addresses_whitelist = self._get_default_email_addresses_whitelist()
        self._assert_correct_email_addresses_whitelist(email_addresses_whitelist)
        return [email.lower().strip() for email in email_addresses_whitelist]

    def _construct_criteria(self):
        unseen_criteria = "UNSEEN"
        if not self.email_addresses_whitelist:
            return unseen_criteria
        if len(self.email_addresses_whitelist) == 1:
            email_address_criteria = f'FROM "{self.email_addresses_whitelist[0]}"'
            criteria = " ".join([unseen_criteria, email_address_criteria])
            return criteria
        else:
            email_addresses_criteria = "OR " + " ".join(
                [f'(FROM "{email}")' for email in self.email_addresses_whitelist]
            )
            criteria = " ".join([unseen_criteria, email_addresses_criteria])
            return criteria

    def _get_body(self, msg):
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if (
                    content_type == "text/plain"
                    and "attachment" not in content_disposition
                ):
                    return part.get_payload(decode=True).decode()
                elif (
                    content_type == "text/html"
                    and "attachment" not in content_disposition
                ):
                    return part.get_payload(decode=True).decode()
        else:
            return msg.get_payload(decode=True).decode()

    def login(self):
        self.mail.login(self.username, self.password)

    def logout(self):
        self.mail.logout()

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()

    def fetch_email_ids(self, criteria=None):
        if not criteria:
            criteria = self.criteria
        self.mail.select("inbox")
        status, messages_data = self.mail.search(None, criteria)
        if status != "OK":
            raise EmailReaderInvalidStatusException(status)
        email_ids = [x.decode("utf8") for x in messages_data[0].split()]
        if not email_ids:
            raise NoEmailsFoundException()
        return email_ids

    def extract_email(self, email_id):
        # defensive approach to avoid `bytes` being passed in
        if not isinstance(email_id, str):
            raise TypeError(
                f"Expected 'email_id' to be a str, but got {type(email_id).__name__}"
            )

        self.mail.select("inbox")
        status, data = self.mail.fetch(email_id, "(RFC822)")
        if status != "OK":
            raise EmailReaderInvalidStatusException(status)

        email_data = email.message_from_bytes(data[0][1])
        sender = email_data["From"]
        receiver = email_data["To"]
        subject = email_data["Subject"]
        date = email_data["Date"]
        message_id = email_data["Message-ID"]
        cc = email_data.get("Cc", "")
        body = self._get_body(email_data)
        has_attachments = False
        attachments = []
        attachments_mime_types = []
        if email_data.is_multipart():
            for part in email_data.walk():
                content_disposition = part.get("Content-Disposition")
                if content_disposition and "attachment" in content_disposition:
                    has_attachments = True
                    file_data = part.get_payload(decode=True)
                    filename = part.get_filename()
                    mime_type = part.get_content_type()
                    attachments.append({"filename": filename, "data": file_data})
                    attachments_mime_types.append(mime_type)

        attachments_dtos = [
            EmailAttachmentDto(
                filename=attachment["filename"],
                data=attachment["data"],
                mime_type=attachment_mime_type,
            )
            for attachment, attachment_mime_type in zip(
                attachments, attachments_mime_types, strict=True
            )
        ]
        email_dto = EmailDto(
            email_id=email_id,
            sender=sender,
            receiver=receiver,
            cc=cc,
            subject=subject,
            body=body,
            sent_at=date,
            message_id=message_id,
            has_attachments=has_attachments,
            attachments=attachments_dtos,
        )
        return email_dto

    def process_emails_extraction(self):
        # `with self` will wrap the login and logout methods
        with self:
            email_ids = self.fetch_email_ids()
            emails = []
            for email_id in email_ids:
                email_data = self.extract_email(email_id)
                emails.append(email_data)
        return emails
