import os
from urllib.parse import quote
from django.http import HttpResponseRedirect, Http404, FileResponse
from django.core.files.storage import default_storage
from django.conf import settings

def _boto3_client_or_none():
    try:
        import boto3  # noqa
    except Exception:
        return None

    endpoint = os.getenv("SPACES_ENDPOINT") or os.getenv("AWS_S3_ENDPOINT_URL")
    key_id = os.getenv("SPACES_KEY") or os.getenv("AWS_ACCESS_KEY_ID")
    secret = os.getenv("SPACES_SECRET") or os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("SPACES_REGION") or os.getenv("AWS_REGION") or "us-east-1"

    if not (endpoint and key_id and secret):
        return None

    import boto3
    session = boto3.session.Session()
    return session.client(
        "s3",
        region_name=region,
        endpoint_url=endpoint,
        aws_access_key_id=key_id,
        aws_secret_access_key=secret,
    )

def media_signed_view(request, key: str):
    """
    GET /v1/media-signed/<path:key>
    - Si hay credenciales de Spaces, genera un presigned URL con expiración corta.
    - Si no, intenta default_storage.url(key).
    - En entorno local con FileSystemStorage, devuelve el archivo directo si existe.
    """
    # 1) Intento firmar con Spaces/S3
    bucket = os.getenv("SPACES_BUCKET") or os.getenv("AWS_STORAGE_BUCKET_NAME")
    client = _boto3_client_or_none()
    if client and bucket:
        try:
            url = client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=300,  # 5 minutos
                HttpMethod="GET",
            )
            return HttpResponseRedirect(url)
        except Exception:
            pass  # probamos siguientes caminos

    # 2) Intento url del storage (si es público o configurado)
    try:
        url = default_storage.url(key)
        if url:
            return HttpResponseRedirect(url)
    except Exception:
        pass

    # 3) Entorno local: tratamos de abrir el archivo físico
    try:
        # default_storage.path(key) sólo existe en FileSystemStorage
        path = default_storage.path(key)
        return FileResponse(open(path, "rb"))
    except Exception:
        raise Http404(f"No se pudo resolver el recurso solicitado: {quote(key)}")
