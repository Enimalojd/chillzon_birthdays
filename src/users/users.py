from datetime import date
from fastapi import APIRouter, Depends, Query, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session


from src.users.repository.database import get_db
from src.users.repository import crud
from src.users.repository.exceptions import (
    NicknameAlreadyExistsError,
    UserNotFoundError,
)
from src.users.schemas import BaseResponseSchema, BaseUser, User
from src.users.schemas import (
    DelitUserResponseSchema,
    UserListResponseSchema,
    UserResponseSchema,
)


router = APIRouter(prefix="/users", tags=["chillzone_users"])


@router.get(
    "/",
    response_model=UserListResponseSchema,
    description="Возвращает список юзеров.",
    status_code=status.HTTP_200_OK,
)
def get_users(db: Session = Depends(get_db)):
    res = crud.get_all_users(db=db)
    users = [User.model_validate(user) for user in res]
    return UserListResponseSchema(users=users, message="Users list")


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    description="Возвращает юзера по id.",
    responses={
        status.HTTP_200_OK: {"model": UserResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": BaseResponseSchema},
    },
)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    res = crud.get_user_by_id(db=db, id=user_id)
    if res:
        return UserResponseSchema(user=res, message="User info")
    raise HTTPException(status_code=404, detail="User not found")


@router.get(
    "/by_discord_nickname/{discord_nickname}",
    status_code=status.HTTP_200_OK,
    description="Возвращает юзера по никнейму дискорда.",
    responses={
        status.HTTP_200_OK: {"model": UserResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": BaseResponseSchema},
    },
)
def get_user_by_discord_nickname(discord_nickname: str, db: Session = Depends(get_db)):
    res = crud.get_user_by_discord_nickname(db=db, discord_nickname=discord_nickname)
    if res:
        return UserResponseSchema(user=res, message="User info")
    raise HTTPException(status_code=404, detail="User not found")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Эндпоинт создаёт нового юзера. Если юзер с данными никнеймом уже существует, то возращается 400 ошибка.",
    responses={
        status.HTTP_201_CREATED: {"model": UserResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": BaseResponseSchema},
    },
)
def create_user(
    discord_nickname: str = Query(title="Discord nickname"),
    birthday: date = Query(default=date.today()),
    name: str = Query(title="User name"),
    db: Session = Depends(get_db),
):
    user_data = BaseUser(
        discord_nickname=discord_nickname, birthday=birthday, name=name
    )
    try:
        res = crud.create_user(db=db, user=user_data)
        return UserResponseSchema(message="User created", user=res)
    except NicknameAlreadyExistsError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Nickname already exists"
        )


@router.patch(
    "/{user_id}",
    status_code=status.HTTP_201_CREATED,
    description="Обновляет юзера.",
    responses={
        status.HTTP_201_CREATED: {"model": UserResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": BaseResponseSchema},
    },
)
def update_user(user: User, db: Session = Depends(get_db)):
    try:
        res = crud.update_user(db=db, user=user)
        return UserResponseSchema(message="User updated", user=res)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удаляет юзера.",
    responses={
        status.HTTP_200_OK: {"model": DelitUserResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": BaseResponseSchema},
    },
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_user(db=db, id=user_id)
        return DelitUserResponseSchema(message="User with id {user_id} deleted")
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
