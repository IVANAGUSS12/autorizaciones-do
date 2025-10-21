from rest_framework import serializers
from .models import Patient, Attachment


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"
        # ajustá estos nombres si en tu modelo se llaman distinto
        read_only_fields = ["id", "created_at", "updated_at"]


class AttachmentSerializer(serializers.ModelSerializer):
    # Campos derivados para ayudar al panel:
    # - url: URL directa (puede ser None si el bucket es privado)
    # - key: clave interna en el bucket (para firmar con /v1/media-signed/<key>)
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
            "url",   # derivado
            "key",   # derivado
            "created_at",
        ]
        read_only_fields = ["id", "url", "key", "created_at"]

    def get_url(self, obj):
        try:
            # django-storages expone .url si AWS_QUERYSTRING_AUTH lo permite
            return obj.file.url
        except Exception:
            return None

    def get_key(self, obj):
        try:
            # nombre/key interna en el bucket (p.ej. 'attachments/2/orden.pdf')
            return obj.file.name
        except Exception:
            return None
