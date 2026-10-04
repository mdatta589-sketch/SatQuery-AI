from fastapi import APIRouter
from app.schemas.change import ChangeAnalysisRequest, ChangeAnalysisResponse, ChangeVQARequest, ChangeVQAResponse
from app.services.change_service import change_service

router = APIRouter(prefix="/api/v1/change", tags=["Change Analysis"])

@router.post("/analyze", response_model=ChangeAnalysisResponse)
def analyze_change(request: ChangeAnalysisRequest):
    result = change_service.analyze_change(
        image_before_id=request.image_before_id,
        image_after_id=request.image_after_id,
        aoi=request.aoi
    )
    return ChangeAnalysisResponse(**result)

@router.post("/vqa", response_model=ChangeVQAResponse)
def change_vqa(request: ChangeVQARequest):
    result = change_service.answer_change_vqa(
        image_before_id=request.image_before_id,
        image_after_id=request.image_after_id,
        question=request.question,
        aoi=request.aoi
    )
    return ChangeVQAResponse(**result)
