from databases import Database
from app import settings



def dsn(
    scheme: str,
    host: str,
    port: int,
    user: str,
    password: str,
    db_name: str,
) -> str:
    return f"{scheme}://{user}:{password}@{host}:{port}/{db_name}"


database = Database(url=dsn(
    settings.DB_SCHEME,
    settings.DB_HOST,
    settings.DB_PORT,
    settings.DB_USER,
    settings.DB_PASS,
    settings.DB_NAME,
))
