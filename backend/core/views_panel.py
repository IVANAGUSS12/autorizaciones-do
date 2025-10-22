from django.http import Http404, HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage

def _serve(path: str):
    try:
        with staticfiles_storage.open(path) as f:
            data = f.read()
    except Exception:
        raise Http404(path)
    return HttpResponse(data, content_type="text/html; charset=utf-8")

def panel_index(request):
    # sirve static/panel/index.html
    return _serve("panel/index.html")

def qr_index(request):
    # sirve static/qr/index.html
    return _serve("qr/index.html")
