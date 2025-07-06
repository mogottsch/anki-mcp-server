from fastmcp.server.server import Transport
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    anki_connect_url: str = "http://localhost:8765"
    anki_connect_version: int = 6
    mcp_transport: Transport = "http"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
