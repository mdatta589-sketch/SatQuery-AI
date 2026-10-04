with open('backend/app/models/grounding/service.py', 'r', encoding='utf8') as f:
    content = f.read()

import re

if 'import asyncio' not in content:
    content = content.replace('import os', 'import os\nimport asyncio')

old_prep = r"image_path = prepare_image\(image_id, image_type\)"
new_prep = r"image_path = await asyncio.to_thread(prepare_image, image_id, image_type)"
content = re.sub(old_prep, new_prep, content)

# I should also check if it passes aoi? It didn't pass aoi in this file!
# GroundingService doesn't accept aoi in this version.

with open('backend/app/models/grounding/service.py', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED grounding service.py blocking")
