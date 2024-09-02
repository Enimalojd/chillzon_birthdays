import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from src.users.repository.repository import UserRepository
from src.users.schemas import BaseUser
from src.users.repository.exceptions import (
    UserNotFoundError,
    NicknameAlreadyExistsError,
)
from src.users.repository.models import UserOrm


@pytest.fixture
def db_session() -> MagicMock:
    return MagicMock(spec=Session)


@pytest.fixture
def user_repository(db_session: MagicMock) -> UserRepository:
    return UserRepository(db_session)


def test_get_all_users(user_repository: UserRepository, db_session: MagicMock):
    db_session.query().all.return_value = [
        UserOrm(
            id=1, discord_nickname="testnick", birthday="2000-01-01", name="Test User"
        )
    ]

    users = user_repository.get_all()

    assert len(users) == 1
    assert users[0].discord_nickname == "testnick"


def test_get_user_by_id(user_repository: UserRepository, db_session: MagicMock):
    db_session.query().filter().first.return_value = UserOrm(
        id=1, discord_nickname="testnick", birthday="2000-01-01", name="Test User"
    )

    user = user_repository.get_by_id(1)

    assert user.discord_nickname == "testnick"


def test_get_user_by_id_not_found(
    user_repository: UserRepository, db_session: MagicMock
):
    db_session.query().filter().first.return_value = None

    with pytest.raises(UserNotFoundError):
        user_repository.get_by_id(1)


def test_create_user(user_repository: UserRepository, db_session: MagicMock):
    user_data = BaseUser(
        discord_nickname="newnick", birthday="2000-01-01", name="New User"  # type: ignore
    )
    db_session.add.side_effect = None
    db_session.commit.side_effect = None

    user = user_repository.create(user_data)

    assert user.discord_nickname == "newnick"
    db_session.add.assert_called_once()


def test_create_user_nickname_exists(
    user_repository: UserRepository, db_session: Session
):
    db_session.add.side_effect = NicknameAlreadyExistsError("newnick")

    user_data = BaseUser(
        discord_nickname="newnick", birthday="2000-01-01", name="New User"  # type: ignore
    )

    with pytest.raises(NicknameAlreadyExistsError):
        user_repository.create(user_data)


def test_update_user(user_repository: UserRepository, db_session: MagicMock):
    user_data = UserOrm(
        id=1, discord_nickname="updatednick", birthday="2000-01-01", name="Updated User"
    )
    db_session.query().filter().first.return_value = user_data

    updated_user = user_repository.update(user_data)

    assert updated_user.discord_nickname == "updatednick"
    db_session.commit.assert_called_once()


def test_delete_user(user_repository: UserRepository, db_session: MagicMock):
    user_data = UserOrm(
        id=1, discord_nickname="testnick", birthday="2000-01-01", name="Test User"
    )
    db_session.query().filter().first.return_value = user_data

    user_repository.delete(1)

    db_session.delete.assert_called_once_with(user_data)
    db_session.commit.assert_called_once()
