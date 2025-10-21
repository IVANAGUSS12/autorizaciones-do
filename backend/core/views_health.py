from django.http import JsonResponse

def health(request):
    """
    Endpoint simple para readiness/liveness.
    Devuelve 200 siempre que Django esté arriba.
    """
    return JsonResponse({"status": "ok"})
