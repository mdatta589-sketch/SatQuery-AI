new_router = """class QueryRouter:
    def route(self, question: str) -> dict:
        q = question.lower()
        
        # 1. CHANGE-VQA
        change_keywords = [
            'compare the images', 'compare these images', 'what changed', 'what has changed',
            'tell me the difference', 'difference between these images', 'compare and tell me the difference',
            'where did the change occur', 'how much changed', 'how much of the area changed',
            'identify changed areas', 'detect changes', 'show changes', 'is there significant change',
            'describe the changes', 'compare'
        ]
        
        if any(kw in q for kw in change_keywords) or ('change' in q and 'vegetation' not in q and 'building' not in q or ('change' in q and ('compare' in q or 'between' in q))):
            # A more robust check. We want to prioritize change_vqa for comparison/temporal change.
            return {"task": "change_vqa", "confidence": 0.9, "reason": "Matched Change-VQA intent"}
            
        # 2. NDVI / VEGETATION
        ndvi_keywords = [
            'analyze vegetation', 'show vegetation', 'vegetation analysis', 'calculate ndvi',
            'show ndvi', 'what is the vegetation condition', 'identify vegetation', 'vegetation health',
            'analyze plant cover', 'how much vegetation is present', 'vegetation', 'ndvi', 'plant'
        ]
        if any(kw in q for kw in ndvi_keywords):
            return {"task": "ndvi", "confidence": 0.9, "reason": "Matched NDVI intent"}
            
        # 3. GROUNDING
        grounding_keywords = [
            'show the', 'locate', 'detect', 'find', 'highlight', 'where are the', 'show me the'
        ]
        # Make sure it's an action indicating grounding, not just "is there..."
        if any(q.startswith(kw) or f" {kw} " in f" {q} " for kw in grounding_keywords):
            return {"task": "grounding", "confidence": 0.9, "reason": "Matched Spatial Grounding intent"}
            
        # 4. VQA
        vqa_keywords = [
            'is there', 'are there', 'what is visible', 'what type', 'what are', 'how many', 'describe the image'
        ]
        if any(q.startswith(kw) or f" {kw} " in f" {q} " for kw in vqa_keywords) or q.endswith('?'):
            return {"task": "vqa", "confidence": 0.8, "reason": "Matched ordinary VQA intent"}
            
        # 5. UNKNOWN
        return {"task": "unknown", "confidence": 0.0, "reason": "Could not determine intent"}

query_router = QueryRouter()
"""
with open('backend/app/services/query_router.py', 'w', encoding='utf8') as f:
    f.write(new_router)
print("UPDATED QUERY ROUTER")
