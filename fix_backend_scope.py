import re

with open('backend/app/api/analysis.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '"scope": "Selected AOI" if req.aoi else "Full Scene",',
    '"scope": req.aoi.get("shape", "Rectangle") if req.aoi else "Full Scene",\n                        "area": req.aoi.get("area", 0) if req.aoi else 0,'
)

with open('backend/app/api/analysis.py', 'w', encoding='utf-8') as f:
    f.write(content)
