from rest_framework import serializers
from .models import Patient, Attachment




class PatientSerializer(serializers.ModelSerializer):
class Meta:
model = Patient
fields = "__all__"
read_only_fields = ["id", "created_at", "updated_at"]




class AttachmentSerializer(serializers.ModelSerializer):
url = serializers.SerializerMethodField()
key = serializers.SerializerMethodField() # ⬅️ clave interna del objeto en Spaces


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
# URL directa (puede ser None si el bucket es privado)
try:
return obj.file.url
except Exception:
return None


def get_key(self, obj):
# Nombre/key interna en el bucket (p.ej. 'attachments/2/orden.pdf')
try:
return obj.file.name
except Exception:
return None
