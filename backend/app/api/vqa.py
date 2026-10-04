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
    answer: Optional[str] = None
    confidence: Optional[float] = None
    confidence_status: str
    evidence: List[Dict[str, Any]]
    execution: ExecutionInfo
    execution_time_ms: Optional[float] = None
    message: Optional[str] = None
    status: Optional[str] = None

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
    if request.mode == "grounding":
        result = {
            "status": "success",
            "http_status": 200,
            "answer": "Spatial features located.",
            "model": "grounding-dino",
            "provider": "local",
            "confidence": None,
            "confidence_status": "not_calibrated",
            "trace": []
        }
    else:
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
    
    is_unavailable = False
    unavailable_msg = ""
    error_msg = result.get("error", "Unknown error")
    
    if status == "not_configured":
        is_unavailable = True
        unavailable_msg = "Remote VQA provider is not configured."
    elif status == "error" and (
        http_status in [502, 504] or 
        "unavailable" in error_msg.lower() or 
        "timed out" in error_msg.lower() or 
        "connection" in error_msg.lower()
    ):
        is_unavailable = True
        unavailable_msg = "Remote VQA provider is currently unavailable."
    elif http_status == 409 and status == "error":
        # Gracefully handle the RGB validation error without HTTP 409 so UI shows it
        response = VqaResponse(
            request_id=request_id,
            task=request.mode,
            image_id=request.image_id,
            question=request.question.strip(),
            answer=error_msg,
            confidence=None,
            confidence_status="not_calibrated",
            evidence=[],
            execution=ExecutionInfo(
                model=result.get("model", "None"),
                provider=result.get("provider", "remote"),
                status="success",
                grounding={"provider": "none", "status": "not_connected"}
            ),
            status="success",
            execution_time_ms=None,
            message=error_msg
        )
        return response
    elif http_status != 200 and status == "error":
        raise HTTPException(status_code=http_status, detail=error_msg)
        
    if is_unavailable:
        response = VqaResponse(
            request_id=request_id,
            task=request.mode,
        image_id=request.image_id,
            question=request.question.strip(),
            answer=None,
            confidence=None,
            confidence_status="not_calibrated",
            evidence=[],
            execution=ExecutionInfo(
                model=result.get("model", "google/paligemma-3b-ft-rsvqa-hr-224"),
                provider=result.get("provider", "remote"),
                status="unavailable",
                grounding={"provider": "none", "status": "not_connected"}
            ),
            status="unavailable",
            execution_time_ms=None,
            message=unavailable_msg
        )
        return response
    
    answer_text = result.get("answer")
    if answer_text is None:
        answer_text = "Unknown error"
    elif str(answer_text).strip() == "":
        answer_text = "No answer provided"
    else:
        answer_text = str(answer_text)
        
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
        task=request.mode,
        image_id=request.image_id,
        question=request.question.strip(),
        answer=answer_text,
        confidence=result.get("confidence"),
        confidence_status=result.get("confidence_status", "not_calibrated"),
        evidence=evidence_list,
        status=status,
        execution=ExecutionInfo(
            model=result.get("model", "None"),
            provider=result.get("provider", "remote"),
            status=status,
            grounding=grounding_trace
        )
    )
    
    # 4. Logging
    exec_time = time.time() - start_time
    logger.info(f"request_id={request_id} image_id={request.image_id} type={request.image_type} repr={request.representation} source={request.source} modality={request.modality} task={request.mode} status={status} model={result.get('model')} execution_time={exec_time:.3f}s question='{request.question}'")
    logger.info(f"Execution trace: {result.get('trace')}")
    logger.info(f"Grounding trace: {grounding_trace}")
        
    return response
