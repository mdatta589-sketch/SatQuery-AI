import os
import httpx
from .provider import VQAProvider
import logging

logger = logging.getLogger(__name__)

class RemoteVQAProvider(VQAProvider):
    def __init__(self):
        self.url = os.getenv("SATQUERY_VQA_URL")
        self.timeout = int(os.getenv("SATQUERY_VQA_TIMEOUT", "120"))
        self.model_name = "google/paligemma-3b-ft-rsvqa-hr-224"

    async def answer(
        self,
        image_path: str,
        question: str,
        image_id: str,
        modality: str,
        representation: str
    ) -> dict:
        
        if not self.url:
            return {
                "status": "not_configured",
                "answer": None,
                "confidence": None,
                "confidence_status": "not_calibrated",
                "evidence": [],
                "model": self.model_name,
                "error": "Remote VQA provider is not configured."
            }

        if not os.path.exists(image_path):
            logger.error(f"Image path does not exist: {image_path}")
            return {
                "status": "error",
                "answer": None,
                "confidence": None,
                "confidence_status": "not_calibrated",
                "evidence": [],
                "model": self.model_name,
                "error": "Selected VQA image could not be prepared.",
                "http_status": 500
            }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Prepare multipart/form-data payload with actual bytes
                with open(image_path, "rb") as f:
                    image_bytes = f.read()
                    
                files = {
                    "image": (os.path.basename(image_path), image_bytes, "image/png")
                }
                data = {
                    "question": question,
                    "image_id": image_id,
                    "modality": modality,
                    "representation": representation
                }
                
                response = await client.post(self.url, data=data, files=files)
                
                if response.status_code == 200:
                    res_json = response.json()
                    return {
                        "answer": res_json.get("answer"),
                        "confidence": res_json.get("confidence"),
                        "confidence_status": res_json.get("confidence_status", "not_calibrated"),
                        "evidence": res_json.get("evidence", []),
                        "model": res_json.get("model", self.model_name),
                        "status": "success"
                    }
                else:
                    logger.error(f"Remote provider HTTP {response.status_code}: {response.text[:200]}")
                    return {
                        "status": "error",
                        "answer": None,
                        "confidence": None,
                        "confidence_status": "not_calibrated",
                        "evidence": [],
                        "model": self.model_name,
                        "error": "Remote VQA provider is currently unavailable.",
                        "http_status": 502
                    }
        except httpx.TimeoutException:
            logger.error("Remote VQA provider timed out.")
            return {
                "status": "error",
                "answer": None,
                "confidence": None,
                "confidence_status": "not_calibrated",
                "evidence": [],
                "model": self.model_name,
                "error": "Remote VQA provider timed out.",
                "http_status": 504
            }
        except Exception as e:
            logger.error(f"Remote VQA provider failure: {str(e)}")
            return {
                "status": "error",
                "answer": None,
                "confidence": None,
                "confidence_status": "not_calibrated",
                "evidence": [],
                "model": self.model_name,
                "error": "Remote VQA provider is currently unavailable.",
                "http_status": 502
            }
