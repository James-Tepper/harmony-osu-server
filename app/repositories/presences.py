from typing import TypedDict, cast
from uuid import UUID

from app.database import database

READ_PARAMS = """\
    presence_id,
    user_id,
    username,
    action,
    rank,
    country,
    mods,
    gamemode,
    longitude,
    latitude,
    timezone,
    info_text,
    beatmap_md5,
    beatmap_id
"""


class Presence(TypedDict):
    presence_id: UUID
    user_id: int
    username: str
    action: int
    rank: int
    country: int
    mods: int
    gamemode: int
    longitude: float
    latitude: float
    timezone: int
    info_text: str
    beatmap_md5: str
    beatmap_id: int


async def create(
    presence_id: UUID,
    user_id: int,
    username: str,
    action: int,
    rank: int,
    country: int,
    mods: int,
    gamemode: int,
    longitude: float,
    latitude: float,
    timezone: int,
    info_text: str,
    beatmap_md5: str,
    beatmap_id: int,
) -> Presence:
    presence = await database.fetch_one(
        query=f"""
            INSERT INTO presences
            (presence_id, user_id, username, action, rank, country, mods, gamemode, longitude, latitude, timezone, info_text, beatmap_md5, beatmap_id)
            VALUES (:presence_id, :user_id, :username, :action, :rank, :country, :mods, :gamemode, :longitude, :latitude, :timezone, :info_text, :beatmap_md5, :beatmap_id)
            RETURNING {READ_PARAMS}
        """,
        values={
            "presence_id": str(presence_id),
            "user_id": user_id,
            "username": username,
            "action": action,
            "rank": rank,
            "country": country,
            "mods": mods,
            "gamemode": gamemode,
            "longitude": longitude,
            "latitude": latitude,
            "timezone": timezone,
            "info_text": info_text,
            "beatmap_md5": beatmap_md5,
            "beatmap_id": beatmap_id,
        },
    )

    assert presence is not None
    return cast(Presence, presence)


async def fetch_one(
    presence_id: UUID,
) -> Presence | None:
    presence = await database.fetch_one(
        query=f"""
            SELECT {READ_PARAMS}
            FROM presences
            WHERE presence_id = :presence_id
        """,
        values={
            "presence_id": str(presence_id),
        },
    )

    return cast(Presence, presence) if presence is not None else None
