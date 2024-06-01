from typing import List
from django.core.files.base import ContentFile
from modules.email_reader.utils import (
    parse_datetime_to_django_timezone,
    convert_bytestring_to_file,
)
from modules.email_reader.models import Email, EmailAttachment


class EmailAttachmentDto:
    def __init__(self, filename: str, data: bytes, mime_type: str):
        self.filename = filename
        self.data = data
        self.mime_type = mime_type

    def to_model(self, email):
        email_attachment = EmailAttachment(
            email=email,
            filename=self.filename,
            mime_type=self.mime_type,
        )
        file = convert_bytestring_to_file(self.filename, self.data)
        email_attachment.file.save(self.filename, ContentFile(file.read()), save=True)
        email_attachment.save()
        return email_attachment

    def to_dict(self):
        return {
            "filename": self.filename,
            "data": self.data,
            "mime_type": self.mime_type,
        }

class EmailDto:
    def __init__(
        self,
        email_id: str,
        sender: str,
        receiver: str,
        cc: str | None,
        subject: str,
        body: str,
        sent_at: str,
        message_id: str,
        has_attachments: bool,
        attachments: List[EmailAttachmentDto],
    ):
        self.email_id = email_id
        self.sender = sender
        self.receiver = receiver
        self.cc = cc
        self.subject = subject
        self.body = body
        self.sent_at = sent_at
        self.message_id = message_id
        self.has_attachments = has_attachments
        self.attachments = attachments

    def to_model(self):
        email = Email(
            email_id=self.email_id,
            sender=self.sender,
            receiver=self.receiver,
            subject=self.subject,
            body=self.body,
            sent_at=parse_datetime_to_django_timezone(self.sent_at),
            message_id=self.message_id,
        )
        email.save()
        for attachment_dto in self.attachments:
            email.attachments.add(attachment_dto.to_model(email))
        return email

    def to_dict(self):
        return {
            "email_id": self.email_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "cc": self.cc,
            "subject": self.subject,
            "body": self.body,
            "sent_at": self.sent_at,
            "message_id": self.message_id,
            "has_attachments": self.has_attachments,
            "attachments": [attachment.to_dict() for attachment in self.attachments],
        }
