from db.schema.users import User
from interfaces.UserPagination import UserPagination


class UserModelList:
    data: list[User]
    pagination: UserPagination
