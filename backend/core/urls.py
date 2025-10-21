from django.urls import path,re_path, include
from rest_framework import routers
from .views import PatientViewSet, AttachmentViewSet
from .views_media import media_signed_redirect

router = routers.DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patient")
router.register(r"attachments", AttachmentViewSet, basename="attachment")

urlpatterns = [
    path("", include(router.urls)),
    re_path(r"^media-signed/(?P<path>.+)$", media_signed_redirect),
]
