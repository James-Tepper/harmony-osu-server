import os
from dotenv import load_dotenv

load_dotenv()


PORT = int(os.environ["PORT"])

DB_SCHEME = os.environ["DB_SCHEME"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.environ["DB_PORT"])
DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]
DB_NAME = os.environ["DB_NAME"]
