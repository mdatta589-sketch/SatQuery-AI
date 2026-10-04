import re

with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = re.sub(
    r"url = http://127\.0\.0\.1:8000/api/v1/catalog/scene/\$\{currentLayer\.id\}/true-color/preview\$\{paramStr\};",
    "url = currentLayer.preview_url;",
    js
)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
