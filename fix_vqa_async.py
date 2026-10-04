with open('backend/app/models/vqa/service.py', 'r', encoding='utf8') as f:
    content = f.read()

import re

# Add import asyncio at the top
if 'import asyncio' not in content:
    content = content.replace('import os', 'import os\nimport asyncio')

# Replace prepare_image call
old_prep = r"image_path = prepare_image\(image_id, image_type, aoi\)"
new_prep = r"image_path = await asyncio.to_thread(prepare_image, image_id, image_type, aoi)"

content = re.sub(old_prep, new_prep, content)

with open('backend/app/models/vqa/service.py', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED vqa service.py blocking")
