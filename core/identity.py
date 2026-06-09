from fastapi import Request

from core.schemas import Identity


def extract_identity(request: Request) -> Identity:
    """
    Extract identity from request Headers
    """
    api_key = (
        request.headers.get("x-api-key")
        or _extract_bearer(request.headers.get("authorization"))
        or "__no_api_key__"
    )

    ip = (
        request.headers.get("x-forwarded-for", "").split(",")[0].strip()
        or request.client.host
        or "__no_ip__"
    )

    tenant_id = request.headers.get("x-tenant-id") or "__no_tenant_id__"

    return Identity(api_key=api_key, ip=ip, tenant_id=tenant_id)


def _extract_bearer(auth_header: str | None) -> str | None:
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:].strip()
    return None
