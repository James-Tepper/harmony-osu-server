import math
import struct
from dataclasses import dataclass
from enum import IntEnum
from typing import TypedDict
from uuid import UUID


class ServerPackets:
    USER_ID = 5
    SEND_MESSAGE = 7
    PONG = 8
    HANDLE_IRC_CHANGE_USERNAME = 9  # unused
    HANDLE_IRC_QUIT = 10
    USER_STATS = 11
    USER_LOGOUT = 12
    SPECTATOR_JOINED = 13
    SPECTATOR_LEFT = 14
    SPECTATE_FRAMES = 15
    VERSION_UPDATE = 19
    SPECTATOR_CANT_SPECTATE = 22
    GET_ATTENTION = 23
    NOTIFICATION = 24
    UPDATE_MATCH = 26
    NEW_MATCH = 27
    DISPOSE_MATCH = 28
    LOBBY_JOIN_UNUSED = 34  # unused
    MATCH_JOIN_SUCCESS = 36
    MATCH_JOIN_FAIL = 37
    FELLOW_SPECTATOR_JOINED = 42
    FELLOW_SPECTATOR_LEFT = 43
    ALL_PLAYERS_LOADED = 45  # unused
    MATCH_START = 46
    MATCH_SCORE_UPDATE = 48
    MATCH_TRANSFER_HOST = 50
    MATCH_ALL_PLAYERS_LOADED = 53
    MATCH_PLAYER_FAILED = 57
    MATCH_COMPLETE = 58
    MATCH_SKIP = 61
    UNAUTHORIZED = 62  # unused
    CHANNEL_JOIN_SUCCESS = 64
    CHANNEL_INFO = 65
    CHANNEL_KICK = 66
    CHANNEL_AUTO_JOIN = 67
    BEATMAP_INFO_REPLY = 69
    PRIVILEGES = 71
    FRIENDS_LIST = 72
    PROTOCOL_VERSION = 75
    MAIN_MENU_ICON = 76
    MONITOR = 80  # unused
    MATCH_PLAYER_SKIPPED = 81
    USER_PRESENCE = 83
    RESTART = 86
    MATCH_INVITE = 88
    CHANNEL_INFO_END = 89
    MATCH_CHANGE_PASSWORD = 91
    SILENCE_END = 92
    USER_SILENCED = 94
    USER_PRESENCE_SINGLE = 95
    USER_PRESENCE_BUNDLE = 96
    USER_DM_BLOCKED = 100
    TARGET_IS_SILENCED = 101
    VERSION_UPDATE_FORCED = 102
    SWITCH_SERVER = 103
    ACCOUNT_RESTRICTED = 104
    RTX = 105  # unused
    MATCH_ABORT = 106
    SWITCH_TOURNAMENT_SERVER = 107


class DataTypes:
    I8 = "<b"
    U8 = "<B"
    I16 = "<h"
    U16 = "<H"
    I32 = "<i"
    U32 = "<I"
    I64 = "<q"
    U64 = "<Q"
    F32 = "<f"
    F64 = "<d"


@dataclass
class Packet:
    packet_id: int
    packet_length: int
    packet_data: bytes


class PacketReader:
    def __init__(self, data: bytes) -> None:
        self.data_view = memoryview(data)

    def read(self, num_bytes: int) -> bytes:
        data = self.data_view[:num_bytes]
        self.data_view = self.data_view[num_bytes:]
        return bytes(data)

    def read_i8(self):
        return struct.unpack("<b", self.read(1))[0]

    def read_u8(self):
        return struct.unpack("<B", self.read(1))[0]

    def read_i16(self):
        return struct.unpack("<h", self.read(2))[0]

    def read_u16(self):
        return struct.unpack("<H", self.read(2))[0]

    def read_i32(self):
        return struct.unpack("<i", self.read(4))[0]

    def read_u32(self):
        return struct.unpack("<I", self.read(4))[0]

    def read_i64(self):
        return struct.unpack("<q", self.read(4))[0]

    def read_u64(self):
        return struct.unpack("<Q", self.read(4))[0]

    def read_f32(self):
        return struct.unpack("<f", self.read(4))[0]

    def read_f64(self):
        return struct.unpack("<d", self.read(4))[0]


def write_packet(datatype, value):
    return struct.pack(datatype, value)


def write_string(value: str) -> bytes:
    # TODO x0b for multiplayer
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


def write_protocol_version_packet(version: int) -> bytes:
    return struct.pack("<HxIi", ServerPackets.PROTOCOL_VERSION, 4, version)


def write_login_reply_packet(user_id: int) -> bytes:
    return struct.pack("<HxIi", ServerPackets.USER_ID, 4, user_id)


def write_user_presence_packet(
    user_id: int,
    username: str,
    timezone: int,
    country: int,
    privileges: int,
    longitude: float,
    latitude: float,
    rank: int,
    gamemode: int,
) -> bytes:
    packet_data = write_packet(DataTypes.I32, user_id)
    packet_data += write_string(username)
    packet_data += write_packet(DataTypes.U8, (timezone + 24))
    packet_data += write_packet(DataTypes.U8, country)
    packet_data += write_packet(
        DataTypes.U8, (privileges & 0x1F) | ((gamemode & 0x7) << 5)
    )
    packet_data += write_packet(DataTypes.F32, longitude)
    packet_data += write_packet(DataTypes.F32, latitude)
    packet_data += write_packet(DataTypes.I32, rank)

    return (
        struct.pack("<HxI", ServerPackets.USER_PRESENCE, len(packet_data)) + packet_data
    )


def write_user_stats_packet(
    user_id: int,
    action: int,
    ranked_score: int,
    accuracy: float,
    play_count: int,
    total_score: int,
    global_rank: int,
    performance_points: int,
    info_text: str,
    beatmap_md5: str,
    mods: int,
    mode: int,
    beatmap_id: int,
) -> bytes:
    packet_data = write_packet(DataTypes.I32, user_id)
    packet_data += write_packet(DataTypes.U8, action)
    packet_data += write_string(info_text)
    packet_data += write_string(beatmap_md5)
    packet_data += write_packet(DataTypes.I32, mods)
    packet_data += write_packet(DataTypes.U8, mode)
    packet_data += write_packet(DataTypes.I32, beatmap_id)
    packet_data += write_packet(DataTypes.U64, ranked_score)
    packet_data += write_packet(DataTypes.F32, (accuracy / 100))
    packet_data += write_packet(DataTypes.I32, play_count)
    packet_data += write_packet(DataTypes.U64, total_score)
    packet_data += write_packet(DataTypes.I32, global_rank)
    packet_data += write_packet(DataTypes.I16, performance_points)

    return struct.pack("<HxI", ServerPackets.USER_STATS, len(packet_data)) + packet_data
