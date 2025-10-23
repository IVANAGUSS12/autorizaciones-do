
import os
from urllib.parse import unquote
from django.http import HttpResponseRedirect, Http404, FileResponse
from django.core.files.storage import default_storage

def _bucket():
    return (
        os.getenv("SPACES_BUCKET")
        or os.getenv("SPACES_NAME")
        or os.getenv("AWS_STORAGE_BUCKET_NAME")
    )

def _endpoint():
    return os.getenv("SPACES_ENDPOINT") or os.getenv("AWS_S3_ENDPOINT_URL")

def _region():
    return os.getenv("SPACES_REGION") or os.getenv("AWS_REGION") or "us-east-1"

def _client():
    try:
        import boto3  # type: ignore
    except Exception:
        return None
    ak = os.getenv("SPACES_KEY") or os.getenv("AWS_ACCESS_KEY_ID")
    sk = os.getenv("SPACES_SECRET") or os.getenv("AWS_SECRET_ACCESS_KEY")
    ep = _endpoint()
    if not (ak and sk and ep):
        return None
    session = boto3.session.Session()
    return session.client(
        "s3",
        region_name=_region(),
        endpoint_url=ep,
        aws_access_key_id=ak,
        aws_secret_access_key=sk,
    )

def _try_presign(client, bucket, key):
    try:
        return client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=300,
            HttpMethod="GET",
        )
    except Exception:
        return None

def media_signed_view(request, key: str):
    original = unquote(key)

    # Probar variaciones comunes (con/sin 'media/' y leading slash)
    candidates = [original]
    if original.startswith("/"):
        candidates.append(original.lstrip("/"))
    if original.startswith("media/"):
        candidates.append(original[len("media/"):])
    if not original.startswith("media/"):
        candidates.append("media/" + original)

    bucket = _bucket()
    client = _client()
    if client and bucket:
        for k in candidates:
            url = _try_presign(client, bucket, k)
            if url:
                return HttpResponseRedirect(url)

    for k in candidates:
        try:
            url = default_storage.url(k)
            if url:
                return HttpResponseRedirect(url)
        except Exception:
            pass

    for k in candidates:
        try:
            path = default_storage.path(k)
            return FileResponse(open(path, "rb"))
        except Exception:
            pass

    raise Http404("The requested resource was not found on this server.")

