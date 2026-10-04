with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
js = re.sub(
    r'is_analysis: true,\s*analysis_data: data,',
    'is_analysis: true,\n                  source_layer_name: parentLayer ? parentLayer.name : data.scene_id,\n                  analysis_data: data,',
    js
)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
