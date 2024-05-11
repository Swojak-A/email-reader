from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HealthchecksConfig(AppConfig):
    name = "modules.healthchecks"
    verbose_name = _("Health Checks")
