import re

with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

replacement = '''
              const parentLayer = layers.find(l => l.id === layerId);
              
              const datasetMeta = {
                  id: nalysis:ndvi:,
                  name: NDVI — ,
                  is_stac: false,
                  is_analysis: true,
                  source_layer_name: parentLayer ? parentLayer.name : data.scene_id,
                  analysis_data: data,
'''

js = re.sub(r'const parentLayer = layers\.find\(l => l\.id === layerId\);\s*const datasetMeta = \{\s*id: nalysis:ndvi:\$\{data\.scene_id\},\s*name: NDVI — \$\{data\.scene_id\.split\(\'_\'\)\[2\]\?\.split\(\'T\'\)\[0\] \|\| data\.scene_id\},\s*is_stac: false,\s*is_analysis: true,\s*analysis_data: data,', replacement.strip() + '\n', js, flags=re.DOTALL)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
