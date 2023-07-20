from typing import TypedDict
from typing import cast

from app import clients
from app.beatmap_status import BeatmapRankedStatus
from app.repositories import presences, stats
from app.repositories.presences import partial_update

# get ranking
# order stats by pp
# ranking = row number of ordered pp query



async def calculate_performance_points(user_id: int, mode: int) -> int:
    top_plays = await clients.database.fetch_all(
        query=f"""
            SELECT s.performance_points
            FROM scores s
            JOIN beatmaps b ON s.beatmap_id = b.beatmap_id
            WHERE s.user_id = :user_id
            AND s.mode = :mode
            AND b.ranked_status = :ranked_status
            ORDER BY s.performance_points DESC
            LIMIT 100
                """,
        values={
            "user_id": user_id,
            "mode": mode,
            "ranked_status": BeatmapRankedStatus.RANKED,
        },
    )
    assert top_plays is not None

    # based off the index, the DESC order pp plays are weighted accordingly

    weighted_pp = sum([score["performance_points"] * (0.95 ** index) for index, score in enumerate(top_plays)])

    await update_performance_points(user_id, mode, int(weighted_pp))
    return weighted_pp


async def update_performance_points(user_id: int, mode: int, weighted_pp: int):
    await clients.database.execute(
        query=f"""
            UPDATE stats
            SET performance_points = :weighted_pp
            WHERE user_id = :user_id
            AND mode = :mode
        """,
        values={
            "user_id": user_id,
            "mode": mode,
            "weighted_pp": weighted_pp,
        },
    )

async def fetch_ranking(user_id: int, mode: int):
    ...
    
    
    ranking = await clients.database.fetch_one(
        query=f"""
                SELECT *,
                ROW_NUMBER() OVER (ORDER BY total_performance_points DESC) AS row_number
                FROM (
                    SELECT user_id, SUM(performance_points) AS total_performance_points
                    FROM stats
                    WHERE performance_points > 1 and mode = :mode
                    GROUP BY user_id
                ) subquery
                ) subquery2
                WHERE user_id = :user_id;
            """,
        values={"user_id": user_id, "mode": mode},
    )
    return ranking if ranking is not None else None
