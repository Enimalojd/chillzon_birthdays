class DatabaseError(Exception):
    def __init__(self, message) -> None:
        super().__init__(f"Database error: {message}")
