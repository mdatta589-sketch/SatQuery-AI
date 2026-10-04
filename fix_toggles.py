with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

import re

old_toggles = """    if (btnBefore) {
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
                if (vqaLabel) vqaLabel.textContent = "Sentinel-2 - 2025-03-28";
                
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
                if (vqaLabel) vqaLabel.textContent = "Sentinel-2 - 2025-04-02";
                
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
                }
                if (caseStudyAoiLayer) caseStudyAoiLayer.bringToFront();
                
                const vqaLabel = document.getElementById('vqa-selected-image-panel');
                if (vqaLabel) vqaLabel.textContent = "Change Analysis";
                
                const KANCHA_AOI = [[17.41, 78.32], [17.45, 78.36]];
                map.fitBounds(KANCHA_AOI, { padding: [40, 40] });
                map.invalidateSize(true);
            }
        });
    }"""

new_toggles = """    if (btnBefore) {
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
                if (vqaLabel) vqaLabel.textContent = "Sentinel-2 - 2025-03-28";
                
                const KANCHA_AOI = [[17.41, 78.32], [17.45, 78.36]];
                map.fitBounds(KANCHA_AOI, { padding: [40, 40] });
                map.invalidateSize(true);
            } else {
                if (changeAfterLayer) map.removeLayer(changeAfterLayer);
                if (changeOverlayLayer) map.removeLayer(changeOverlayLayer);
                if (changeBeforeLayer) {
                    changeBeforeLayer.addTo(map);
                    changeBeforeLayer.bringToFront();
                }
                if (window.changeLegendControl) map.removeControl(window.changeLegendControl);
                const beforeId = document.getElementById('change-before-select').value;
                const bLayerData = layers.find(l => l.id === beforeId);
                const vqaLabel = document.getElementById('vqa-selected-image-panel');
                if (vqaLabel && bLayerData) vqaLabel.textContent = `Before: ${bLayerData.name}`;
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
                if (vqaLabel) vqaLabel.textContent = "Sentinel-2 - 2025-04-02";
                
                const KANCHA_AOI = [[17.41, 78.32], [17.45, 78.36]];
                map.fitBounds(KANCHA_AOI, { padding: [40, 40] });
                map.invalidateSize(true);
            } else {
                if (changeBeforeLayer) map.removeLayer(changeBeforeLayer);
                if (changeOverlayLayer) map.removeLayer(changeOverlayLayer);
                if (changeAfterLayer) {
                    changeAfterLayer.addTo(map);
                    changeAfterLayer.bringToFront();
                }
                if (window.changeLegendControl) map.removeControl(window.changeLegendControl);
                const afterId = document.getElementById('change-after-select').value;
                const aLayerData = layers.find(l => l.id === afterId);
                const vqaLabel = document.getElementById('vqa-selected-image-panel');
                if (vqaLabel && aLayerData) vqaLabel.textContent = `After: ${aLayerData.name}`;
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
                }
                if (caseStudyAoiLayer) caseStudyAoiLayer.bringToFront();
                
                const vqaLabel = document.getElementById('vqa-selected-image-panel');
                if (vqaLabel) vqaLabel.textContent = "Change Analysis";
                
                const KANCHA_AOI = [[17.41, 78.32], [17.45, 78.36]];
                map.fitBounds(KANCHA_AOI, { padding: [40, 40] });
                map.invalidateSize(true);
            } else {
                if (changeBeforeLayer) map.removeLayer(changeBeforeLayer);
                if (changeAfterLayer) {
                    changeAfterLayer.addTo(map);
                    changeAfterLayer.bringToFront();
                }
                if (changeOverlayLayer) {
                    changeOverlayLayer.addTo(map);
                    changeOverlayLayer.bringToFront();
                    if (window.changeLegendControl) window.changeLegendControl.addTo(map);
                }
                const vqaLabel = document.getElementById('vqa-selected-image-panel');
                if (vqaLabel) vqaLabel.textContent = "Change Analysis";
            }
        });
    }"""

content = content.replace(old_toggles, new_toggles)
with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("REPLACED TOGGLES")
