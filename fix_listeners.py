import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

old_listeners = '''    if (btnBefore) {
        btnBefore.addEventListener('click', () => {
            if (changeAnalysisMode === 'case-study') {
                if (caseStudyAfterLayer) map.removeLayer(caseStudyAfterLayer);
                if (caseStudyChangeLayer) map.removeLayer(caseStudyChangeLayer);
                if (caseStudyBeforeLayer) {
                    caseStudyBeforeLayer.addTo(map);
                    caseStudyBeforeLayer.bringToFront();
                }
                if (caseStudyAoiLayer) caseStudyAoiLayer.bringToFront();
                if (window.changeLegendControl) map.removeControl(window.changeLegendControl);
                
                const vqaLabel = document.getElementById('vqa-selected-image-panel');
                if (vqaLabel) vqaLabel.textContent = "Sentinel-2 ?" 2025-03-28";
                
                if (caseStudyBeforeMeta) {
                    populateInspector({
                        id: caseStudyBeforeScene,
                        name: "Sentinel-2 ?" 2025-03-28",
                        is_stac: true,
                        bounds: caseStudyBeforeMeta.bounds,
                        preview_url: caseStudyBeforeMeta.preview_url || caseStudyBeforeMeta.image_url,
                        bands: [ { id: 'True Color', description: 'Visual' } ],
                        metadata: { crs: caseStudyBeforeMeta.display_crs || 'EPSG:4326' },
                        scene_info: { datetime: caseStudyBeforeMeta.datetime || "2025-03-28", scene_id: caseStudyBeforeScene, cloud_cover: caseStudyBeforeMeta["eo:cloud_cover"] }
                    });
                }
                const KANCHA_AOI = [[17.41, 78.32], [17.45, 78.36]];
                map.fitBounds(KANCHA_AOI, { padding: [40, 40] });
                map.invalidateSize(true);
            } else {
                if (changeAfterLayer) map.removeLayer(changeAfterLayer);
                if (changeOverlayLayer) map.removeLayer(changeOverlayLayer);
                if (changeBeforeLayer) {
                    changeBeforeLayer.addTo(map);
                    changeBeforeLayer.bringToFront();
                }
                if (window.changeLegendControl) map.removeControl(window.changeLegendControl);
                if (beforeSel && beforeSel.value) updateInspectorForCaseStudy(beforeSel.value);
            }
        });
    }
    
    if (btnAfter) {
        btnAfter.addEventListener('click', () => {
            if (changeAnalysisMode === 'case-study') {
                if (caseStudyBeforeLayer) map.removeLayer(caseStudyBeforeLayer);
                if (caseStudyChangeLayer) map.removeLayer(caseStudyChangeLayer);
                if (caseStudyAfterLayer) {
                    caseStudyAfterLayer.addTo(map);
                    caseStudyAfterLayer.bringToFront();
                }
                if (caseStudyAoiLayer) caseStudyAoiLayer.bringToFront();
                if (window.changeLegendControl) map.removeControl(window.changeLegendControl);
                
                const vqaLabel = document.getElementById('vqa-selected-image-panel');
                if (vqaLabel) vqaLabel.textContent = "Sentinel-2 ?" 2025-04-02";
                
                if (caseStudyAfterMeta) {
                    populateInspector({
                        id: caseStudyAfterScene,
                        name: "Sentinel-2 ?" 2025-04-02",
                        is_stac: true,
                        bounds: caseStudyAfterMeta.bounds,
                        preview_url: caseStudyAfterMeta.preview_url || caseStudyAfterMeta.image_url,
                        bands: [ { id: 'True Color', description: 'Visual' } ],
                        metadata: { crs: caseStudyAfterMeta.display_crs || 'EPSG:4326' },
                        scene_info: { datetime: caseStudyAfterMeta.datetime || "2025-04-02", scene_id: caseStudyAfterScene, cloud_cover: caseStudyAfterMeta["eo:cloud_cover"] }
                    });
                }
                const KANCHA_AOI = [[17.41, 78.32], [17.45, 78.36]];
                map.fitBounds(KANCHA_AOI, { padding: [40, 40] });
                map.invalidateSize(true);
            } else {
                if (changeBeforeLayer) map.removeLayer(changeBeforeLayer);
                if (changeOverlayLayer) map.removeLayer(changeOverlayLayer);
                if (changeAfterLayer) {
                    changeAfterLayer.addTo(map);
                    changeAfterLayer.bringToFront();
                }
                if (window.changeLegendControl) map.removeControl(window.changeLegendControl);
                if (afterSel && afterSel.value) updateInspectorForCaseStudy(afterSel.value);
            }
        });
    }
    
    if (btnChange) {
        btnChange.addEventListener('click', () => {
            if (changeAnalysisMode === 'case-study') {
                if (caseStudyBeforeLayer) map.removeLayer(caseStudyBeforeLayer);
                if (caseStudyAfterLayer) {
                    caseStudyAfterLayer.addTo(map);
                    caseStudyAfterLayer.bringToFront();
                }
                if (caseStudyChangeLayer) {
                    caseStudyChangeLayer.addTo(map);
                    caseStudyChangeLayer.bringToFront();
                    if (window.changeLegendControl) window.changeLegendControl.addTo(map);
                } else {
                    if (window.changeLegendControl) map.removeControl(window.changeLegendControl);
                    alert("Run Change Analysis first");
                }
                if (caseStudyAoiLayer) caseStudyAoiLayer.bringToFront();
                
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
                } catch(e) {
                    console.warn("Could not set inspector for change", e);
                }
                
                const KANCHA_AOI = [[17.41, 78.32], [17.45, 78.36]];
                map.fitBounds(KANCHA_AOI, { padding: [40, 40] });
                map.invalidateSize(true);
            } else {
                if (changeBeforeLayer) map.removeLayer(changeBeforeLayer);
                if (changeAfterLayer) {
                    changeAfterLayer.addTo(map);
                    changeAfterLayer.bringToFront();
                }
                if (changeOverlayLayer) {
                    changeOverlayLayer.addTo(map);
                    changeOverlayLayer.bringToFront();
                }
                if (window.changeLegendControl) window.changeLegendControl.addTo(map);
                if (afterSel && afterSel.value) updateInspectorForCaseStudy(afterSel.value);
            }
        });
    }'''

# Create a regex to match the old listeners precisely, ignoring the weird unicode chars.
# Wait, let's just find the if (btnBefore) { ... } block all the way to the end of if (btnChange) { ... }
start_marker = "      if (btnBefore) {"
end_marker = "      if (beforeSel) {"

idx_start = content.find(start_marker)
idx_end = content.find(end_marker)

if idx_start != -1 and idx_end != -1:
    new_content = content[:idx_start] + old_listeners + "\n\n" + content[idx_end:]
    with open('frontend/app.js', 'w', encoding='utf8') as f:
        f.write(new_content)
    print("REPLACED LISTENERS")
else:
    print("COULD NOT FIND LISTENERS TO REPLACE")

