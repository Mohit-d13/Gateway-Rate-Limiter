from collections.abc import AsyncIterable
from unittest import mock

import fakeredis
import httpx
import pytest
import pytest_asyncio
from redis import asyncio as redis

from core.client import get_redis_client
from core.main import app


@pytest_asyncio.fixture
async def redis_client() -> AsyncIterable[redis.Redis]:
    async with fakeredis.FakeAsyncRedis() as client:
        yield client


@pytest_asyncio.fixture
async def app_client(
    redis_client: redis.Redis,
) -> AsyncIterable[httpx.AsyncClient]:
    def get_redis_override() -> redis.Redis:
        return redis_client

    transport = httpx.ASGITransport(app=app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(
        transport=transport, base_url="http://test"
    ) as app_client:
        with mock.patch.dict(
            app.dependency_overrides, {get_redis_client: get_redis_override}
        ):
            yield app_client


@pytest.mark.asyncio
async def test_read_policy(app_client: httpx.AsyncClient) -> None:
    response = await app_client.get("/admin/policy/api_key/myid")
    data = response.json()

    assert response.status_code == 200
    assert data["capacity"] == 100
    assert data["window"] == 60


@pytest.mark.asyncio
async def test_read_policy_with_invalid_parameter(
    app_client: httpx.AsyncClient,
) -> None:
    response = await app_client.get("/admin/policy/invalid/myid")

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Invalid parameter:Dimension must be 'api_key', 'ip' or 'tenant_id'"
    )


@pytest.mark.asyncio
async def test_update_policy(app_client: httpx.AsyncClient) -> None:
    response = await app_client.put(
        "/admin/policy/api_key/myid", json={"capacity": 3, "window": 60}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["capacity"] == 3
    assert data["window"] == 60
    assert data["key"] == "policy:api_key:myid"


@pytest.mark.asyncio
async def test_update_policy_with_invalid_parameter(
    app_client: httpx.AsyncClient,
) -> None:
    response = await app_client.put(
        "/admin/policy/invalid/myid", json={"capacity": 3, "window": 60}
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Invalid parameter:Dimension must be 'api_key', 'ip' or 'tenant_id'"
    )


@pytest.mark.asyncio
async def test_update_policy_with_invalid_data(
    app_client: httpx.AsyncClient,
) -> None:
    response = await app_client.put(
        "/admin/policy/invalid/myid", json={"capacity": 0, "window": 60}
    )

    assert response.status_code == 422
