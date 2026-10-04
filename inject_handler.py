new_handler = """    if (btnQueryPanel) {
        btnQueryPanel.addEventListener('click', async () => {
            const qInput = document.getElementById('query-input-panel');
            const q = qInput.value.trim();
            
            if (!q) {
                document.getElementById('header-status').textContent = 'ERROR: Empty question';
                alert("Enter a question about the selected image.");
                return;
            }
            if (q.length > 500) {
                document.getElementById('header-status').textContent = 'ERROR: Question too long';
                alert("Question is too long.");
                return;
            }
            
            const historyList = document.getElementById('vqa-history-list');
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            
            const qDiv = document.createElement('div');
            qDiv.style.fontWeight = '600';
            qDiv.style.marginBottom = '4px';
            qDiv.innerHTML = `<i class="fa-solid fa-user" style="margin-right: 6px; color: #888;"></i> ${q}`;
            historyItem.appendChild(qDiv);
            
            const aDiv = document.createElement('div');
            aDiv.style.marginBottom = '8px';
            historyItem.appendChild(aDiv);
            historyList.appendChild(historyItem);
            
            const resultSec = document.getElementById('vqa-result-section');
            resultSec.style.display = 'block';
            document.getElementById('vqa-answer').textContent = "Analyzing request intent...";
            
            if (vqaEvidenceLayer) vqaEvidenceLayer.clearLayers();
            
            try {
                btnQueryPanel.disabled = true;
                
                const beforeSel = document.getElementById('change-before-select');
                const afterSel = document.getElementById('change-after-select');
                const beforeId = beforeSel ? beforeSel.value : null;
                const afterId = afterSel ? afterSel.value : null;
                
                let aoiData = null;
                if (currentAOI) {
                    const b = currentAOI.bounds;
                    aoiData = { type: 'Polygon', bbox: { west: b.getWest(), north: b.getNorth(), east: b.getEast(), south: b.getSouth() } };
                }
                
                // 1. Ask the backend to route the query
                document.getElementById('header-status').textContent = 'ROUTING TASK...';
                const routeRes = await loggedFetch('http://127.0.0.1:8000/api/v1/query/route', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: q })
                });
                
                if (!routeRes.ok) throw new Error("Failed to reach routing service.");
                const routeData = await routeRes.json();
                const task = routeData.task;
                
                document.getElementById('header-status').textContent = `TASK DETECTED: ${task.toUpperCase().replace('_', ' ')}`;
                
                let data = null;
                let ctx = null;
                let ansText = '';
                
                if (task === 'change_vqa') {
                    if (!beforeId || !afterId) throw new Error("Change-VQA requires both a Before and After satellite scene. Please select the two scenes first.");
                    if (beforeId === afterId) throw new Error("Before and After scenes must be different. Please select different acquisition dates.");
                    if (!aoiData) throw new Error("Please select an Area of Interest before running Change-VQA.");
                    
                    document.getElementById('header-status').textContent = 'RUNNING CHANGE VQA...';
                    const res = await loggedFetch('http://127.0.0.1:8000/api/v1/change/vqa', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ image_before_id: beforeId, image_after_id: afterId, question: q, aoi: aoiData })
                    });
                    data = await res.json();
                    
                    if (data.status === 'success') {
                        const changeEv = (data.evidence || []).find(e => e.type === 'image_overlay');
                        if (changeEv) {
                            const evData = changeEv.data;
                            if (changeAnalysisMode === 'case-study') {
                                const KANCHA_AOI = [[17.41, 78.32], [17.45, 78.36]];
                                const imgOverlay = L.imageOverlay(evData, KANCHA_AOI, {opacity: 1.0, interactive: false});
                                
                                if (caseStudyChangeLayer) map.removeLayer(caseStudyChangeLayer);
                                caseStudyChangeLayer = imgOverlay;
                                
                                if (caseStudyBeforeLayer) map.removeLayer(caseStudyBeforeLayer);
                                if (caseStudyAfterLayer) {
                                    caseStudyAfterLayer.addTo(map);
                                    caseStudyAfterLayer.bringToFront();
                                }
                                caseStudyChangeLayer.addTo(map);
                                caseStudyChangeLayer.bringToFront();
                                if (caseStudyAoiLayer) caseStudyAoiLayer.bringToFront();
                                
                                if (!window.changeLegendControl) {
                                    window.changeLegendControl = L.control({position: 'bottomright'});
                                    window.changeLegendControl.onAdd = function(map) {
                                        const div = L.DomUtil.create('div', 'satquery-change-legend');
                                        div.innerHTML = `
                                            <div class="legend-title" style="font-weight: 600; font-size: 11px; margin-bottom: 6px;">Change Analysis</div>
                                            <div class="legend-row" style="display: flex; align-items: center; margin-bottom: 4px;">
                                                <span class="legend-color" style="display: inline-block; width: 14px; height: 14px; background: rgba(255, 40, 40, 0.8); margin-right: 8px;"></span>
                                                <span style="font-size: 11px;">Detected change</span>
                                            </div>
                                            <div class="legend-row" style="display: flex; align-items: center;">
                                                <span class="legend-neutral" style="display: inline-block; width: 14px; height: 14px; background: rgba(255, 255, 255, 0.3); border: 1px dashed rgba(255,255,255,0.5); margin-right: 8px;"></span>
                                                <span style="font-size: 11px;">Satellite imagery</span>
                                            </div>
                                        `;
                                        L.DomEvent.disableClickPropagation(div);
                                        return div;
                                    };
                                }
                                window.changeLegendControl.addTo(map);
                                
                                map.fitBounds(KANCHA_AOI, { padding: [40, 40] });
                                map.invalidateSize(true);
                                
                                const vqaLabel = document.getElementById('vqa-selected-image-panel');
                                if (vqaLabel) vqaLabel.textContent = "Change Analysis";
                                
                                try {
                                    document.getElementById('inspector-name').textContent = "Change-VQA";
                                    document.getElementById('inspector-sensor').textContent = "Sentinel-2 L2A";
                                    document.getElementById('inspector-band').textContent = "Before: 2025-03-28";
                                    document.getElementById('inspector-dim').textContent = "After: 2025-04-02";
                                    document.getElementById('inspector-dtype').textContent = "Baseline Raster Difference";
                                    document.getElementById('inspector-res').textContent = "0.25 (Threshold)";
                                    document.getElementById('inspector-source-crs').textContent = "-";
                                    document.getElementById('inspector-display-crs').textContent = "-";
                                    document.getElementById('inspector-coord-crs').textContent = "-";
                                    document.getElementById('inspector-bounds').textContent = "-";
                                } catch(e) {}
                            } else {
                                const imgOverlay = L.imageOverlay(evData, changeEv.bounds, {opacity: 1.0, interactive: false});
                                if (changeOverlayLayer) map.removeLayer(changeOverlayLayer);
                                changeOverlayLayer = imgOverlay;
                                
                                if (changeBeforeLayer) map.removeLayer(changeBeforeLayer);
                                if (changeAfterLayer) {
                                    changeAfterLayer.addTo(map);
                                    changeAfterLayer.bringToFront();
                                }
                                changeOverlayLayer.addTo(map);
                                changeOverlayLayer.bringToFront();
                                
                                const rect = L.rectangle(changeEv.bounds, {color: '#ef4444', weight: 2, fill: false});
                                rect.addTo(map);
                            }
                        }
                        
                        const methodFormat = data.method === 'baseline_raster_difference' ? 'Baseline Raster Difference' : data.method;
                        const exec = data.execution || {};
                        ansText = `<div style="font-family: sans-serif; line-height: 1.5; font-size: 13px;">
<strong>CHANGE-VQA</strong><br><br>
<strong>Question:</strong><br>
${data.question || q}<br><br>
<strong>Answer:</strong><br>
${data.answer}<br><br>
<strong>Change detected:</strong><br>
${data.change_percentage.toFixed(2)}%<br><br>
<strong>Changed pixels:</strong><br>
${data.changed_pixel_count.toLocaleString()}<br><br>
<strong>Valid pixels:</strong><br>
${data.total_valid_pixel_count.toLocaleString()}<br><br>
<strong>Before:</strong><br>
${data.before_scene}<br><br>
<strong>After:</strong><br>
${data.after_scene}<br><br>
<strong>Method:</strong><br>
${methodFormat}<br><br>
<strong>Evidence:</strong><br>
Visual overlay on map<br><br>
<strong>Execution:</strong><br>
Task: ${exec.task || 'change_vqa'}<br>
Model: ${exec.model || 'change_interpreter'}<br>
Provider: ${exec.provider || 'local'}<br>
Status: ${exec.status || 'success'}
</div>`;
                    } else {
                        ansText = "Change-VQA failed.<br><br>" + (data.error || "Please check the selected scenes and AOI and try again.");
                    }
                    
                } else if (task === 'ndvi') {
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
                        ansText = `NDVI Analysis failed: ${data.message || data.error || 'Unknown error'}`;
                    }
                    
                } else if (task === 'grounding' || task === 'vqa') {
                    ctx = getVqaContext();
                    if (!ctx) {
                        let obj = task === 'grounding' ? 'spatial detection' : 'a visual question';
                        throw new Error(`Please select or upload a satellite image before asking for ${obj}.`);
                    }
                    
                    document.getElementById('header-status').textContent = `RUNNING ${task.toUpperCase()}...`;
                    const res = await loggedFetch('http://127.0.0.1:8000/api/v1/vqa/query', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            image_id: currentLayer.id,
                            image_type: ctx.image_type,
                            source: ctx.source,
                            modality: ctx.modality,
                            representation: ctx.representation,
                            question: q,
                            mode: task,
                            aoi: aoiData
                        })
                    });
                    data = await res.json();
                    
                    if (data.status === 'success' || data.status === 'unavailable') {
                        ansText = data.answer || data.message || "Unable to complete query.";
                    } else {
                        ansText = `Failed: ${data.detail || data.error || data.message || 'Unknown error'}`;
                    }
                    
                    // Render grounding bounding boxes if available
                    const evidenceEl = document.getElementById('vqa-evidence');
                    if (data.evidence && data.evidence.length > 0) {
                        evidenceEl.innerHTML = '';
                        data.evidence.forEach(ev => {
                            const div = document.createElement('div');
                            div.style.marginBottom = '8px';
                            const scoreStr = ev.confidence !== null && ev.confidence !== undefined 
                                ? `Grounding score: ${ev.confidence.toFixed(2)}` 
                                : '';
                            div.innerHTML = `<strong>${ev.label}</strong><br><span style="font-size: 11px; color: var(--text-secondary);">${scoreStr}</span><br><a href="#" style="font-size:11px;">[Show on map]</a>`;
                            evidenceEl.appendChild(div);
                            
                            const link = div.querySelector('a');
                            link.addEventListener('click', (evClick) => {
                                evClick.preventDefault();
                                if (ev.geometry && ev.geometry.coordinate_system === 'wgs84') {
                                    if (ev.type === 'bbox' && ev.geometry.coordinates.length === 4) {
                                        const [x1, y1, x2, y2] = ev.geometry.coordinates;
                                        const bounds = [[y1, x1], [y2, x2]];
                                        L.rectangle(bounds, {color: '#f00', weight: 2}).bindPopup(ev.label).addTo(vqaEvidenceLayer);
                                    }
                                } else if (ev.geometry && ev.geometry.coordinate_system === 'image_pixel') {
                                      if (currentLayer && currentLayer.bounds) {
                                          if (ev.type === 'bbox' && ev.geometry.coordinates.length === 4) {
                                              const [x1, y1, x2, y2] = ev.geometry.coordinates;
                                              const w = 1024;
                                              const h = 1024;
                                              let bounds = currentLayer.bounds;
                                              if (aoiData) {
                                                  bounds = [[aoiData.south, aoiData.west], [aoiData.north, aoiData.east]];
                                              }
                                              const s = bounds[0][0], w_ = bounds[0][1], n = bounds[1][0], e_ = bounds[1][1];
                                              const lat1 = n - (y1 / h) * (n - s);
                                              const lon1 = w_ + (x1 / w) * (e_ - w_);
                                              const lat2 = n - (y2 / h) * (n - s);
                                              const lon2 = w_ + (x2 / w) * (e_ - w_);
                                            L.rectangle([[lat1, lon1], [lat2, lon2]], {color: '#f00', weight: 2}).bindPopup(`${ev.label} (${scoreStr})`).addTo(vqaEvidenceLayer);
                                        }
                                    } else {
                                        alert("Cannot map pixel coordinates to this image.");
                                    }
                                }
                            });
                        });
                    }
                    
                } else {
                    // unknown task
                    ansText = "I can currently analyze satellite imagery using visual question answering, spatial object detection, vegetation/NDVI analysis, and before/after change analysis. Try asking something like 'Is there water?', 'Show the water bodies', 'Analyze vegetation', or 'Compare these images'.";
                    document.getElementById('header-status').textContent = 'TASK UNKNOWN';
                    data = { execution: { provider: 'system', model: 'router', status: 'success' } };
                }
                
                aDiv.innerHTML = `<span style="color: var(--accent);"><i class="fa-solid fa-reply" style="margin-right: 6px;"></i> ${ansText}</span>`;
                
                const statusDiv = document.createElement('div');
                statusDiv.style.fontSize = '11px';
                statusDiv.style.color = 'var(--text-muted)';
                statusDiv.style.marginTop = '8px';
                statusDiv.textContent = `Provider: ${data.execution?.provider || 'remote'} | Model: ${data.execution?.model || 'unknown'} | Status: ${data.execution?.status || 'success'}`;
                historyItem.appendChild(statusDiv);
                
                document.getElementById('vqa-answer').textContent = 'Analysis complete.';
                if (data.confidence_status === 'not_calibrated') {
                    document.getElementById('vqa-confidence').textContent = "Not calibrated";
                } else if (data.confidence) {
                    document.getElementById('vqa-confidence').textContent = `${data.confidence}`;
                }
                
                if (data.execution) {
                    document.getElementById('vqa-execution').textContent = `Task: ${data.execution.task || task}\nModel: ${data.execution.model}\nProvider: ${data.execution.provider}\nStatus: ${data.execution.status}`;
                }
                
            } catch (err) {
                console.error(err);
                document.getElementById('header-status').textContent = 'ERROR';
                const errMsg = err.message || "An unknown error occurred.";
                aDiv.innerHTML = `<span style="color: #ef4444;"><i class="fa-solid fa-triangle-exclamation" style="margin-right: 6px;"></i> ${errMsg}</span>`;
                document.getElementById('vqa-answer').textContent = "Error during execution.";
                document.getElementById('vqa-execution').textContent = `Task: unknown\nModel: unknown\nProvider: local\nStatus: error\n\nMessage:\n${errMsg}`;
            } finally {
                btnQueryPanel.disabled = false;
            }
        });
    }"""

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

content = content.replace("    // --- NEW BTNQUERYPANEL HANDLER INJECTED HERE ---", new_handler)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("INJECTED NEW HANDLER")
