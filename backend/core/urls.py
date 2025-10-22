from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, AttachmentViewSet, health
from .views_media import media_signed

router = DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patients")
router.register(r"attachments", AttachmentViewSet, basename="attachments")

urlpatterns = [
    path("health/", health, name="health"),
    path("media-signed/<path:object_key>", media_signed, name="media_signed"),
    path("", include(router.urls)),
]
