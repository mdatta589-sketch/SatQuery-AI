from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
import time
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/vqa", tags=["VQA"])

class VqaRequest(BaseModel):
    image_id: str
    image_type: str
    source: str
    modality: str
    representation: str
    question: str
    mode: str = "vqa"
    aoi: dict | None = None

class ExecutionInfo(BaseModel):
    model: Optional[str] = None
    provider: str = "remote"
    status: str
    grounding: Dict[str, Any] = {"provider": "none", "status": "not_connected"}

class VqaResponse(BaseModel):
    request_id: str
    task: str
    image_id: str
    question: str
    answer: str
    confidence: Optional[float] = None
    confidence_status: str
    evidence: List[Dict[str, Any]]
    execution: ExecutionInfo

@router.post("/query", response_model=VqaResponse)
async def query_vqa(request: VqaRequest):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    # 1. Validation
    if not request.image_id:
        raise HTTPException(status_code=400, detail="image_id is required.")
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="question is required.")
        
    # 2. VQA Service execution
    from app.models.vqa.service import vqa_service
    
    result = await vqa_service.answer(
        aoi=request.aoi,
        image_id=request.image_id,
        image_type=request.image_type,
        modality=request.modality,
        representation=request.representation,
        question=request.question.strip()
    )
    
    status = result.get("status", "error")
    http_status = result.get("http_status", 200)
    
    if http_status != 200 and status == "error":
        raise HTTPException(status_code=http_status, detail=result.get("error", "Unknown error"))
    
    answer_text = result.get("answer")
    if not answer_text and status == "not_configured":
        answer_text = "VQA provider not configured."
    elif not answer_text:
        answer_text = "Unknown error"
        
    # 3. Grounding Service execution (Response Fusion)
    evidence_list = []
    grounding_trace = {"provider": "none", "status": "not_connected"}
    
    if status == "success" and answer_text:
        from app.models.grounding.service import grounding_service
        evidence_list, grounding_trace = await grounding_service.get_evidence(
            image_id=request.image_id,
            image_type=request.image_type,
            modality=request.modality,
            representation=request.representation,
            question=request.question.strip(),
            answer=answer_text
        )
    
    response = VqaResponse(
        request_id=request_id,
        task="vqa",
        image_id=request.image_id,
        question=request.question.strip(),
        answer=answer_text,
        confidence=result.get("confidence"),
        confidence_status=result.get("confidence_status", "not_calibrated"),
        evidence=evidence_list,
        execution=ExecutionInfo(
            model=result.get("model", "None"),
            provider=result.get("provider", "remote"),
            status=status,
            grounding=grounding_trace
        )
    )
    
    # 4. Logging
    exec_time = time.time() - start_time
    logger.info(f"request_id={request_id} image_id={request.image_id} type={request.image_type} repr={request.representation} source={request.source} modality={request.modality} task=vqa status={status} model={result.get('model')} execution_time={exec_time:.3f}s question='{request.question}'")
    logger.info(f"Execution trace: {result.get('trace')}")
    logger.info(f"Grounding trace: {grounding_trace}")
        
    return response
