from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Patient, Attachment
from .serializers import PatientSerializer, AttachmentSerializer
from django.http import JsonResponse


# /v1/health/ (readiness para DigitalOcean)
def health_check(request):
    return JsonResponse({"status": "ok"})

@method_decorator(csrf_exempt, name="dispatch")   # exento de CSRF (QR/panel)
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by("-created_at")
    serializer_class = PatientSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # sin sesiones


@method_decorator(csrf_exempt, name="dispatch")   # exento de CSRF (uploads)
class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.select_related("patient").all().order_by("-created_at")
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # sin sesiones
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "delete", "head", "options"]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # Validaciones básicas para evitar 500
        if not data.get("patient"):
            return Response({"detail": "patient is required"}, status=status.HTTP_400_BAD_REQUEST)
        if "file" not in request.data or request.data.get("file") in (None, "", b""):
            return Response({"detail": "file is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
