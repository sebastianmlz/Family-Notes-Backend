from uuid import UUID
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError, PermissionDenied
from ..models import Note
from ..serializers import NoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # 1. Obtenemos el ID del perfil desde la URL (?profile_id=...)
        profile_id = self.request.query_params.get("profile_id")

        # 2. Si el frontend no manda un ID, devolvemos una lista vacía.
        # Esto cumple tu regla: "cada perfil ve sus propias notas".
        if profile_id is None:
            return Note.objects.none()

        try:
            UUID(profile_id)
        except ValueError:
            raise ValidationError({"profile_id": "Invalid UUID."})

        # 3. Filtro de Seguridad y Privacidad:
        # - Filtramos por el ID del perfil solicitado.
        # - VALIDAMOS que el perfil pertenezca a la familia del usuario actual.
        return Note.objects.filter(
            profile_id=profile_id, profile__family=user.family_account
        ).select_related("profile", "profile__family")

    def perform_create(self, serializer):
        profile = serializer.validated_data["profile"]
        if profile.family.owner_id != self.request.user.id:
            raise PermissionDenied("Cannot create note for that profile.")
        serializer.save()

    def perform_update(self, serializer):
        profile = serializer.validated_data.get("profile", serializer.instance.profile)
        if profile.family.owner_id != self.request.user.id:
            raise PermissionDenied("Profile not allowed.")
        serializer.save()
