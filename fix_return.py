import re

with open('backend/app/api/analysis.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = '''                    return {
                        "scene_id": req.scene_id,
                        "analysis": "NDVI",'''

replacement = '''                    return {
                        "scene_id": req.scene_id,
                        "source_dataset": req.scene_id,
                        "source_type": req.source_type,
                        "bands_used": ["B04", "B08"],
                        "analysis": "NDVI",'''

code = code.replace(target, replacement)

with open('backend/app/api/analysis.py', 'w', encoding='utf-8') as f:
    f.write(code)
