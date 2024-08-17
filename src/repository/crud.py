from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.repository.exceptions import DatabaseError
from src.schemas import User as UserSchema
from .models import User


def get_all_users(db: Session) -> list[User]:
    try:
        return db.query(User).all()
    except SQLAlchemyError as error:
        raise DatabaseError(error)


def get_user_by_id(db: Session, id: int) -> User:
    try:
        return db.query(User).filter(User.id == id).first()
    except SQLAlchemyError as error:
        raise DatabaseError(error)


def get_user_by_discord_nickname(db: Session, discord_nickname: str) -> User:
    try:
        return db.query(User).filter(User.discord_nickname == discord_nickname).first()
    except SQLAlchemyError as error:
        raise DatabaseError(error)


def create_user(db: Session, user: UserSchema) -> User:
    try:
        db_user = User(discord_nickname=user.discord_nickname, birthday=user.birthday)
        db.add(User)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as error:
        raise DatabaseError(error)


def update_user(db: Session, user: UserSchema) -> User:
    try:
        db_user = get_user_by_id(db, user.id)
        db_user.discord_nickname = user.discord_nickname  # type: ignore
        db_user.birthday = user.birthday  # type: ignore
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as error:
        raise DatabaseError(error)


def delete_user(db: Session, id: int) -> User:
    try:
        db_user = get_user_by_id(db, id)
        db.delete(db_user)
        db.commit()
        return db_user
    except SQLAlchemyError as error:
        raise DatabaseError(error)
