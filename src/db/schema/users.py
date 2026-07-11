from __future__ import annotations
from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
    )
    name: str = Field(max_length=256)
    email: str = Field(max_length=256)
    password: str = Field(max_length=256)
    role_id: int = Field(foreign_key="roles.id")
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)
    deleted_at: datetime | None = Field(default=None)
