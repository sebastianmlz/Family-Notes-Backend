import uuid
from django.db import models

from core import settings


class Family(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=255, unique=True, db_index=True, verbose_name="Family Name"
    )
    password = models.CharField(max_length=255, verbose_name="Hashed Family Password")
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="family_account",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Family"
        verbose_name_plural = "Families"

    def __str__(self):
        return self.name
