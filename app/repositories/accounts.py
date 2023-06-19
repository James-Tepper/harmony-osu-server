from typing import TypedDict
from typing import cast
from app.database import database


READ_PARAMS = """\
    user_id,
    username,
    password
"""

class Account(TypedDict):
    user_id: int
    username: str
    password: str


async def create(
    username: str,
    password: str
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
) -> Account:
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
    assert account is not None
    return cast(Account, account)


async def fetch_by_id(
    user_id: int
) -> Account:
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
    assert account is not None
    return cast(Account, account)
