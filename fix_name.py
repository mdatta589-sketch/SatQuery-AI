with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
js = re.sub(
    r"name: NDVI — \$\{data\.scene_id\.split\('_'\)\[2\]\.split\('T'\)\[0\]\},",
    "name: NDVI — ,",
    js
)
# also with the strange character that got inserted: ?"
js = re.sub(
    r"name: NDVI \D+ \$\{data\.scene_id\.split\('_'\)\[2\]\.split\('T'\)\[0\]\},",
    "name: NDVI - ,",
    js
)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
