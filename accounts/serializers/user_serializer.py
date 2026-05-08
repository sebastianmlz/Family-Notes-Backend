from rest_framework import serializers
from django.db import transaction
from ..models import User, Family


class RegisterSerializer(serializers.ModelSerializer):
    # Campo extra que no está en el modelo User, pero lo necesitamos para la familia
    family_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "family_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        family_name = validated_data.pop("family_name")

        # INGENIERÍA DE CALIDAD: Transacción Atómica
        # Si algo falla al crear la familia, se deshace la creación del usuario.
        with transaction.atomic():
            # 1. Creamos el usuario con el método seguro de Django
            user = User.objects.create_user(**validated_data)

            # 2. Creamos la familia vinculada a este nuevo dueño
            Family.objects.create(name=family_name, owner=user)

        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer mínimo de solo-lectura para exponer datos del usuario en `me`."""

    class Meta:
        model = User
        fields = ["id", "username", "email"]
        read_only_fields = ["id", "username", "email"]
