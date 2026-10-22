from typing import Literal
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gui_engine: Literal["playwright", "selenium"] = "playwright"
    headless: bool = True
    base_url: str = "http://localhost"

    db_url: str = "sqlite:///:memory:"

    qtest_url: str = ""
    qtest_token: SecretStr = SecretStr("")
    qtest_project_id: int = 0
    qtest_enabled: bool = False
    verify_ssl: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


def get_settings() -> Settings:
    return Settings()