from rest_framework import viewsets, permissions
from ..models import Family
from ..serializers import FamilySerializer


class FamilyViewSet(viewsets.ModelViewSet):
    serializer_class = FamilySerializer
    # 1. SEGURIDAD: Solo usuarios autenticados por Django entran aquí
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        FILTRADO SEGURO:
        Un usuario SOLO debe poder ver la familia a la que pertenece.
        """
        # Suponiendo que luego añadiremos un campo 'owner' o similar a Family
        # Por ahora, si no hay filtro, un hacker podría ver TODAS las familias.
        # Como estamos en desarrollo, filtraremos por el contexto del usuario:
        return Family.objects.filter(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        CALIDAD: No permitimos borrar una familia si no eres el dueño.
        """
        self.get_object()
        return super().destroy(request, *args, **kwargs)
