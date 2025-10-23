from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def health_check(request):
    """Readiness probe para DigitalOcean. Devuelve 200 siempre."""
    return JsonResponse({"status": "ok"}, status=200)
