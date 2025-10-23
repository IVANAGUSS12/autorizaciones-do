from django.http import JsonResponse
from .models import Patient, Attachment

# Clonan la respuesta de /v1/patients/ y /v1/attachments/ (para no tocar el front).

def patients_json(request):
    qs = Patient.objects.all().order_by("-created_at").values(
        "id", "nombre", "dni", "email", "telefono", "cobertura", "medico",
        "observaciones", "fecha_cx", "sector_code", "estado", "created_at"
    )
    return JsonResponse(list(qs), safe=False)

def attachments_json(request):
    qs = Attachment.objects.all().order_by("-created_at")
    data = []
    for a in qs:
        data.append({
            "id": a.id,
            "patient": a.patient_id,
            "kind": a.kind,
            "name": getattr(a, "name", "") or "",
            "url": None,
            "key": getattr(getattr(a, "file", None), "name", None),
            "created_at": a.created_at,
        })
    return JsonResponse(data, safe=False)
