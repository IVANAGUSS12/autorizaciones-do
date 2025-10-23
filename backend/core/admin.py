from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Patient, Attachment

class SafeClearableFileInput(ClearableFileInput):
    """
    Evita que el admin intente acceder a value.url (que explota en buckets privados).
    Simplemente no muestra el link "Currently:" y deja solo el input de archivo.
    """
    def get_context(self, name, value, attrs):
        ctx = super().get_context(name, value, attrs)
        # Forzamos a que no se muestre el bloque "initial"
        ctx["widget"]["is_initial"] = False
        ctx["widget"]["initial_text"] = ""
        # No tocamos el input; solo evitamos el render del link basado en .url
        return ctx

class AttachmentAdminForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = "__all__"
        widgets = {
            "file": SafeClearableFileInput
        }

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "last_name", "first_name", "coverage", "created_at")
    search_fields = ("last_name", "first_name", "coverage")
    list_filter = ("coverage", "created_at")
    ordering = ("-created_at",)

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    form = AttachmentAdminForm
    list_display = ("id", "patient", "kind", "name", "created_at", "media_link")
    readonly_fields = ("media_link",)
    search_fields = ("name", "patient__last_name", "patient__first_name")
    list_filter = ("kind", "created_at")
    ordering = ("-created_at",)

    def media_link(self, obj):
        """
        Link seguro vía /v1/media-signed/<key> (no usa file.url).
        """
        f = getattr(obj, "file", None)
        key = getattr(f, "name", None) if f else None
        if not key:
            return "—"
        url = f"/v1/media-signed/{key}"
        return format_html('<a href="{}" target="_blank" rel="noopener">Abrir/Descargar</a>', url)

    media_link.short_description = "Archivo"
