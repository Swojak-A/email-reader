import io
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
