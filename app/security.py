import hashlib
import bcrypt


def hash_password(password: str):
    md5_password = hashlib.md5(password.encode()).hexdigest()
    bcrypt_password = bcrypt.hashpw(md5_password.encode(), bcrypt.gensalt())
    return bcrypt_password


def check_password(password: str, hashword: bytes):
    return bcrypt.checkpw(password.encode(), hashword)
