import struct
from uuid import UUID
# struct.unpack("<I", )

# sends user id as I32
# packet id = 5 (LOGIN REPLY)| length = 4 | user id = 1
# read case login reply handler for length

LOGIN_REPLY = 5
USER_PRESENCE = 83


def login_reply_packet(user_id: int) -> bytes:
    return struct.pack("<HxIi", LOGIN_REPLY, 4, user_id)


def user_presence_packet(
    user_id: int,
    username: str,
    timezone: int,
    country: int,
    permission: int,
    longitude: float,
    latitude: float,
    rank: int,
    gamemode: int,
) -> bytes:
    packet_data = struct.pack("<i", user_id,)
    packet_data += write_string(username)
    packet_data += struct.pack("<B", timezone + 24)
    packet_data += struct.pack("<B", country)
    packet_data += struct.pack("<B", (permission & 0x1f) | ((gamemode & 0x7) << 5))
    packet_data += struct.pack("<f", longitude)
    packet_data += struct.pack("<f", latitude)
    packet_data += struct.pack("<i", rank)
    
    return struct.pack("<HxI", USER_PRESENCE, len(packet_data)) + packet_data


def write_string(value: str) -> bytes:
    #TODO x0b for multiplayer
    data = value.encode()
    data_len = len(data)
    output = bytearray([11 if data_len else 0])
    while data_len:
        b = data_len & 0b1111111
        data_len >>= 7
        if data_len != 0:
            b |= 0b10000000

        output.append(b)

    output += data
    return output
