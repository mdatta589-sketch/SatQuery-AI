from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter(prefix="/api/v1/grounding", tags=["Grounding"])

class GroundingRequest(BaseModel):
    image_id: str
    image_type: str
    modality: str
    representation: str
    question: str
    answer: str

@router.post("/query")
async def query_grounding(request: GroundingRequest):
    # As per prompt, API returns empty/not_connected
    
    # Normally we would call:
    # from app.models.grounding.service import grounding_service
    # evidence, execution = await grounding_service.get_evidence(...)
    
    return {
        "status": "not_connected",
        "evidence": [],
        "confidence_status": "not_calibrated",
        "execution": {
            "provider": "none",
            "status": "not_connected"
        }
    }
