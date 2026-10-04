import sys
import re
with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

replacement = '''
        let aoiData = null;
        if (currentAOI && currentAOI.bounds) {
            aoiData = {
                type: 'bbox',
                north: currentAOI.bounds.north,
                south: currentAOI.bounds.south,
                east: currentAOI.bounds.east,
                west: currentAOI.bounds.west
            };
        }
        
        try {
            const res = await fetch('http://127.0.0.1:8000/api/v1/vqa/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    image_id: imageId,
                    image_type: imageType,
                    source: currentLayer.name,
                    modality: 'optical',
                    representation: 'rgb',
                    question: question,
                    mode: 'vqa',
                    aoi: aoiData
                })
            });
'''

js = re.sub(r'try \{\s*const res = await fetch\(\'http://127\.0\.0\.1:8000/api/v1/vqa/query\', \{\s*method: \'POST\',\s*headers: \{ \'Content-Type\': \'application/json\' \},\s*body: JSON\.stringify\(\{.*?\}\)\s*\}\);', replacement.strip(), js, flags=re.DOTALL)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
