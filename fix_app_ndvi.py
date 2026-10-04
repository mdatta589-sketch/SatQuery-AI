with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

old_code = """                } else if (task === 'ndvi') {
                    if (!currentLayer || !currentLayer.is_stac) throw new Error("NDVI requires Sentinel-2 Red (B04) and Near-Infrared (B08) bands.");
                    
                    document.getElementById('header-status').textContent = 'RUNNING NDVI ANALYSIS...';
                    const source_type = currentLayer.is_stac ? 'stac' : 'local';
                    const res = await loggedFetch('http://127.0.0.1:8000/api/v1/analysis/ndvi', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ scene_id: currentLayer.id, source_type: source_type, aoi: aoiData })
                    });
                    data = await res.json();
                    
                    if (data.status === 'success') {
                        ansText = `NDVI Analysis completed successfully.\nMean NDVI: ${data.mean_ndvi ? data.mean_ndvi.toFixed(3) : 'N/A'}`;
                        data.execution = { task: 'ndvi', model: 'NDVI spectral analysis', provider: 'local', status: 'success' };
                        const resultId = data.result_id;
                        const renderUrl = `http://127.0.0.1:8000/api/v1/analysis/render?result_id=${resultId}&colormap=RdYlGn`;
                        
                        if (currentLayer) {
                            currentLayer.is_analysis = true;
                            currentLayer.analysis_data = {
                                analysis: 'NDVI',
                                result_id: resultId
                            };
                            updateMapLayer(currentLayer, renderUrl);
                        }
                    } else {
                        ansText = `NDVI Analysis failed: ${data.detail || data.message || data.error || 'Unknown error'}`;
                        data = { execution: { provider: 'local', model: 'NDVI spectral analysis', status: 'error' } };
                    }"""

new_code = """                } else if (task === 'ndvi') {
                    if (!currentLayer || !currentLayer.is_stac) throw new Error("NDVI requires Sentinel-2 Red (B04) and Near-Infrared (B08) bands.");
                    
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
NDVI analysis completed. The selected AOI has a mean NDVI of ${mean_val.toFixed(2)}, ${mean_desc}. Approximately ${(stats.vegetation_area_percentage || 0).toFixed(1)}% of valid pixels have NDVI &ge; 0.40.
</div>`;
                    
                    data.execution = { task: 'ndvi', model: 'NDVI spectral analysis', provider: 'local', status: 'success' };
                    
                    // Extract resultId from image_url
                    const urlParts = data.image_url.split('/');
                    const resultId = urlParts[urlParts.length - 2];
                    
                    const renderUrl = `http://127.0.0.1:8000/api/v1/analysis/render?result_id=${resultId}&colormap=ndvi&vmin=-1.0&vmax=1.0`;
                    
                    if (currentLayer) {
                        currentLayer.is_analysis = true;
                        currentLayer.analysis_data = {
                            analysis: 'NDVI',
                            result_id: resultId
                        };
                        
                        // We must create a new L.imageOverlay to show it!
                        if (window.ndviOverlayLayer) map.removeLayer(window.ndviOverlayLayer);
                        window.ndviOverlayLayer = L.imageOverlay(renderUrl, currentLayer.bounds, {opacity: 1.0});
                        window.ndviOverlayLayer.addTo(map);
                        window.ndviOverlayLayer.bringToFront();
                    }"""

content = content.replace(old_code, new_code)
with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED app.js NDVI")
