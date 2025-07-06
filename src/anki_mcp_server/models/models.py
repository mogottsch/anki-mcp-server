from pydantic import BaseModel
from typing import Any

class ModelList(BaseModel):
    models: list[str]

class ModelDetails(BaseModel):
    model_name: str
    details: Any

class ErrorResponse(BaseModel):
    error: str
    operation: str 