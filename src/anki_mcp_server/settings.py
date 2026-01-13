from functools import lru_cache

from fastmcp.server.server import Transport
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    anki_connect_url: str = "http://localhost:8765"
    anki_connect_version: int = 6
    mcp_transport: Transport = "http"
    mcp_port: int = 8629
    mcp_host: str = "127.0.0.1"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
