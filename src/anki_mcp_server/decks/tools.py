from fastmcp import FastMCP
from anki_mcp_server.anki_connect import make_anki_request
from anki_mcp_server.decks.models import DeckList, ErrorResponse


async def list_decks() -> DeckList | ErrorResponse:
    """Get the names of all decks from Anki"""
    try:
        decks = await make_anki_request("deckNames")
        return DeckList(decks=decks)
    except Exception as e:
        return ErrorResponse(error=str(e), operation="retrieving decks")


def register_decks_tools(mcp: FastMCP):
    mcp.tool(list_decks)
    
