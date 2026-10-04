import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

# Add caseStudyAoiLayer global
if 'let caseStudyAoiLayer' not in content:
    content = content.replace('let caseStudyChangeLayer = null;', 'let caseStudyChangeLayer = null;\nlet caseStudyAoiLayer = null;')

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
        
        // 6. Set the map view to Kancha Gachibowli and draw blue rectangle.
        const kanchaBounds = [[17.41, 78.32], [17.45, 78.36]];
        map.fitBounds(kanchaBounds);
        
        caseStudyAoiLayer = L.rectangle(kanchaBounds, {color: 'blue', weight: 2, fill: false});
        caseStudyAoiLayer.addTo(map);
        
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
}'''

content = re.sub(r'function activateKanchaCaseStudy\(\) \{.*?(?=\nfunction |\nconst |\n$)', new_activate, content, flags=re.DOTALL)

# Update legend control logic inside ev.type === 'image_overlay'
old_legend = '''                            window.changeLegendControl.onAdd = function(map) {
                                const div = L.DomUtil.create('div', 'satquery-change-legend');
                                div.innerHTML = 
                                    <div class="legend-title">Change Analysis</div>
                                    <div class="legend-row">
                                        <span class="legend-color"></span>
                                        <span>Detected change</span>
                                    </div>
                                    <div class="legend-row">
                                        <span class="legend-neutral"></span>
                                        <span>Satellite imagery</span>
                                    </div>
                                ;
                                L.DomEvent.disableClickPropagation(div);
                                return div;
                            };'''

new_legend = '''                            window.changeLegendControl.onAdd = function(map) {
                                const div = L.DomUtil.create('div', 'satquery-change-legend');
                                div.style.background = 'white';
                                div.style.border = '2px solid #ccc';
                                div.style.padding = '8px';
                                div.style.borderRadius = '4px';
                                div.innerHTML = 
                                    <div style="font-weight:bold;margin-bottom:5px;">Change Analysis</div>
                                    <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
                                        <div style="width:12px;height:12px;background:rgba(255,0,0,0.6);border:1px solid red;"></div>
                                        <span>Detected change</span>
                                    </div>
                                    <div style="display:flex;align-items:center;gap:6px;">
                                        <div style="width:12px;height:12px;border:2px solid blue;"></div>
                                        <span>Analysis AOI</span>
                                    </div>
                                ;
                                L.DomEvent.disableClickPropagation(div);
                                return div;
                            };'''

if old_legend in content:
    content = content.replace(old_legend, new_legend)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("REPLACED app.js")
