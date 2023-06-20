from typing import TypedDict
from typing import cast
from app.database import database
from datetime import datetime


READ_PARAMS = """\
    user_id,
    username,
    password,
    created_at,
    updated_at
"""

class Account(TypedDict):
    user_id: int
    username: str
    password: str
    created_at: datetime
    updated_at: datetime


async def create(
    username: str,
    password: str,
) -> Account:
    account = await database.fetch_one(
        query=f"""
            INSERT INTO accounts 
            (username, password)
            VALUES (:username, :password)
            RETURNING {READ_PARAMS}
        """,
        values={
            "username": username,
            "password": password,
        }
    )
    assert account is not None
    return cast(Account, account)


async def fetch_by_username(
    username: str
) -> Account | None:
    account = await database.fetch_one(
        query=f"""
            SELECT {READ_PARAMS}
            FROM accounts
            WHERE username = :username
        """,
        values={
            "username": username,
        }
    )
    return cast(Account, account) if account is not None else None


async def fetch_by_id(
    user_id: int
) -> Account | None:
    account = await database.fetch_one(
        query=f"""
            SELECT {READ_PARAMS}
            FROM accounts
            WHERE user_id = :user_id
        
        """,
        values={
                "user_id": user_id,
        }
    )
    return cast(Account, account) if account is not None else None


async def fetch_many(
    privileges: int | None = None,
    page: int = 1,
    page_size: int = 50,
) -> list[Account]:
    accounts = database.fetch_all(
        query=f"""
                                  
                                  
                    """)
