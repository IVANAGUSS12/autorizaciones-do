from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Patient, Attachment


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "dni", "cobertura", "medico", "estado", "created_at")
    search_fields = ("nombre", "dni", "email")
    list_filter = ("cobertura", "estado", "medico")
    ordering = ("-created_at",)


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "kind", "name", "file_key", "open_signed", "created_at")
    search_fields = ("name", "kind", "patient__nombre")
    list_filter = ("kind",)
    ordering = ("-created_at",)

    def file_key(self, obj):
        try:
            return obj.file.name  # NUNCA usamos file.url en admin
        except Exception:
            return "-"
    file_key.short_description = "Key"

    def open_signed(self, obj):
        try:
            key = obj.file.name
        except Exception:
            key = None
        if not key:
            return "-"
        url = reverse("media_signed", args=[key])
        return format_html('<a href="{}" target="_blank">Abrir</a>', url)
    open_signed.short_description = "Vista/Descarga"
