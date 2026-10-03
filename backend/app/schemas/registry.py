from pydantic import BaseModel
from typing import Optional, List

class ModelRegistryEntry(BaseModel):
    task: str
    model: str
    provider: str
    endpoint: Optional[str] = None
    status: str

class ModelRegistryResponse(BaseModel):
    models: List[ModelRegistryEntry]
