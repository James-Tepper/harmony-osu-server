import asyncio
import re
import sys
from getpass import getpass

from app.gamemodes import GameMode
from app.database import database
from app.repositories import accounts, stats
from app.repositories.accounts import Account
from app.main import app


async def sign_up():
    while True:
        username = input("Input username: ")
        email = input("Input email: ")
        password = getpass("Input password: ")

        if (
            not re.match(r"^(?!.*\.\.)(?!.*\.$)[^\W_]{3,20}$", username)
            or not re.match(
                r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{1,30}$", email
            )
            or not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[\S]{8,}$", password)
        ):
            print("INVALID INPUT")
            continue

        account: Account = await accounts.create(
            username,
            email,
            password,
        )

        game_mode_instance = GameMode()

        for mode in vars(game_mode_instance):
            if mode.startswith("__"):
                continue

            await stats.create(
            user_id=account["user_id"],
            action=0,
            status_text="Idle",
            beatmap_checksum="Hi",
            current_mods=0,
            play_mode=getattr(game_mode_instance, mode),
            beatmap_id=0,
            ranked_score=100_000,
            accuracy=100.00,
            play_count=0,
            total_score=0,
            rank=1,
            performance=100_000,
        )


if __name__ == "__main__":
    asyncio.run(sign_up())


"""
RAW SQL

INSERT INTO stats (user_id, action, status_text, beatmap_checksum, current_mods, play_mode, beatmap_id, ranked_score, accuracy, play_count, total_score, rank, performance)
VALUES (1, 0, 'Idle', 'Hi', 0, 0, 0, 100000, 100.00, 0, 0, 1, 100000);


"""
