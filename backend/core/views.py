from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Patient, Attachment
from .serializers import PatientSerializer, AttachmentSerializer

# ✅ Ruta de salud para DigitalOcean
@csrf_exempt
def health(request):
    return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by("-created_at")
    serializer_class = PatientSerializer
    permission_classes = [permissions.AllowAny]


@method_decorator(csrf_exempt, name="dispatch")
class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all().order_by("-created_at")
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        data = request.data
        if not data.get("patient"):
            return JsonResponse({"error": "Patient is required"}, status=400)
        if "file" not in data or not data["file"]:
            return JsonResponse({"error": "File is required"}, status=400)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=201)
