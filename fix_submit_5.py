import re
with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

# I need to add the overlay logic after the result card is prepared.
# Wait, let's just find `document.getElementById('header-status').textContent = data.status === 'error' ...`
# and put the overlay logic there.

match = re.search(r"document\.getElementById\('header-status'\)\.textContent = data\.status === 'error'.*?;", content)
if match:
    overlay_logic = """
                if (task === 'change' && data.status === 'success' && data.overlay_base64) {
                    if (changeAnalysisMode === 'case-study') {
                        const KANCHA_AOI = [[17.41, 78.32], [17.45, 78.36]];
                        const imgOverlay = L.imageOverlay("data:image/png;base64," + data.overlay_base64, KANCHA_AOI, {opacity: 0.65, interactive: false});
                        
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
                        const imgOverlay = L.imageOverlay("data:image/png;base64," + data.overlay_base64, data.bounds, {opacity: 0.65, interactive: false});
                        if (changeOverlayLayer) map.removeLayer(changeOverlayLayer);
                        changeOverlayLayer = imgOverlay;
                        
                        if (changeBeforeLayer) map.removeLayer(changeBeforeLayer);
                        if (changeAfterLayer) {
                            changeAfterLayer.addTo(map);
                            changeAfterLayer.bringToFront();
                        }
                        changeOverlayLayer.addTo(map);
                        changeOverlayLayer.bringToFront();
                        
                        const rect = L.rectangle(data.bounds, {color: '#ef4444', weight: 2, fill: false});
                        rect.addTo(map);
                    }
                }
"""
    content = content[:match.start()] + overlay_logic + content[match.start():]
    print("ADDED OVERLAY LOGIC")

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
