import logging
import os
from app.models.vqa.remote_provider import RemoteVQAProvider
from app.models.vqa.preprocessing import validate_image_representation, prepare_image

logger = logging.getLogger(__name__)

class VQAService:
    def __init__(self):
        self.provider_type = os.getenv("SATQUERY_VQA_PROVIDER", "remote")
        # Currently we only support remote
        self.provider = RemoteVQAProvider()

    async def answer(self, image_id: str, image_type: str, modality: str, representation: str, question: str, aoi: dict | None = None) -> dict:
        trace = []
        
        # Step 1: Input Validation
        if not validate_image_representation(image_type, representation):
            trace.append({"step": "input_validation", "status": "error"})
            return {
                "answer": None,
                "model": getattr(self.provider, "model_name", "Unknown"),
                "provider": self.provider_type,
                "status": "error",
                "error": "VQA currently requires an RGB image. Select Sentinel-2 True Color or upload an RGB image.",
                "http_status": 409,
                "trace": trace
            }
        trace.append({"step": "input_validation", "status": "success"})

        # Step 2: Image Preparation
        try:
            image_path = prepare_image(image_id, image_type, aoi)
            trace.append({"step": "image_preparation", "status": "success"})
        except Exception as e:
            trace.append({"step": "image_preparation", "status": "error"})
            return {
                "answer": None,
                "model": getattr(self.provider, "model_name", "Unknown"),
                "provider": self.provider_type,
                "status": "error",
                "error": f"Failed to prepare image: {str(e)}",
                "http_status": 500,
                "trace": trace
            }

        # Step 3: VQA Model Inference
        try:
            result = await self.provider.answer(
                image_path=image_path,
                question=question,
                image_id=image_id,
                modality=modality,
                representation=representation
            )
            status = result.get("status", "error")
            if status == "success":
                trace.append({"step": "vqa_model", "status": "success"})
            else:
                trace.append({"step": "vqa_model", "status": status})
                
            return {
                "answer": result.get("answer"),
                "confidence": result.get("confidence"),
                "confidence_status": result.get("confidence_status", "not_calibrated"),
                "evidence": result.get("evidence", []),
                "model": result.get("model", getattr(self.provider, "model_name", "Unknown")),
                "provider": self.provider_type,
                "status": status,
                "error": result.get("error"),
                "http_status": result.get("http_status", 500 if status == "error" else 200),
                "trace": trace
            }
        except Exception as e:
            trace.append({"step": "vqa_model", "status": "error"})
            return {
                "answer": None,
                "model": getattr(self.provider, "model_name", "Unknown"),
                "provider": self.provider_type,
                "status": "error",
                "error": f"Unexpected inference error: {str(e)}",
                "http_status": 500,
                "trace": trace
            }

# Singleton instance for the API to import and use
vqa_service = VQAService()
