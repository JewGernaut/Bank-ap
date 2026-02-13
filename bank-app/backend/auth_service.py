from __future__ import annotations

import hashlib
import os
import secrets
import sqlite3
from dataclasses import dataclass
from datetime import datetime

from .database import BankDatabase


@dataclass
class AuthResult:
    ok: bool
    message: str


class AuthService:
    def __init__(self, database: BankDatabase) -> None:
        self.database = database

    def bootstrap(self) -> None:
        self.database.initialize()
        self._ensure_demo_user()

    def authenticate(self, login: str, password: str) -> AuthResult:
        with self.database.connection() as conn:
            row = conn.execute(
                """
                SELECT
                    u.first_name,
                    u.last_name,
                    u.password_hash,
                    a.account_number,
                    c.card_number
                FROM users u
                JOIN accounts a ON a.user_id = u.id
                JOIN cards c ON c.account_id = a.id
                WHERE u.login = ?
                """,
                (login,),
            ).fetchone()

        if row is None:
            return AuthResult(False, "Пользователь с таким логином не найден.")

        if not _verify_password(password, row["password_hash"]):
            return AuthResult(False, "Неверный пароль.")

        card_tail = row["card_number"][-4:]
        message = (
            f"Добро пожаловать, {row['first_name']} {row['last_name']}\n"
            f"Л/С: {row['account_number']}\n"
            f"Карта: **** **** **** {card_tail}"
        )
        return AuthResult(True, message)

    def register_user(
        self,
        login: str,
        first_name: str,
        last_name: str,
        password: str,
    ) -> AuthResult:
        registered_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        password_hash = _hash_password(password)

        try:
            with self.database.connection() as conn:
                account_number = self._generate_unique_account_number(conn)
                card_number = self._generate_unique_card_number(conn)

                cursor = conn.execute(
                    """
                    INSERT INTO users (login, first_name, last_name, password_hash, registered_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (login, first_name, last_name, password_hash, registered_at),
                )
                user_id = cursor.lastrowid

                cursor = conn.execute(
                    """
                    INSERT INTO accounts (user_id, account_number)
                    VALUES (?, ?)
                    """,
                    (user_id, account_number),
                )
                account_id = cursor.lastrowid

                conn.execute(
                    """
                    INSERT INTO cards (account_id, card_number)
                    VALUES (?, ?)
                    """,
                    (account_id, card_number),
                )
        except sqlite3.IntegrityError as exc:
            text = str(exc)
            if "users.login" in text:
                return AuthResult(False, "Логин уже существует.")
            if "accounts.account_number" in text:
                return AuthResult(False, "Л/С уже существует.")
            if "cards.card_number" in text:
                return AuthResult(False, "Номер карты уже существует.")
            return AuthResult(False, "Ошибка регистрации в базе данных.")

        return AuthResult(True, "Пользователь зарегистрирован.")

    def _ensure_demo_user(self) -> None:
        with self.database.connection() as conn:
            row = conn.execute(
                "SELECT id FROM users WHERE login = ?",
                ("demo",),
            ).fetchone()

        if row is not None:
            return

        self.register_user(
            login="demo",
            first_name="Иван",
            last_name="Иванов",
            password="demo123",
        )

    def _generate_unique_account_number(self, conn: sqlite3.Connection) -> str:
        return self._generate_unique_number(
            conn=conn,
            table="accounts",
            column="account_number",
            prefix="40817",
            total_length=20,
        )

    def _generate_unique_card_number(self, conn: sqlite3.Connection) -> str:
        return self._generate_unique_number(
            conn=conn,
            table="cards",
            column="card_number",
            prefix="2200",
            total_length=16,
        )

    @staticmethod
    def _generate_unique_number(
        conn: sqlite3.Connection,
        table: str,
        column: str,
        prefix: str,
        total_length: int,
    ) -> str:
        random_len = total_length - len(prefix)
        if random_len <= 0:
            raise ValueError("total_length must be greater than prefix length")

        for _ in range(1000):
            value = prefix + "".join(secrets.choice("0123456789") for _ in range(random_len))
            row = conn.execute(
                f"SELECT 1 FROM {table} WHERE {column} = ? LIMIT 1",
                (value,),
            ).fetchone()
            if row is None:
                return value

        raise RuntimeError("Не удалось сгенерировать уникальный номер")


def _hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return f"{salt.hex()}${digest.hex()}"


def _verify_password(password: str, stored: str) -> bool:
    try:
        salt_hex, digest_hex = stored.split("$", maxsplit=1)
    except ValueError:
        return False

    salt = bytes.fromhex(salt_hex)
    expected = bytes.fromhex(digest_hex)
    current = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return current == expected
