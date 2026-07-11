from sqlmodel import SQLModel


class UserCreate(SQLModel):
    name: str
    email: str
    password: str
    role_id: int
