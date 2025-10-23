
from rest_framework import serializers
from .models import Patient, Attachment

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

class AttachmentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    key = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = [
            "id", "patient", "kind", "name",
            "file",    # write-only
            "url", "key", "created_at",
        ]
        read_only_fields = ["id", "url", "key", "created_at"]
        extra_kwargs = {"file": {"write_only": True}}

    def get_url(self, obj):
        return None

    def get_key(self, obj):
        f = getattr(obj, "file", None)
        return getattr(f, "name", None) if f else None
