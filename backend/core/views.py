from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from .models import Patient, Attachment
from .serializers import PatientSerializer, AttachmentSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by("-created_at")
    serializer_class = PatientSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        # basic filters expected by your front-end
        q = self.request.query_params
        cov = q.get("cobertura") or ""
        est = q.get("estado") or ""
        med = q.get("medico") or ""
        sector_code = q.get("sector__code") or q.get("sector") or ""

        if cov: qs = qs.filter(cobertura=cov)
        if est: qs = qs.filter(estado=est)
        if med: qs = qs.filter(medico=med)
        if sector_code: qs = qs.filter(sector_code=sector_code)

        return qs

class AttachmentViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = Attachment.objects.all().order_by("-created_at")
    serializer_class = AttachmentSerializer
    parser_classes = (MultiPartParser, FormParser)
