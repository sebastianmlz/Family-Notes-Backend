import uuid
from django.db import models


class Profile(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Profile Name", db_index=True)
    age = models.PositiveIntegerField(verbose_name="Age")
    pin = models.CharField(max_length=255, verbose_name="Hashed Profile PIN")
    family = models.ForeignKey(
        "Family", on_delete=models.CASCADE, related_name="profiles"
    )
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        unique_together = ["family", "name"]

    def __str__(self):
        return f"{self.name} - {self.family.name}"
