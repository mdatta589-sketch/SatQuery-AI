import re
with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

kancha_func = """
const KANCHA_CASE_STUDY = {
    before: {
        id: "S2B_MSIL2A_20250328T050659_R019_T44QKE_20250328T072008"
    },
    after: {
        id: "S2C_MSIL2A_20250402T050711_R019_T44QKE_20250402T101606"
    }
};

function activateKanchaCaseStudy() {
    console.log("CASE STUDY ACTIVATED");
    changeAnalysisMode = "case-study";
    const beforeSel = document.getElementById("change-before-select");
    const afterSel = document.getElementById("change-after-select");
    
    beforeSel.innerHTML = "";
    afterSel.innerHTML = "";
    beforeSel.add(new Option("Sentinel-2 — 2025-03-28 — T44QKE", KANCHA_CASE_STUDY.before.id));
    afterSel.add(new Option("Sentinel-2 — 2025-04-02 — T44QKE", KANCHA_CASE_STUDY.after.id));
    beforeSel.value = KANCHA_CASE_STUDY.before.id;
    afterSel.value = KANCHA_CASE_STUDY.after.id;
    
    caseStudyBeforeScene = KANCHA_CASE_STUDY.before.id;
    caseStudyAfterScene = KANCHA_CASE_STUDY.after.id;

    if (imageOverlay) { map.removeLayer(imageOverlay); imageOverlay = null; }
    if (caseStudyBeforeLayer) { map.removeLayer(caseStudyBeforeLayer); caseStudyBeforeLayer = null; }
    if (caseStudyAfterLayer) { map.removeLayer(caseStudyAfterLayer); caseStudyAfterLayer = null; }
    if (caseStudyChangeLayer) { map.removeLayer(caseStudyChangeLayer); caseStudyChangeLayer = null; }
    if (caseStudyAoiLayer) { map.removeLayer(caseStudyAoiLayer); caseStudyAoiLayer = null; }

    const KANCHA_AOI = [[17.41, 78.32], [17.45, 78.36]];
    map.fitBounds(KANCHA_AOI, { padding: [40, 40] });
    map.invalidateSize(true);
    
    caseStudyAoiLayer = L.rectangle(KANCHA_AOI, {color: '#0066ff', weight: 3, fill: false});
    caseStudyAoiLayer.addTo(map);
    caseStudyAoiLayer.bringToFront();
    
    const boundsObj = L.latLngBounds(KANCHA_AOI);
    currentAOI = {
        geometry_type: 'Polygon',
        type: 'Polygon',
        bbox: { west: boundsObj.getWest(), north: boundsObj.getNorth(), east: boundsObj.getEast(), south: boundsObj.getSouth() },
        bounds: boundsObj,
        geometry: null
    };

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
        caseStudyBeforeLayer.bringToFront();
        caseStudyAoiLayer.bringToFront();
        
        const toggles = document.getElementById('case-study-vis-toggles');
        if (toggles) toggles.style.display = 'flex';
        
        const vqaLabel = document.getElementById('vqa-selected-image-panel');
        if (vqaLabel) vqaLabel.textContent = "Sentinel-2 — 2025-03-28";
        
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
        
        document.getElementById('change-analysis-message').style.display = 'none';
        document.getElementById('change-analysis-selectors').style.display = 'flex';
    });
}

function updateChangeAnalysisDropdowns() {
    if (changeAnalysisMode === 'case-study') return;
    
    const beforeSel = document.getElementById('change-before-select');
    const afterSel = document.getElementById('change-after-select');
    const msg = document.getElementById('change-analysis-message');
    const selectors = document.getElementById('change-analysis-selectors');
    
    const stacLayers = layers.filter(l => l.is_stac);
    if (stacLayers.length >= 2) {
        if (msg) msg.style.display = 'none';
        if (selectors) selectors.style.display = 'flex';
        
        const bVal = beforeSel.value;
        const aVal = afterSel.value;
        
        beforeSel.innerHTML = '';
        afterSel.innerHTML = '';
        stacLayers.forEach(l => {
            beforeSel.add(new Option(l.name, l.id));
            afterSel.add(new Option(l.name, l.id));
        });
        
        if (bVal && stacLayers.some(l => l.id === bVal)) beforeSel.value = bVal;
        if (aVal && stacLayers.some(l => l.id === aVal)) afterSel.value = aVal;
    } else {
        if (msg) msg.style.display = 'block';
        if (selectors) selectors.style.display = 'none';
    }
}
"""

content = content + kancha_func

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("ADDED FUNCTIONS")
