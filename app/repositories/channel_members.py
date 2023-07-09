from typing import Literal
from uuid import UUID

from app import clients


def make_key(channel_id: int | Literal["*"]) -> str:
    return f"server:channel-members:{channel_id}"


def serialize(presence_id: UUID) -> str:
    return str(presence_id)


def deserialize(channel_id: bytes) -> UUID:
    return UUID(channel_id.decode())


async def add(
    channel_id: int,
    presence_id: UUID,
) -> UUID:
    await clients.redis.sadd(
        make_key(channel_id),
        serialize(presence_id),
    )
    return presence_id


async def remove(
    channel_id: int,
    presence_id: UUID,
) -> UUID | None:
    remove_attempt = await clients.redis.srem(
        make_key(channel_id),
        serialize(presence_id),
    )
    return presence_id if remove_attempt == 1 else None


async def members(channel_id: int) -> set[UUID]:
    channel_key = make_key(channel_id)
    members = await clients.redis.smembers(channel_key)

    return {deserialize(member) for member in members}
