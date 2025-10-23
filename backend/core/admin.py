from django.contrib import admin
from django.utils.html import format_html
from .models import Patient, Attachment

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "last_name", "first_name", "coverage", "created_at")
    search_fields = ("last_name", "first_name", "coverage")
    list_filter = ("coverage", "created_at")
    ordering = ("-created_at",)

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "kind", "name", "created_at", "media_link")
    readonly_fields = ("media_link",)
    search_fields = ("name", "patient__last_name", "patient__first_name")
    list_filter = ("kind", "created_at")
    ordering = ("-created_at",)

    def media_link(self, obj):
        """
        En lugar de usar file.url (que puede fallar si el bucket es privado),
        usamos nuestro endpoint /v1/media-signed/<key>.
        """
        f = getattr(obj, "file", None)
        key = getattr(f, "name", None) if f else None
        if not key:
            return "—"
        url = f"/v1/media-signed/{key}"
        return format_html('<a href="{}" target="_blank">Abrir/Descargar</a>', url)

    media_link.short_description = "Archivo"
