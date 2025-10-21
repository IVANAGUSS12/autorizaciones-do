from django.http import Http404, HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage

def _serve_static_html(path: str) -> HttpResponse:
    # lee el HTML desde los estáticos recolectados por collectstatic
    try:
        with staticfiles_storage.open(path) as f:
            data = f.read()
    except Exception:
        raise Http404(f"No se encontró {path}")
    return HttpResponse(data, content_type="text/html; charset=utf-8")

def panel_index(request):
    # sirve core/static/panel/index.html → /panel/
    return _serve_static_html("panel/index.html")

def qr_index(request):
    # sirve core/static/qr/index.html → /qr/
    return _serve_static_html("qr/index.html")
