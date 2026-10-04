with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

import re
# Find the exact string we want to replace
target = "const afterSel = document.getElementById('change-after-select');"

# How many times does it appear?
count = content.count(target)
print(f"Target appears {count} times")

# If we want to replace the first one that occurs in the global scope?
# Actually, let's just append the listeners to the end of the DOMContentLoaded block!
match = re.search(r"updateChangeAnalysisDropdowns\(\);\s*\}\)\;\s*\}\s*const stacCloudCover = document\.getElementById\('stac-cloud-cover'\);", content, flags=re.DOTALL)

if match:
    dom_new = """updateChangeAnalysisDropdowns();
        });
    }

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
    }

    const stacCloudCover = document.getElementById('stac-cloud-cover');"""
    
    content = content[:match.start()] + dom_new + content[match.end():]
    
    with open('frontend/app.js', 'w', encoding='utf8') as f:
        f.write(content)
    print("ADDED BUTTON LISTENERS")
else:
    print("NOT FOUND DOMContentLoaded hook")
