from pydantic import BaseModel

class SyncResponse(BaseModel):
    success: bool
    message: str

class ErrorResponse(BaseModel):
    error: str
    operation: str 