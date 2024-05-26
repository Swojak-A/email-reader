from django.core.validators import EmailValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from modules.core.models import BaseModel


class Email(BaseModel):
    email_id = models.CharField(
        verbose_name=_("Email ID"), max_length=255, default="", blank=True
    )
    subject = models.CharField(
        verbose_name=_("Subject"), max_length=255, default="", blank=True
    )
    body = models.TextField(verbose_name=_("Body"), default="", blank=True)
    sender = models.EmailField(verbose_name=_("Sender"), validators=[EmailValidator])
    receiver = models.EmailField(
        verbose_name=_("Receiver"), validators=[EmailValidator]
    )
    sent_at = models.DateTimeField(verbose_name=_("Sent at"), default=timezone.now)
    message_id = models.CharField(
        verbose_name=_("Message ID"), max_length=255, default="", blank=True
    )

    @property
    def has_attachments(self):
        return bool(self.attachments.exists())

    class Meta:
        verbose_name = _("Email")
        verbose_name_plural = _("Emails")

    def __str__(self):
        return f"{self.sender}: {self.subject}"

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        super().save(force_insert, force_update, using, update_fields)


class EmailAttachment(BaseModel):
    email = models.ForeignKey(
        Email,
        verbose_name=_("Email"),
        on_delete=models.CASCADE,
        related_name="attachments",
    )
    filename = models.CharField(
        verbose_name=_("Filename"), max_length=255, default="", blank=True
    )
    file = models.FileField(verbose_name=_("File"), upload_to="email_attachments/")
    mime_type = models.CharField(
        verbose_name=_("MIME Type"), max_length=255, default="", blank=True
    )

    class Meta:
        verbose_name = _("Email Attachment")
        verbose_name_plural = _("Email Attachments")

    def __str__(self):
        return f"{self.filename} ({self.mime_type})"
