from datetime import date

from pydantic import BaseModel


class User(BaseModel):
    id: int
    discord_nickname: str
    birthday: date

    class Config:
        orm_mode = True
