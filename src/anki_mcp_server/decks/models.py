from pydantic import BaseModel

class DeckList(BaseModel):
    decks: list[str]

class ErrorResponse(BaseModel):
    error: str
    operation: str 