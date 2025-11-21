import sqlite3

from src.app.logger import SecureLogger
from src.app.validation import InputValidator


class UserService:

    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.logger = SecureLogger("UserService")
        self.validator = InputValidator()
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    def get_user_by_username(self, username: str) -> dict | None:
        is_valid, error_msg = self.validator.validate_username(username)
        if not is_valid:
            self.logger.warning(f"Invalid username attempt: {error_msg}")
            raise ValueError(error_msg or "Invalid username")

        self.logger.info(f"Attempting to retrieve user: {username}")
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, username, email FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()

        if row:
            self.logger.info("User retrieved successfully")
            return {"id": row[0], "username": row[1], "email": row[2]}
        self.logger.info("User not found")
        return None

    def create_user(self, username: str, email: str) -> dict:
        is_valid, error_msg = self.validator.validate_username(username)
        if not is_valid:
            self.logger.warning(f"Invalid username in create_user: {error_msg}")
            raise ValueError(error_msg or "Invalid username")

        is_valid, error_msg = self.validator.validate_email(email)
        if not is_valid:
            self.logger.warning(f"Invalid email in create_user: {error_msg}")
            raise ValueError(error_msg or "Invalid email")

        self.logger.info(f"Attempting to create user: {username}")
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
            self.conn.commit()
            self.logger.info("User created successfully")
            return {"id": cursor.lastrowid, "username": username, "email": email}
        except sqlite3.IntegrityError as e:
            self.logger.error("Failed to create user: integrity error")
            raise ValueError(f"User with username '{username}' already exists") from e

    def close(self):
        self.conn.close()
