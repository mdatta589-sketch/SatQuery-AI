from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class CrossModalRequest(BaseModel):
    optical_image_id: str
    sar_image_id: str
    query: Optional[str] = None
    aoi: Optional[Dict[str, Any]] = None

class CrossModalResponse(BaseModel):
    status: str
    optical_source: str
    sar_source: str
    analysis_type: str
    result: Optional[Any] = None
    evidence: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    execution_time_ms: Optional[int] = None
