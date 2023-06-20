from typing import TypedDict
from typing import cast
from uuid import UUID
from app.database import database


READ_PARAMS = """\
    presence_id,
    user_id,
    username,
    timezone,
    country,
    permission,
    longitude,
    latitude,
    rank,
    gamemode
"""

class Presence(TypedDict):
    presence_id: UUID
    user_id: int
    username: str
    timezone: int
    country: int
    permission: int
    longitude: float
    latitude: float
    rank: int
    gamemode: int


async def create(
    presence_id: UUID,
    user_id: int,
    username: str,
    timezone: int,
    country: int,
    permission: int,
    longitude: float,
    latitude: float,
    rank: int,
    gamemode: int,
) -> Presence:
    presence = await database.fetch_one(
        query=f"""
            INSERT INTO presences
            (presence_id, user_id, username, timezone, country, permission, longitude, latitude, rank, gamemode)
            VALUES (:presence_id, :user_id, :username, :timezone, :country, :permission, :longitude, :latitude, :rank, :gamemode)
            RETURNING {READ_PARAMS}
        """,
        values={
            "presence_id": presence_id,
            "user_id": user_id,
            "username": username,
            "timezone": timezone,
            "country": country,
            "permission": permission,
            "longitude": longitude,
            "latitude": latitude,
            "rank": rank,
            "gamemode": gamemode,
        }
    )

    assert presence is not None
    return cast(Presence, presence)


async def fetch_by_presence_id(
    presence_id: UUID,
) -> Presence | None:
    presence = await database.fetch_one(
        query=f"""
            SELECT {READ_PARAMS}
            FROM presences
            WHERE presence_id = :presence_id
        """,
        values={
            "presence_id": presence_id,
        }
    )

    return cast(Presence, presence) if presence is not None else None
