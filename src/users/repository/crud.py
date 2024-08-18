from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from src.users.repository.exceptions import (
    DatabaseError,
    NicknameAlreadyExistsError,
    UserNotFoundError,
)
from src.users.schemas import User as UserSchema, BaseUser
from .models import UserOrm


def get_all_users(db: Session) -> list[UserOrm]:
    try:
        return db.query(UserOrm).all()
    except SQLAlchemyError as error:
        raise DatabaseError(error)


def get_user_by_id(db: Session, id: int) -> UserOrm:
    try:
        print("Я ТУТ!!!")
        return db.query(UserOrm).filter(UserOrm.id == id).first()
    except SQLAlchemyError as error:
        raise DatabaseError(error)


def get_user_by_discord_nickname(db: Session, discord_nickname: str) -> UserOrm:
    try:
        return (
            db.query(UserOrm)
            .filter(UserOrm.discord_nickname == discord_nickname)
            .first()
        )
    except SQLAlchemyError as error:
        raise DatabaseError(error)


def create_user(db: Session, user: BaseUser) -> UserOrm:
    try:
        db_user = UserOrm(
            discord_nickname=user.discord_nickname,
            birthday=user.birthday,
            name=user.name,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        raise NicknameAlreadyExistsError(user.discord_nickname)


def update_user(db: Session, user: UserSchema) -> UserOrm:
    try:
        db_user = get_user_by_id(db, user.id)
        db_user.discord_nickname = user.discord_nickname
        db_user.birthday = user.birthday
        db.commit()
        db.refresh(db_user)
        return db_user
    except UnmappedInstanceError as error:
        raise UserNotFoundError(error)


def delete_user(db: Session, id: int) -> None:
    try:
        db_user = get_user_by_id(db, id)
        db.delete(db_user)
        db.commit()
    except UnmappedInstanceError as error:
        raise UserNotFoundError(error)
