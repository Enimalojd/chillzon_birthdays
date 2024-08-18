from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    discord_nickname: Mapped[str] = mapped_column(index=True, unique=True)
    name: Mapped[str]
    birthday: Mapped[date]
