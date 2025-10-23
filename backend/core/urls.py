from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, AttachmentViewSet, health

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'attachments', AttachmentViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/health/', health, name='health'),  # ✅ health check
]
