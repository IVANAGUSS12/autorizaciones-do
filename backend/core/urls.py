from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PatientViewSet, AttachmentViewSet

router = DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patients")
router.register(r"attachments", AttachmentViewSet, basename="attachments")

urlpatterns = [
    path("", include(router.urls)),
    # si ya tenés /v1/health/ en otro archivo, dejalo como estaba
]
