class CrossModalService:
    def analyze(self, optical_image_id: str, sar_image_id: str, query: str | None = None, aoi: dict | None = None) -> dict:
        return {
            "status": "unavailable",
            "optical_source": optical_image_id,
            "sar_source": sar_image_id,
            "analysis_type": "optical_sar_fusion",
            "error": "Cross-modal model provider is currently unavailable.",
            "execution_time_ms": None
        }

cross_modal_service = CrossModalService()
