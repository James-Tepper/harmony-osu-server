from typing import TypedDict
from uuid import UUID, uuid4

import uvicorn
from fastapi import APIRouter, FastAPI, Request, Response

from app import lifecycle, login, packets, security, settings
from app.actions import Action
from app.gamemodes import GameMode
from app.repositories import rankings
from app.login import LoginData, LoginReply, WriteLoginReply
from app.repositories import accounts, channel_members, channels, presences, stats
from app.repositories.accounts import Account
from app.repositories.channels import Channels
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


@app.on_event("startup")
async def startup():
    await lifecycle.start()


@app.on_event("shutdown")
async def shutdown():
    await lifecycle.shutdown()


# Sorted by login_reply
async def handle_login(request: Request):
    login_data: LoginData = login.parse_login_data(await request.body())

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

    default_action = Action.IDLE
    vanilla_game_mode = GameMode.VN_OSU

    # TODO Implement a way to delete a presence when user logs off
    user_presence: Presence = await presences.create(
        presence_id=uuid4(),
        user_id=account["user_id"],
        username=account["username"],
        action=default_action,
        rank=1,
        country=1,
        mods=0,
        gamemode=vanilla_game_mode,
        longitude=0.0,
        latitude=0.0,
        timezone=0,
        info_text="",
        beatmap_md5="",
        beatmap_id=10,
    )

    response_data = packets.write_protocol_version_packet(19)

    response_data += packets.write_login_reply_packet(user_presence["user_id"])
    response_data += packets.write_user_presence_packet(
        user_id=user_presence["user_id"],
        username=user_presence["username"],
        timezone=user_presence["timezone"],
        country=user_presence["country"],
        privileges=account["privileges"],
        longitude=user_presence["longitude"],
        latitude=user_presence["latitude"],
        rank=user_presence["rank"],
        gamemode=user_presence["gamemode"],
    )

    user_stats: Stats = await stats.fetch_one(
        user_id=user_presence["user_id"],
    )

    response_data += packets.write_user_stats_packet(
        user_id=user_presence["user_id"],
        action=Action.IDLE,
        ranked_score=user_stats["ranked_score"],
        accuracy=user_stats["accuracy"],
        play_count=user_stats["play_count"],
        total_score=user_stats["total_score"],
        global_rank=user_stats["global_rank"],
        performance_points=await rankings.calculate_performance_points(user_presence["user_id"], user_stats["mode"]),
        info_text=user_presence["info_text"],
        beatmap_md5=user_presence["beatmap_md5"],
        mods=user_presence["mods"],
        mode=user_stats["mode"],
        beatmap_id=user_presence["beatmap_id"],
    )

    login_reply = WriteLoginReply(str(user_presence["presence_id"]))
    return login_reply.handle_login_reply(response_data)


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
