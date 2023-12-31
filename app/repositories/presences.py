from typing import Any, TypedDict, cast
from uuid import UUID

from app import clients

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
    presence = await clients.database.fetch_one(
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
    presence = await clients.database.fetch_one(
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


async def partial_update(
    presence_id: UUID,
    action: int | None = None,
    rank: int | None = None,
    mods: int | None = None,
    gamemode: int | None = None,
    info_text: str | None = None,
    beatmap_md5: str | None = None,
    beatmap_id: int | None = None,
) -> Presence | None:
    sql_values = {
        "presence_id": str(presence_id),
        "action": action,
        "rank": rank,
        "mods": mods,
        "gamemode": gamemode,
        "info_text": info_text,
        "beatmap_md5": beatmap_md5,
        "beatmap_id": beatmap_id,
    }

    filtered_sql_values = {}
    for key, value in sql_values.items():
        if value is not None:
            filtered_sql_values.update({key: value})

    set_query = "SET"
    for key, value in filtered_sql_values.items():
        set_query += f" {key} = :{key},"

    set_query = set_query[:-1]

    presence = await clients.database.fetch_one(
        query=f"""
            UPDATE presences
            {set_query}
            WHERE presence_id = :presence_id
            RETURNING {READ_PARAMS}
        """,
        values=filtered_sql_values,
    )
    return cast(Presence, presence) if presence is not None else None


async def delete(presence_id: UUID) -> Presence | None:
    presence = await clients.database.fetch_one(
        query=f"""
            DELETE FROM presences
            WHERE presence_id = :presence_id
            RETURNING {READ_PARAMS}
        """,
        values={
            "presence_id": str(presence_id)
        },
    )
    return cast(Presence, presence) if presence is not None else None
