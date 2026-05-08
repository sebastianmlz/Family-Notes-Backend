from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Hacemos que el email sea único y obligatorio
    email = models.EmailField(unique=True)

    # Podés agregar campos globales aquí si quisieras
    # Pero recordá que la lógica específica de la familia ya está en Family

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "System User"
