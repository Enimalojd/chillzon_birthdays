from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

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


T = TypeVar("T")


class AbstractRepository(ABC, Generic[T]):
    def __init__(self, db: Session):
        self.db = db

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> T:
        pass

    @abstractmethod
    def create(self, entity: T) -> T:
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass


class UserRepository(AbstractRepository[UserOrm]):
    def __init__(self, db: Session):
        super().__init__(db)

    def get_all(self) -> List[UserOrm]:
        try:
            return self.db.query(UserOrm).all()
        except SQLAlchemyError as error:
            raise DatabaseError(error)

    def get_by_id(self, id: int) -> UserOrm:
        try:
            user = self.db.query(UserOrm).filter(UserOrm.id == id).first()
            if not user:
                raise UserNotFoundError(f"User with id {id} not found")
            return user
        except SQLAlchemyError as error:
            raise DatabaseError(error)

    def get_by_discord_nickname(self, discord_nickname: str) -> UserOrm:
        try:
            user = (
                self.db.query(UserOrm)
                .filter(UserOrm.discord_nickname == discord_nickname)
                .first()
            )
            if not user:
                raise UserNotFoundError(
                    f"User with discord nickname {discord_nickname} not found"
                )
            return user
        except SQLAlchemyError as error:
            raise DatabaseError(error)

    def create(self, user: BaseUser) -> UserOrm:
        try:
            db_user = UserOrm(
                discord_nickname=user.discord_nickname,
                birthday=user.birthday,
                name=user.name,
            )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            raise NicknameAlreadyExistsError(user.discord_nickname)

    def update(self, user: UserSchema) -> UserOrm:
        try:
            db_user = self.get_by_id(user.id)
            db_user.discord_nickname = user.discord_nickname
            db_user.birthday = user.birthday
            db_user.name = user.name
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except UnmappedInstanceError as error:
            raise UserNotFoundError(error)

    def delete(self, id: int) -> None:
        try:
            db_user = self.get_by_id(id)
            self.db.delete(db_user)
            self.db.commit()
        except UnmappedInstanceError as error:
            raise UserNotFoundError(error)
