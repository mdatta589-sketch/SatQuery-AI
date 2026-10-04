import sys
import re
with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix updateAnalysisSceneDropdown
replacement_dropdown = '''
function updateAnalysisSceneDropdown() {
    const sel = document.getElementById('analysis-scene');
    if (!sel) return;
    sel.innerHTML = '';
    const analysisSources = layers.filter(l => !l.is_analysis);
    if (analysisSources.length === 0) {
        sel.innerHTML = '<option value="">No dataset loaded...</option>';
        return;
    }
    analysisSources.forEach(l => {
        const opt = document.createElement('option');
        opt.value = l.id;
        opt.textContent = l.name;
        sel.appendChild(opt);
    });
}
'''
js = re.sub(r'function updateAnalysisSceneDropdown\(\) \{.*?\n\}\n', replacement_dropdown.strip() + '\n\n', js, flags=re.DOTALL)

# Fix click handler
replacement_click = '''
    btnCalcNdvi.addEventListener('click', async () => {
        const layerId = document.getElementById('analysis-scene').value;
        if (!layerId) {
            alert("Load or upload a raster before calculating NDVI.");
            return;
        }
        
        const selectedLayer = layers.find(l => l.id === layerId);
        const source_type = selectedLayer.is_stac ? 'stac' : 'upload';
        
        btnCalcNdvi.disabled = true;
        btnCalcNdvi.textContent = 'Calculating...';
        document.getElementById('header-status').textContent = 'Calculating NDVI...';
        
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
            const res = await fetch('http://127.0.0.1:8000/api/v1/analysis/ndvi', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ scene_id: layerId, source_type: source_type, aoi: aoiData })
            });
'''
js = re.sub(r'btnCalcNdvi\.addEventListener\(\'click\', async \(\) => \{.*?body: JSON\.stringify\(\{ scene_id: sceneId, aoi: aoiData \}\)\s*\}\);', replacement_click.strip(), js, flags=re.DOTALL)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
