import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_else = '''        } else {
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
        btnRunAnalysis.textContent = 'Run Analysis';'''

new_else = '''        } else {
            document.getElementById('btn-calc-ndvi').click();
            btnRunAnalysis.disabled = false;
            btnRunAnalysis.textContent = 'Run Analysis';
        }'''

if old_else in js:
    js = js.replace(old_else, new_else)
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Replaced else block")
else:
    print("Could not find else block")
