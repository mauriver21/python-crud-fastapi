from sqlmodel import SQLModel


class UserUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
