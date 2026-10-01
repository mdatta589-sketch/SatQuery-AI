def build_grounding_prompt(question: str, answer: str) -> str | None:
    """
    Extracts a grounding target from the VQA question/answer.
    Conservative extraction to avoid inventing arbitrary targets.
    """
    q_lower = question.lower()
    
    if "road" in q_lower:
        return "road"
    if "river" in q_lower or "lake" in q_lower:
        return "river . lake"
    if "urban" in q_lower or "building" in q_lower:
        return "urban area . buildings"
    if "water" in q_lower:
        return "water"
    if "tree" in q_lower or "forest" in q_lower:
        return "tree . forest"
    if "cloud" in q_lower:
        return "cloud"
    if "vehicle" in q_lower or "car" in q_lower:
        return "vehicle . car"
        
    # If we cannot confidently derive a grounding target, return None
    return None
