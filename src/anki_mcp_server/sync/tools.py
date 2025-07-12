from fastmcp import FastMCP
from anki_mcp_server.anki_connect import make_anki_request
from anki_mcp_server.sync.models import SyncResponse, ErrorResponse


async def sync_collection() -> SyncResponse | ErrorResponse:
    """Sync the Anki collection with AnkiWeb"""
    try:
        result = await make_anki_request("sync")
        return SyncResponse(success=True, message="Collection synced successfully")
    except Exception as e:
        return ErrorResponse(error=str(e), operation="syncing collection")


def register_sync_tools(mcp: FastMCP):
    mcp.tool(sync_collection) 