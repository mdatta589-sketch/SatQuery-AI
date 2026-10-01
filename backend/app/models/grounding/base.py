from abc import ABC, abstractmethod
from typing import List
from app.schemas.evidence import EvidenceItem

class GroundingProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @abstractmethod
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
        """
        Takes the original image, question, and VQA answer and returns 
        a list of spatial evidence items.
        """
        pass
