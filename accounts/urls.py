from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import UserViewSet, FamilyViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"families", FamilyViewSet, basename="family")
router.register(r"profiles", ProfileViewSet, basename="profile")

urlpatterns = [path("", include(router.urls))]
