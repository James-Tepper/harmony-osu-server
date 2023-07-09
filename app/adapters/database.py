from databases import Database as _Database

from app import settings


class Database(_Database):
    ...


def dsn(
    scheme: str,
    host: str,
    port: int,
    user: str,
    password: str,
    db_name: str,
) -> str:
    return f"{scheme}://{user}:{password}@{host}:{port}/{db_name}"
