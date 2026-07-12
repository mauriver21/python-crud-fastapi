from interfaces.UserCreate import UserCreate
from interfaces.UserUpdate import UserUpdate
import models.user as user_model


def list(page: int = 0, page_size: int = 10):
    try:
        return user_model.list(page, page_size)
    except Exception as error:
        raise Exception("[User repo]: Failed user listing") from error


def create(user: UserCreate):
    try:
        return user_model.create(user)
    except Exception as error:
        raise Exception("[User repo]: Failed user creation") from error


def update(id: str, user: UserUpdate):
    try:
        return user_model.update(id, user)
    except Exception as error:
        raise Exception("[User repo]: Failed user updating") from error


def logical_delete(id: str):
    try:
        return user_model.logical_delete(id)
    except Exception as error:
        raise Exception("[User repo]: Failed user removing") from error
