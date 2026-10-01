// =============== NEW SATQUERY FEATURES ===============

// 1. Mode Switching
const appModeSelector = document.getElementById('app-mode-selector');
const studentExplanation = document.getElementById('student-explanation');
const farmerResultCard = document.getElementById('farmer-result-card');
const researcherResultCard = document.getElementById('researcher-result-card');
const farmerTemporalControls = document.getElementById('farmer-temporal-controls');
const ndviControls = document.getElementById('ndvi-controls');
const analysisResultSection = document.getElementById('analysis-result-section');
const analysisType = document.getElementById('analysis-type');

if (appModeSelector) {
    appModeSelector.addEventListener('change', (e) => {
        const mode = e.target.value;
        
        // Hide all first
        if (studentExplanation) studentExplanation.style.display = 'none';
        if (farmerResultCard) farmerResultCard.style.display = 'none';
        if (researcherResultCard) researcherResultCard.style.display = 'none';
        
        if (mode === 'student') {
            if (studentExplanation) studentExplanation.style.display = 'block';
            if (farmerResultCard) farmerResultCard.style.display = 'block';
            analysisType.value = 'temporal';
            farmerTemporalControls.style.display = 'block';
            ndviControls.style.display = 'none';
        } else if (mode === 'farmer') {
            if (farmerResultCard) farmerResultCard.style.display = 'block';
            analysisType.value = 'temporal';
            farmerTemporalControls.style.display = 'block';
            ndviControls.style.display = 'none';
        } else if (mode === 'researcher') {
            if (researcherResultCard) researcherResultCard.style.display = 'block';
            analysisType.value = 'ndvi';
            farmerTemporalControls.style.display = 'none';
            ndviControls.style.display = 'block';
        }
    });
}

if (analysisType) {
    analysisType.addEventListener('change', (e) => {
        const type = e.target.value;
        if (type === 'temporal') {
            farmerTemporalControls.style.display = 'block';
            ndviControls.style.display = 'none';
        } else {
            farmerTemporalControls.style.display = 'none';
            ndviControls.style.display = 'block';
        }
    });
}

// 2. AOI Selection
let currentAoiBounds = null;
const btnDrawRect = document.getElementById('btn-draw-rect');
const btnDrawPoly = document.getElementById('btn-draw-poly');
const btnClearAoi = document.getElementById('btn-clear-aoi');
const aoiDetails = document.getElementById('aoi-details');
const aoiPrompt = document.getElementById('aoi-prompt');

if (btnDrawRect) {
    btnDrawRect.addEventListener('click', () => {
        if (drawnItems && drawnItems.getLayers().length > 0) {
            drawnItems.clearLayers();
        }
        new L.Draw.Rectangle(map, { shapeOptions: { color: 'var(--accent)' } }).enable();
    });
}
if (btnDrawPoly) {
    btnDrawPoly.addEventListener('click', () => {
        if (drawnItems && drawnItems.getLayers().length > 0) {
            drawnItems.clearLayers();
        }
        new L.Draw.Polygon(map, { shapeOptions: { color: 'var(--accent)' } }).enable();
    });
}
if (btnClearAoi) {
    btnClearAoi.addEventListener('click', () => {
        if (drawnItems) drawnItems.clearLayers();
        currentAoiBounds = null;
        if (aoiDetails) aoiDetails.style.display = 'none';
        if (aoiPrompt) aoiPrompt.style.display = 'block';
    });
}

// Hook into the Leaflet draw created event (we already have one in app.js, we will just add another listener or override it)
map.on(L.Draw.Event.CREATED, function (e) {
    // Note: the original listener adds it to drawnItems. We will just compute the bounds.
    setTimeout(() => {
        if (drawnItems && drawnItems.getLayers().length > 0) {
            const layer = drawnItems.getLayers()[0];
            const bounds = layer.getBounds();
            currentAoiBounds = [bounds.getWest(), bounds.getSouth(), bounds.getEast(), bounds.getNorth()];
            
            if (aoiDetails) {
                aoiDetails.style.display = 'block';
                document.getElementById('aoi-area').textContent = 'Selected';
                document.getElementById('aoi-center').textContent = bounds.getCenter().lat.toFixed(4) + ', ' + bounds.getCenter().lng.toFixed(4);
                document.getElementById('aoi-bounds').textContent = bounds.getWest().toFixed(4) + ', ' + bounds.getSouth().toFixed(4) + '\\n' + bounds.getEast().toFixed(4) + ', ' + bounds.getNorth().toFixed(4);
            }
            if (aoiPrompt) aoiPrompt.style.display = 'none';
        }
    }, 100);
});


