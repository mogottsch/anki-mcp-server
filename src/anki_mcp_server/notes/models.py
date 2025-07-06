from pydantic import BaseModel

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

class ErrorResponse(BaseModel):
    error: str
    operation: str 
