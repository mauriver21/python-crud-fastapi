from __future__ import annotations

from datetime import datetime, timezone
from math import ceil
from typing import Any
from uuid import UUID

from sqlmodel import SQLModel, Session, create_engine, select

from config import config
from db.schema.users import User
from interfaces.UserCreate import UserCreate
from interfaces.UserModelList import UserModelList
from interfaces.UserPagination import UserPagination
from interfaces.UserUpdate import UserUpdate


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _build_database_url() -> str:
    db_config = config["db"]
    dialect = db_config["dialect"]

    if dialect == "sqlite":
        return f"sqlite:///{db_config['database']}"

    return (
        f"{dialect}://{db_config['user']}:{db_config['password']}"
        f"@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    )


def _get_engine():
    return create_engine(_build_database_url(), echo=False)


def create_user_model() -> dict[str, Any]:
    engine = _get_engine()
    SQLModel.metadata.create_all(engine)

    async def create(user: UserCreate) -> User:
        with Session(engine) as session:
            data = User(**user.model_dump())
            session.add(data)
            session.commit()
            session.refresh(data)
            return data

    async def read(user_id: str) -> User | None:
        with Session(engine) as session:
            statement = select(User).where(User.id == UUID(user_id))
            return session.exec(statement).first()

    async def find_by_email(email: str) -> User | None:
        with Session(engine) as session:
            statement = select(User).where(
                User.email == email,
                User.deleted_at.is_(None),
            )
            return session.exec(statement).first()

    async def update(user_id: str, updates: UserUpdate) -> User | None:
        with Session(engine) as session:
            statement = select(User).where(User.id == UUID(user_id))
            data = session.exec(statement).first()
            if data is None:
                return None

            for key, value in updates.model_dump(exclude_unset=True).items():
                setattr(data, key, value)

            data.updated_at = _utc_now()
            session.add(data)
            session.commit()
            session.refresh(data)
            return data

    async def logical_delete(user_id: str) -> User | None:
        with Session(engine) as session:
            statement = select(User).where(User.id == UUID(user_id))
            data = session.exec(statement).first()
            if data is None:
                return None

            data.deleted_at = _utc_now()
            session.add(data)
            session.commit()
            session.refresh(data)
            return data

    async def list_users(page: int = 0, page_size: int = 10) -> UserModelList:
        offset = page * page_size

        with Session(engine) as session:
            statement = (
                select(User)
                .where(User.deleted_at.is_(None))
                .offset(offset)
                .limit(page_size)
            )
            data = list(session.exec(statement).all())

            count_statement = select(User.id).where(User.deleted_at.is_(None))
            total_elements = len(session.exec(count_statement).all())

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
