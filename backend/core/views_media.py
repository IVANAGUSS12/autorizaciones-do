import os
import boto3
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.views.decorators.http import require_GET

SPACES_KEY = os.getenv("SPACES_KEY")
SPACES_SECRET = os.getenv("SPACES_SECRET")
SPACES_REGION = os.getenv("SPACES_REGION", "sfo3")
SPACES_ENDPOINT = os.getenv("SPACES_ENDPOINT", "https://sfo3.digitaloceanspaces.com")
SPACES_NAME = os.getenv("SPACES_NAME")  # nombre exacto del bucket

_session = boto3.session.Session(
    aws_access_key_id=SPACES_KEY,
    aws_secret_access_key=SPACES_SECRET,
    region_name=SPACES_REGION,
)
_s3 = _session.client("s3", endpoint_url=SPACES_ENDPOINT)


@require_GET
def media_signed(request, object_key: str):
    """
    Genera URL pre-firmada (5 min) para visualizar/descargar en Spaces.
    Mantiene bucket privado y evita problemas de CORS/público.
    """
    if not object_key:
        raise Http404("Missing object key")
    if not SPACES_NAME:
        return HttpResponseForbidden("Bucket no configurado")

    try:
        url = _s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": SPACES_NAME,
                "Key": object_key,
                "ResponseContentDisposition": "inline",
            },
            ExpiresIn=300,
        )
    except Exception as e:
        return HttpResponseForbidden(f"Error: {e}")

    return HttpResponseRedirect(url)
