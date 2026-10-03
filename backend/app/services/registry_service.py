class RegistryService:
    def get_models(self) -> list[dict]:
        return [
            {
                "task": "vqa",
                "model": "google/paligemma-3b-ft-rsvqa-hr-224",
                "provider": "remote",
                "endpoint": "/vqa",
                "status": "active"
            },
            {
                "task": "grounding",
                "model": "GroundingDINO_SwinT_OGC",
                "provider": "remote",
                "endpoint": "/ground",
                "status": "active"
            },
            {
                "task": "change_vqa",
                "model": "future-change-model",
                "provider": "remote",
                "endpoint": None,
                "status": "unavailable"
            },
            {
                "task": "cross_modal",
                "model": "future-sar-optical-model",
                "provider": "remote",
                "endpoint": None,
                "status": "unavailable"
            }
        ]

registry_service = RegistryService()
