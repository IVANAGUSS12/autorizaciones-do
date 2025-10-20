from rest_framework import serializers
from .models import Patient, Attachment

class AttachmentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = ["id","patient","kind","name","file","url","created_at"]
        read_only_fields = ["id","url","created_at"]

    def get_url(self, obj):
        try:
            return obj.file.url
        except Exception:
            return None

class PatientSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = [
            "id","nombre","dni","email","telefono","cobertura","medico",
            "observaciones","fecha_cx","sector_code","estado","created_at",
            "attachments"
        ]
        read_only_fields = ["id","created_at","attachments"]
