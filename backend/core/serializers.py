from rest_framework import serializers
from .models import Patient, Attachment

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

class AttachmentSerializer(serializers.ModelSerializer):
    """
    Evitamos exponer file.url (que a veces dispara excepción con storage S3/Spaces).
    Subimos el archivo con 'file' (write_only) y devolvemos 'key' para usar con /v1/media-signed/<key>.
    """
    url = serializers.SerializerMethodField()
    key = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = [
            "id",
            "patient",
            "kind",
            "name",
            "file",       # queda para escritura
            "url",        # siempre None (no resolvemos .url)
            "key",        # ruta/clave dentro del bucket
            "created_at",
        ]
        read_only_fields = ["id", "url", "key", "created_at"]
        extra_kwargs = {
            "file": {"write_only": True}
        }

    def get_url(self, obj):
        # Nunca intentamos resolver storage.url acá
        return None

    def get_key(self, obj):
        f = getattr(obj, "file", None)
        if not f:
            return None
        # Devuelve la ruta tal cual quedó en el storage (p.ej. 'patients/123/orden.pdf')
        return getattr(f, "name", None)
