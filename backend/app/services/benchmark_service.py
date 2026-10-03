class BenchmarkService:
    def get_status(self) -> list[dict]:
        return [
            {
                "dataset": "RSVQAxBEN",
                "task": "vqa",
                "model": "google/paligemma-3b-ft-rsvqa-hr-224",
                "metric": "accuracy",
                "score": None,
                "status": "not_evaluated"
            },
            {
                "dataset": "DIOR",
                "task": "grounding",
                "model": "GroundingDINO_SwinT_OGC",
                "metric": "mAP",
                "score": None,
                "status": "not_evaluated"
            }
        ]

benchmark_service = BenchmarkService()
