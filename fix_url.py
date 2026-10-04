import re

with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Let's fix True Color url for STAC to use the preview_url (which points to /preview.png)
replacement = '''
        if (currentLayer.is_stac) {
            if (band === 'True Color') {
                url = currentLayer.preview_url;
'''

js = re.sub(
    r'if \(currentLayer\.is_stac\) \{\s*if \(band === \'True Color\'\) \{\s*url = http://127\.0\.0\.1:8000/api/v1/catalog/scene/\$\{currentLayer\.id\}/true-color/preview\$\{paramStr\};',
    replacement.strip(),
    js
)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
