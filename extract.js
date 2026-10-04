if (btnQueryPanel) {
      btnQueryPanel.addEventListener('click', async () => {
            const qInput = document.getElementById('query-input-panel');
            const q = qInput.value.trim();
            
            document.getElementById('header-status').textContent = 'VALIDATING...';
            
            const qLower = q.toLowerCase();
            const changeKeywords = [
                'compare', 'difference', 'changed', 'changes', 
                'what changed', 'detect changes', 'change between these images', 
                'compare these images', 'how has this area changed', 
                'identify changed areas', 'show changes',
                'where changed', 'where did the change occur',
                'how much changed', 'how much of the area changed',
                'significant change', 'describe changes'
            ];
            const isChangeQuery = changeKeywords.some(kw => qLower.includes(kw));
            
            const beforeSel = document.getElementById('change-before-select');
            const afterSel = document.getElementById('change-after-select');
            const beforeId = beforeSel ? beforeSel.value : null;
            const afterId = afterSel ? afterSel.value : null;
            
            let task = 'vqa';
            let ctx = null;
            
            if (isChangeQuery && beforeId && afterId && beforeId !== afterId) {
                task = 'change_vqa';
            } else {
                ctx = getVqaContext();
                if (!ctx) {
                    document.getElementById('header-status').textContent = 'ERROR: No image selected';
                    alert("No satellite image selected.");
                    return;
                }
            }
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
          
          document.getElementById('gpu-offline-banner').style.display = 'none';
          
          const historyContainer = document.getElementById('query-history-container');
          document.getElementById('query-history-empty').style.display = 'none';
          
          const historyItem = document.createElement('div');
          historyItem.style.background = 'var(--app-bg)';
          historyItem.style.border = '1px solid var(--border)';
          historyItem.style.borderRadius = 'var(--radius)';
          historyItem.style.padding = '12px';
          
          const qDiv = document.createElement('div');
          qDiv.style.fontWeight = '600';
          qDiv.style.color = 'var(--text)';
          qDiv.style.marginBottom = '8px';
          qDiv.textContent = "Q: " + q;
          
          const aDiv = document.createElement('div');
          aDiv.style.color = 'var(--text-light)';
          aDiv.innerHTML = '<i class="fa-solid fa-spinner fa-spin" style="margin-right: 6px;"></i> Analyzing satellite image...';
          
          historyItem.appendChild(qDiv);
          historyItem.appendChild(aDiv);
          historyContainer.prepend(historyItem);
          
          const resultSec = document.getElementById('vqa-result-section');
          resultSec.style.display = 'block';
          
          document.getElementById('vqa-answer').textContent = "Analyzing satellite image...";
          document.getElementById('vqa-answer').style.color = "var(--text-light)";
          document.getElementById('vqa-confidence').textContent = "-";
          document.getElementById('vqa-evidence').textContent = "-";
          document.getElementById('vqa-execution').textContent = "-";
          
          btnQueryPanel.disabled = true;
          document.getElementById('header-status').textContent = 'RUNNING ROUTER...';
          
          let aoiData = null;
        if (currentAOI) {
            aoiData = {
                type: 'bbox',
                shape: currentAOI.geometry_type,
                area: currentAOI.area_m2 || 0,
                north: currentAOI.bbox.north,
                south: currentAOI.bbox.south,
                east: currentAOI.bbox.east,
                west: currentAOI.bbox.west,
                geometry: currentAOI.geometry
            };
        }
        
        try {
            if (vqaEvidenceLayer) vqaEvidenceLayer.clearLayers();
            
            // 1. Route the query
            let data = null;
            if (task === 'change_vqa') {
                document.getElementById('header-status').textContent = 'RUNNING CHANGE VQA...';
                
                const beforeSel = document.getElementById('change-before-select');
                const afterSel = document.getElementById('change-after-select');
                
                if (!beforeSel.value || !afterSel.value) {
                    throw new Error("Change-VQA requires two different satellite scenes.<br><br>Please select both a Before and After scene.");
                }
                
                if (beforeSel.value === afterSel.value) {
                    throw new Error("Before and After scenes must be different.<br><br>Please select different acquisition dates.");
                }
                
                if (!aoiData) {
                    throw new Error("Please select an Area of Interest before running Change-VQA.");
                }
                const payload = {
                    image_before_id: beforeSel.value,
                    image_after_id: afterSel.value,
                    question: q,
                    aoi: aoiData
                };
                
                const res = await loggedFetch('http://127.0.0.1:8000/api/v1/change/vqa', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                data = await res.json();
            } else {
                document.getElementById('header-status').textContent = 'RUNNING VQA...';
                const routeRes = await loggedFetch('http://127.0.0.1:8000/api/v1/query/route', {
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
                data = await routeRes.json();
            }
              
              
                
                
                if (task === 'change_vqa' && data.status === 'success') {
                    const changeEv = (data.evidence || []).find(e => e.type === 'image_overlay');
                    if (!changeEv) {
                        data.answer = "Change Analysis succeeded, but visual overlay was missing from the backend response. Evidence array: " + JSON.stringify(data.evidence);
                    } else {
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
                                            <span class="legend-color" style="display: inline-block; width: 14px; height: 14px; background: rgba(255, 60, 60, 0.6); margin-right: 8px;"></span>
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
                                document.getElementById('inspector-name').textContent = "Change Analysis";
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
                }
document.getElementById('header-status').textContent = data.status === 'error' || data.execution?.status === 'error' ? 'ERROR' : 'SUCCESS';
              
              let ansText = data.answer;
                if (task === 'change') {
                    if (data.status === 'success') {
                        const methodFormat = data.method === 'baseline_raster_difference' ? 'Baseline Raster Difference' : data.method;
                        let caseStudyHtml = '';
                        const caseStudySel = document.getElementById('change-case-study');
                        const beforeSel = document.getElementById('change-before-select');
                        const afterSel = document.getElementById('change-after-select');
                        
                        if (caseStudySel && caseStudySel.value === 'kancha') {
                            caseStudyHtml = `Kancha Gachibowli, Hyderabad<br><br><strong>Before</strong><br>28 March 2025<br><br><strong>After</strong><br>2 April 2025<br><br>`;
                        } else {
                            caseStudyHtml = `<strong>Before</strong><br>${beforeSel.value}<br><br><strong>After</strong><br>${afterSel.value}<br><br>`;
                        }
                        
                        ansText = `<div style="font-family: sans-serif; line-height: 1.5; font-size: 13px;">
<strong>CHANGE ANALYSIS</strong><br><br>
${caseStudyHtml}<strong>Changed area</strong><br>
${data.change_percentage.toFixed(2)}%<br><br>
<strong>Changed pixels</strong><br>
${data.changed_pixel_count.toLocaleString()}<br><br>
<strong>Valid pixels</strong><br>
${data.total_valid_pixel_count.toLocaleString()}<br><br>
<strong>Threshold</strong><br>
${data.threshold}<br><br>
<strong>Method</strong><br>
${methodFormat}<br><br>
<strong>Status</strong><br>
✓ Analysis completed successfully
</div>`;
                    } else {
                        ansText = "Change Analysis failed.<br><br>Please check the selected scenes and AOI and try again.";
                    }
                } else if (!ansText) {
                    ansText = "No answer returned.";
                }
              aDiv.innerHTML = `<span style="color: var(--accent);"><i class="fa-solid fa-reply" style="margin-right: 6px;"></i> ${ansText}</span>`;
              
              const statusDiv = document.createElement('div');
              statusDiv.style.fontSize = '11px';
              statusDiv.style.color = 'var(--text-muted)';
              statusDiv.style.marginTop = '8px';
              statusDiv.textContent = `Provider: ${data.execution?.provider || 'remote'} | Model: ${data.execution?.model || 'unknown'} | Status: ${data.execution?.status || 'success'}`;
              historyItem.appendChild(statusDiv);
              
              document.getElementById('vqa-answer').textContent = ansText;
              document.getElementById('vqa-confidence').textContent = data.confidence_status === 'not_calibrated' ? "Not calibrated" : `${data.confidence}`;
              
              // Handle Evidence
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
                      link.addEventListener('click', (e) => {
                          e.preventDefault();
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
                  }