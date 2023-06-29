from typing import TypedDict
from uuid import UUID, uuid4

import uvicorn
from fastapi import APIRouter, FastAPI, Request, Response

from app import packets, security, settings
from app.database import database
from app.login_reply import LoginReply, WriteLoginReply
from app.repositories import accounts, presences, stats
from app.repositories.accounts import Account
from app.repositories.presences import Presence
from app.repositories.stats import Stats

app = FastAPI()

osu_web_router = APIRouter(default_response_class=Response)
bancho_router = APIRouter(default_response_class=Response)


app.host("osu.jamestepper.com", osu_web_router)
app.host("c.jamestepper.com", bancho_router)
app.host("ce.jamestepper.com", bancho_router)
app.host("c4.jamestepper.com", bancho_router)
app.host("c5.jamestepper.com", bancho_router)
app.host("c6.jamestepper.com", bancho_router)


class LoginData(TypedDict):
    username: str
    password_md5: str
    version: str
    timezone: int
    location: int
    client_hash: str
    block_non_friend_pm: int


@app.on_event("startup")
async def on_startup():
    await database.connect()


@app.on_event("shutdown")
async def on_shutdown():
    await database.disconnect()


def parse_login_data(raw_data: bytes):
    data = raw_data.decode()

    username, password_md5, remainder = data.split("\n", maxsplit=2)
    version, timezone, location, client_hash, block_non_friend_pm = remainder.split(
        "|", maxsplit=4
    )

    login_data: LoginData = {
        "username": username,
        "password_md5": password_md5,
        "version": version,
        "timezone": int(timezone),
        "location": int(location),
        "client_hash": client_hash,
        "block_non_friend_pm": int(block_non_friend_pm),
    }

    return login_data


# Sorted by login_reply
async def handle_login(request: Request):
    # print(request.headers)
    login_data = parse_login_data(await request.body())

    login_reply = WriteLoginReply()

    if login_data is None:
        return login_reply.handle_login_reply(LoginReply.AUTHENTICATION_FAILED)

    account = await accounts.fetch_by_username(login_data["username"])

    if account is None:
        return login_reply.handle_login_reply(LoginReply.AUTHENTICATION_FAILED)

    if not security.check_password(
        login_data["password_md5"], account["password"].encode()
    ):
        return login_reply.handle_login_reply(LoginReply.AUTHENTICATION_FAILED)

    # TODO Implement a way to delete a presence when user logs off
    presence: Presence = await presences.create(
        presence_id=uuid4(),
        user_id=account["user_id"],
        username=account["username"],
        timezone=1,
        country=1,
        permission=16,
        longitude=0.0,
        latitude=0.0,
        rank=1,
        gamemode=0,
    )

    response_data = bytearray()

    response_data += packets.write_protocol_version_packet(19)
    response_data += packets.write_login_reply_packet(presence["user_id"])

    response_data += packets.write_user_presence_packet(
        user_id=presence["user_id"],
        username=presence["username"],
        timezone=presence["timezone"],
        country=presence["country"],
        permission=presence["permission"],
        longitude=presence["longitude"],
        latitude=presence["latitude"],
        rank=presence["rank"],
        gamemode=presence["gamemode"],
    )

    user_stats: Stats = await stats.fetch_one(
        user_id=presence["user_id"],
    )

    response_data += packets.write_user_stats_packet(
        user_id=presence["user_id"],
        action=0,
        ranked_score=user_stats["ranked_score"],
        accuracy=100.00,
        play_count=222,
        total_score=1000,
        global_rank=1,
        performance_points=10000,
        info_text=user_stats["info_text"],
        beatmap_md5=user_stats["beatmap_md5"],
        mods=user_stats["mods"],
        mode=user_stats["mode"],
        beatmap_id=user_stats["beatmap_id"],
    )


    login_reply = WriteLoginReply(str(presence["presence_id"]))
    return login_reply.handle_login_reply(response_data)

    # return Response(
    #     content=response_data, headers={"cho-token": str(presence["presence_id"])}
    # )


# \x05\x00 H packet id
# \x00 x skip a byte
# \x04\x00\x00\x00 I length of data
# \x01\x00\x00\x00 i data (user id)

# user presence
# 83, 0, 
# 0, 
# 30, 0, 0, 0, 
# 1, 0, 0, 0, 
# 11, 9, 82, 97, 110, 100, 111, 109, 105, 122, 101,
# 25,
# 1,
# 16, 
# 0, 0, 0, 0, 
# 0, 0, 0, 0, 
# 1, 0, 0, 0,

# user stats
# 11, 0,                              H packet_id
# 0,                                  x skip a byte
# 57, 0, 0, 0,                        I length of data
# 1, 0, 0, 0,                         4 user_id 
# 0,                                  1 action
# 11, 4, 73, 100, 108, 101,           S info_text                
# 11, 5, 104, 101, 108, 108, 111,     S beatmap_md5                    
# 0, 0, 0, 0,                         4 mods
# 0,                                  1 mode
# 0, 0, 0, 0,                         4 beatmap_id
# 16, 39, 0, 0, 0, 0, 0, 0,           8 ranked_score                
# 0, 0, 128, 63,                      4 accuracy
# 222, 0, 0, 0,                       4 play_count
# 232, 3, 0, 0, 0, 0, 0, 0,           8 total_score                
# 1, 0, 0, 0,                         4 global_rank
# 16, 39                            2 performance_points


async def handle_bancho_request(request: Request):
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
