import struct

# struct.unpack("<I", )

# sends user id as I32
# packet id = 5 (LOGIN REPLY)| length = 4 | user id = 1
# read case login reply handler for length
def login_reply_packet(user_id: int) -> bytes:
    return struct.pack("<HxIi", 5, 4, user_id)
