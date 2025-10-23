
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import PatientViewSet, AttachmentViewSet, health_view
from .views_media import media_signed_view

router = DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patients")
router.register(r"attachments", AttachmentViewSet, basename="attachments")

urlpatterns = [
    path("health/", health_view, name="health"),
    path("", include(router.urls)),
    path("media-signed/<path:key>", media_signed_view, name="media-signed"),
]
