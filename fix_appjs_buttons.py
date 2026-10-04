import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

# Replace the buttons logic
def replace_buttons(match):
    return '''    if (btnBefore) {
        btnBefore.addEventListener('click', () => {
            if (changeAnalysisMode === 'case-study') {
                if (caseStudyAfterLayer) map.removeLayer(caseStudyAfterLayer);
                if (caseStudyChangeLayer) map.removeLayer(caseStudyChangeLayer);
                if (caseStudyBeforeLayer) caseStudyBeforeLayer.addTo(map);
                if (window.changeLegendControl) map.removeControl(window.changeLegendControl);
                
                const vqaLabel = document.getElementById('vqa-selected-image-panel');
                if (vqaLabel) vqaLabel.textContent = "Sentinel-2 — 2025-03-28";
                
                if (caseStudyBeforeMeta) {
                    populateInspector({
                        id: caseStudyBeforeScene,
                        name: "Sentinel-2 — 2025-03-28",
                        is_stac: true,
                        bounds: caseStudyBeforeMeta.bounds,
                        preview_url: caseStudyBeforeMeta.preview_url || caseStudyBeforeMeta.image_url,
                        bands: [ { id: 'True Color', description: 'Visual' } ],
                        metadata: { crs: caseStudyBeforeMeta.display_crs || 'EPSG:4326' },
                        scene_info: { datetime: caseStudyBeforeMeta.datetime || "2025-03-28", scene_id: caseStudyBeforeScene, cloud_cover: caseStudyBeforeMeta["eo:cloud_cover"] }
                    });
                }
                map.invalidateSize(true);
            } else {
                if (changeAfterLayer) map.removeLayer(changeAfterLayer);
                if (changeOverlayLayer) map.removeLayer(changeOverlayLayer);
                if (changeBeforeLayer) changeBeforeLayer.addTo(map);
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
                if (caseStudyAfterLayer) caseStudyAfterLayer.addTo(map);
                if (window.changeLegendControl) map.removeControl(window.changeLegendControl);
                
                const vqaLabel = document.getElementById('vqa-selected-image-panel');
                if (vqaLabel) vqaLabel.textContent = "Sentinel-2 — 2025-04-02";
                
                if (caseStudyAfterMeta) {
                    populateInspector({
                        id: caseStudyAfterScene,
                        name: "Sentinel-2 — 2025-04-02",
                        is_stac: true,
                        bounds: caseStudyAfterMeta.bounds,
                        preview_url: caseStudyAfterMeta.preview_url || caseStudyAfterMeta.image_url,
                        bands: [ { id: 'True Color', description: 'Visual' } ],
                        metadata: { crs: caseStudyAfterMeta.display_crs || 'EPSG:4326' },
                        scene_info: { datetime: caseStudyAfterMeta.datetime || "2025-04-02", scene_id: caseStudyAfterScene, cloud_cover: caseStudyAfterMeta["eo:cloud_cover"] }
                    });
                }
                map.invalidateSize(true);
            } else {
                if (changeBeforeLayer) map.removeLayer(changeBeforeLayer);
                if (changeOverlayLayer) map.removeLayer(changeOverlayLayer);
                if (changeAfterLayer) changeAfterLayer.addTo(map);
                if (window.changeLegendControl) map.removeControl(window.changeLegendControl);
                if (afterSel && afterSel.value) updateInspectorForCaseStudy(afterSel.value);
            }
        });
    }
    
    if (btnChange) {
        btnChange.addEventListener('click', () => {
            if (changeAnalysisMode === 'case-study') {
                if (caseStudyBeforeLayer) map.removeLayer(caseStudyBeforeLayer);
                if (caseStudyAfterLayer) caseStudyAfterLayer.addTo(map);
                if (caseStudyChangeLayer) {
                    caseStudyChangeLayer.addTo(map);
                    if (window.changeLegendControl) window.changeLegendControl.addTo(map);
                } else {
                    if (window.changeLegendControl) map.removeControl(window.changeLegendControl);
                    alert("Run Change Analysis first");
                }
                map.invalidateSize(true);
            } else {
                if (changeBeforeLayer) map.removeLayer(changeBeforeLayer);
                if (changeAfterLayer) changeAfterLayer.addTo(map);
                if (changeOverlayLayer) changeOverlayLayer.addTo(map);
                if (window.changeLegendControl) window.changeLegendControl.addTo(map);
                if (afterSel && afterSel.value) updateInspectorForCaseStudy(afterSel.value);
            }
        });
    }'''

content = re.sub(r'    if \(btnBefore\) \{.*?if \(btnChange\) \{.*?\n        \}\);\n    \}', replace_buttons, content, flags=re.DOTALL)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("REPLACED app.js")
