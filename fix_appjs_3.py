import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

# Fix activateKanchaCaseStudy
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
    document.getElementById('inspector-content').style.display = 'none';
    document.getElementById('inspector-empty').style.display = 'block';

    caseStudyBeforeScene = KANCHA_CASE_STUDY.before.id;
    caseStudyAfterScene = KANCHA_CASE_STUDY.after.id;

    // Center map and invalidate size immediately
    map.setView([17.43, 78.34], 13);
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
        
        const kanchaBounds = [[17.41, 78.32], [17.45, 78.36]];
        caseStudyAoiLayer = L.rectangle(kanchaBounds, {color: 'blue', weight: 2, fill: false});
        caseStudyAoiLayer.addTo(map);
        console.log("AOI DRAWN");
        map.invalidateSize(true);
        
        const boundsObj = L.latLngBounds(kanchaBounds);
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

# Fix image_overlay handling in vqa result
def replace_overlay(match):
    return '''                        if (ev.type === 'image_overlay') {
                            console.log("CHANGE OVERLAY RECEIVED");
                            const imgOverlay = L.imageOverlay(ev.data, ev.bounds, {opacity: 1.0}); // will set appropriately
                            
                            if (changeAnalysisMode === 'case-study') {
                                if (caseStudyChangeLayer) map.removeLayer(caseStudyChangeLayer);
                                caseStudyChangeLayer = imgOverlay;
                                
                                if (caseStudyBeforeLayer) map.removeLayer(caseStudyBeforeLayer);
                                if (caseStudyAfterLayer) caseStudyAfterLayer.addTo(map);
                                caseStudyChangeLayer.addTo(map);
                                console.log("CHANGE OVERLAY ADDED");
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
                                            <div style="width:12px;height:12px;border:2px solid blue;"></div>
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
