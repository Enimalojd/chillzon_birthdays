from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from src.users.repository.database import get_db
from src.users.repository.exceptions import (
    NicknameAlreadyExistsError,
    UserNotFoundError,
)
from src.users.schemas import BaseUser, User
from src.users.schemas import (
    DelitUserResponseSchema,
    UserListResponseSchema,
    UserResponseSchema,
)
from src.users.repository.repository import UserRepository


router = APIRouter(prefix="/users", tags=["chillzone_users"])


@router.get(
    "/",
    response_model=UserListResponseSchema,
    description="Возвращает список юзеров.",
    status_code=status.HTTP_200_OK,
)
def get_users(db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    users = user_repository.get_all()
    return UserListResponseSchema(
        users=[User.model_validate(user) for user in users],
        length=len(users),
        message="Users list",
    )


@router.get(
    "/{user_id}", status_code=status.HTTP_200_OK, description="Возвращает юзера по id."
)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    try:
        user = user_repository.get_by_id(user_id)
        return UserResponseSchema(user=user, message="User info")
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


@router.get(
    "/by_discord_nickname/{discord_nickname}",
    status_code=status.HTTP_200_OK,
    description="Возвращает юзера по никнейму дискорда.",
)
def get_user_by_discord_nickname(discord_nickname: str, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    try:
        user = user_repository.get_by_discord_nickname(discord_nickname)
        return UserResponseSchema(user=user, message="User info")
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Эндпоинт создаёт нового юзера. Если юзер с данными никнеймом уже существует, то возращается 400 ошибка.",
)
def create_user(
    discord_nickname: str = Query(title="Discord nickname"),
    birthday: date = Query(default=date.today()),
    name: str = Query(title="User name"),
    db: Session = Depends(get_db),
):
    user_repository = UserRepository(db)
    user_data = BaseUser(
        discord_nickname=discord_nickname, birthday=birthday, name=name
    )
    try:
        user = user_repository.create(user_data)
        return UserResponseSchema(message="User created", user=user)
    except NicknameAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Nickname already exists")


@router.patch(
    "/{user_id}", status_code=status.HTTP_201_CREATED, description="Обновляет юзера."
)
def update_user(user: User, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    try:
        updated_user = user_repository.update(user)
        return UserResponseSchema(message="User updated", user=updated_user)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


@router.delete(
    "/{user_id}", status_code=status.HTTP_204_NO_CONTENT, description="Удаляет юзера."
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    try:
        user_repository.delete(user_id)
        return DelitUserResponseSchema(message=f"User with id {user_id} deleted")
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
