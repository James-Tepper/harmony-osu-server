from typing import TypedDict, cast

from app.database import database

# from repositories.presences import Action


READ_PARAMS = """\
        user_id,
        action,
        status_text,
        beatmap_checksum,
        current_mods,
        play_mode,
        beatmap_id,
        ranked_score,
        accuracy,
        play_count,
        total_score,
        rank,
        performance
"""


class Stats(TypedDict):
    user_id: int
    action: int
    status_text: str
    beatmap_checksum: str
    current_mods: int
    play_mode: int
    beatmap_id: int
    ranked_score: int
    accuracy: float
    play_count: int
    total_score: int
    rank: int
    performance: int


async def create(
    user_id: int,
    action: int,
    status_text: str,
    beatmap_checksum: str,
    current_mods: int,
    play_mode: int,
    beatmap_id: int,
    ranked_score: int,
    accuracy: float,
    play_count: int,
    total_score: int,
    rank: int,
    performance: int,
) -> Stats:
    stats = await database.fetch_one(
        query=f"""
            INSERT INTO stats
            (user_id, action, status_text, beatmap_checksum, current_mods, play_mode, beatmap_id, ranked_score, accuracy, play_count, total_score, rank, performance)
            VALUES (:user_id, :action, :status_text, :beatmap_checksum, :current_mods, :play_mode, :beatmap_id, :ranked_score, :accuracy, :play_count, :total_score, :rank, :performance)
            RETURNING {READ_PARAMS}
        """,
        values={
            "user_id": user_id,
            "action": action,
            "status_text": status_text,
            "beatmap_checksum": beatmap_checksum,
            "current_mods": current_mods,
            "play_mode": play_mode,
            "beatmap_id": beatmap_id,
            "ranked_score": ranked_score,
            "accuracy": accuracy,
            "play_count": play_count,
            "total_score": total_score,
            "rank": rank,
            "performance": performance,
        },
    )

    assert stats is not None
    return cast(Stats, stats)


async def fetch_one(
    user_id: int,
):
    stats = await database.fetch_one(
        query=f"""
            SELECT {READ_PARAMS}
            FROM stats 
            WHERE user_id = :user_id
        """,
        values={
            "user_id": user_id,
        },
    )

    assert stats is not None
    return cast(Stats, stats)
