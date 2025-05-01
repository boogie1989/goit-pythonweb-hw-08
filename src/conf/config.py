import os

DB_HOST = os.getenv("DB_HOST", "localhost")


class Config:
    DB_URL = f"postgresql+asyncpg://postgres:567234@{DB_HOST}:5432"


config = Config
