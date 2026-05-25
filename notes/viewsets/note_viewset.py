from uuid import UUID
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.pagination import PageNumberPagination
from ..models import Note
from ..serializers import NoteSerializer


class NotePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = NotePagination

    def get_queryset(self):
        user = self.request.user
        
        # Return all notes for profiles belonging to the user's family, ordered by newest first
        queryset = Note.objects.filter(
            profile__family=user.family_account
        ).select_related("profile", "profile__family").order_by("-created_at")

        profile_id = self.request.query_params.get("profile_id") or self.request.query_params.get("profile")
        if profile_id:
            try:
                UUID(profile_id)
                queryset = queryset.filter(profile_id=profile_id)
            except ValueError:
                raise ValidationError({"profile_id": "Invalid UUID."})

        return queryset

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

