from rest_framework import mixins, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import User
from ..serializers.user_serializer import RegisterSerializer, UserSerializer


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.none()

    def get_serializer_class(self):
        # CALIDAD: Usamos un serializer distinto según la acción
        if self.action == "create":
            return RegisterSerializer
        return UserSerializer

    def get_permissions(self):
        # SEGURIDAD: El registro es público, lo demás requiere estar logeado
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """
        REGISTRO SEGURO:
        Aquí es donde se dispara la transacción atómica que crea
        al Usuario y a la Familia al mismo tiempo.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "message": "User and Family created successfully.",
                "user_email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        """
        EFICIENCIA: Endpoint para que el frontend obtenga los datos
        del usuario que tiene la sesión iniciada.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
