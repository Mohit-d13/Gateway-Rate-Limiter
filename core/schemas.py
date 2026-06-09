from dataclasses import dataclass

from pydantic import BaseModel, Field, field_validator


@dataclass
class Identity:
    api_key: str
    ip: str
    tenant_id: str


class BasePolicy(BaseModel):
    dimension: str
    identity_id: str

    @field_validator("dimension")
    def check_dimensions(cls, value):
        if value not in ("api_key", "ip", "tenant_id"):
            raise ValueError(
                "Invalid: Dimension must be 'api_key', 'ip', or 'tenant_id'"
            )
        return value


class UpdatePolicy(BaseModel):
    capacity: int = Field(gt=1, le=1000)
    window: int = Field(gt=1, le=3600)


class MetricsPolicy(BaseModel):
    capacity: int
    window: int


class ReadPolicy(MetricsPolicy):
    key: str
