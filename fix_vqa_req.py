import re

with open('backend/app/api/vqa.py', 'r') as f:
    content = f.read()

# Add aoi to VqaRequest
content = content.replace('mode: str = "vqa"', 'mode: str = "vqa"\n    aoi: dict | None = None')

# Pass request.aoi to answer
content = content.replace(
    'result = await vqa_service.answer(',
    'result = await vqa_service.answer(\n        aoi=request.aoi,'
)

with open('backend/app/api/vqa.py', 'w') as f:
    f.write(content)
