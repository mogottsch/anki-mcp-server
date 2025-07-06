from typing import Any

from fastmcp import FastMCP
from anki_mcp_server.anki_connect import make_anki_request
from anki_mcp_server.notes.models import (
    NoteInfo,
    NoteCreated,
    NoteUpdated,
    ErrorResponse,
    NoteList,
)


async def add_note(
    deck_name: str,
    model_name: str,
    fields: dict[str, str],
    tags: list[str] | None = None,
) -> NoteCreated | ErrorResponse:
    """Add a new note to Anki."""
    try:
        note = {
            "deckName": deck_name,
            "modelName": model_name,
            "fields": fields,
            "tags": tags or [],
        }
        note_id = await make_anki_request("addNote", {"note": note})
        return NoteCreated(note_id=note_id)
    except Exception as e:
        return ErrorResponse(error=str(e), operation="add_note")


async def get_note(note_id: int) -> NoteInfo | ErrorResponse:
    """Get info for a note by note_id."""
    try:
        notes = await make_anki_request("notesInfo", {"notes": [note_id]})
        if not notes:
            return ErrorResponse(error="Note not found", operation="get_note")
        note = notes[0]
        fields = {k: v["value"] for k, v in note["fields"].items()}
        return NoteInfo(
            note_id=note["noteId"],
            fields=fields,
            tags=note["tags"],
            card_ids=note["cards"],
        )
    except Exception as e:
        return ErrorResponse(error=str(e), operation="get_note")


async def update_note(
    note_id: int, fields: dict[str, str] | None = None, tags: list[str] | None = None
) -> NoteUpdated | ErrorResponse:
    """Update fields and tags for a note by note_id."""
    try:
        params: dict[str, Any] = {"note": {"id": note_id}}
        if fields is not None:
            params["note"]["fields"] = fields
        if tags is not None:
            params["note"]["tags"] = tags
        await make_anki_request("updateNoteFields", params)
        return NoteUpdated(note_id=note_id)
    except Exception as e:
        return ErrorResponse(error=str(e), operation="update_note")


async def list_notes_in_deck(deck_name: str) -> NoteList | ErrorResponse:
    try:
        note_ids = await make_anki_request(
            "findNotes", {"query": f'deck:"{deck_name}"'}
        )
        if not note_ids:
            return NoteList(notes=[])
        notes = await make_anki_request("notesInfo", {"notes": note_ids})
        note_infos = [
            NoteInfo(
                note_id=note["noteId"],
                fields={k: v["value"] for k, v in note["fields"].items()},
                tags=note["tags"],
                card_ids=note["cards"],
            )
            for note in notes
        ]
        return NoteList(notes=note_infos)
    except Exception as e:
        print(e)
        return ErrorResponse(error=str(e), operation="list_notes_in_deck")


def register_notes_tools(mcp: FastMCP):
    mcp.tool(add_note)
    mcp.tool(get_note)
    mcp.tool(update_note)
    mcp.tool(list_notes_in_deck)
