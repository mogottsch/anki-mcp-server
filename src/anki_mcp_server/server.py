from fastmcp import FastMCP

from anki_mcp_server.decks.tools import register_decks_tools
from anki_mcp_server.models.tools import register_models_tools
from anki_mcp_server.notes.tools import register_notes_tools

mcp = FastMCP("anki-mcp-server")

register_decks_tools(mcp)
register_models_tools(mcp)
register_notes_tools(mcp)


http_app = mcp.http_app()
