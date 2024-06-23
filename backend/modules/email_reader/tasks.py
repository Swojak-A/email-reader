from modules.email_reader.interface import EmailReader
from modules.email_reader.models import EmailAddress
from scheduler import celery_app


@celery_app.task(
    bind=True,
    track_started=True,
    queue="celerybeat",
    name="check_and_extract_new_emails",
)
def check_and_extract_new_emails(self):
    whitelist = EmailAddress.objects.filter(is_whitelisted=True).values_list(
        "email", flat=True
    )
    email_reader = EmailReader(email_addresses_whitelist=whitelist)
    emails = email_reader.process_emails_extraction()
    for email in emails:
        email.to_model()
