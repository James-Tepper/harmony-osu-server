from datetime import datetime
from typing import TypedDict, cast

from app import clients

READ_PARAMS = """\
    name,
    topic,
    read_privileges,
    write_privileges,
    auto_join,
    temporary,
    created_at,
    updated_at
"""


class Channels(TypedDict):
    name: str
    topic: str
    read_privileges: int
    write_privileges: int
    auto_join: bool
    temporary: bool
    created_at: datetime
    updated_at: datetime


async def create(
    name: str,
    topic: str,
    read_privileges: int,
    write_privileges: int,
    auto_join: bool,
    temporary: bool,
    created_at: datetime,
    updated_at: datetime,
) -> Channels:
    channel = await clients.database.fetch_one(
        query=f"""
            INSERT INTO channels
            (name, topic, read_privileges, write_privileges, auto_join, temporary, created_at, updated_at)
            VALUES (name, :topic, :read_privileges, :write_privileges, :auto_join, :temporary, :created_at, :updated_at)
            RETURNING {READ_PARAMS}
            """,
        values={
            "name": name,
            "topic": topic,
            "read_privileges": read_privileges,
            "write_privileges": write_privileges,
            "auto_join": auto_join,
            "temporary": temporary,
            "created_at": created_at,
            "updated_at": updated_at,
        },
    )
    assert channel is not None
    return cast(Channels, channel)


async def fetch_one(name: str) -> Channels | None:
    channel = await clients.database.fetch_one(
        query=f"""
            SELECT {READ_PARAMS} 
            FROM stats
            WHERE name = :name
        """,
        values={
            "name": name,
        },
    )
    return cast(Channels, channel) if channel is not None else None
