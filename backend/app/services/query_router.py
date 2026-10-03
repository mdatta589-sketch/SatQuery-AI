class QueryRouter:
    def route(self, question: str) -> dict:
        q = question.lower()
        if "change" in q or "before and after" in q:
            if "where" in q or "what" in q or "did" in q:
                return {"task": "change_vqa", "confidence": 0.85, "reason": "Keyword match for change question"}
            return {"task": "change", "confidence": 0.9, "reason": "Keyword match for change analysis"}
        elif "sar" in q and ("optical" in q or "compare" in q):
            return {"task": "cross_modal", "confidence": 0.95, "reason": "Keywords for cross-modal SAR/Optical"}
        elif "vegetation" in q and "analyze" in q:
            return {"task": "ndvi", "confidence": 0.9, "reason": "Keywords for NDVI analysis"}
        elif "show me" in q or "find" in q or "where is" in q:
            return {"task": "grounding", "confidence": 0.8, "reason": "Keywords for grounding/detection"}
        else:
            return {"task": "vqa", "confidence": 0.7, "reason": "Defaulting to visual question answering"}

query_router = QueryRouter()
