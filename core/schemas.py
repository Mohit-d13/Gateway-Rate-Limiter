from dataclasses import dataclass

from pydantic import BaseModel, Field


@dataclass
class Identity:
    api_key: str
    ip: str
    tenant_id: str


class UpdatePolicy(BaseModel):
    capacity: int = Field(gt=1, le=1000)
    window: int = Field(gt=1, le=3600)


class MetricsPolicy(BaseModel):
    capacity: int
    window: int


class ReadPolicy(MetricsPolicy):
    key: str
