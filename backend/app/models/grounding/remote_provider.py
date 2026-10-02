import os
import httpx
import logging
from typing import List
import uuid
from app.schemas.evidence import EvidenceItem, EvidenceGeometry
from .base import GroundingProvider
from app.processing.geometry import pixel_to_geographic

logger = logging.getLogger(__name__)

class RemoteGroundingProvider(GroundingProvider):
    def __init__(self):
        self.url = os.getenv("SATQUERY_GROUNDING_URL", "")
        self.timeout = int(os.getenv("SATQUERY_GROUNDING_TIMEOUT", "120"))
        self._provider_name = "grounding_dino"

    @property
    def provider_name(self) -> str:
        return self._provider_name

    async def get_evidence(
        self,
        image_path: str,
        question: str,
        answer: str,
        image_id: str,
        modality: str,
        representation: str,
        prompt: str
    ) -> tuple[List[EvidenceItem], dict]:
        """
        Calls the remote Grounding DINO provider.
        Returns (evidence_items, execution_info)
        """
        execution_info = {
            "provider": self.provider_name,
            "status": "success"
        }
        
        if not self.url:
            execution_info["status"] = "not_configured"
            return [], execution_info

        if not os.path.exists(image_path):
            logger.error(f"Grounding image path does not exist: {image_path}")
            execution_info["status"] = "error"
            return [], execution_info

        error_state = {
            "provider": self.provider_name,
            "status": "error",
            "error": {
                "code": "REMOTE_GROUNDING_PROVIDER_UNAVAILABLE",
                "message": "Remote grounding provider is currently unavailable."
            }
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                with open(image_path, "rb") as f:
                    image_bytes = f.read()
                    
                files = {
                    "image": (os.path.basename(image_path), image_bytes, "image/png")
                }
                data = {
                    "text": prompt,
                    "box_threshold": "0.30",
                    "text_threshold": "0.25",
                    "image_id": image_id,
                    "modality": modality,
                    "representation": representation
                }
                
                response = await client.post(self.url, data=data, files=files)
                
                if response.status_code == 200:
                    res_json = response.json()
                    status = res_json.get("status", "error")
                    
                    if status != "success":
                        return [], error_state
                        
                    evidence_list = []
                    for idx, ev in enumerate(res_json.get("detections", [])):
                        box = ev.get("box", [])
                        
                        coords = box
                        coord_sys = "image_pixel"
                        
                        if len(box) == 4:
                            # Try mapping pixel to geographic
                            x1, y1, x2, y2 = box
                            lon1, lat1 = pixel_to_geographic(image_path, x1, y1)
                            lon2, lat2 = pixel_to_geographic(image_path, x2, y2)
                            
                            if lon1 is not None and lat1 is not None and lon2 is not None and lat2 is not None:
                                coords = [lon1, lat1, lon2, lat2]
                                coord_sys = "wgs84"
                        
                        evidence_list.append(EvidenceItem(
                            evidence_id=f"ground_{idx}_{uuid.uuid4().hex[:8]}",
                            type="bbox",
                            label=ev.get("phrase", "unknown"),
                            geometry=EvidenceGeometry(
                                type="bbox",
                                coordinates=coords,
                                coordinate_system=coord_sys
                            ),
                            source="grounding_model",
                            confidence=ev.get("score")
                        ))
                    
                    execution_info["count"] = len(evidence_list)
                    return evidence_list, execution_info
                else:
                    logger.error(f"Remote grounding provider HTTP {response.status_code}: {response.text[:200]}")
                    error_state["error"]["message"] = f"HTTP {response.status_code}: {response.text[:200]}"
                    return [], error_state
                    
        except httpx.TimeoutException:
            logger.error("Remote grounding provider timed out.")
            return [], error_state
        except Exception as e:
            logger.error(f"Remote grounding provider failure: {str(e)}")
            return [], error_state
