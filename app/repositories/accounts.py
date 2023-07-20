from datetime import datetime
from typing import TypedDict, cast

from app import clients

READ_PARAMS = """\
    user_id,
    username,
    privileges,
    email,
    password,
    created_at,
    updated_at
"""


class Account(TypedDict):
    user_id: int
    username: str
    privileges: int
    email: str
    password: str
    created_at: datetime
    updated_at: datetime


async def create(
    username: str,
    privileges: int,
    email: str,
    password: str,
) -> Account:
    account = await clients.database.fetch_one(
        query=f"""
            INSERT INTO accounts
            (username, privileges, email, password)
            VALUES (:username, :privileges, :email :password)
            RETURNING {READ_PARAMS}
        """,
        values={
            "username": username,
            "privileges": privileges,
            "email": email,
            "password": password,
        },
    )
    assert account is not None
    return cast(Account, account)


async def fetch_by_username(username: str) -> Account | None:
    account = await clients.database.fetch_one(
        query=f"""
            SELECT {READ_PARAMS}
            FROM accounts
            WHERE username = :username
        """,
        values={
            "username": username,
        },
    )
    return cast(Account, account) if account is not None else None


async def fetch_by_id(user_id: int) -> Account | None:
    account = await clients.database.fetch_one(
        query=f"""
            SELECT {READ_PARAMS}
            FROM accounts
            WHERE user_id = :user_id
        """,
        values={
            "user_id": user_id,
        },
    )
    return cast(Account, account) if account is not None else None


async def fetch_many(
    privileges: int | None = None,
    page: int = 1,
    page_size: int = 50,
) -> list[Account]:

    privileges_query = "WHERE privileges = :privileges"

    accounts = clients.database.fetch_all(
        query=f"""
            SELECT {READ_PARAMS} FROM accounts
            {privileges_query if privileges is not None else None}
            LIMIT :limit
            OFFSET :offset
            """,
        values={
            f"'privileges': {privileges}," if privileges is not None else ""
            "limit": page_size,
            "offset": (page - 1) * page_size,
        },
    )
    return cast(list[Account], accounts)
