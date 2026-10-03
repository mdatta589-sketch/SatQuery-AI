from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class RouterRequest(BaseModel):
    question: str
    context: Optional[Dict[str, Any]] = None

class RouterResponse(BaseModel):
    task: str
    confidence: float
    reason: str
