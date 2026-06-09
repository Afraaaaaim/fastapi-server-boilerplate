from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Server
    port: int = 8080
    env: Literal["development", "staging", "production"] = "development"
    workers: int = 1

    # Logging
    log_level: Literal["debug", "info", "warning", "error"] = "info"
    log_format: Literal["text", "json"] = "text"
    log_file: str = ""  # empty = stdout

    # Auth
    api_keys: list[str] = []  # comma-separated in env: API_KEYS=key1,key2

    # Rate limiting
    rate_limit: str = "100/minute"  # slowapi format: "N/period"

    # OpenTelemetry
    otlp_endpoint: str = ""  # empty = disabled
    service_name: str = "fastapi-server-boilerplate"

    # Docs
    docs_enabled: bool = True  # set False in production

    @property
    def is_development(self) -> bool:
        return self.env == "development"

    @property
    def is_production(self) -> bool:
        return self.env == "production"

    @property
    def otlp_enabled(self) -> bool:
        return bool(self.otlp_endpoint)

    @property
    def auth_enabled(self) -> bool:
        return bool(self.api_keys)


@lru_cache
def get_settings() -> Settings:
    return Settings()