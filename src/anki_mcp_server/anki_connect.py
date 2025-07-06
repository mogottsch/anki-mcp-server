from typing import Any
import httpx
from anki_mcp_server.settings import get_settings


def create_anki_payload(action: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    settings = get_settings()
    return {
        "action": action,
        "version": settings.anki_connect_version,
        "params": params or {},
    }

def validate_anki_response(result: dict[str, Any]) -> Any:
    if result.get("error"):
        raise Exception(f"AnkiConnect error: {result['error']}")
    return result.get("result")

async def make_anki_request(action: str, params: dict[str, Any] | None = None) -> Any:
    settings = get_settings()
    payload = create_anki_payload(action, params)
    async with httpx.AsyncClient() as client:
        response = await client.post(settings.anki_connect_url, json=payload, timeout=30.0)
        response.raise_for_status()
        result = response.json()
        return validate_anki_response(result) 
