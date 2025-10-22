from rest_framework import serializers
from .models import Patient, Attachment


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class AttachmentSerializer(serializers.ModelSerializer):
    # devolvemos solo key; url = None para evitar tocar storage.url (evita 500)
    url = serializers.SerializerMethodField()
    key = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = [
            "id",
            "patient",
            "kind",
            "name",
            "file",
            "url",
            "key",
            "created_at",
        ]
        read_only_fields = ["id", "url", "key", "created_at"]

    def get_url(self, obj):
        # No usamos obj.file.url (si el bucket es privado puede tirar excepción)
        return None

    def get_key(self, obj):
        try:
            f = getattr(obj, "file", None)
            if not f:
                return None
            return f.name  # p.ej. 'attachments/3/orden_123.pdf'
        except Exception:
            return None
