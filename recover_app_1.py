import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

# 1. Add globals
globals_old = '''let currentAOI = null; // Current Area of Interest'''
globals_new = '''let currentAOI = null; // Current Area of Interest
let changeAnalysisMode = "live";
let caseStudyBeforeScene = null;
let caseStudyAfterScene = null;
let caseStudyBeforeLayer = null;
let caseStudyAfterLayer = null;
let caseStudyChangeLayer = null;
let caseStudyAoiLayer = null;
let caseStudyBeforeMeta = null;
let caseStudyAfterMeta = null;

async function loggedFetch(url, options = {}) {
    console.log([FETCH REQUEST] \ \);
    const res = await fetch(url, options);
    console.log([FETCH RESPONSE] \ \);
    return res;
}'''

content = content.replace(globals_old, globals_new)

# 2. Add Kancha Case Study activate function
update_dropdowns = '''function updateChangeAnalysisDropdowns() {'''
kancha_func = '''const KANCHA_CASE_STUDY = {
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
    });
}

function updateChangeAnalysisDropdowns() {
    if (changeAnalysisMode === 'case-study') return;'''

content = content.replace(update_dropdowns, kancha_func)

# 3. Add to DOMContentLoaded
dom_old = '''const afterSel = document.getElementById('change-after-select');'''
dom_new = '''const afterSel = document.getElementById('change-after-select');
      const btnBefore = document.getElementById('btn-vis-before');
      const btnAfter = document.getElementById('btn-vis-after');
      const btnChange = document.getElementById('btn-vis-change');
      
      if (btnBefore) {
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
                  } catch(e) {}
                  
                  const KANCHA_AOI = [[17.41, 78.32], [17.45, 78.36]];
                  map.fitBounds(KANCHA_AOI, { padding: [40, 40] });
                  map.invalidateSize(true);
              }
          });
      }'''

content = content.replace(dom_old, dom_new)

# 4. Handle Case Study selector
case_study_old = '''const stacCloudCover = document.getElementById('stac-cloud-cover');'''
case_study_new = '''const caseStudySel = document.getElementById('change-case-study');
    if (caseStudySel) {
        caseStudySel.addEventListener('change', () => {
            if (caseStudySel.value === 'kancha') {
                activateKanchaCaseStudy();
                return;
            }
            changeAnalysisMode = "live";
            updateChangeAnalysisDropdowns();
        });
    }

    const stacCloudCover = document.getElementById('stac-cloud-cover');'''

content = content.replace(case_study_old, case_study_new)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("RECOVERED STAGE 1")
