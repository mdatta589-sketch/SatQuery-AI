import os
import logging
from typing import List, Dict, Any, Tuple
from app.schemas.evidence import EvidenceItem
from .deterministic import DeterministicGroundingProvider
from .remote_provider import RemoteGroundingProvider
from .prompt import build_grounding_prompt
from app.models.vqa.preprocessing import prepare_image

logger = logging.getLogger(__name__)

class GroundingService:
    def __init__(self):
        provider_type = os.getenv("SATQUERY_GROUNDING_PROVIDER", "deterministic")
        if provider_type == "remote":
            self.provider = RemoteGroundingProvider()
        else:
            self.provider = DeterministicGroundingProvider()

    async def get_evidence(
        self,
        image_id: str,
        image_type: str,
        modality: str,
        representation: str,
        question: str,
        answer: str
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Returns (evidence_list, execution_trace).
        """
        prompt = build_grounding_prompt(question, answer)
        if not prompt:
            return [], {
                "provider": self.provider.provider_name,
                "status": "not_applicable"
            }
            
        execution_trace = {
            "provider": self.provider.provider_name,
            "status": "not_connected"
        }
        
        try:
            image_path = prepare_image(image_id, image_type)
            
            evidence_items, execution_trace = await self.provider.get_evidence(
                image_path=image_path,
                question=question,
                answer=answer,
                image_id=image_id,
                modality=modality,
                representation=representation,
                prompt=prompt
            )
            
            return [e.model_dump() for e in evidence_items], execution_trace
            
        except Exception as e:
            logger.error(f"Grounding service error: {e}")
            execution_trace["status"] = "error"
            return [], execution_trace

grounding_service = GroundingService()
