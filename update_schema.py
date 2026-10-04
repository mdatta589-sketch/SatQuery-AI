with open('backend/app/schemas/change.py', 'r', encoding='utf8') as f:
    content = f.read()

import re

new_schema = """class ChangeVQAResponse(BaseModel):
    task: str = "change_vqa"
    status: str
    question: Optional[str] = None
    answer: Optional[str] = None
    change_percentage: Optional[float] = None
    changed_pixel_count: Optional[int] = None
    total_valid_pixel_count: Optional[int] = None
    threshold: Optional[float] = None
    method: Optional[str] = None
    before_scene: Optional[str] = None
    after_scene: Optional[str] = None
    evidence: Optional[List[Dict[str, Any]]] = None
    execution: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time_ms: Optional[int] = None"""

content = re.sub(r"class ChangeVQAResponse\(BaseModel\):.*", new_schema, content, flags=re.DOTALL)

with open('backend/app/schemas/change.py', 'w', encoding='utf8') as f:
    f.write(content)
print("UPDATED SCHEMA")
