with open('backend/app/api/vqa.py', 'r', encoding='utf8') as f:
    content = f.read()

import re

# Change the task field in the response to use request.mode
content = re.sub(
    r'task="vqa",\s*image_id=request\.image_id,',
    r'task=request.mode,\n        image_id=request.image_id,',
    content
)

content = re.sub(
    r'task=vqa',
    r'task={request.mode}',
    content
)

with open('backend/app/api/vqa.py', 'w', encoding='utf8') as f:
    f.write(content)
print("UPDATED VQA ROUTE")
