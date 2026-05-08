from rest_framework import serializers
from django.contrib.auth.hashers import make_password  # Importante para seguridad
from ..models import Family


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ["id", "name", "password", "created_at", "updated_at"]

        # 1. SEGURIDAD: Impedimos que los metadatos sean modificables vía API
        read_only_fields = ["id", "created_at", "updated_at"]

        # 2. SEGURIDAD: La clave entra para crear, pero NUNCA sale en un GET
        extra_kwargs = {"password": {"write_only": True}}

    def validate_name(self, value):
        # Tu validación está bien, pero podemos ser más específicos
        if len(value) < 3:
            raise serializers.ValidationError(
                "Family name must be at least 3 characters long."
            )
        return value

    def create(self, validated_data):
        # 3. EFICIENCIA: Antes de guardar, hasheamos la contraseña
        # validated_data ya pasó por los validadores de campo
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
