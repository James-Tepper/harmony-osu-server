import redis
from databases import Database

from app import clients, settings
from app.adapters import database, redis


async def start():
    await _start_database()
    await _start_redis()


async def shutdown():
    await _shutdown_database()
    await _shutdown_redis()


async def _start_database():
    clients.database = database.Database(
        url=database.dsn(
            scheme=settings.DB_SCHEME,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASS,
            db_name=settings.DB_NAME,
        )
    )
    await clients.database.connect()


async def _start_redis():
    clients.redis = await redis.from_url(
        url=redis.dsn(
            scheme=settings.REDIS_SCHEME,
            username=settings.REDIS_USER,
            password=settings.REDIS_PASS,
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            database=settings.REDIS_DB,
        )
    )


async def _shutdown_database():
    await clients.database.disconnect()
    del clients.database


async def _shutdown_redis():
    await clients.redis.close()
    del clients.redis
