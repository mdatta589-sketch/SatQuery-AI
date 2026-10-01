from typing import List, Optional, Any
from pydantic import BaseModel

class EvidenceGeometry(BaseModel):
    type: str  # "bbox", "polygon", "point"
    coordinates: Any  # Geometry coordinates
    coordinate_system: str  # "image_pixel", "map", "wgs84"

class EvidenceItem(BaseModel):
    evidence_id: str
    type: str
    label: str
    geometry: EvidenceGeometry
    source: str
    confidence: Optional[float] = None
    description: Optional[str] = None
