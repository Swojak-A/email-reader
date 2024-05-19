from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _


class EmailReaderConfig(AppConfig):
    name = 'modules.email_reader'
    verbose_name = _('Email Reader')
