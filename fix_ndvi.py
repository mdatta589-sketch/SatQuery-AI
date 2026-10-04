with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

import re

# Fix NDVI parsing
old_ndvi = """                    if (data.status === 'success') {
                        ansText = `NDVI Analysis completed successfully.\\nMean NDVI: ${data.mean_ndvi ? data.mean_ndvi.toFixed(3) : 'N/A'}`;"""
new_ndvi = """                    if (data.scene_id) {
                        data.status = 'success';
                        data.execution = { task: 'ndvi', model: 'NDVI spectral analysis', provider: 'local', status: 'success' };
                        ansText = `NDVI Analysis completed successfully.\\nMean NDVI: ${data.statistics && data.statistics.mean !== undefined ? data.statistics.mean.toFixed(3) : 'N/A'}`;"""

content = content.replace(old_ndvi, new_ndvi)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED NDVI")
