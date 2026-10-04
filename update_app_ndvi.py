with open('frontend/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

import re

target_text = """            ndvi: (currentLayer && currentLayer.is_analysis && currentLayer.analysis_data) ? currentLayer.analysis_data : null,"""

replacement_text = """            ndvi: (currentLayer && currentLayer.is_analysis && currentLayer.analysis_data) ? {
                ...currentLayer.analysis_data,
                source_crs: currentLayer.metadata?.source_crs || currentLayer.metadata?.crs || '-',
                display_crs: 'EPSG:3857',
                resolution: currentLayer.metadata?.resolution ? ${Math.abs(currentLayer.metadata.resolution).toFixed(0)} m : '-'
            } : null,"""

content = content.replace(target_text, replacement_text)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
