from typing import TypedDict, Union

from fastapi import Response

from app import packets


class LoginReply:
    AUTHENTICATION_FAILED = -1
    OUTDATED_BANCHO_VERSION = -2
    USER_IS_BANNED = -3
    # UNUSED -4
    CONNECTION_FAILED = -5
    NEED_SUPPORTER = -6
    PASSWORD_RESET = -7
    REQUIRE_VERIFICATION = -8


class LoginData(TypedDict):
    username: str
    password_md5: str
    version: str
    timezone: int
    location: int
    client_hash: str
    block_non_friend_pm: int


# TODO FIX AND IMPLEMENT PROPERLY
class WriteLoginReply:
    def __init__(
        self,
        presence_id: Union[str, None] = None,
    ) -> None:
        if presence_id:
            self.presence_id = presence_id

    def handle_login_reply(
        self, login_id_or_response_data: Union[int, bytes]
    ) -> Response:
        # response data
        if (
            isinstance(login_id_or_response_data, bytes)
            and self.presence_id is not None
        ):
            bytes(login_id_or_response_data)
            return Response(
                content=login_id_or_response_data,
                headers={"cho-token": self.presence_id},
            )

        # login id
        match login_id_or_response_data:
            case -1:
                message = "Authentication Failed"
            case -2:
                message = "Outdated Version Of Bancho"
            case -3:
                message = "User Is Banned"
            # -4 does nothing
            case -5:
                message = "Connection Failed"
            case -6:
                message = "Supporter Is Required"
            case -7:
                message = "A Password Reset Email Has Been Sent"  # TODO make service to send email to reset pw
            case -8:
                message = "A Verification Email Has Been Sent"
            case _:
                message = "Welcome!"

        return Response(
            content=packets.write_login_reply_packet(int(login_id_or_response_data)),
            headers={"cho-token": message},
        )


def parse_login_data(raw_data: bytes) -> LoginData:
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
