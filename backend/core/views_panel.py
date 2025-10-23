from django.http import FileResponse, Http404
from django.conf import settings
from pathlib import Path

def _safe_file_response(path: Path):
    if not path.exists() or not path.is_file():
        raise Http404("Archivo no encontrado.")
    # FileResponse ya pone Content-Type text/html por extensión (según servidor);
    # si quisieras forzar: FileResponse(..., content_type="text/html")
    return FileResponse(open(path, "rb"))

def panel_index(request):
    html_path = Path(settings.BASE_DIR) / "core" / "static" / "panel" / "index.html"
    return _safe_file_response(html_path)

def qr_index(request):
    html_path = Path(settings.BASE_DIR) / "core" / "static" / "qr" / "index.html"
    return _safe_file_response(html_path)
