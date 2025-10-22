from django.http import JsonResponse
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Patient, Attachment
from .serializers import PatientSerializer, AttachmentSerializer


# /v1/health/
def health(request):
    return JsonResponse({"status": "ok"})


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by("-created_at")
    serializer_class = PatientSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # API pública (QR)


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.select_related("patient").all().order_by("-created_at")
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # API pública (QR)
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "delete", "head", "options"]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        if not data.get("patient"):
            return Response({"detail": "patient is required"}, status=status.HTTP_400_BAD_REQUEST)
        if "file" not in request.data or request.data.get("file") in (None, "", b""):
            return Response({"detail": "file is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
