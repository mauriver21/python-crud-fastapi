from __future__ import annotations

from datetime import datetime, timezone
from math import ceil
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class UserBase(BaseModel):
    email: str
    first_name: str | None = None
    last_name: str | None = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None


class User(UserBase):
    id: str = Field(default_factory=lambda: str(uuid4()))
    password: str
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)
    deleted_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class UserPagination(BaseModel):
    total_pages: int
    size: int
    page: int
    total_elements: int


class UserModelList(BaseModel):
    data: list[User]
    pagination: UserPagination


def create_user_model() -> dict[str, Any]:
    users: dict[str, User] = {}

    async def create(user: UserCreate) -> User:
        data = User(**user.model_dump())
        users[data.id] = data
        return data

    async def read(user_id: str) -> User | None:
        return users.get(user_id)

    async def find_by_email(email: str) -> User | None:
        for user in users.values():
            if user.email == email and user.deleted_at is None:
                return user
        return None

    async def update(user_id: str, updates: UserUpdate) -> User | None:
        current_user = users.get(user_id)
        if current_user is None:
            return None

        update_data = updates.model_dump(exclude_unset=True)
        updated_user = current_user.model_copy(
            update={**update_data, "updated_at": _utc_now()}
        )
        users[user_id] = updated_user
        return updated_user

    async def logical_delete(user_id: str) -> User | None:
        current_user = users.get(user_id)
        if current_user is None:
            return None

        deleted_user = current_user.model_copy(update={"deleted_at": _utc_now()})
        users[user_id] = deleted_user
        return deleted_user

    async def list_users(page: int = 0, page_size: int = 10) -> UserModelList:
        active_users = [user for user in users.values() if user.deleted_at is None]
        offset = page * page_size
        data = active_users[offset : offset + page_size]
        total_elements = len(active_users)
        total_pages = ceil(total_elements / page_size) if page_size > 0 else 0

        return UserModelList(
            data=data,
            pagination=UserPagination(
                total_pages=total_pages,
                size=page_size,
                page=page,
                total_elements=total_elements,
            ),
        )

    return {
        "create": create,
        "read": read,
        "find_by_email": find_by_email,
        "update": update,
        "delete": logical_delete,
        "list": list_users,
    }
