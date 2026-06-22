import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from core.client import RedisClient, create_redis_client
from core.identity import extract_identity
from core.policy import get_policy, seed_default_policies
from core.schemas import MetricsPolicy, ReadPolicy, UpdatePolicy
from core.utils import BUCKET_SCRIPT


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # Create redis client and attach it to FastAPI app instance
    redis_client = await create_redis_client()
    app.state.redis = redis_client

    # Load the Lua script into Redis and store the SHA for later use
    sha = await redis_client.script_load(BUCKET_SCRIPT)
    app.state.bucket_script_sha = sha

    # Initialize default policies
    await seed_default_policies(redis_client)

    try:
        yield
    finally:
        # Shutdown
        await redis_client.aclose()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def main():
    return {"message": "Hello from rate-limiter!"}


@app.get("/healthz")
def health():
    return {"status": "OK"}


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """
    Extract identity, check policies on every dimension,
    rate limit based on request usage
    """
    # Skip rate limiting for health/meta routes
    SKIP_PATHS = {"/healthz", "/docs", "/openapi.json"}
    if request.url.path in SKIP_PATHS or request.url.path.startswith("/admin/"):
        return await call_next(request)

    identity = extract_identity(request)
    redis = request.app.state.redis
    sha = request.app.state.bucket_script_sha
    now = time.time()

    dimensions = [
        ("api_key", identity.api_key),
        ("ip", identity.ip),
        ("tenant_id", identity.tenant_id),
    ]

    for dimension, identity_id in dimensions:
        metrics = await get_policy(dimension, identity_id, redis)
        capacity = metrics.capacity
        refill_rate = capacity / metrics.window
        key = f"rl:{dimension}:{identity_id}"

        result = await redis.evalsha(sha, 1, key, capacity, refill_rate, now)
        if result[0] == 0:  # denied
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "dimension": dimension,
                    "retry_after": 1,
                },
                headers={"Retry-After": "1"},
            )

    response = await call_next(request)
    return response


@app.put("/admin/policy/{dimension}/{identity_id}", response_model=ReadPolicy)
async def update_policy(
    dimension: str,
    identity_id: str,
    metrics: UpdatePolicy,
    redis: RedisClient,
):
    """
    Update rate limiting policies
    """
    if dimension not in ("api_key", "ip", "tenant_id"):
        raise HTTPException(
            status_code=400,
            detail="Invalid parameter:Dimension must be 'api_key', 'ip' or 'tenant_id'",
        )

    key = f"policy:{dimension}:{identity_id}"
    await redis.hset(
        key, mapping={"capacity": metrics.capacity, "window": metrics.window}
    )

    return ReadPolicy(capacity=metrics.capacity, window=metrics.window, key=key)


@app.get("/admin/policy/{dimension}/{identity_id}", response_model=MetricsPolicy)
async def read_policy(dimension: str, identity_id: str, redis: RedisClient):
    """
    Get policy metrics
    """
    if dimension not in ("api_key", "ip", "tenant_id"):
        raise HTTPException(
            status_code=400,
            detail="Invalid parameter:Dimension must be 'api_key', 'ip' or 'tenant_id'",
        )

    metrics = await get_policy(dimension, identity_id, redis)
    return metrics
