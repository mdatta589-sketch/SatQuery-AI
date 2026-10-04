import re
with open('backend/app/models/vqa/service.py', 'r') as f:
    content = f.read()

# Update signature
content = content.replace(
    'async def answer(self, image_id: str, image_type: str, modality: str, representation: str, question: str) -> dict:',
    'async def answer(self, image_id: str, image_type: str, modality: str, representation: str, question: str, aoi: dict | None = None) -> dict:'
)

# Pass aoi to prepare_image
content = content.replace(
    'image_path = prepare_image(image_id, image_type)',
    'image_path = prepare_image(image_id, image_type, aoi)'
)

with open('backend/app/models/vqa/service.py', 'w') as f:
    f.write(content)
