import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

old_btnChange = '''    if (btnChange) {
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

new_btnChange = '''    if (btnChange) {
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
                
                const vqaLabel = document.getElementById('vqa-selected-image-panel');
                if (vqaLabel) vqaLabel.textContent = "Change Analysis";
                
                document.getElementById('inspector-empty').style.display = 'none';
                document.getElementById('inspector-content').style.display = 'block';
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

content = content.replace(old_btnChange, new_btnChange)
with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("REPLACED app.js")
