from rest_framework import serializers
from ..models import Note


class NoteSerializer(serializers.ModelSerializer):
    # Creamos un campo extra que solo es de lectura para el nombre
    profile_name = serializers.CharField(source="profile.name", read_only=True)

    class Meta:
        model = Note
        fields = [
            "id",
            "profile",  # Aquí recibimos el UUID del perfil
            "profile_name",  # Aquí entregamos el nombre para la UX
            "title",
            "content",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("The title is too short for a note.")
        return value
