from typing import Any
import json

from fastmcp import FastMCP

from anki_mcp_server.anki_connect import make_anki_request
from anki_mcp_server.notes.models import (
    ErrorResponse,
    MediaDirPath,
    MediaFile,
    MediaStored,
    NoteCreated,
    NoteDeleted,
    NoteInfo,
    NoteList,
    NoteMoved,
    NoteUpdated,
)


async def add_note(
    deck_name: str,
    model_name: str,
    fields: dict[str, str],
    tags: list[str] = [],
    picture: list[MediaFile] = [],
    audio: list[MediaFile] = [],
    video: list[MediaFile] = [],
) -> NoteCreated | ErrorResponse:
    """Add a new note to Anki with optional media attachments.

    Media files can be specified with a url, path, or base64-encoded data.
    The media will be appended to the fields specified in the media object's fields list.
    """
    try:
        note: dict[str, Any] = {
            "deckName": deck_name,
            "modelName": model_name,
            "fields": fields,
            "tags": tags or [],
        }

        if picture:
            note["picture"] = [p.model_dump(exclude_none=True) for p in picture]
        if audio:
            note["audio"] = [a.model_dump(exclude_none=True) for a in audio]
        if video:
            note["video"] = [v.model_dump(exclude_none=True) for v in video]

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
    note_id: int,
    fields: dict[str, str] | str | None = None,
    tags: list[str] = [],
) -> NoteUpdated | ErrorResponse:
    """Update fields and tags for a note by note_id.

    Fields can be provided as a dictionary or a JSON string.
    Tags: only updates if a non-empty list is provided.
    """
    try:
        params: dict[str, Any] = {"note": {"id": note_id}}
        if fields is not None:
            # Handle both dict and JSON string inputs
            if isinstance(fields, str):
                params["note"]["fields"] = json.loads(fields)
            else:
                params["note"]["fields"] = fields
        # Only update tags if explicitly provided (non-empty list)
        if tags:
            params["note"]["tags"] = tags
        await make_anki_request("updateNote", params)
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


async def move_note_to_deck(note_id: int, deck_name: str) -> NoteMoved | ErrorResponse:
    """Move a note's cards into the specified deck.

    Notes in Anki are associated with one or more cards; decks are assigned per-card.
    This tool moves all cards for the note into the target deck.
    """
    try:
        # Ensure the deck exists (safe even if it already exists).
        await make_anki_request("createDeck", {"deck": deck_name})

        notes = await make_anki_request("notesInfo", {"notes": [note_id]})
        if not notes:
            return ErrorResponse(error="Note not found", operation="move_note_to_deck")

        note = notes[0]
        card_ids: list[int] = note.get("cards", [])

        if card_ids:
            await make_anki_request(
                "changeDeck", {"cards": card_ids, "deck": deck_name}
            )

        return NoteMoved(note_id=note_id, deck_name=deck_name, card_ids=card_ids)
    except Exception as e:
        return ErrorResponse(error=str(e), operation="move_note_to_deck")


async def delete_note(note_id: int) -> NoteDeleted | ErrorResponse:
    """Delete a note by note_id."""
    try:
        await make_anki_request("deleteNotes", {"notes": [note_id]})
        return NoteDeleted(note_id=note_id)
    except Exception as e:
        return ErrorResponse(error=str(e), operation="delete_note")


async def add_deck(deck_name: str) -> dict[str, str]:
    try:
        await make_anki_request("createDeck", {"deck": deck_name})
        return {"status": "success", "deck_name": deck_name}
    except Exception as e:
        return {"status": "error", "error": str(e), "operation": "add_deck"}


async def store_media_file(
    filename: str,
    data: str | None = None,
    path: str | None = None,
    url: str | None = None,
    delete_existing: bool | None = None,
) -> MediaStored | ErrorResponse:
    """Store a media file in Anki's media folder.

    Provide one of data (base64), path, or url.
    Returns the filename as stored in Anki.
    """
    try:
        params: dict[str, Any] = {"filename": filename}
        if data is not None:
            params["data"] = data
        if path is not None:
            params["path"] = path
        if url is not None:
            params["url"] = url
        if delete_existing is not None:
            params["deleteExisting"] = delete_existing

        stored_filename = await make_anki_request("storeMediaFile", params)
        return MediaStored(filename=stored_filename)
    except Exception as e:
        return ErrorResponse(error=str(e), operation="store_media_file")


async def get_media_dir_path() -> MediaDirPath | ErrorResponse:
    """Get the full path to Anki's collection.media folder."""
    try:
        path = await make_anki_request("getMediaDirPath")
        return MediaDirPath(path=path)
    except Exception as e:
        return ErrorResponse(error=str(e), operation="get_media_dir_path")


def register_notes_tools(mcp: FastMCP[Any]):
    mcp.tool(add_note)
    mcp.tool(get_note)
    mcp.tool(update_note)
    mcp.tool(list_notes_in_deck)
    mcp.tool(move_note_to_deck)
    mcp.tool(delete_note)
    mcp.tool(add_deck)
    mcp.tool(store_media_file)
    mcp.tool(get_media_dir_path)
