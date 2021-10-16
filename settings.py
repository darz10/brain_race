from typing import List
from pydantic import BaseSettings, PostgresDsn, Field, RedisDsn


class Settings(BaseSettings):
    """Параметры конфигурации"""

    psql_conn: PostgresDsn = Field(..., description="Подключение к postgresql")
    redis_conn: RedisDsn = Field(..., description="Подключение к redis")

    origins: List[str]

    algorithm: str
    secret_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "br_"


settings = Settings()
