from typing import Optional

from pydantic import BaseSettings, PostgresDsn, AnyHttpUrl


class Settings(BaseSettings):
    DATABASE_AI_URI: PostgresDsn
    CLASSIFIER_URI: AnyHttpUrl
    ALLOW_ORIGINS: Optional[list[str]] = ["*"]
    ALLOW_CREDENTIALS: Optional[bool] = True
    ALLOW_METHODS: Optional[list[str]] = ["*"]
    ALLOW_HEADERS: Optional[list[str]] = ["*"]


settings = Settings(".env")
