from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Patient, Attachment
from .serializers import PatientSerializer, AttachmentSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by("-created_at")
    serializer_class = PatientSerializer
    permission_classes = [permissions.AllowAny]

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all().order_by("-created_at")
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.AllowAny]

@api_view(["GET"])
def health_view(request):
    return Response({"status": "ok"})
