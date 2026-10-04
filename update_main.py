with open('backend/app/main.py', 'r', encoding='utf8') as f:
    content = f.read()

import re
if 'cross_modal' not in content:
    content = content.replace('from app.api import query, catalog, vqa, export, change, analysis, grounding, upload, chat',
                              'from app.api import query, catalog, vqa, export, change, analysis, grounding, upload, chat, cross_modal')
    content = content.replace('app.include_router(upload.router)',
                              'app.include_router(upload.router)\napp.include_router(cross_modal.router)')

with open('backend/app/main.py', 'w', encoding='utf8') as f:
    f.write(content)
print("Updated main.py")
