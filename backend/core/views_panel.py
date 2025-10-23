from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.conf import settings
from pathlib import Path
import json

def panel_index(request):
    return render(request, "panel.html")

def qr_index(request):
    return render(request, "qr.html")

def qr_gracias(request):
    return render(request, "gracias.html")

def qr_i(request):
    """
    Devuelve el JSON que usa el QR para combos (coberturas, médicos, sectores).
    Lee core/static/qr/i.json si existe; si no, devuelve estructura vacía.
    """
    path = Path(settings.BASE_DIR) / "core" / "static" / "qr" / "i.json"
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return JsonResponse(data, safe=False)
        except Exception:
            # JSON inválido → que se note en consola del browser
            raise Http404("i.json inválido")
    return JsonResponse({"coverages": [], "doctors": [], "sectors": []})
