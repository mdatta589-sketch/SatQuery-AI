from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import Response
import io
import cv2
import numpy as np
from app.services.cross_modal_service import cross_modal_service, CROSS_MODAL_CACHE

router = APIRouter(prefix="/api/v1/cross-modal", tags=["Cross-Modal"])

class CrossModalRequest(BaseModel):
    optical_image_id: str
    sar_image_id: str
    question: str
    aoi: dict

@router.post("/analyze")
def analyze(request: CrossModalRequest):
    if not request.optical_image_id or not request.sar_image_id:
        raise HTTPException(status_code=400, detail="Cross-modal analysis requires both an optical/multispectral image and a SAR image.")
        
    result = cross_modal_service.analyze(
        optical_id=request.optical_image_id,
        sar_id=request.sar_image_id,
        aoi=request.aoi
    )
    
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("error"))
        
    return result

@router.get("/result/{result_id}/image.png")
def get_result_image(result_id: str):
    if result_id not in CROSS_MODAL_CACHE:
        raise HTTPException(status_code=404, detail="Result not found or expired")
        
    data = CROSS_MODAL_CACHE[result_id]
    img = data['image'] # (3, H, W)
    
    # OpenCV expects (H, W, C) in BGR
    # We stored as RGB in (3, H, W)
    # Transpose to (H, W, 3)
    img_hwc = np.transpose(img, (1, 2, 0))
    # Convert RGB to BGR for cv2
    img_bgr = cv2.cvtColor(img_hwc, cv2.COLOR_RGB2BGR)
    
    is_success, buffer = cv2.imencode(".png", img_bgr)
    if not is_success:
        raise HTTPException(status_code=500, detail="Failed to encode image")
        
    return Response(content=buffer.tobytes(), media_type="image/png")
