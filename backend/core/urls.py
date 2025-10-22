from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PatientViewSet, AttachmentViewSet, health

router = DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patients")
router.register(r"attachments", AttachmentViewSet, basename="attachments")

urlpatterns = [
    # /v1/health/
    path("health/", health, name="health"),

    # /v1/patients/  /v1/attachments/
    path("", include(router.urls)),
]
