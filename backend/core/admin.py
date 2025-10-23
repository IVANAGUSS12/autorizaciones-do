from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Patient, Attachment

def _get_first_attr(obj, names, default="—"):
    for n in names:
        if hasattr(obj, n):
            val = getattr(obj, n)
            if val not in (None, ""):
                return val
    return default

class SafeClearableFileInput(ClearableFileInput):
    def get_context(self, name, value, attrs):
        ctx = super().get_context(name, value, attrs)
        ctx["widget"]["is_initial"] = False
        ctx["widget"]["initial_text"] = ""
        return ctx

class AttachmentAdminForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = "__all__"
        widgets = {"file": SafeClearableFileInput}

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "patient_name", "patient_coverage", "created_at")
    search_fields = ("id",)
    list_filter = ("created_at",)
    ordering = ("-created_at",)

    def patient_name(self, obj):
        full = _get_first_attr(obj, ["full_name", "nombre_completo", "name"])
        if full != "—":
            return full
        last_ = _get_first_attr(obj, ["last_name", "apellido", "apellido_paciente"], "")
        first_ = _get_first_attr(obj, ["first_name", "nombre", "nombre_paciente"], "")
        combo = f"{last_}, {first_}".strip().strip(",")
        return combo or "—"
    patient_name.short_description = "Paciente"

    def patient_coverage(self, obj):
        return _get_first_attr(obj, ["coverage", "obra_social", "cobertura", "plan"], "—")
    patient_coverage.short_description = "Cobertura"

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    form = AttachmentAdminForm
    list_display = ("id", "patient", "kind", "name", "created_at", "media_link")
    readonly_fields = ("media_link",)
    search_fields = ("name",)
    list_filter = ("kind", "created_at")
    ordering = ("-created_at",)

    def media_link(self, obj):
        f = getattr(obj, "file", None)
        key = getattr(f, "name", None) if f else None
        if not key:
            return "—"
        # dejamos que el browser encodee; el view hará unquote al recibirla
        url = f"/v1/media-signed/{key}"
        return format_html('<a href="{}" target="_blank" rel="noopener">Abrir/Descargar</a>', url)
    media_link.short_description = "Archivo"