// 3. Temporal Analysis Logic
let lastAnalysisReport = {};

async function fetchSceneForDate(bbox, targetDate) {
    // construct date range: targetDate to targetDate + 1 month
    const d = new Date(targetDate);
    const dEnd = new Date(d);
    dEnd.setMonth(d.getMonth() + 1);
    
    const endStr = dEnd.toISOString().split('T')[0];
    
    const req = {
        bbox: bbox,
        start_date: targetDate,
        end_date: endStr,
        max_cloud_cover: 20,
        limit: 1
    };
    
    const resp = await fetch('http://127.0.0.1:8000/api/v1/catalog/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(req)
    });
    
    if (!resp.ok) return null;
    const data = await resp.json();
    if (data.results && data.results.length > 0) {
        return data.results[0].id;
    }
    return null;
}

async function runNdvi(sceneId) {
    const res = await fetch('http://127.0.0.1:8000/api/v1/analysis/ndvi', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scene_id: sceneId, roi: null })
    });
    if (!res.ok) return null;
    return await res.json();
}

async function runVqa(sceneId, question) {
    const body = {
        image_id: sceneId,
        image_type: 'satellite_scene',
        source: 'sentinel-2',
        modality: 'optical',
        representation: 'rgb',
        question: question,
        mode: 'vqa'
    };
    const res = await fetch('http://127.0.0.1:8000/api/v1/vqa/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    if (!res.ok) return null;
    return await res.json();
}

const btnRunAnalysis = document.getElementById('btn-run-analysis');
if (btnRunAnalysis) {
    btnRunAnalysis.addEventListener('click', async () => {
        const type = analysisType.value;
        const bbox = currentAoiBounds || [map.getBounds().getWest(), map.getBounds().getSouth(), map.getBounds().getEast(), map.getBounds().getNorth()];
        
        btnRunAnalysis.disabled = true;
        btnRunAnalysis.textContent = 'Running Analysis...';
        if (analysisResultSection) analysisResultSection.style.display = 'none';
        
        if (type === 'temporal') {
            try {
                const prevDate = document.getElementById('farmer-prev-date').value;
                const currDate = document.getElementById('farmer-curr-date').value;
                
                document.getElementById('res-prev-date').textContent = prevDate + " (Searching...)";
                document.getElementById('res-curr-date').textContent = currDate + " (Searching...)";
                if (analysisResultSection) analysisResultSection.style.display = 'block';
                
                const prevScene = await fetchSceneForDate(bbox, prevDate);
                const currScene = await fetchSceneForDate(bbox, currDate);
                
                if (!prevScene || !currScene) {
                    alert("Could not find clear satellite images for both dates in the selected area.");
                    btnRunAnalysis.disabled = false;
                    btnRunAnalysis.textContent = 'Run Analysis';
                    return;
                }
                
                document.getElementById('res-prev-date').textContent = prevDate +  (Scene: );
                document.getElementById('res-curr-date').textContent = currDate +  (Scene: );
                
                document.getElementById('res-veg-change').textContent = "Analyzing vegetation...";
                const prevNdvi = await runNdvi(prevScene);
                const currNdvi = await runNdvi(currScene);
                
                let vegDesc = "Unknown";
                if (prevNdvi && currNdvi) {
                    const diff = currNdvi.statistics.mean - prevNdvi.statistics.mean;
                    if (diff > 0.05) vegDesc = "Vegetation increased";
                    else if (diff < -0.05) vegDesc = "Vegetation decreased";
                    else vegDesc = "Little visible change detected";
                }
                document.getElementById('res-veg-change').textContent = vegDesc;
                
                document.getElementById('res-water-change').textContent = "Analyzing water...";
                const prevWater = await runVqa(prevScene, "Is there water in the image?");
                const currWater = await runVqa(currScene, "Is there water in the image?");
                
                let w1 = (prevWater && prevWater.answer.toLowerCase() === 'yes') ? "Detected" : "Not detected";
                let w2 = (currWater && currWater.answer.toLowerCase() === 'yes') ? "Detected" : "Not detected";
                document.getElementById('res-water-change').textContent = Previous:  | Current: ;
                
                let overall = "Changes were observed in the satellite imagery between the two dates.";
                if (vegDesc === "Vegetation decreased") overall = "Vegetation cover has decreased. " + overall;
                else if (vegDesc === "Vegetation increased") overall = "Vegetation cover has increased. " + overall;
                document.getElementById('res-overall').textContent = overall;
                
                lastAnalysisReport = {
                    type: 'temporal',
                    bbox, prevDate, currDate, prevScene, currScene, vegDesc, w1, w2, overall,
                    prevNdviStats: prevNdvi ? prevNdvi.statistics : null,
                    currNdviStats: currNdvi ? currNdvi.statistics : null,
                    prevVqa: prevWater, currVqa: currWater
                };
                
            } catch (err) {
                console.error(err);
                alert("Error during temporal analysis: " + err.message);
            }
        } else {
            // Standard NDVI fallback to existing logic if needed, or implement here
            const sceneId = document.getElementById('analysis-scene').value;
            if (!sceneId) {
                alert("Please select a scene first from the Data tab.");
                btnRunAnalysis.disabled = false;
                btnRunAnalysis.textContent = 'Run Analysis';
                return;
            }
            try {
                if (analysisResultSection) analysisResultSection.style.display = 'block';
                const ndvi = await runNdvi(sceneId);
                if (ndvi) {
                    if (document.getElementById('res-researcher-aoi')) {
                        document.getElementById('res-researcher-aoi').textContent = JSON.stringify(ndvi.statistics, null, 2);
                    }
                    lastAnalysisReport = { type: 'ndvi', sceneId, ndvi };
                }
            } catch (err) {
                console.error(err);
                alert("Error during analysis: " + err.message);
            }
        }
        
        btnRunAnalysis.disabled = false;
        btnRunAnalysis.textContent = 'Run Analysis';
    });
}

// 4. Map Language
const mapLanguage = document.getElementById('map-language');
if (mapLanguage) {
    mapLanguage.addEventListener('change', (e) => {
        const lang = e.target.value;
        if (basemapLayer) map.removeLayer(basemapLayer);
        
        if (lang === 'english') {
            basemapLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                subdomains: 'abcd',
                maxZoom: 20
            });
        } else {
            basemapLayer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                maxZoom: 19
            });
        }
        
        if (document.getElementById('basemap-toggle') && document.getElementById('basemap-toggle').checked) {
            basemapLayer.addTo(map);
        }
    });
}

