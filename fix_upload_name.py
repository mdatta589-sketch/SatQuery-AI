import re

with open('backend/app/api/upload.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = '''        "name": "SENTINEL-2 OPTICAL" if len(bands) > 1 else files[0].filename,'''

replacement = '''        "name": files[0].filename.split('.')[0] + " (Multiband)" if bands[0]["metadata"]["bands"] > 1 else (files[0].filename.split('_')[0] + " — B04 + B08" if len(bands) >= 2 and any('B04' in b['id'] for b in bands) and any('B08' in b['id'] for b in bands) else files[0].filename),'''

code = code.replace(target, replacement)

with open('backend/app/api/upload.py', 'w', encoding='utf-8') as f:
    f.write(code)
