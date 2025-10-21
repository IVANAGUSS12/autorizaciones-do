from rest_framework import viewsets, mixins
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny

from .models import Patient, Attachment
from .serializers import PatientSerializer, AttachmentSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by("-created_at")
    serializer_class = PatientSerializer

    # Público (QR) sin SessionAuth → evita CSRF
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params
        cobertura = q.get("cobertura") or ""
        estado = q.get("estado") or ""
        medico = q.get("medico") or ""
        sector_code = q.get("sector_code") or ""
        if cobertura:
            qs = qs.filter(cobertura=cobertura)
        if estado:
            qs = qs.filter(estado=estado)
        if medico:
            qs = qs.filter(medico=medico)
        if sector_code:
            qs = qs.filter(sector_code=sector_code)
        return qs


class AttachmentViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = Attachment.objects.all().order_by("-created_at")
    serializer_class = AttachmentSerializer
    parser_classes = (MultiPartParser, FormParser)

    # Público para flujo QR (sin CSRF)
    permission_classes = [AllowAny]
    authentication_classes = []

