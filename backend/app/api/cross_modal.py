from fastapi import APIRouter
from app.schemas.cross_modal import CrossModalRequest, CrossModalResponse
from app.services.cross_modal_service import cross_modal_service

router = APIRouter(prefix="/api/v1/cross-modal", tags=["Cross-Modal"])

@router.post("/analyze", response_model=CrossModalResponse)
async def analyze_cross_modal(request: CrossModalRequest):
    result = cross_modal_service.analyze(
        optical_image_id=request.optical_image_id,
        sar_image_id=request.sar_image_id,
        query=request.query,
        aoi=request.aoi
    )
    return CrossModalResponse(**result)
