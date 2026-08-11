from __future__ import annotations
from time import perf_counter
from uuid import uuid4
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.metrics import metrics
from app.core.rate_limit import rate_limiter

MAX_BODY_BYTES = 64 * 1024

async def request_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid4())
    request.state.request_id = request_id

    client = request.client.host if request.client else "unknown"
    if request.url.path not in {"/health", "/health/live", "/health/ready", "/metrics"}:
        if not rate_limiter.allow(client):
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded", "request_id": request_id},
                headers={"Retry-After": "60", "X-Request-ID": request_id},
            )

    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > MAX_BODY_BYTES:
        return JSONResponse(
            status_code=413,
            content={"detail": "Request body too large", "request_id": request_id},
            headers={"X-Request-ID": request_id},
        )

    started = perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        metrics.observe_request((perf_counter() - started) * 1000, 500)
        raise

    metrics.observe_request((perf_counter() - started) * 1000, response.status_code)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    return response
