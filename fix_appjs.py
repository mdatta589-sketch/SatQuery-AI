import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

# We need to add the new global state variables
if 'let caseStudyBeforeScene' not in content:
    content = content.replace('let changeAnalysisMode = "live";', 
                              'let changeAnalysisMode = "live";\nlet caseStudyBeforeScene = null;\nlet caseStudyAfterScene = null;\nlet caseStudyBeforeLayer = null;\nlet caseStudyAfterLayer = null;\nlet caseStudyChangeLayer = null;\nlet caseStudyBeforeMeta = null;\nlet caseStudyAfterMeta = null;')

# Rewrite activateKanchaCaseStudy
new_activate = '''function activateKanchaCaseStudy() {
    changeAnalysisMode = "case-study";
    const beforeSel = document.getElementById("change-before-select");
    const afterSel = document.getElementById("change-after-select");
    
    if (beforeSel && afterSel) {
        beforeSel.innerHTML = "";
        afterSel.innerHTML = "";
        beforeSel.add(new Option("Sentinel-2 — 2025-03-28 — T44QKE", KANCHA_CASE_STUDY.before.id));
        afterSel.add(new Option("Sentinel-2 — 2025-04-02 — T44QKE", KANCHA_CASE_STUDY.after.id));
        beforeSel.value = KANCHA_CASE_STUDY.before.id;
        afterSel.value = KANCHA_CASE_STUDY.after.id;
    }
    
    const toggles = document.getElementById('case-study-vis-toggles');
    if (toggles) toggles.style.display = 'flex';
    
    // 1. Clear all previous raster/image layers.
    if (imageOverlay) { map.removeLayer(imageOverlay); imageOverlay = null; }
    if (caseStudyBeforeLayer) { map.removeLayer(caseStudyBeforeLayer); caseStudyBeforeLayer = null; }
    if (caseStudyAfterLayer) { map.removeLayer(caseStudyAfterLayer); caseStudyAfterLayer = null; }
    if (caseStudyChangeLayer) { map.removeLayer(caseStudyChangeLayer); caseStudyChangeLayer = null; }
    if (changeBeforeLayer) { map.removeLayer(changeBeforeLayer); changeBeforeLayer = null; }
    if (changeAfterLayer) { map.removeLayer(changeAfterLayer); changeAfterLayer = null; }
    if (changeOverlayLayer) { map.removeLayer(changeOverlayLayer); changeOverlayLayer = null; }
    if (window.changeLegendControl) { map.removeControl(window.changeLegendControl); window.changeLegendControl = null; }
    
    clearLayerList();
    document.getElementById('inspector-content').style.display = 'none';
    document.getElementById('inspector-empty').style.display = 'block';

    caseStudyBeforeScene = KANCHA_CASE_STUDY.before.id;
    caseStudyAfterScene = KANCHA_CASE_STUDY.after.id;

    // 2. Fetch metadata for BOTH exact STAC IDs.
    Promise.all([
        fetch("http://127.0.0.1:8000/api/v1/catalog/scene/" + caseStudyBeforeScene).then(r => r.json()),
        fetch("http://127.0.0.1:8000/api/v1/catalog/scene/" + caseStudyAfterScene).then(r => r.json())
    ]).then(([beforeData, afterData]) => {
        // 3. Store both metadata objects.
        caseStudyBeforeMeta = beforeData;
        caseStudyAfterMeta = afterData;
        
        // 4. Obtain both actual preview URLs.
        const beforeUrl = beforeData.preview_url || beforeData.image_url;
        const afterUrl = afterData.preview_url || afterData.image_url;
        
        // 5. Add the BEFORE preview to Leaflet.
        caseStudyBeforeLayer = L.imageOverlay(beforeUrl, beforeData.bounds, { opacity: 1.0 });
        caseStudyAfterLayer = L.imageOverlay(afterUrl, afterData.bounds, { opacity: 1.0 });
        caseStudyBeforeLayer.addTo(map);
        
        // 6. Set the map view to Kancha Gachibowli.
        const kanchaBounds = [[17.41, 78.32], [17.45, 78.36]];
        map.fitBounds(kanchaBounds);
        
        // 7. Update Image label to: Sentinel-2 — 2025-03-28
        const vqaLabel = document.getElementById('vqa-selected-image-panel');
        if (vqaLabel) vqaLabel.textContent = "Sentinel-2 — 2025-03-28";
        
        // 8. Update Inspector with the actual BEFORE scene metadata.
        const layerMeta = {
            id: caseStudyBeforeScene,
            name: "Sentinel-2 — 2025-03-28",
            is_stac: true,
            bounds: beforeData.bounds,
            preview_url: beforeUrl,
            bands: [ { id: 'True Color', description: 'Visual' } ],
            metadata: { 
                crs: beforeData.display_crs || beforeData.source_crs || 'EPSG:4326', 
                width: beforeData.display_width || 10980, 
                height: beforeData.display_height || 10980 
            },
            scene_info: {
                datetime: beforeData.datetime || "2025-03-28T05:06:59Z",
                cloud_cover: beforeData["eo:cloud_cover"] || 0.0,
                scene_id: caseStudyBeforeScene,
                assets: beforeData.assets || {}
            }
        };
        populateInspector(layerMeta);
        
        // 9. Do NOT call change analysis.
    }).catch(err => {
        console.error("Failed to load case study scenes:", err);
    });
}
'''

content = re.sub(r'function activateKanchaCaseStudy\(\) \{.*?(?=\nfunction |\nconst |\n$)', new_activate, content, flags=re.DOTALL)

# Replace the buttons logic
new_buttons = '''    if (btnBefore) {
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
            } else {
                if (changeBeforeLayer) map.removeLayer(changeBeforeLayer);
                if (changeAfterLayer) changeAfterLayer.addTo(map);
                if (changeOverlayLayer) changeOverlayLayer.addTo(map);
                if (window.changeLegendControl) window.changeLegendControl.addTo(map);
                if (afterSel && afterSel.value) updateInspectorForCaseStudy(afterSel.value);
            }
        });
    }'''

content = re.sub(r'    if \(btnBefore\) \{.*?if \(btnChange\) \{.*?\n        \}\);\n    \}', new_buttons, content, flags=re.DOTALL)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("REPLACED app.js")
