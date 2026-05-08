from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from ..models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # 1. Definimos los campos que el frontend necesita ver o enviar
        fields = ["id", "family", "name", "age", "pin", "is_admin", "created_at"]

        # 2. SEGURIDAD: Metadata que el usuario NO puede manipular
        read_only_fields = ["id", "family", "created_at"]

        # 3. SEGURIDAD: El PIN es ultra sensible. Solo entra, nunca sale.
        extra_kwargs = {"pin": {"write_only": True}}

    def validate_pin(self, value):
        # 4. REGLA DE NEGOCIO: Validamos que el PIN sea de exactamente 4 o 6 números
        if not value.isdigit() or len(value) not in [4, 6]:
            raise serializers.ValidationError("The PIN must be exactly 4 or 6 digits.")
        return value

    def validate_age(self, value):
        if value < 0 or value > 120:
            raise serializers.ValidationError("Age must be between 0 and 120.")
        return value

    def create(self, validated_data):
        # 5. SEGURIDAD: Hasheamos el PIN antes de guardarlo en NeonDB
        validated_data["pin"] = make_password(validated_data["pin"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # 6. SEGURIDAD: Si el usuario cambia su PIN, hay que hashear el nuevo
        if "pin" in validated_data:
            validated_data["pin"] = make_password(validated_data["pin"])
        return super().update(instance, validated_data)
