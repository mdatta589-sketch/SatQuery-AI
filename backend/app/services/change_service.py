class ChangeService:
    def analyze_change(self, image_before_id: str, image_after_id: str, aoi: dict | None = None) -> dict:
        return {
            "status": "not_implemented",
            "method": "stub",
            "error": "Change analysis is not yet implemented.",
            "execution_time_ms": None
        }

    def answer_change_vqa(self, image_before_id: str, image_after_id: str, question: str, aoi: dict | None = None) -> dict:
        return {
            "status": "unavailable",
            "model": "unknown",
            "provider": "remote_gpu",
            "error": "Change-VQA model provider is currently unavailable.",
            "execution_time_ms": None
        }

change_service = ChangeService()
