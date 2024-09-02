class DatabaseError(Exception):
    def __init__(self, message) -> None:
        super().__init__(f"Database error: {message}")


class NicknameAlreadyExistsError(DatabaseError):
    def __init__(self, nickname) -> None:
        super().__init__(f"Nickname {nickname} already exists")


class UserNotFoundError(DatabaseError):
    def __init__(self, param) -> None:
        super().__init__(f"User {param} not found")
