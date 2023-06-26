from typing import TypedDict, cast

from app.database import database

# from repositories.presences import Action


READ_PARAMS = """\
        user_id,
        action,
        info_text,
        beatmap_md5,
        mods,
        mode,
        beatmap_id,
        ranked_score,
        accuracy,
        play_count,
        total_score,
        global_rank,
        performance_points
"""


class Stats(TypedDict):
    user_id: int
    action: int
    info_text: str
    beatmap_md5: str
    mods: int
    mode: int
    beatmap_id: int
    ranked_score: int
    accuracy: float
    play_count: int
    total_score: int
    global_rank: int
    performance_points: int


async def create(
    user_id: int,
    action: int,
    info_text: str,
    beatmap_md5: str,
    mods: int,
    mode: int,
    beatmap_id: int,
    ranked_score: int,
    accuracy: float,
    play_count: int,
    total_score: int,
    global_rank: int,
    performance_points: int,
) -> Stats:
    stats = await database.fetch_one(
        query=f"""
            INSERT INTO stats
            (user_id, action, info_text, beatmap_md5, mods, mode, beatmap_id, ranked_score, accuracy, play_count, total_score, global_rank, performance_points)
            VALUES (:user_id, :action, :info_text, :beatmap_md5, :mods, :mode, :beatmap_id, :ranked_score, :accuracy, :play_count, :total_score, :global_rank, :performance_points)
            RETURNING {READ_PARAMS}
        """,
        values={
            "user_id": user_id,
            "action": action,
            "info_text": info_text,
            "beatmap_md5": beatmap_md5,
            "mods": mods,
            "mode": mode,
            "beatmap_id": beatmap_id,
            "ranked_score": ranked_score,
            "accuracy": accuracy,
            "play_count": play_count,
            "total_score": total_score,
            "global_rank": global_rank,
            "performance_points": performance_points,
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
