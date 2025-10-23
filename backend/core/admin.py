from django.contrib import admin
from django.utils.html import format_html
from django.core.files.storage import default_storage
from .models import Patient, Attachment

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "dni", "cobertura", "medico", "fecha_cx", "sector_code", "estado", "created_at")
    list_filter = ("sector_code", "estado", "created_at")
    search_fields = ("nombre", "dni", "email", "telefono", "cobertura", "medico")

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "kind", "archivo", "created_at")
    list_filter = ("kind", "created_at")
    search_fields = ("patient__nombre", "patient__dni", "name", "key")

    def archivo(self, obj):
        key = getattr(obj, "key", None) or getattr(getattr(obj, "file", None), "name", None)
        if not key:
            return "-"
        try:
            url = default_storage.url(key)
            return format_html('<a href="{}" target="_blank">abrir</a>', url)
        except Exception:
            return "-"
    archivo.short_description = "Archivo"
