from rest_framework import serializers
from django.core.files.storage import default_storage
from .models import Patient, Attachment

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id", "nombre", "dni", "email", "telefono", "cobertura", "medico",
            "observaciones", "fecha_cx", "sector_code", "estado", "created_at",
        ]

class AttachmentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = ["id", "patient", "kind", "name", "url", "key", "created_at"]

    def get_url(self, obj):
        # Construye URL firmada/publica a partir de obj.key via storage
        key = getattr(obj, "key", None) or getattr(getattr(obj, "file", None), "name", None)
        if not key:
            return None
        try:
            return default_storage.url(key)
        except Exception:
            return None
