from django.contrib.admin import ModelAdmin, register

from modules.email_reader.models import Email, EmailAddress, EmailAttachment


@register(EmailAddress)
class EmailAddressAdmin(ModelAdmin):
    list_display = ("email", "is_whitelisted")
    list_filter = ("is_whitelisted",)
    search_fields = ("email",)


@register(EmailAttachment)
class EmailAttachmentAdmin(ModelAdmin):
    list_display = ("filename", "mime_type", "email")
    list_filter = ("mime_type",)
    search_fields = ("filename", "mime_type")


@register(Email)
class EmailAdmin(ModelAdmin):
    list_display = ("sender", "email_id", "subject", "has_attachments", "sent_at")
    list_filter = ("sender", "sent_at")
    search_fields = ("sender", "subject")

    def has_attachments(self, obj):
        return obj.has_attachments

    has_attachments.boolean = True
