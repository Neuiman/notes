import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:

    DB_URL = os.getenv("DB_URL")
    ASYNC_DB_URL = os.getenv("ASYNC_DB_URL")
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


