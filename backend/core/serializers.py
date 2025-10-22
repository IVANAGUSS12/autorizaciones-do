from rest_framework import serializers
from .models import Patient, Attachment


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class AttachmentSerializer(serializers.ModelSerializer):
    # Campos calculados para el panel/QR
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
        try:
            f = getattr(obj, "file", None)
            if not f:
                return None
            # Si el storage expone URL directa, úsala
            return f.url
        except Exception:
            return None

    def get_key(self, obj):
        try:
            f = getattr(obj, "file", None)
            if not f:
                return None
            # Path interno (sirve para /v1/media-signed/<key>)
            return f.name
        except Exception:
            return None
