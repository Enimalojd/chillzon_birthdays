from datetime import date

from pydantic import BaseModel


class BaseUser(BaseModel):
    discord_nickname: str
    name: str
    birthday: date

    class Config:
        orm_mode = True
        from_attributes = True


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class BaseResponseSchema(BaseModel):
    message: str


class UserResponseSchema(BaseResponseSchema):
    user: User


class UserListResponseSchema(BaseResponseSchema):
    length: int
    users: list[User]


class DelitUserResponseSchema(BaseResponseSchema):
    pass
