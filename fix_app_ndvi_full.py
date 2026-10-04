with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

import re
old_block_pattern = r"\} else if \(task === 'ndvi'\) \{.*?\}(?=\s*\} else if \(task === 'grounding')"
match = re.search(old_block_pattern, content, re.DOTALL)
if not match:
    print("Could not find the NDVI block!")
    exit(1)

old_code = match.group(0)

new_code = """} else if (task === 'ndvi') {
                    if (!currentLayer || !currentLayer.is_stac) throw new Error("NDVI requires Sentinel-2 Red (B04) and Near-Infrared (B08) bands. Please load a Sentinel-2 image first.");
                    
                    document.getElementById('header-status').textContent = 'RUNNING NDVI ANALYSIS...';
                    const source_type = currentLayer.is_stac ? 'stac' : 'local';
                    const res = await loggedFetch('http://127.0.0.1:8000/api/v1/analysis/ndvi', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ scene_id: currentLayer.id, source_type: source_type, aoi: aoiData })
                    });
                    
                    if (!res.ok) {
                        const errData = await res.json();
                        throw new Error(errData.detail || errData.message || errData.error || 'Unknown error');
                    }
                    data = await res.json();
                    
                    const stats = data.statistics || {};
                    const mean_val = stats.mean || 0.0;
                    
                    let mean_desc = "indicating very low or no vegetation";
                    if (mean_val > 0.6) mean_desc = "indicating dense, healthy vegetation";
                    else if (mean_val > 0.3) mean_desc = "indicating moderate vegetation";
                    else if (mean_val > 0.1) mean_desc = "indicating sparse vegetation";
                    
                    ansText = `<div style="font-family: sans-serif; line-height: 1.5; font-size: 13px;">
<strong>NDVI ANALYSIS</strong><br><br>
<strong>Mean NDVI:</strong><br>${mean_val.toFixed(3)}<br><br>
<strong>Minimum:</strong><br>${(stats.min || 0).toFixed(3)}<br><br>
<strong>Maximum:</strong><br>${(stats.max || 0).toFixed(3)}<br><br>
<strong>Median:</strong><br>${(stats.median || 0).toFixed(3)}<br><br>
<strong>Valid Pixels:</strong><br>${(stats.valid_pixel_count || 0).toLocaleString()}<br><br>
<strong>Vegetation Pixels:</strong><br>${(stats.vegetation_area_percentage || 0).toFixed(1)}% of valid area<br><br>
<strong>Interpretation:</strong><br>
NDVI analysis completed. The selected AOI has a mean NDVI of ${mean_val.toFixed(2)}, ${mean_desc}. Approximately ${(stats.vegetation_area_percentage || 0).toFixed(1)}% of valid pixels have NDVI &ge; 0.40.<br><br>
<strong>Execution:</strong><br>
Task: ndvi<br>
Model: NDVI spectral analysis<br>
Provider: local<br>
Status: success
</div>`;
                    
                    data.execution = { task: 'ndvi', model: 'NDVI spectral analysis', provider: 'local', status: 'success' };
                    
                    const urlParts = data.image_url.split('/');
                    const resultId = urlParts[urlParts.length - 2];
                    
                    // Create layer
                    const datasetMeta = {
                        id: `analysis:ndvi:${data.scene_id}`,
                        name: `NDVI - ${data.scene_id.includes('_') ? data.scene_id.split('_')[2].split('T')[0] : data.scene_id.substring(0, 8)}`,
                        is_stac: false,
                        is_analysis: true,
                        source_layer_name: currentLayer.name,
                        analysis_data: data,
                        bounds: data.bounds,
                        preview_url: data.image_url,
                        bands: [{ id: 'NDVI', description: 'Vegetation Index' }],
                        metadata: {
                            crs: 'EPSG:4326',
                            source_crs: currentLayer.metadata.source_crs || currentLayer.metadata.crs,
                            resolution: currentLayer.metadata.resolution,
                            dtype: 'float32',
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
                """

content = content.replace(old_code, new_code)
with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED app.js NDVI completely")
