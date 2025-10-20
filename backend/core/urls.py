from django.urls import path, include
from rest_framework import routers
from .views import PatientViewSet, AttachmentViewSet

router = routers.DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patient")
router.register(r"attachments", AttachmentViewSet, basename="attachment")

urlpatterns = [
    path("", include(router.urls)),
]
