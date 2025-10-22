from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, permissions, authentication

from .models import Patient, Attachment
from .serializers import PatientSerializer, AttachmentSerializer


class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all().order_by("-created_at")
    serializer_class = PatientSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # sin sesión ⇒ sin CSRF para API pública


class AttachmentViewSet(ModelViewSet):
    """
    - GET /v1/attachments/       → lista (no se cae si falta file/url)
    - POST /v1/attachments/      → multipart (archivo)
      fields: patient (id), kind, name, file
    """
    queryset = Attachment.objects.select_related("patient").all().order_by("-created_at")
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # sin sesión ⇒ sin CSRF
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "delete", "head", "options"]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # Validamos que llegue patient y file
        if not data.get("patient"):
            return Response({"detail": "patient is required"}, status=status.HTTP_400_BAD_REQUEST)
        if "file" not in request.data or request.data.get("file") in (None, "", b""):
            return Response({"detail": "file is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
