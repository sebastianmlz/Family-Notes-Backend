import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import User, Family, Profile
from .models import Note


@pytest.mark.django_db
class TestNotePrivacy:
    def setup_method(self):
        self.client = APIClient()
        # 1. Creamos el entorno: Usuario, Familia y Perfil
        self.user = User.objects.create_user(username="sebas", password="123")
        self.family = Family.objects.create(name="Familia Lopez", owner=self.user)
        self.user.family_account = self.family
        self.user.save()
        self.profile = Profile.objects.create(
            name="Sebas Perfil",
            family=self.family,
            age=25,  # <-- Agregá esto aquí
        )
        self.client.force_authenticate(user=self.user)

    def test_list_notes_only_for_correct_profile(self):
        # Creamos una nota para el perfil[cite: 1]
        Note.objects.create(
            title="Nota Privada", content="Contenido", profile=self.profile
        )

        url = reverse("note-list")
        # Probamos enviando el profile_id correcto
        response = self.client.get(f"{url}?profile_id={self.profile.id}")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["title"] == "Nota Privada"

    def test_empty_list_if_no_profile_id(self):
        url = reverse("note-list")
        # Según tu lógica, si no hay profile_id, devuelve vacío[cite: 3]
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_validation_short_title(self):
        url = reverse("note-list")
        data = {
            "title": "No",  # Título demasiado corto
            "content": "Test",
            "profile": self.profile.id,
        }
        response = self.client.post(url, data, format="json")

        # Debe fallar por la validación del Serializer[cite: 2]
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data
