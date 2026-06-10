from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_ignore_empty=True,
        populate_by_name=True,
    )

    # Server
    port: int = 8080
    env: Literal["development", "staging", "production"] = "development"
    workers: int = 1

    # Logging
    log_level: Literal["debug", "info", "warning", "error"] = "info"
    log_format: Literal["text", "json"] = "text"
    log_file: str = ""

    # Auth — stored as raw comma-separated string to avoid JSON parsing
    api_keys_raw: str = Field(default="", alias="API_KEYS")

    # Rate limiting
    rate_limit: str = "100/minute"

    # OpenTelemetry
    otlp_endpoint: str = ""
    service_name: str = "fastapi-server-boilerplate"

    # Docs
    docs_enabled: bool = True

    @property
    def api_keys(self) -> list[str]:
        return [k.strip() for k in self.api_keys_raw.split(",") if k.strip()]

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
        return bool(self.api_keys_raw.strip())


@lru_cache
def get_settings() -> Settings:
    return Settings()