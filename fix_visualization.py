import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

# 1. Update activateKanchaCaseStudy
def replace_activate(match):
    return '''function activateKanchaCaseStudy() {
    console.log("CASE STUDY ACTIVATED");
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
    
    // 1. Clear all previous raster/image layers (DO NOT CLEAR MAP OR BASEMAP)
    if (imageOverlay) { map.removeLayer(imageOverlay); imageOverlay = null; }
    if (caseStudyBeforeLayer) { map.removeLayer(caseStudyBeforeLayer); caseStudyBeforeLayer = null; }
    if (caseStudyAfterLayer) { map.removeLayer(caseStudyAfterLayer); caseStudyAfterLayer = null; }
    if (caseStudyChangeLayer) { map.removeLayer(caseStudyChangeLayer); caseStudyChangeLayer = null; }
    if (caseStudyAoiLayer) { map.removeLayer(caseStudyAoiLayer); caseStudyAoiLayer = null; }
    if (changeBeforeLayer) { map.removeLayer(changeBeforeLayer); changeBeforeLayer = null; }
    if (changeAfterLayer) { map.removeLayer(changeAfterLayer); changeAfterLayer = null; }
    if (changeOverlayLayer) { map.removeLayer(changeOverlayLayer); changeOverlayLayer = null; }
    if (window.changeLegendControl) { map.removeControl(window.changeLegendControl); window.changeLegendControl = null; }
    if (vqaEvidenceLayer) { vqaEvidenceLayer.clearLayers(); }
    
    clearLayerList();

    caseStudyBeforeScene = KANCHA_CASE_STUDY.before.id;
    caseStudyAfterScene = KANCHA_CASE_STUDY.after.id;

    const KANCHA_AOI = [[17.41, 78.32], [17.45, 78.36]];
    map.fitBounds(KANCHA_AOI, { padding: [40, 40] });
    map.invalidateSize(true);
    console.log("CASE STUDY MAP CENTERED");

    Promise.all([
        loggedFetch("http://127.0.0.1:8000/api/v1/catalog/scene/" + caseStudyBeforeScene).then(r => r.json()),
        loggedFetch("http://127.0.0.1:8000/api/v1/catalog/scene/" + caseStudyAfterScene).then(r => r.json())
    ]).then(([beforeData, afterData]) => {
        caseStudyBeforeMeta = beforeData;
        caseStudyAfterMeta = afterData;
        
        const beforeUrl = beforeData.preview_url || beforeData.image_url;
        const afterUrl = afterData.preview_url || afterData.image_url;
        
        caseStudyBeforeLayer = L.imageOverlay(beforeUrl, beforeData.bounds, { opacity: 1.0 });
        caseStudyAfterLayer = L.imageOverlay(afterUrl, afterData.bounds, { opacity: 1.0 });
        caseStudyBeforeLayer.addTo(map);
        console.log("BEFORE PREVIEW LOADED");
        console.log("AFTER PREVIEW LOADED");
        
        caseStudyAoiLayer = L.rectangle(KANCHA_AOI, {color: '#0066ff', weight: 3, fill: false});
        caseStudyAoiLayer.addTo(map);
        console.log("AOI DRAWN");
        map.fitBounds(KANCHA_AOI, { padding: [40, 40] });
        map.invalidateSize(true);
        
        const boundsObj = L.latLngBounds(KANCHA_AOI);
        const nw = boundsObj.getNorthWest();
        const se = boundsObj.getSouthEast();
        currentAOI = {
            geometry_type: 'Polygon',
            type: 'Polygon',
            bbox: { west: nw.lng, north: nw.lat, east: se.lng, south: se.lat },
            bounds: boundsObj,
            geometry: {
                type: 'Polygon',
                coordinates: [[
                    [nw.lng, nw.lat],
                    [se.lng, nw.lat],
                    [se.lng, se.lat],
                    [nw.lng, se.lat],
                    [nw.lng, nw.lat]
                ]]
            }
        };
        
        const vqaLabel = document.getElementById('vqa-selected-image-panel');
        if (vqaLabel) vqaLabel.textContent = "Sentinel-2 — 2025-03-28";
        
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
    }).catch(err => {
        console.error("Failed to load case study scenes:", err);
    });
}'''

content = re.sub(r'function activateKanchaCaseStudy\(\) \{.*?(?=\nfunction |\nconst |\n$)', replace_activate, content, flags=re.DOTALL)

