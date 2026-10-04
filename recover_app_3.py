import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

payload_old = '''                const payload = {
                    image_before_id: beforeSel.value,
                    image_after_id: afterSel.value,
                    aoi: aoiData
                };'''
payload_new = '''                if (!beforeSel.value || !afterSel.value) {
                    throw new Error("Change Analysis requires two different satellite scenes.<br><br>Please select both a Before and After scene.");
                }
                
                if (beforeSel.value === afterSel.value) {
                    throw new Error("Before and After scenes must be different.<br><br>Please select different acquisition dates.");
                }
                
                if (!aoiData) {
                    throw new Error("Please select an Area of Interest before running Change Analysis.");
                }
                const payload = {
                    image_before_id: beforeSel.value,
                    image_after_id: afterSel.value,
                    aoi: aoiData
                };'''
content = content.replace(payload_old, payload_new)

ev_old = '''                        if (ev.type === 'image_overlay') {
                            const imgOverlay = L.imageOverlay(ev.data, ev.bounds, {opacity: 0.65, interactive: false});
                            imgOverlay.addTo(map);
                            
                            const rect = L.rectangle(ev.bounds, {color: '#ef4444', weight: 2, fill: false});
                            rect.addTo(map);
                        }'''
ev_new = '''                        if (ev.type === 'image_overlay') {
                            if (changeAnalysisMode === 'case-study') {
                                const KANCHA_AOI = [[17.41, 78.32], [17.45, 78.36]];
                                const imgOverlay = L.imageOverlay(ev.data, KANCHA_AOI, {opacity: 0.65, interactive: false});
                                
                                if (caseStudyChangeLayer) map.removeLayer(caseStudyChangeLayer);
                                caseStudyChangeLayer = imgOverlay;
                                
                                if (caseStudyBeforeLayer) map.removeLayer(caseStudyBeforeLayer);
                                if (caseStudyAfterLayer) {
                                    caseStudyAfterLayer.addTo(map);
                                    caseStudyAfterLayer.bringToFront();
                                }
                                caseStudyChangeLayer.addTo(map);
                                caseStudyChangeLayer.bringToFront();
                                if (caseStudyAoiLayer) caseStudyAoiLayer.bringToFront();
                                
                                if (!window.changeLegendControl) {
                                    window.changeLegendControl = L.control({position: 'bottomright'});
                                    window.changeLegendControl.onAdd = function(map) {
                                        const div = L.DomUtil.create('div', 'satquery-change-legend');
                                        div.innerHTML = 
                                            <div class="legend-title" style="font-weight: 600; font-size: 11px; margin-bottom: 6px;">Change Analysis</div>
                                            <div class="legend-row" style="display: flex; align-items: center; margin-bottom: 4px;">
                                                <span class="legend-color" style="display: inline-block; width: 14px; height: 14px; background: rgba(255, 60, 60, 0.6); margin-right: 8px;"></span>
                                                <span style="font-size: 11px;">Detected change</span>
                                            </div>
                                            <div class="legend-row" style="display: flex; align-items: center;">
                                                <span class="legend-neutral" style="display: inline-block; width: 14px; height: 14px; background: rgba(255, 255, 255, 0.3); border: 1px dashed rgba(255,255,255,0.5); margin-right: 8px;"></span>
                                                <span style="font-size: 11px;">Satellite imagery</span>
                                            </div>
                                        ;
                                        L.DomEvent.disableClickPropagation(div);
                                        return div;
                                    };
                                }
                                window.changeLegendControl.addTo(map);
                                
                                map.fitBounds(KANCHA_AOI, { padding: [40, 40] });
                                map.invalidateSize(true);
                            } else {
                                const imgOverlay = L.imageOverlay(ev.data, ev.bounds, {opacity: 0.65, interactive: false});
                                imgOverlay.addTo(map);
                                const rect = L.rectangle(ev.bounds, {color: '#ef4444', weight: 2, fill: false});
                                rect.addTo(map);
                            }
                        }'''
content = content.replace(ev_old, ev_new)

ans_old = '''                let ansText = data.answer;
                if (!ansText) {
                    ansText = "No answer returned.";
                }'''
ans_new = '''                let ansText = data.answer;
                if (task === 'change') {
                    if (data.status === 'success') {
                        const methodFormat = data.method === 'baseline_raster_difference' ? 'Baseline Raster Difference' : data.method;
                        let caseStudyHtml = '';
                        const caseStudySel = document.getElementById('change-case-study');
                        if (caseStudySel && caseStudySel.value === 'kancha') {
                            caseStudyHtml = Kancha Gachibowli, Hyderabad<br><br><strong>Before</strong><br>28 March 2025<br><br><strong>After</strong><br>2 April 2025<br><br>;
                        } else {
                            caseStudyHtml = <strong>Before</strong><br>\<br><br><strong>After</strong><br>\<br><br>;
                        }
                        
                        ansText = <div style="font-family: sans-serif; line-height: 1.5; font-size: 13px;">
<strong>CHANGE ANALYSIS</strong><br><br>
\<strong>Changed area</strong><br>
\%<br><br>
<strong>Changed pixels</strong><br>
\<br><br>
<strong>Valid pixels</strong><br>
\<br><br>
<strong>Threshold</strong><br>
\<br><br>
<strong>Method</strong><br>
\<br><br>
<strong>Status</strong><br>
✓ Analysis completed successfully
</div>;
                    } else {
                        ansText = "Change Analysis failed.<br><br>Please check the selected scenes and AOI and try again.";
                    }
                } else if (!ansText) {
                    ansText = "No answer returned.";
                }'''
content = content.replace(ans_old, ans_new)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("RECOVERED STAGE 3")
