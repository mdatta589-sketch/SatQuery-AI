import re
with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

replacement = '''
            aoiData = {
                type: 'bbox',
                shape: currentAOI.type || 'Rectangle',
                area: currentAOI.area || 0,
                north: currentAOI.bounds.getNorth(),
                south: currentAOI.bounds.getSouth(),
                east: east,
                west: west
            };
'''
js = re.sub(r'aoiData = \{\s*type: \'bbox\',\s*north: currentAOI\.bounds\.getNorth\(\),\s*south: currentAOI\.bounds\.getSouth\(\),\s*east: east,\s*west: west\s*\};', replacement.strip(), js)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
