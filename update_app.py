with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

# 1. Update STAC Search
import re
old_search = r"const maxCloud = document\.getElementById\('stac-cloud-cover'\)\.value \|\| 20;"
new_search = """const maxCloud = document.getElementById('stac-cloud-cover').value || 20;
            const collection = document.getElementById('stac-collection') ? document.getElementById('stac-collection').value : 'sentinel-2-l2a';"""
content = re.sub(old_search, new_search, content)

old_fetch = r"max_cloud_cover: parseFloat\(maxCloud\)"
new_fetch = """max_cloud_cover: parseFloat(maxCloud), collection: collection"""
content = re.sub(old_fetch, new_fetch, content)


# 2. Update Dropdowns
old_update_dropdowns = r"function updateChangeAnalysisDropdowns\(\) \{"
new_update_dropdowns = """function updateCrossModalDropdowns() {
    const optSel = document.getElementById('cross-modal-opt-scene');
    const sarSel = document.getElementById('cross-modal-sar-scene');
    if (!optSel || !sarSel) return;
    
    const currOpt = optSel.value;
    const currSar = sarSel.value;
    
    optSel.innerHTML = '<option value="">-- Select Optical Image --</option>';
    sarSel.innerHTML = '<option value="">-- Select SAR Image --</option>';
    
    layers.forEach(l => {
        if (!l.is_analysis) {
            optSel.add(new Option(l.name, l.id));
            sarSel.add(new Option(l.name, l.id));
        }
    });
    
    if (currOpt) optSel.value = currOpt;
    if (currSar) sarSel.value = currSar;
}

function updateChangeAnalysisDropdowns() {"""
content = content.replace(old_update_dropdowns, new_update_dropdowns)

old_loadStac = r"updateChangeAnalysisDropdowns\(\);"
new_loadStac = """updateChangeAnalysisDropdowns();\n                updateCrossModalDropdowns();"""
content = content.replace(old_loadStac, new_loadStac)


# 3. Add router handling for cross_modal
old_router = r"\} else if \(task === 'ndvi'\) \{"
new_router = """} else if (task === 'cross_modal') {
                    const optId = document.getElementById('cross-modal-opt-scene').value;
                    const sarId = document.getElementById('cross-modal-sar-scene').value;
                    
                    if (!optId || !sarId) {
                        throw new Error("Cross-modal analysis requires both an optical/multispectral image and a SAR image. Please select them from the Cross-Modal Setup panel.");
                    }
                    
                    document.getElementById('header-status').textContent = 'RUNNING CROSS-MODAL ANALYSIS...';
                    
                    const res = await loggedFetch('http://127.0.0.1:8000/api/v1/cross-modal/analyze', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            optical_image_id: optId,
                            sar_image_id: sarId,
                            question: q,
                            aoi: aoiData
                        })
                    });
                    
                    if (!res.ok) {
                        const errData = await res.json();
                        throw new Error(errData.detail || errData.message || errData.error || 'Unknown error during cross-modal analysis.');
                    }
                    
                    data = await res.json();
                    
                    const optLayer = layers.find(l => l.id === optId);
                    const sarLayer = layers.find(l => l.id === sarId);
                    
                    const water = data.water || {};
                    const built = data.built_up || {};
                    
                    ansText = `<div style="font-family: sans-serif; line-height: 1.5; font-size: 13px;">
<strong>CROSS-MODAL ANALYSIS</strong><br><br>
<strong>Optical image:</strong><br>${optLayer ? optLayer.name : optId}<br><br>
<strong>SAR image:</strong><br>${sarLayer ? sarLayer.name : sarId}<br><br>
<strong>Analysis:</strong><br>Optical + SAR complementary fusion<br><br>
<strong>Water:</strong><br>${water.detected ? 'Detected' : 'Not detected'}<br>Evidence: ${water.evidence || 'N/A'}<br><br>
<strong>Built-up:</strong><br>${built.detected ? 'Detected' : 'Not detected'}<br>Evidence: ${built.evidence || 'N/A'}<br><br>
<strong>Execution:</strong><br>
Task: cross_modal<br>
Model/Tool: optical_sar_fusion<br>
Provider: local<br>
Status: success
</div>`;
                    
                    data.execution = data.execution_trace || { task: 'cross_modal', model: 'optical_sar_fusion', provider: 'local', status: 'success' };
                    
                    const resultId = data.result_id;
                    const renderUrl = data.image_url;
                    
                    const datasetMeta = {
                        id: `analysis:crossmodal:${data.result_id}`,
                        name: `Fusion - Opt+SAR`,
                        is_stac: false,
                        is_analysis: true,
                        source_layer_name: "Cross-Modal Fusion",
                        analysis_data: data,
                        bounds: data.bounds,
                        preview_url: data.image_url,
                        bands: [{ id: 'Fusion', description: 'Red=Built, Blue=Water, Grey=SAR' }],
                        metadata: {
                            crs: 'EPSG:4326',
                            source_crs: 'EPSG:4326',
                            resolution: 10,
                            dtype: 'uint8',
                            driver: 'Analysis'
                        }
                    };
                    
                    const existingIndex = layers.findIndex(l => l.id === datasetMeta.id);
                    if (existingIndex >= 0) {
                        layers[existingIndex] = datasetMeta;
                    } else {
                        layers.push(datasetMeta);
                    }
                    clearLayerList();
                    layers.forEach(addLayerToList);
                    updateNoDataState();
                    selectLayer(datasetMeta.id);
                    
                } else if (task === 'ndvi') {"""
content = content.replace(old_router, new_router)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("Updated app.js")
