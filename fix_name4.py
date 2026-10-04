with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
js = re.sub(r'name: NDVI [^]+,\s*is_stac', "name: NDVI - ,\n                  is_stac", js)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
