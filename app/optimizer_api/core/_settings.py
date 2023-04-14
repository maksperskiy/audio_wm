from typing import Optional

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    DATABASE_URI: PostgresDsn
    ALLOW_ORIGINS: Optional[list[str]] = ["*"]
    ALLOW_CREDENTIALS: Optional[bool] = True
    ALLOW_METHODS: Optional[list[str]] = ["*"]
    ALLOW_HEADERS: Optional[list[str]] = ["*"]


settings = Settings(".env")
