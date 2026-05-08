import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User, Family


@pytest.mark.django_db
class TestUserRegistration:
    def test_register_user_creates_family(self):
        client = APIClient()
        url = reverse("user-list")  # Ajusta si tu router tiene otro nombre
        data = {
            "username": "sebas_test",
            "email": "test@uagrm.edu.bo",
            "password": "password123",
            "family_name": "Familia Test",
        }

        response = client.post(url, data, format="json")

        # Verificaciones (Assertions)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="test@uagrm.edu.bo").exists()
        assert Family.objects.filter(name="Familia Test").exists()

        # Calidad: Verificar que el dueño de la familia sea el usuario creado
        user = User.objects.get(email="test@uagrm.edu.bo")
        family = Family.objects.get(name="Familia Test")
        assert family.owner == user
