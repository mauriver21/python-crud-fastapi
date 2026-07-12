from fastapi import HTTPException

from interfaces.UserCreate import UserCreate
from interfaces.UserUpdate import UserUpdate
import repositories.user as user_repository


def list(page: int = 0, page_size: int = 10):
    try:
        return user_repository.list(page, page_size)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


def create(user: UserCreate):
    try:
        return user_repository.create(user)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


def update(id: str, user: UserUpdate):
    try:
        return user_repository.update(id, user)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


def remove(id: str):
    try:
        return user_repository.logical_delete(id)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
