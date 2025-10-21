from django.http import JsonResponse

def health(request):
    """
    Endpoint simple para los health checks de DigitalOcean.
    Devuelve siempre 200 OK si el servidor está corriendo.
    """
    return JsonResponse({"status": "ok"})
