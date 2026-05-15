from pydantic import BaseModel


class MediaFile(BaseModel):
    """A media file to be attached to a note."""
    filename: str
    url: str | None = None
    path: str | None = None
    data: str | None = None
    skip_hash: str | None = None
    fields: list[str]


class MediaStored(BaseModel):
    filename: str


class MediaDirPath(BaseModel):
    path: str


class NoteInfo(BaseModel):
    note_id: int
    fields: dict[str, str]
    tags: list[str]
    card_ids: list[int]


class NoteList(BaseModel):
    notes: list[NoteInfo]


class NoteCreated(BaseModel):
    note_id: int


class NoteUpdated(BaseModel):
    note_id: int


class NoteMoved(BaseModel):
    note_id: int
    deck_name: str
    card_ids: list[int]


class NoteDeleted(BaseModel):
    note_id: int


class ErrorResponse(BaseModel):
    error: str
    operation: str