# 2. Update buttons to always call map.fitBounds(KANCHA_AOI, {padding: [40,40]})
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
                const KANCHA_AOI = [[17.41, 78.32], [17.45, 78.36]];
                map.fitBounds(KANCHA_AOI, { padding: [40, 40] });
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
                const KANCHA_AOI = [[17.41, 78.32], [17.45, 78.36]];
                map.fitBounds(KANCHA_AOI, { padding: [40, 40] });
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
                const KANCHA_AOI = [[17.41, 78.32], [17.45, 78.36]];
                map.fitBounds(KANCHA_AOI, { padding: [40, 40] });
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


# 3. Update VQA change overlay handler
def replace_overlay(match):
    return '''                        if (ev.type === 'image_overlay') {
                            console.log("CHANGE OVERLAY RECEIVED");
                            
                            if (changeAnalysisMode === 'case-study') {
                                const KANCHA_AOI = [[17.41, 78.32], [17.45, 78.36]];
                                // Clip the overlay to the exact AOI, not the full scene bounds
                                const imgOverlay = L.imageOverlay(ev.data, KANCHA_AOI, {opacity: 0.65, interactive: false});
                                
                                if (caseStudyChangeLayer) map.removeLayer(caseStudyChangeLayer);
                                caseStudyChangeLayer = imgOverlay;
                                
                                if (caseStudyBeforeLayer) map.removeLayer(caseStudyBeforeLayer);
                                if (caseStudyAfterLayer) caseStudyAfterLayer.addTo(map);
                                caseStudyChangeLayer.addTo(map);
                                console.log("CHANGE OVERLAY ADDED");
                                map.fitBounds(KANCHA_AOI, { padding: [40, 40] });
                                map.invalidateSize(true);
                                
                                if (window.changeLegendControl) {
                                    map.removeControl(window.changeLegendControl);
                                }
                                window.changeLegendControl = L.control({position: 'bottomright'});
                                window.changeLegendControl.onAdd = function(map) {
                                    const div = L.DomUtil.create('div', 'satquery-change-legend');
                                    div.style.background = 'white';
                                    div.style.border = '2px solid #ccc';
                                    div.style.padding = '8px';
                                    div.style.borderRadius = '4px';
                                    div.innerHTML = 
                                        <div style="font-weight:bold;margin-bottom:5px;">Change Analysis</div>
                                        <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
                                            <div style="width:12px;height:12px;background:rgba(255,0,0,1.0);border:1px solid red;"></div>
                                            <span>Detected change</span>
                                        </div>
                                        <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
                                            <div style="width:12px;height:12px;border:2px solid #0066ff;"></div>
                                            <span>Kancha Gachibowli AOI</span>
                                        </div>
                                        <div style="display:flex;align-items:center;gap:6px;">
                                            <div style="width:12px;height:12px;background:transparent;border:1px solid #ccc;"></div>
                                            <span>Satellite imagery</span>
                                        </div>
                                    ;
                                    L.DomEvent.disableClickPropagation(div);
                                    return div;
                                };
                                window.changeLegendControl.addTo(map);
                            } else {
                                const imgOverlay = L.imageOverlay(ev.data, ev.bounds, {opacity: 1.0});
                                if (changeOverlayLayer) map.removeLayer(changeOverlayLayer);
                                changeOverlayLayer = imgOverlay;
                                
                                if (changeBeforeLayer) map.removeLayer(changeBeforeLayer);
                                if (changeAfterLayer) changeAfterLayer.addTo(map);
                                changeOverlayLayer.addTo(map);
                                
                                if (window.changeLegendControl) {
                                    map.removeControl(window.changeLegendControl);
                                }
                                window.changeLegendControl = L.control({position: 'bottomright'});
                                window.changeLegendControl.onAdd = function(map) {
                                    const div = L.DomUtil.create('div', 'satquery-change-legend');
                                    div.innerHTML = <div class="legend-title">Change Analysis</div>;
                                    L.DomEvent.disableClickPropagation(div);
                                    return div;
                                };
                                window.changeLegendControl.addTo(map);
                            }
                            return;
                        }'''

content = re.sub(r'                        if \(ev\.type === \'image_overlay\'\) \{.*?return; // Skip the default grounding bbox rendering\s*\}', replace_overlay, content, flags=re.DOTALL)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("REPLACED app.js")
