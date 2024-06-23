from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    uuid = models.UUIDField(
        _("UUID"), editable=False, default=uuid4, unique=True, db_index=True
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"),
        auto_now=True,
    )

    @property
    def uuid_str(self) -> str:
        return str(self.uuid)

    class Meta:
        abstract = True
