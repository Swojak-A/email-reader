import io
import re
from datetime import datetime
import pytz
from django.utils import timezone


def parse_datetime_to_django_timezone(date_str):
    date_format = "%a, %d %b %Y %H:%M:%S %z"
    naive_dt = datetime.strptime(date_str, date_format)
    utc_dt = naive_dt.astimezone(pytz.utc)
    django_dt = timezone.localtime(utc_dt)
    return django_dt


def convert_bytestring_to_file(filename, data):
    file = io.BytesIO(data)
    file.name = filename
    return file


def extract_email_address(email_str):
    email_regex = r"<(.+?)>|([\w\.-]+@[\w\.-]+)"

    matches = re.findall(email_regex, email_str)
    if matches:
        # The regular expression returns a list of tuples, where one element
        #  will be empty and the other will contain the email.
        for match in matches:
            email = match[0] if match[0] else match[1]
            if email:
                return email
    return None
