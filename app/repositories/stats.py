from typing import TypedDict, cast

from app import clients

READ_PARAMS = """\
    user_id,
    mode,
    ranked_score,
    accuracy,
    play_count,
    total_score,
    global_rank,
    performance_points
"""


class Stats(TypedDict):
    user_id: int
    mode: int
    ranked_score: int
    accuracy: float
    play_count: int
    total_score: int
    global_rank: int
    performance_points: int


async def create(
    user_id: int,
    mode: int,
    ranked_score: int,
    accuracy: float,
    play_count: int,
    total_score: int,
    global_rank: int,
    performance_points: int,
) -> Stats:
    stats = await clients.database.fetch_one(
        query=f"""
            INSERT INTO stats
            (user_id, mode, ranked_score, accuracy, play_count, total_score, global_rank, performance_points)
            VALUES (:user_id, :mode, :ranked_score, :accuracy, :play_count, :total_score, :global_rank, :performance_points)
            RETURNING {READ_PARAMS}
        """,
        values={
            "user_id": user_id,
            "mode": mode,
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
    stats = await clients.database.fetch_one(
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
