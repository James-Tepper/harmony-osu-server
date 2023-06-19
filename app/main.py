from typing import TypedDict

from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Request
from fastapi import Response

import uvicorn

from app.database import database
from app import settings

app = FastAPI()

osu_web_router = APIRouter(default_response_class=Response)
bancho_router = APIRouter(default_response_class=Response)


app.host("osu.jamestepper.com", osu_web_router)
app.host("c.jamestepper.com", bancho_router)
app.host("ce.jamestepper.com", bancho_router)
app.host("c4.jamestepper.com", bancho_router)
app.host("c5.jamestepper.com", bancho_router)
app.host("c6.jamestepper.com", bancho_router)



class Login_Data(TypedDict):
    username: str
    password_md5: str
    version: str
    timezone: int
    location: int
    client_hash: str
    block_non_friend_pm: int


# headers
# {'cho-token': 'aiopdfjhw389rf3u289orhfj2389fj'}


@app.on_event("startup")
async def on_startup():
    await database.connect()


@app.on_event("shutdown")
async def on_shutdown():
    await database.disconnect()


def parse_login_data(raw_data: bytes):
    data = raw_data.decode()

    username, password_md5, remainder = data.split("\n", maxsplit=2)
    version, timezone, location, client_hash, block_non_friend_pm = remainder.split("|", maxsplit=4)

    login_data: Login_Data = {
        "username": username,
        "password_md5": password_md5,
        "version": version,
        "timezone": int(timezone),
        "location": int(location),
        "client_hash": client_hash,
        "block_non_friend_pm": int(block_non_friend_pm),
    }

    return login_data


async def handle_login(request: Request):
    # print(request.headers)
    login_data = parse_login_data(await request.body())

    if login_data is None:
        return

    import struct
    # sends user id as I32
    # packet id = 5 (LOGIN REPLY)| length = 4 | user id = 1
    # read case login reply handler for length
    response_data = struct.pack("<HxIi", 5, 4, -1)
    
    token: str = "cho-token"

    return Response(
            content=response_data,
            headers={"cho-token": token}
    )

#cho-token


async def handle_bancho_request(request: Request) -> Response:
    ...




@bancho_router.post("/")
async def handle_bancho_http_request(request: Request):
    if "osu-token" not in request.headers:
        response = await handle_login(request)
    else:
        response = await handle_bancho_request(request)
    return response


if __name__ == "__main__":
    uvicorn.run(app=app, port=settings.PORT)
