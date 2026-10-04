import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

new_block = '''                        if (ev.type === 'image_overlay') {
                            const imgOverlay = L.imageOverlay(ev.data, ev.bounds, {opacity: 0.6});
                            
                            if (changeAnalysisMode === 'case-study') {
                                if (caseStudyChangeLayer) map.removeLayer(caseStudyChangeLayer);
                                caseStudyChangeLayer = imgOverlay;
                                
                                if (caseStudyBeforeLayer) map.removeLayer(caseStudyBeforeLayer);
                                if (caseStudyAfterLayer) caseStudyAfterLayer.addTo(map);
                                caseStudyChangeLayer.addTo(map);
                            } else {
                                if (changeOverlayLayer) map.removeLayer(changeOverlayLayer);
                                changeOverlayLayer = imgOverlay;
                                
                                if (changeBeforeLayer) map.removeLayer(changeBeforeLayer);
                                if (changeAfterLayer) changeAfterLayer.addTo(map);
                                changeOverlayLayer.addTo(map);
                            }
                            
                            console.log("CHANGE OVERLAY RECEIVED:", !!ev.data);
                            console.log("CHANGE OVERLAY BOUNDS:", ev.bounds);
                            
                            if (window.changeLegendControl) {
                                map.removeControl(window.changeLegendControl);
                            }
                            window.changeLegendControl = L.control({position: 'bottomright'});
                            window.changeLegendControl.onAdd = function(map) {
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
                            };
                            window.changeLegendControl.addTo(map);
                            
                            return; // Skip the default grounding bbox rendering
                        }'''

content = re.sub(r'                        if \(ev\.type === \'image_overlay\'\) \{.*?return; // Skip the default grounding bbox rendering\s*\}', new_block, content, flags=re.DOTALL)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("REPLACED")
