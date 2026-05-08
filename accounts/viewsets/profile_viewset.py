from rest_framework import viewsets, permissions
from ..models import Profile
from ..serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(family__owner=user)

    def perform_create(self, serializer):
        user = self.request.user
        user_family = user.family_account
        serializer.save(family=user_family)
