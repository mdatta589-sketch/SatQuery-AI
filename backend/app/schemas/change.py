from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ChangeAnalysisRequest(BaseModel):
    image_before_id: str
    image_after_id: str
    aoi: Optional[Dict[str, Any]] = None

class ChangeAnalysisResponse(BaseModel):
    status: str
    method: str
    image_before_id: str
    image_after_id: str
    changed_pixel_count: Optional[int] = None
    total_valid_pixel_count: Optional[int] = None
    change_percentage: Optional[float] = None
    threshold: Optional[float] = None
    message: Optional[str] = None
    evidence: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    execution_time_ms: Optional[int] = None

class ChangeVQARequest(BaseModel):
    image_before_id: str
    image_after_id: str
    question: str
    aoi: Optional[Dict[str, Any]] = None

class ChangeVQAResponse(BaseModel):
    task: str = "change_vqa"
    status: str
    question: Optional[str] = None
    answer: Optional[str] = None
    change_percentage: Optional[float] = None
    changed_pixel_count: Optional[int] = None
    total_valid_pixel_count: Optional[int] = None
    threshold: Optional[float] = None
    method: Optional[str] = None
    before_scene: Optional[str] = None
    after_scene: Optional[str] = None
    evidence: Optional[List[Dict[str, Any]]] = None
    execution: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time_ms: Optional[int] = None