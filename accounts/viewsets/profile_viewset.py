from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
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

    @action(detail=True, methods=["post"], url_path="verify-pin")
    def verify_pin(self, request, pk=None):
        profile = self.get_object()
        pin = request.data.get("pin")
        if not pin:
            return Response({"error": "PIN is required"}, status=status.HTTP_400_BAD_REQUEST)

        if check_password(pin, profile.pin):
            return Response({"valid": True})
        else:
            return Response({"valid": False, "error": "Invalid PIN"}, status=status.HTTP_400_BAD_REQUEST)

