from redis import asyncio as redis

from core.schemas import MetricsPolicy

DEFAULT_POLICIES = {
    "api_key": {"capacity": 100, "window": 60},
    "ip": {"capacity": 200, "window": 60},
    "tenant_id": {"capacity": 500, "window": 60},
}


async def seed_default_policies(redis_client: redis.Redis):
    """
    Initialize default policies at application startup,
    only writes if the key doesn't already exist.
    """
    for dimension, policy in DEFAULT_POLICIES.items():
        key = f"policy:{dimension}:__default__"
        exists = await redis_client.exists(key)
        if not exists:
            await redis_client.hset(key, mapping=policy)


async def get_policy(
    dimension: str, identity_id: str, redis_client: redis.Redis
) -> MetricsPolicy:
    """
    Look up policy for a specific id, or fall back to __default__ policy,
    get policies metrics like bucket capacity and time window
    """
    # Try specific policy first
    specific_key = f"policy:{dimension}:{identity_id}"
    policy = await redis_client.hgetall(specific_key)

    if not policy:
        # Fall back to default for the dimension
        default_key = f"policy:{dimension}:__default__"
        policy = await redis_client.hgetall(default_key)

    if not policy:
        # Last resort: hardcoded fallback so we never crash
        policy = DEFAULT_POLICIES.get(
            dimension, {"capacity": 100, "window": 60}
        )

    return MetricsPolicy(
        capacity=int(policy["capacity"]), window=int(policy["window"])
    )
