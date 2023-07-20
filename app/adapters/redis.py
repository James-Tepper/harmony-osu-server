import redis.asyncio
from redis.asyncio import Redis as _Redis


class Redis(_Redis):
    ...

# TODO Add optional username
def dsn(
    scheme: str,
    username: str,
    password: str,
    host: str,
    port: int,
    database: int,
):
    return f"{scheme}://{username}:{password}@{host}:{port}/{database}"


async def from_url(url: str) -> Redis:
    return await redis.asyncio.from_url(url)
