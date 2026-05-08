from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import NoteViewSet

router = DefaultRouter()
router.register(r"notes", NoteViewSet, basename="note")

urlpatterns = [path("", include(router.urls))]