// 5. Export Report
function generateReportHTML(mode) {
    let content = <html><head><title>SatQuery  Report</title><style>body{font-family:sans-serif; padding: 20px;} h1{color:#333;} .card{border:1px solid #ddd; padding:15px; border-radius:5px; margin-bottom:15px;}</style></head><body>;
    content += <h1>SatQuery AI -  Report</h1>;
    content += <p>Generated on: </p>;
    
    if (lastAnalysisReport.type === 'temporal') {
        content += <div class="card">
            <h3>Farm Comparison</h3>
            <p><strong>Bounding Box:</strong> </p>
            <p><strong>Previous Date:</strong>  (Scene: )</p>
            <p><strong>Current Date:</strong>  (Scene: )</p>
            <hr/>
            <p><strong>Vegetation Change:</strong> </p>
            <p><strong>Water Presence:</strong> Previous:  | Current: </p>
            <p><strong>Overall:</strong> </p>
        </div>;
        
        if (mode === 'student' || mode === 'researcher') {
            content += <div class="card">
                <h3>Technical Explanation</h3>
                <p><strong>Sentinel-2:</strong> A high-resolution optical satellite measuring visible and near-infrared light.</p>
                <p><strong>NDVI:</strong> Used to measure crop health by comparing near-infrared reflectance.</p>
                <p><strong>AI:</strong> We use PaliGemma (Vision-Language Model) to analyze the imagery and Grounding DINO to extract spatial locations.</p>
            </div>;
        }
        
        if (mode === 'researcher') {
            content += <div class="card">
                <h3>Raw Statistics</h3>
                <pre></pre>
            </div>;
        }
    } else {
        content += <p>No temporal analysis available to export. Run a Farm Comparison first.</p>;
    }
    
    content += <p style="font-style:italic; font-size: 12px; color: #666;">Satellite observations are indicative and should be verified on the ground.</p>;
    content += </body></html>;
    return content;
}

const btnExportFarmer = document.getElementById('btn-export-farmer');
const btnExportStudent = document.getElementById('btn-export-student');
const btnExportResearcher = document.getElementById('btn-export-researcher');

function downloadHtml(mode) {
    const blob = new Blob([generateReportHTML(mode)], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = satquery__report.html;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

if (btnExportFarmer) btnExportFarmer.addEventListener('click', () => downloadHtml('farmer'));
if (btnExportStudent) btnExportStudent.addEventListener('click', () => downloadHtml('student'));
if (btnExportResearcher) {
    btnExportResearcher.addEventListener('click', () => {
        const blob = new Blob([JSON.stringify(lastAnalysisReport, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = satquery_researcher_data.json;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
}
