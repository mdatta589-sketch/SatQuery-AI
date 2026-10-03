from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ChangeAnalysisRequest(BaseModel):
    image_before_id: str
    image_after_id: str
    aoi: Optional[Dict[str, Any]] = None

class ChangeAnalysisResponse(BaseModel):
    status: str
    change_percentage: Optional[float] = None
    changed_pixel_count: Optional[int] = None
    total_valid_pixel_count: Optional[int] = None
    method: str
    evidence: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    execution_time_ms: Optional[int] = None

class ChangeVQARequest(BaseModel):
    image_before_id: str
    image_after_id: str
    question: str
    aoi: Optional[Dict[str, Any]] = None

class ChangeVQAResponse(BaseModel):
    status: str
    answer: Optional[str] = None
    model: str
    provider: str
    evidence: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    execution_time_ms: Optional[int] = None
