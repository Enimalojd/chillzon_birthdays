from sqlalchemy import Date, String, Column, Integer

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    discord_nickname = Column(String, index=True)
    birthday = Column(Date)