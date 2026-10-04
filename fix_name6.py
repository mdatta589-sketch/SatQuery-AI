with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
js = re.sub(r'name: `NDVI[^`]+`,\n\s+is_stac: false,', "name: `NDVI - ${data.scene_id.includes('_') ? data.scene_id.split('_')[2].split('T')[0] : data.scene_id.substring(0, 8)}`,\n                  is_stac: false,", js)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
