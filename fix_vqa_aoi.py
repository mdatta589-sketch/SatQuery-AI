import re
with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

replacement = '''
        let aoiData = null;
        if (currentAOI && currentAOI.bounds) {
            let nw = currentAOI.bounds.getNorthWest().wrap();
            let se = currentAOI.bounds.getSouthEast().wrap();
            let west = nw.lng;
            let east = se.lng;
            if (west > east) {
                west = currentAOI.bounds.getWest();
                east = currentAOI.bounds.getEast();
            }
            aoiData = {
                type: 'bbox',
                north: currentAOI.bounds.getNorth(),
                south: currentAOI.bounds.getSouth(),
                east: east,
                west: west
            };
        }
        
        try {
            if (vqaEvidenceLayer) vqaEvidenceLayer.clearLayers();
            
            const res = await fetch('http://127.0.0.1:8000/api/v1/vqa/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    image_id: currentLayer.id,
                    image_type: ctx.image_type,
                    source: ctx.source,
                    modality: ctx.modality,
                    representation: ctx.representation,
                    question: q,
                    mode: 'vqa',
                    aoi: aoiData
                })
            });
'''

js = re.sub(r'try \{\s*if \(vqaEvidenceLayer\) vqaEvidenceLayer\.clearLayers\(\);\s*const res = await fetch\(\'http://127\.0\.0\.1:8000/api/v1/vqa/query\', \{\s*method: \'POST\',\s*headers: \{ \'Content-Type\': \'application/json\' \},\s*body: JSON\.stringify\(\{\s*image_id: currentLayer\.id,\s*image_type: ctx\.image_type,\s*source: ctx\.source,\s*modality: ctx\.modality,\s*representation: ctx\.representation,\s*question: q,\s*mode: \'vqa\'\s*\}\)\s*\}\);', replacement.strip(), js, flags=re.DOTALL)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
