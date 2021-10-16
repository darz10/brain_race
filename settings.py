from typing import List
from pydantic import BaseSettings, PostgresDsn, Field


class Settings(BaseSettings):
    """Параметры конфигурации"""

    psql_conn: PostgresDsn = Field(
        ..., description="Подключение к базе данных"
    )

    origins: List[str]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "br_"


settings = Settings()
