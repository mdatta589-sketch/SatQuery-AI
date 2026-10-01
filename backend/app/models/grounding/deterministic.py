from typing import List
from app.schemas.evidence import EvidenceItem
from .base import GroundingProvider

class DeterministicGroundingProvider(GroundingProvider):
    """
    A safe, deterministic grounding provider that returns empty evidence
    unless connected to a real detector. This ensures we never hallucinate
    spatial evidence.
    """
    
    @property
    def provider_name(self) -> str:
        return "none"

    async def get_evidence(
        self,
        image_path: str,
        question: str,
        answer: str,
        image_id: str,
        modality: str,
        representation: str,
        prompt: str = ""
    ) -> tuple[List[EvidenceItem], dict]:
        # Do NOT invent fake geometry
        # Return empty list until a real detector is hooked up
        return [], {"provider": self.provider_name, "status": "not_connected"}
