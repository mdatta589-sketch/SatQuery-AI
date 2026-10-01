from abc import ABC, abstractmethod

class VQAProvider(ABC):
    @abstractmethod
    async def answer(
        self,
        image_path: str,
        question: str,
        image_id: str,
        modality: str,
        representation: str
    ) -> dict:
        """
        Takes an image path and a question, and returns a dictionary matching:
        {
            "answer": "...",
            "confidence": null,
            "confidence_status": "not_calibrated",
            "evidence": [],
            "model": "google/paligemma-3b-ft-rsvqa-hr-224",
            "status": "success"
        }
        """
        pass
